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
        Help command to create a socket and associate it to a server.Server object.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind((host, port))
    s.listen(3) 
    return server.Server(s,handler_factory=handler_factory)
        
        
def connect(host="127.0.0.1", port=10123, handler_factory=handlers.NullHandler):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return connection.Connection(s,handler_factory=handler_factory)
        



