bjsonrpc Application Programming Interface
==============================================

.. module:: bjsonrpc
   :synopsis: JSON-RPC over TCP/IP implementation with lots of features.

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


.. _bjsonrpc.server:

bjsonrpc.server module
------------------------
.. autoclass:: bjsonrpc.server.Server
    :members:
    :undoc-members: 
    :inherited-members:

.. _bjsonrpc.connection:

bjsonrpc.connection module
--------------------------
.. autoclass:: bjsonrpc.connection.Connection
    :members:
    :undoc-members: 
    :inherited-members:
    
.. autoclass:: bjsonrpc.connection.RemoteObject
    :members:
    :undoc-members: 
    :inherited-members:

bjsonrpc.request module
------------------------
.. autoclass:: bjsonrpc.request.Request
    :members:
    :undoc-members: 
    :inherited-members:
    
bjsonrpc.handlers module
------------------------
.. autoclass:: bjsonrpc.handlers.BaseHandler
    :members: _setup
    :undoc-members: 
    :inherited-members:
    
.. autoclass:: bjsonrpc.handlers.NullHandler
    :members:
    :undoc-members: 
    :inherited-members:
    
bjsonrpc.proxies module
------------------------    
.. autoclass:: bjsonrpc.proxies.Proxy
    :members:
    :undoc-members: 
    :inherited-members:

bjsonrpc.jsonlib module
------------------------    
.. autofunction:: bjsonrpc.jsonlib.dumps
    
.. autofunction:: bjsonrpc.jsonlib.loads
    
bjsonrpc.exceptions module
--------------------------    
.. autoexception:: bjsonrpc.exceptions.EofError
.. autoexception:: bjsonrpc.exceptions.ServerError
