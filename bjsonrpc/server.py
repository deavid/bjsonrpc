"""
    bjson/server.py
    
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
import socket, select

from connection import Connection
from exceptions import EofError

class Server(object):
    def __init__(self, conn, handler_factory):
        self._conn = conn
        self._handler = handler_factory
        self._debug_socket = False
        self._debug_dispatch = False
        
    def serve(self):
        try:
            sockets = []
            connections = []
            connidx = {}
            while True:
                ready_to_read, ready_to_write, in_error = select.select([self._conn]+sockets,[],[],3.0)
                if not ready_to_read:
                    for c in connections:
                        try:
                            count = c.dispatch_until_empty()
                            if count:
                                print "!!!", count
                        except EofError:
                            c.close()
                            connections.remove(c)
                            #print "Closing client conn."
                    
                    #print ". . ."
                    continue
                
            
                if self._conn in ready_to_read:
                    clientsck, clientaddr = self._conn.accept()
                    sockets.append(clientsck)
            
                    c = Connection(socket = clientsck, address = clientaddr, handler_factory = self._handler)
                    connidx[clientsck.fileno()] = c
                    c._debug_socket = self._debug_socket
                    c._debug_dispatch = self._debug_socket
                    
                    connections.append(c)
                
                for sck in ready_to_read:
                    fileno = sck.fileno()
                    if fileno not in connidx: continue
                    c = connidx[fileno]
                    try:
                        c.dispatch_until_empty()
                    except EofError:
                        c.close()
                        sockets.remove(c._sck)
                        connections.remove(c)
                        #print "Closing client conn."
                    

        finally:
            for c in connections: c.close()
            self._conn.shutdown(socket.SHUT_RDWR)
            self._conn.close()
        