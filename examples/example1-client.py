"""
    example1-client.py
    
    Example Client using alternative jpc library.
    
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

class MyHandler(BaseHandler):
    def notify(self,text):
        print "Notify:", text
        



conn = bjsonrpc.connect(host="127.0.0.1",port=10123,handler_factory=MyHandler)

def benchmark():
    print conn.call.echo('Hello World!')
    total = 0
    count = 0
    valuecount = 10000
    start = time.time()
    for i in range(valuecount):
        randval = random.uniform(-100,100)
        total += randval
        count += 1
        conn.notify.addvalue(randval)

    rtotal, rcount = conn.method.gettotal(), conn.method.getcount()
    print total,count
    print rtotal.value, rcount.value

    end = time.time()
    lapse = float(end-start)
    print "Notify Total: %.2fs   %.2f reg/s" % (lapse, valuecount/lapse)
    
    
    valuecount = 3000
    start = time.time()
    values = []
    for i in range(valuecount):
        values.append(conn.method.getrandom())

    print sum([x.value for x in values])
    end = time.time()
    lapse = float(end-start)
    print "Method Total: %.2fs   %.2f reg/s" % (lapse, valuecount/lapse)
    

    valuecount = 500
    start = time.time()
    values = []
    for i in range(valuecount):
        values.append(conn.call.getrandom())

    print sum(values)
    end = time.time()
    lapse = float(end-start)
    print "Call Total: %.2fs   %.2f reg/s" % (lapse, valuecount/lapse)
    

    

benchmark()

