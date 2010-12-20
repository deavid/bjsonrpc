"""
    bjson/connection.py
    
    Asynchronous Bidirectional JSON-RPC protocol implementation over TCP/IP
    
    Copyright (c) 2010 David Martinez Marti
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions
    are met:
    1. Redistributions of source code must retain the above copyright
       notice, this list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.
    3. Neither the name of copyright holders nor the names of its
       contributors may be used to endorse or promote products derived
       from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
    TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
    PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL COPYRIGHT HOLDERS OR CONTRIBUTORS
    BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
    CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
    SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
    INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
    CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.

"""

from proxies import Proxy
from request import Request
from exceptions import EofError

import jsonlib as json

import socket


class Connection(object):
    def __init__(self, conn, addr = None, handler_factory = None):
        self._buffer = ''
        self._conn = conn
        self._addr = addr
        self._handler = handler_factory 
        if self._handler: self.handler = self._handler(self)
        self._id = 1
        self._requests = {}

        self.call = Proxy(self,sync_type=0)
        self.method = Proxy(self,sync_type=1)
        self.notify = Proxy(self,sync_type=2)
        

    def _dispatch_method(self, request):
        req_id = request.get("id",None)
        req_method = request.get("method")
        req_args = request.get("params",[])
        req_kwargs = request.get("kwparams",{})
        if req_kwargs: req_kwargs = dict((str(k), v) for k, v in req_kwargs.iteritems())
        
        try:
            req_function = self.handler._get_method(req_method)
            result = req_function(*req_args, **req_kwargs)
        except:
            print
            print traceback.format_exc()
            print
            if req_id is not None: 
                return {'result': None, 'error': repr(sys.exc_info()[1]), 'id': req_id}
        
        if req_id is None: return None
        return {'result': result, 'error': None, 'id': req_id}

    def dispatch_until_empty(self):
        next = 0
        count = 0
        while next != -1:
            if not self.read_and_dispatch(timeout=0): break
            count += 1
            next = self._buffer.find('\n')
        return count
                
                
    def read_and_dispatch(self,timeout=None):
        try:
            self._conn.settimeout(timeout)
            data = self.read()
        finally:
            self._conn.settimeout(None)
            
        if not data: return False 
        item = json.loads(data)       
        response = None
        if 'id' not in item: item['id'] = None
        
        if 'method' in item: 
            response = self._dispatch_method(item)
        elif 'result' in item: 
            assert(item['id'] in self._requests)
            request = self._requests[item['id']]
            del self._requests[item['id']]
            request.response = item
            request.eventResponse.set() # helper for threads.
        else:
            response = {'result': None, 'error': "Unknown format", 'id': item['id']}
        
            
        if response is not None:
            try:
                self.write(json.dumps(response))
            except TypeError:
                print "response was:", repr(response)
                raise
        return True
    
    
    def _proxy(self, sync_type, name, args, kwargs):
        """
        Call method on server.

        sync_type :: 
          = 0 .. call method, wait, get response.
          = 1 .. call method, inmediate return of object.
          = 2 .. call notification and exit.
          
        """
       
        data = {}
        
        data['method'] = name

        if sync_type in [0,1]:
            data['id'] = self._id
            self._id += 1
            
        if len(args) > 0: data['params'] = args
        if len(kwargs) > 0: data['kwparams'] = kargs
            
        if sync_type == 2: # short-circuit for speed!
            self.write(json.dumps(data))
            return None
                    
        req = Request(self, data)
        if sync_type == 2: return None
        if sync_type == 1: return req
        
        return req.value

    def close(self):
        try:
            self._conn.shutdown(socket.SHUT_RDWR)
        except socket.error:
            pass
        self._conn.close()
    
    def write_prefixed(self, data):
        """Write length prefixed data to socket."""

        length = len(data)
        while length >= 255:
            l = chr(255)
            out = data[:255]
            self._conn.sendall(l + data)
            data = data[255:]
            length = len(data)
        
        l = chr(length)

        self._conn.sendall(l + data)


    def read_prefixed(self):
        """Read length prefixed data from socket."""
        buf = []
        end = False
        while not end:
            slength = self._read2(1)
            if slength == "": raise EofError(0)
            length = ord(slength)
            if length < 255: end = True
            buf.append(self._read2(length))
            
        return "".join(buf)
        
    def write_line(self, data):
        """Write line to socket"""
        assert('\n' not in data)
        self._conn.sendall(data + '\n')


    def read_line(self):
        """Read line from socket."""
        return self._readn()

    write = write_line 
    read = read_line 

    def _read2(self, length):
        buffer = self._buffer
        buflen = len(buffer)
        while buflen < length:
            data = self._conn.recv(length-buflen)
            if not data:
                raise EofError(len(buffer))
            buffer += data
            buflen = len(buffer)
            

        self._buffer = buffer[length:]
        return buffer[: length]

    def _readn(self):
        buffer = self._buffer
        pos = buffer.find('\n')
        #print "read..."
        while pos == -1:
            try:
                data = self._conn.recv(2048)
            except IOError:
                return ''
            except:
                raise
            if not data:
                raise EofError(len(buffer))
            #print "readbuf+:",repr(data)
            buffer += data
            pos = buffer.find('\n')

        self._buffer = buffer[pos + 1:]
        buffer = buffer[:pos]
        #print "read:", repr(buffer)
        return buffer
        
    def _serve(self):
        try:
            while True: self.read_and_dispatch()
        finally:
            self.close()
