""" 
    Copyright (c) 2010 David Martinez Marti
    All rights reserved.

    Licensed under 3-clause BSD License. 
    See LICENSE.txt for the full license text.

"""

__version__ = '0.2'
__release__ = '0.2.0'


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

bjsonrpc_options = {
    'threaded' : False
}

from bjsonrpc.main import createserver, connect

import bjsonrpc.server
import bjsonrpc.connection
import bjsonrpc.request
import bjsonrpc.handlers
import bjsonrpc.proxies
import bjsonrpc.jsonlib
import bjsonrpc.exceptions

