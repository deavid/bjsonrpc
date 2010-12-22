"""
    example2-client.py
    
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

import time
import random

conn = bjsonrpc.connect(host="127.0.0.1",port=10123)
conn._debug_socket = True
ch1 = conn.call.newChronometer()
ch2 = conn.call.newChronometer()
list1 = conn.call.newList()
list2 = conn.call.newList()

ch1.call.start()
conn._debug_socket = False
print "ch1 start."
time.sleep(0.05); print "  %.4f\t%.4f" % (ch1.call.lapse(), ch2.call.lapse())
time.sleep(0.05)
ch2.call.start(); print "ch2 start."
time.sleep(0.05); print "  %.4f\t%.4f" % (ch1.call.lapse(), ch2.call.lapse())
time.sleep(0.05); 
ch1.call.stop();  print "ch1 stop."
time.sleep(0.05); print "  %.4f\t%.4f" % (ch1.call.lapse(), ch2.call.lapse())
time.sleep(0.15); print "  %.4f\t%.4f" % (ch1.call.lapse(), ch2.call.lapse())
ch2.call.stop();  print "ch2 stop."
time.sleep(0.05); print "  %.4f\t%.4f" % (ch1.call.lapse(), ch2.call.lapse())
time.sleep(0.05); print "  %.4f\t%.4f" % (ch1.call.lapse(), ch2.call.lapse())

print "---"

for i in range(10):
    list1.notify.add(i)
    
conn._debug_socket = True
list2.notify.addlist([random.randint(0,100) for i in range(30)])    

# Get the two list of items and totals at same time.
m_items1 = list1.method.items(5,10) 
m_items2 = list2.method.items(5,10)
m_sum1 = list1.method.sum()
m_sum2 = list2.method.sum()

# .value method waits if we haven't received yet the response.
print m_sum1.value, m_sum2.value
print sum(m_items1.value), sum(m_items2.value)

del list1
del list2

