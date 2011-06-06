.. _bjsonrpc.jsonlib:

    
Module bjsonrpc.jsonlib 
------------------------    

This module wraps a json library and maps their import/export methods to dumps
and loads. First it tries to load *simplejson* and if it fails it tries *json* (the
internal JSON library for python2.6 or newer)


.. autofunction:: bjsonrpc.jsonlib.dumps
    
.. autofunction:: bjsonrpc.jsonlib.loads
    
