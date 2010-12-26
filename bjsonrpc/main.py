"""
    bjson/main.py
    
    Copyright (c) 2010 David Martinez Marti
    All rights reserved.

    Licensed under 3-clause BSD License. See LICENSE.txt for the full license text.

"""

import socket
import sys
import inspect, traceback

__all__ = [
    "createserver",
    "connect",
    "server",
    "connection",
    "request",
    "handlers",
    "proxies",
    "jsonlib",
    "exceptions"
]

import server
import connection
import request
import handlers
import proxies
import jsonlib
import exceptions


def createserver(host="127.0.0.1", port=10123, handler_factory=handlers.NullHandler):
    """
        Creates a *bjson.server.Server* object linked to a listening socket.
        
        Parameters:
        
        **host**
          Address (IP or Host Name) to listen to as in *socket.bind*.
          Use "0.0.0.0" to listen to all address. By default this points to 
          127.0.0.1 to avoid security flaws.
          
        **port**
          Port number to bind the socket. In Unix, port numbers less
          than 1024 requires special permissions. 
          
        **handler_factory**
          Class to instantiate to publish remote functions.
        
        **(return value)**
          A *bjson.server.Server* instance or raises an exception.
        
        Servers are usually created this way::
        
            import bjsonrpc
            
            server = bjsonrpc.createserver("0.0.0.0")
            server.serve()
            
        Check :ref:`bjsonrpc.server` documentation
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind((host, port))
    s.listen(3) 
    return server.Server(s,handler_factory=handler_factory)
        
        
def connect(host="127.0.0.1", port=10123, handler_factory=handlers.NullHandler):
    """
        Creates a *bjson.connection.Connection* object linked to a connected
        socket.
        
        Parameters:
        
        **host**
          Address (IP or Host Name) to connect to.
          
        **port**
          Port number to connect to.
          
        **handler_factory**
          Class to instantiate to publish remote functions to the server. 
          By default this is *NullHandler* which means that no functions are
          executable by the server.
        
        **(return value)**
          A *bjson.connection.Connection* instance or raises an exception.
        
        Connections are usually created this way::
        
            import bjsonrpc
            
            conn = bjsonrpc.connect("rpc.host.net")
            print conn.call.some_method_in_server_side()
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return connection.Connection(s,handler_factory=handler_factory)
        



