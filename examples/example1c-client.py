"""
    example1b-client.py
    
    Example Client using alternative jpc library. (PDA-oriented for PythonCE)
    
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

import random, sys
import time
import simplejson
sys.path.insert(0,"..")
import bjsonrpc

from bjsonrpc.handlers import BaseHandler

class MyHandler(BaseHandler):
    def notify(self,text):
        print "Notify:", text
        
port = 10123
host = "127.0.0.1"
if sys.argv:
    n = 0
    try: 
        n = int(sys.argv[2])
    except Exception:
        pass
    if n > 1024: port = n
    h = ""
    try: 
        h = sys.argv[1]
    except Exception:
        pass
    if len(h) > 4: host = h


print host, port
conn = bjsonrpc.connect(host=host,port=port,handler_factory=MyHandler)

def benchmark():
    demo_text = "Hello World!"
    total = 20
    for i in range(total):
        demo_text += demo_text
        total2 = int(150 / (i+10) + 1)
        t1 = time.time()
        for n in range(total2):
            v = conn.call.lenecho(demo_text)
        t2 = time.time()
        delta = (t2-t1) / float(total2)
        bytes = len(v)
        kbytes = bytes / 1024.0
        mbytes = kbytes / 1024.0
        kbytespersec = bytes / 1024.0 / delta
        if mbytes > 1:
            print "%d/%d*%d: %.2f MB in %.3fs at %.2fkB/s" % (i+1,total, total2, mbytes, delta,kbytespersec)
        elif kbytes > 10:
            print "%d/%d*%d: %.1f kB in %.3fs at %.2fkB/s" % (i+1,total, total2, kbytes, delta,kbytespersec)
        else:
            print "%d/%d*%d: %d bytes in %.3fs at %.2fkB/s" % (i+1,total, total2, bytes, delta,kbytespersec)

benchmark()

