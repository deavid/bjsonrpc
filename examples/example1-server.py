"""
    example1-server.py
    
    Example Server using jpc alternative library.
    
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

import sys
sys.path.insert(0,"../") # prefer local version
import bjsonrpc
from bjsonrpc.handlers import BaseHandler

import random
import time

class Chronometer(BaseHandler):
    def _setup(self):
        self._begin = 0
        self._end = 0
        self._state = 0 # 0 is off, 1 is on.

    def begin(self): return self._begin
    def end(self): 
        if self._state == 0: return self._end
        else: return time.time()
            
    def start(self):
        self._begin = time.time()
        self._state = 1
    
    def stop(self):
        self._end = time.time()
        self._state = 0
        
    def lapse(self):
        return self.end() - self.begin()
        
        
        
class MyList(BaseHandler):
    def _setup(self):
        self._list = []
        
    def add(self,item):
        self._list.append(item)

    def addlist(self,itemlist):
        self._list += itemlist
        
    def items(self, start = None, end = None):
        return self._list[start:end]
    
    def remove(self,item):
        self._list.remove(item)
        
    def clear(self):
        self._list = []
    
    def sum(self): return sum(self._list)
    def min(self): return min(self._list)
    def max(self): return max(self._list)
        




class MyHandler(BaseHandler):
    @classmethod
    def _factory(cls, *args, **kwargs):
        def handler_factory(connection):
            handler = cls(connection, *args, **kwargs)
            return handler
        return handler_factory
    
    def __init__(self, connection, *args, **kwargs):
        BaseHandler.__init__(self,connection)
        print args
        print kwargs
        
    def _setup(self):
        self.value_count = 0
        self.value_total = 0
    
    def newChronometer(self):
        return Chronometer(self)

    def newList(self):
        return MyList(self)
    
        
    def addvalue(self,number):
        n = float(number)
        self.value_count += 1
        self.value_total += n
        
    def getrandom(self):
        return random.randint(0,100)
    
    def gettotal(self):
        self._conn.notify.notify("total")
        return self.value_total
        
    def getcount(self):
        return self.value_count
        
    def echo(self, string):
        #print self._addr 
        #print self._conn 
        #print self._methods 
        print string
        return string

import threading
def thread1():  
    time.sleep(0.2)  
    conn = bjsonrpc.connect(host="127.0.0.1",port=10123)
    conn.call.echo("Hello world")
    conn.close()
    

s = bjsonrpc.createserver(handler_factory=MyHandler._factory(domain="yourdomain-dot-com"), port = 10123, host = "0.0.0.0")
s.debug_socket(True)
threading.Thread(target=thread1).start()

s.serve()
