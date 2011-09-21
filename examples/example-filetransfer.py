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
SEND_FILE = "example-filetransfer.py"
DST_FILE = "/tmp/temp.out"
if len(sys.argv) > 2:
    n = 0
    try: 
        n = int(sys.argv[2])
    except Exception:
        pass
    if n > 1024: RPC_PORT = n
    RPC_HOST = sys.argv[1]
    try: 
        SEND_FILE = sys.argv[3]
    except Exception:
        pass

from StringIO import StringIO


class MyHandler(BaseHandler):
    def newWriteFileTransfer(self):
        #fobj = StringIO()
        fobj = open(DST_FILE,"w")
        return FileTransferHandler(self,fobj,'w')

    def echo(self, string):
        print string
        return string
        
    def lenecho(self, string):
        print len(string)
        return string
        
    def stop(self):
        sys.exit(0)

import threading, os, os.path
import hashlib, traceback

def sha1digest(filename):
    hashobj = hashlib.sha1()
    f1 = open(filename,"r")
    while True:
        x = f1.read(256*1024)
        if not x: break
        hashobj.update(x)
    f1.close()
    return hashobj.hexdigest()

def thread1():  
    time.sleep(0.1)  
    print "Connecting to server at %s:%s" % (RPC_HOST, RPC_PORT)
        
    conn = bjsonrpc.connect(host=RPC_HOST,port=RPC_PORT)
    try:
        conn.call.echo("Connected!")
        filename = os.path.realpath(SEND_FILE)
        fsz = os.path.getsize(filename)
        print "File: %s Size: %.3fMb" % (filename, fsz/1024.0/1024.0)
        sha1_orig = sha1digest(filename)
        print "Source File SHA-1 Digest:", sha1_orig 
        fread = open(filename,"r")
        
        
        
        fth = FileTransferHelper(conn.call.newWriteFileTransfer())
        t1 = tstart = time.time()
        # Thread version of:
        # ... fth.send_file(fread)
        subth1 = threading.Thread(target=fth.send_file, args=(fread,))
        subth1.daemon = False
        subth1.start()
            
        while subth1.isAlive():
            try:
                subth1.join(0.1)
            except Exception, e:
                print e
                break
            t1 = time.time()
            delta = t1 - tstart
            pos = fth.tell()
            posmb = pos  / 1024.0 / 1024.0
            ppos = pos * 100.0 / float(fsz)
            rem = delta / ppos * (100 - ppos)
            speedmb = posmb / delta
            status = ("working, %.2fs remaining" % rem if subth1.isAlive() else "done after  %.2f seconds!" % delta)
            sys.stdout.write("Pos %.1f%%: %.3f MB @ %.1fMB/s -- %s%s\r" % (ppos,posmb,speedmb, status ," "*10))
            sys.stdout.flush()
        print
        del fth
        sha1_dst = sha1digest(DST_FILE)
        print "Recv.  File SHA-1 Digest:",  sha1_dst
        assert(sha1_dst == sha1_orig)
        
    finally:
        conn.notify.stop()
        conn.close()
    

s = bjsonrpc.createserver(handler_factory=MyHandler, port = RPC_PORT, host = "0.0.0.0")
# s.debug_socket(True)
print "Starting server at port", RPC_PORT
th1 = threading.Thread(target=thread1)
th1.daemon = False
th1.start()
try:
    s.serve()
except Exception, e:
    print traceback.format_exc()
    sys.exit(1)