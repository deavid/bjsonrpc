"""
    bjson/request.py
    
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

from threading import Event
import traceback

from bjsonrpc.exceptions import ServerError
import bjsonrpc.jsonlib as json

class Request(object):
    """
        Represents a request to the other end which may be not be completed yet.
        This class is automatically created by *method* Proxy.
        
        Parameters:
        
        **conn**
            Connection instance which this Request belongs to. 
            (internally stored as Request.conn)
            
        **request_data** 
            Dictionary object to serialize as JSON to send to the other end.
            (internally stored as Request.data)
            
            
        Attributes:
        
        **response**
            JSON Object of the response, as a dictionary. If no response has
            been received, this is None. 
            
        **event_response**
            A threading.Event object, which is set to true when a response has 
            been received. Useful to wake up threads or to wait exactly until
            the response is received.
            
        **callbacks**
            List array where the developer can append functions to call when
            the response is received. The function will get the Request object
            as a first argument.

        **request_id**
            Number of ID that identifies the call. For notifications this is None.
            Be careful because it may be not an integer. Strings and other objects
            may be valid for other implementations.
            
    """
    def __init__(self, conn, request_data):
        self.conn = conn
        self.data = request_data
        self.response = None
        self.event_response = Event()
        self.callbacks = []
        self.thread_wait = self.event_response.wait
        self.request_id = None
        if 'id' in self.data: 
            self.request_id = self.data['id']
            
        if self.request_id:
            self.conn.addrequest(self)
            
        data = json.dumps(self.data, self.conn)

        self.conn.write(data)
    
    def hasresponse(self):
        """
            Method thet checks if there's a response or not.
            Returns True if there it is or False if it haven't arrived yet.
        """
        if self.response is not None: return True
        self.conn.dispatch_until_empty()
        return self.response is not None
        
    def setresponse(self, value):
        """
            Method used by Connection instance to tell Request that a Response
            is available to this request. 
            
            Parameters:
            
            **value**
                Value (JSON decoded) received from socket.
        """
        self.response = value
        for callback in self.callbacks: 
            try:
                callback(self)
            except Exception, exc:
                print "Error on callback.", repr(exc)
                print traceback.format_exc()
                
        self.event_response.set() # helper for threads.
    
    def wait(self):
        """
            Block until there is a response. Will manage the socket and dispatch
            messages until the response is found.
        """
        #if self.response is None:
        #    self.conn.read_ensure_thread()
            
        while self.response is None:
            self.conn.read_and_dispatch(condition=lambda: self.response is None)
    
    def __call__(self):
        return self.value
        
    @property
    def value(self):
        """
            Property to get value response. If the response is not available, it waits
            to it (see *wait* method). If the response contains an Error, this
            method raises *exceptions.ServerError* with the error text inside.
            
            From version 0.2.0 you can also call the class itself to get the value::
            
                req_stime = rpcconn.method.getServerTime()
                print req_stime.value  
                print req_stime()     # equivalent to the prior line.
                
        """
        self.wait()
        
        if self.response.get('error', None) is not None:
            raise ServerError(self.response['error'])

        return self.response['result']        
