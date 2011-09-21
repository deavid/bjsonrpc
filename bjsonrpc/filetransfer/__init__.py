# encoding: UTF-8
"""
    bjson/filetransfer/__init__.py
    
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

from bjsonrpc.handlers import BaseHandler
from bjsonrpc.binary import BinaryData

class FileTransferHandler(BaseHandler):
    def _setup(self, fileobj, mode):
        assert(mode in ['r','w'])
        self.fileobj = fileobj
        self.mode = mode
        self.encode = None
        self.decode = None
        self.binary_data_codec = "base64"
        
    def set_binary_data_codec(self, codec):
        self.binary_data_codec = codec
        self.encode = None
        self.decode = None
        
    def set_codec(self, codec):
        self.encode = BinaryData.encode[codec]
        self.decode = BinaryData.decode[codec]
        
    def write(self, data):
        assert(self.mode == 'w')
        if isinstance(data, BinaryData):
            data = data.data
        elif self.decode:
            data = self.decode(data)
            
        return self.fileobj.write(data)
    
    def read(self, size, donotsend = False):
        assert(self.mode == 'r')
        data = self.fileobj.read(size)
        if donotsend: return None
        if self.encode:
            encdata = self.encode(data)
        else:
            encdata = BinaryData(data, encoding = self.binary_data_codec)
        return encdata
    
    def seekable(self):
        return self.fileobj.seekable()
    
    def tell(self):
        return self.fileobj.tell()
        
    def seek(self,offset, whence=0):
        return self.fileobj.seek(offset, whence)
        
    
class FileTransferHelper(object):
    BLOCK_SZ = 64*1024
    def __init__(self, file_transfer_handler, codec = 'base64'):
        self.fth = file_transfer_handler
        self.codec = codec
        self.fth.call.set_binary_data_codec(self.codec)
        
    def write(self, data):
        encdata = BinaryData(data, encoding = self.codec)
        return self.fth.call.write(encdata)
        
    def read(self, size = 0):
        if size == 0: size = BLOCK_SZ
        encdata = self.fth.call.read(size)
        return encdata.data
        
    def tell(self):
        return self.fth.call.tell()
        
    def seekable(self):
        return self.fth.call.seekable()
        
    def seek(self, offset, whence = 0):
        return self.fth.call.seek(offset, whence)
        
    def send_file(self, fread):
        while True:
            bindata = fread.read(self.BLOCK_SZ)
            if not bindata: break
            self.write(bindata)
    
        