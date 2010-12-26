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
from types import MethodType, FunctionType

import socket, traceback, sys

class RemoteObject(object):
    def __init__(self,conn,obj):
        self._conn = conn
        self.name = obj['__remoteobject__']
        
        self.call = Proxy(self._conn, obj=self.name, sync_type=0)
        self.method = Proxy(self._conn, obj=self.name, sync_type=1)
        self.notify = Proxy(self._conn, obj=self.name, sync_type=2)
    
    def __del__(self):
        self._close()
        
    def _close(self):
        self.call.__delete__()
        self.name = None
        
        
        

class Connection(object):
    """ 
    Creates a **connection** to a peer bounded to a connected socket::
    
        import bjson
        
        
    """
    def __init__(self, socket, address = None, handler_factory = None):
        self._debug_socket = False
        self._debug_dispatch = False
        self._buffer = ''
        self._sck = socket
        self._address = address
        self._handler = handler_factory 
        if self._handler: self.handler = self._handler(self)
        self._id = 0
        self._requests = {}
        self._objects = {}

        self.call = Proxy(self,sync_type=0)
        self.method = Proxy(self,sync_type=1)
        self.notify = Proxy(self,sync_type=2)
        
    def getID(self):
        self._id += 1
        return self._id 
        
    def load_object(self,obj):
        # dict loaded.
        if '__remoteobject__' in obj: return RemoteObject(self,obj)
        if '__objectreference__' in obj: return self._objects[obj['__objectreference__']]
        if '__functionreference__' in obj:
            name = obj['__functionreference__']
            if '.' in name:
                objname,methodname = name.split('.')
                obj = self._objects[objname]
            else:
                obj = self.handler
                methodname = name
            method = obj._get_method(methodname)
            return method
            
        
        return obj

    def dump_object(self,obj):
        # object of unknown type
        if type(obj) is FunctionType or type(obj) is MethodType :
            conn = getattr(obj,'_conn',None)
            if conn != self: raise TypeError
            return self.dump_functionreference(obj)
            
        if not isinstance(obj,object): raise TypeError
        if not hasattr(obj,'__class__'): raise TypeError
        if isinstance(obj,RemoteObject): return self.dump_objectreference(obj)
        if hasattr(obj,'_get_method'): return self.dump_remoteobject(obj)
        raise TypeError

    def dump_functionreference(self,obj):
        return { '__functionreference__' : obj.__name__ }

    def dump_objectreference(self,obj):
        return { '__objectreference__' : obj.name }
        
    def dump_remoteobject(self,obj):
        # An object can be remotely called if :
        #  - it derives from object (new-style classes)
        #  - it is an instance
        #  - has an internal function _get_method to handle remote calls
        if not hasattr(obj,'__remoteobjects__'): obj.__remoteobjects__ = {}
        if self in obj.__remoteobjects__:
            instancename = obj.__remoteobjects__[self] 
        else:
            classname = obj.__class__.__name__
            instancename = "%s_%04x" % (classname.lower(),self.getID())
            self._objects[instancename] = obj
            obj.__remoteobjects__[self] = instancename
        return { '__remoteobject__' : instancename }



    def _dispatch_method(self, request):
        req_id = request.get("id",None)
        req_method = request.get("method")
        req_args = request.get("params",[])
        if type(req_args) is dict: 
            req_kwargs = req_args
            req_args = []
        else:
            req_kwargs = request.get("kwparams",{})
            
        if req_kwargs: req_kwargs = dict((str(k), v) for k, v in req_kwargs.iteritems())
        if '.' in req_method: # local-object.
            objectname, req_method = req_method.split('.')[:2]
            if objectname not in self._objects: raise ValueError, "Invalid object identifier"
            if req_method == '__delete__': 
                req_object = None
                del self._objects[objectname]
                result = None
            else:
                req_object = self._objects[objectname]
        else:
            req_object = self.handler
            
        try:
            if req_object:
                req_function = req_object._get_method(req_method)
                result = req_function(*req_args, **req_kwargs)
        except:
            if self._debug_dispatch:
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
            self._sck.settimeout(timeout)
            data = self.read()
        finally:
            self._sck.settimeout(None)
            
        if not data: return False 
        item = json.loads(data,self)  
        if type(item) is list: # batch call
            for i in item: self.dispatch_item(i)
        elif type(item) is dict: # std call
            self.dispatch_item(item)
        else: # Unknown format :-(
            print "Received message with unknown format type:" , type(item)
            return False
        return True
        
            
             
    def dispatch_item(self,item):
        assert(type(item) is dict)
        response = None
        if 'id' not in item: item['id'] = None
        
        if 'method' in item: 
            response = self._dispatch_method(item)
        elif 'result' in item: 
            assert(item['id'] in self._requests)
            request = self._requests[item['id']]
            del self._requests[item['id']]
            request.setResponse(item)
            
        else:
            response = {'result': None, 'error': "Unknown format", 'id': item['id']}
        
            
        if response is not None:
            try:
                self.write(json.dumps(response,self))
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

        if sync_type in [0,1]: data['id'] = self.getID()
            
        if len(args) > 0: data['params'] = args
        if len(kwargs) > 0: 
            if len(args) == 0: data['params'] = kwargs
            else: data['kwparams'] = kwargs
            
            
        if sync_type == 2: # short-circuit for speed!
            self.write(json.dumps(data,self))
            return None
                    
        req = Request(self, data)
        if sync_type == 2: return None
        if sync_type == 1: return req
        
        return req.value

    def close(self):
        try:
            self._sck.shutdown(socket.SHUT_RDWR)
        except socket.error:
            pass
        self._sck.close()
    
    def write_line(self, data):
        """Write line to socket"""
        assert('\n' not in data)
        if self._debug_socket: print "<:%d:" % len(data), data
        self._sck.sendall(data + '\n')


    def read_line(self):
        """Read line from socket."""
        data = self._readn()
        if self._debug_socket: print ">:%d:" % len(data), data
        return data

    write = write_line 
    read = read_line 

    def _readn(self):
        buffer = self._buffer
        pos = buffer.find('\n')
        #print "read..."
        while pos == -1:
            try:
                data = self._sck.recv(2048)
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
