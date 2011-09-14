"""
    bjson/binary.py
    
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

# File oriented to export-import binary data through JSON.
import quopri, base64, hashlib, zlib, binascii

class BinaryData(object):
    digest = {
        'crc32' : lambda x: binascii.unhexlify("%08x" % (zlib.crc32(x) & 0xFFFFFFFF)), 
        'md5' : lambda x: hashlib.md5(x).digest() ,
        'sha1' : lambda x: hashlib.sha1(x).digest() ,
        'sha224' : lambda x: hashlib.sha224(x).digest() ,
        }
    encode = {
        'hex' : binascii.hexlify,
        'base64' : base64.b64encode,
        'quopri' : quopri.encodestring,
        'zlib-base64' : lambda x : base64.b64encode(zlib.compress(x)),
        }
    decode = {
        'hex' : binascii.unhexlify,
        'base64' : base64.b64decode,
        'quopri' : quopri.decodestring,
        'zlib-base64' : lambda x : zlib.decompress(base64.b64decode(x)),
        }
    
    def __init__(self, data=None, jsonobj=None, **options):
        if data and jsonobj:
            raise ValueError, "BinaryData.__init__ can only have 'data' or 'jsonobj' arguments. Not both."
        
        if not data and not jsonobj:
            raise ValueError, "BinaryData.__init__ must get one of 'data' or 'jsonobj' arguments. None of them were passed."
        
        if data: return self._create_new(data, options)
        if jsonobj: return self._load_json(jsonobj, options)
    
    @classmethod
    def compute_digest(cls, data, hashtype):
        if hashtype.count(":") != 2:
            raise ValueError, "HashType must be in the form ALG:ENC:LEN"
        algorithm, encoding, length = hashtype.split(":")
        if encoding not in cls.encode:
            raise ValueError, "Encoding name not known: %s" % repr(encoding)
        if algorithm not in cls.digest:
            raise ValueError, "Digest algorithm name not known: %s" % repr(algorithm)
        if length:
            if not length.startswith("len"):
                raise ValueError, "Length does not start with 'len': %s" % repr(length)
            try:
                length = int(length[3:])
            except ValueError:
                raise ValueError, "Non-numeric length: %s" % repr(length[3:])
        
        data_digest = cls.digest[algorithm](data)
        encoded_digest = cls.encode[encoding](data_digest)
        
        if length:
            if length > len(encoded_digest):
                raise ValueError, "Length %d is too high for this digest+encoding. Maximum is %d." % (length, len(encoded_digest))
            encoded_digest = encoded_digest[:length]
        return encoded_digest
            
        
        
    
    def _create_new(self, data, options):
        if hasattr(data, "read"): 
            # If is a file, read it all.
            data = data.read() 
            
        self.data = data
        # TODO: Allow composite, zlib-base64
        self.encoding = options.get('encoding','base64')
        if self.encoding not in self.encode:
            raise ValueError, "Encoding name not known: %s" % repr(self.encoding)
            
        self.encoded_data = self.encode[self.encoding](self.data)
        self.hashtype = options.get('digest','sha1:base64:len8')
        if self.hashtype:
            self.digest = self.compute_digest(self.data, self.hashtype)
        else:
            self.digest = None
            
        self.dump_mode = options.get('dump_mode','standard')
        
    def _load_json(self,jsonobj, options):
        if 'short' in jsonobj:
            jsonobj['encoding'], jsonobj['data'], jsonobj['digest'] = jsonobj['short'].split("|")
            if not jsonobj['digest']: jsonobj['digest'] = None
            del jsonobj['short']
        self.encoded_data = jsonobj['data']
        self.encoding = jsonobj['encoding']
        if self.encoding not in self.decode:
            raise ValueError, "Encoding name not known: %s" % repr(self.encoding)
            
        self.data = self.decode[self.encoding](self.encoded_data)
        
        if jsonobj['digest']:
            idx_hash = jsonobj['digest'].rfind(":")
            self.hashtype = jsonobj['digest'][:idx_hash]
            remote_digest = jsonobj['digest'][idx_hash+1:]
            self.digest = self.compute_digest(self.data, self.hashtype)
            if self.digest != remote_digest:
                raise ValueError, "Data corrupted. Digests doesn't match: calculated: %s source: %s" % (self.digest,calc_digest)
        
        
    def format(self):
        return { 
            #'data' : self.data,
            'data-len' : len(self.data),
            'encoding' : self.encoding,
            #'encoded-data' : self.encoded_data,
            'encoded-data-len' : len(self.encoded_data),
            'hashtype' : self.hashtype,
            'digest' : self.digest,
        }
    
    def dump(self, dump_mode = None):
        # Returns a object suitable for json-embedding.
        if dump_mode is None: dump_mode = self.dump_mode
        if self.dump_mode == 'standard': return self.dump_standard()
        if self.dump_mode == 'short': return self.dump_short()
        raise ValueError, "Unknown Mode name '%s'." % dump_mode
        
    def dump_standard(self):
        retobj = {}
        retobj['encoding'] = self.encoding
        retobj['data'] = self.encoded_data
        if self.hashtype:
            retobj['digest'] = self.hashtype + ":" + self.digest
        else:
            retobj['digest'] = None
        return retobj
        
    def dump_short(self):
        """
            Short-mode is unsupported and may fail, or change in the future. Use standard mode.
        """
        retobj = {}
        stdobj = self.dump_standard()
        if stdobj['digest'] is None: stdobj['digest']=''
        retobj['short'] = "%(encoding)s|%(data)s|%(digest)s" % stdobj
        return retobj
        
        
            
    


