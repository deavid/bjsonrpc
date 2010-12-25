bjsonrpc Application Programming Interface
==============================================

.. module:: bjsonrpc
    
.. autofunction:: createserver

.. autofunction:: connect

bjsonrpc.server module
------------------------
.. autoclass:: bjsonrpc.server.Server
    :members:
    :undoc-members: 
    :inherited-members:

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
    :members:
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
