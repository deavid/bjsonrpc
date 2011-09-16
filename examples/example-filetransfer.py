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
from bjsonrpc.filetransfer import FileTransferHandler, FileTransferHelper
from bjsonrpc.binary import BinaryData
import random
import time

RPC_PORT = 10123
RPC_HOST = "127.0.0.1"
if len(sys.argv) > 2:
    n = 0
    try: 
        n = int(sys.argv[2])
    except Exception:
        pass
    if n > 1024: RPC_PORT = n
    RPC_HOST = sys.argv[1]

from StringIO import StringIO


class MyHandler(BaseHandler):
    def newFileTransfer(self,mode):
        #fobj = StringIO()
        fobj = open("/tmp/temp.out","w")
        
        return FileTransferHandler(self,fobj,mode)

    def echo(self, string):
        print string
        return string
        
    def lenecho(self, string):
        print len(string)
        return string
        
    def stop(self):
        sys.exit(0)

import threading, os, os.path

def thread1():  
    time.sleep(0.2)  
    print "Connecting to server at %s:%s" % (RPC_HOST, RPC_PORT)
        
    conn = bjsonrpc.connect(host=RPC_HOST,port=RPC_PORT)
    try:
        conn.call.echo("Connected!")
        codec = 'base64'
        filename = "/home/deavid/Downloads/LeeDrOiD_V3.0.8.2_GB_A2SD.zip"
        fsz = os.path.getsize(filename)
        fread = open(filename,"r")
        print "Size: %.2fMb" % (fsz/1024.0/1024.0)
        fth = FileTransferHelper(conn.call.newFileTransfer('w'), codec)
        t1 = tstart = time.time()
        while True:
            bindata = fread.read(64*1024)
            if not bindata: break
                
            fth.write(bindata)
            if time.time() - t1 > 2:
                t1 = time.time()
                delta = t1 - tstart
                pos = fth.tell()
                posmb = pos  / 1024.0 / 1024.0
                speedmb = posmb / delta
                print "Pos: %.2f MB @ %.3fMB/s" % (posmb,speedmb)
    
        t1 = time.time()
        delta = t1 - tstart
        pos = fth.tell()
        posmb = pos  / 1024.0 / 1024.0
        speedmb = posmb / delta
        print "-> Size: %.2f MB @ %.3fMB/s" % (posmb,speedmb)
        del fth

    finally:
        conn.notify.stop()
        conn.close()
    

s = bjsonrpc.createserver(handler_factory=MyHandler, port = RPC_PORT, host = "0.0.0.0")
# s.debug_socket(True)
print "Starting server at port", RPC_PORT
threading.Thread(target=thread1).start()

s.serve()
