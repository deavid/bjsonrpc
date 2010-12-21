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
from exceptions import ServerError
import jsonlib as json

class Request(object):
    def __init__(self, conn, request_data):
        self.conn = conn
        self.data = request_data
        self.response = None
        self.eventResponse = Event()
        self.thread_wait = self.eventResponse.wait
        self.id = None
        if 'id' in self.data: self.id = self.data['id']
        if self.id:
            assert(self.id not in self.conn._requests)
            self.conn._requests[self.id] = self
            
        data = json.dumps(self.data,self.conn)

        self.conn.write(data)
        
    
    def wait(self):
        while self.response is None:
            self.conn.read_and_dispatch()
        
    @property
    def value(self):
        """get request value response"""
        self.wait()
        
        if self.response.get('error', None) is not None:
            raise ServerError(self.response['error'])

        return self.response['result']        
