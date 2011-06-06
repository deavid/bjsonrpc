Application Programming Interface (API)
========================================

Contents:

.. toctree::
    :maxdepth: 4
 
    bjsonrpc-server
    bjsonrpc-connection
    bjsonrpc-request
    bjsonrpc-handlers
    bjsonrpc-proxies
    bjsonrpc-jsonlib
    bjsonrpc-exceptions
    
.. module:: bjsonrpc
   :synopsis: JSON-RPC over TCP/IP implementation with lots of features.
   
 
Module bjsonrpc
----------------------
bjsonrpc is a pure-python module to connect two peers and call remote procedures
(RPC). This implementation resembles JSON-RPC 1.1 with several additions that
add more interctivity.

You can have a *server*, which accepts multiple client connections, or a client
which is one connection itself.

The implementation is symmetric/bidirectional. That means that the same things 
you can do with a server and with a client. You could create a client which waits
for server requests.
   
bjsonrpc provides two helper functions to easily create 
a server or a connection, linked to a socket:

.. autofunction:: bjsonrpc.createserver

.. autofunction:: bjsonrpc.connect

Other module attributes:
    
.. attribute:: bjsonrpc.__version__

    Version number of the library as a string with the format X.Y

.. attribute:: bjsonrpc.__release__

    Release number of the library as a string with the format X.Y.Z
    

.. attribute:: bjsonrpc.bjsonrpc_options

    Dictionary with global options for the library. 

    **threaded**
        (Default: False) When is set to True, threads will be created for handling 
        each incoming item.

