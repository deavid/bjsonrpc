Quickstart
=================================

To create a program pair that communicates through jsonrpc protocol, this is the 
straightforward way:

Download and Install
----------------------------------

Download the latest package (if you haven't downloaded it yet), from 
the `PyPI page for bjsonrpc`_.

You will need Python 2.5 (2.6 or later recommended) and a JSON library for python.
Python 2.6 and later bundles a json library. With earlier versions you will have
to download and install python-simplejson.

Install the package with the standard distutils::

    $ sudo python setup.py install
    
And the installation is done. 

.. _`PyPI page for bjsonrpc`: http://pypi.python.org/pypi/bjsonrpc/0.2.0

Creating a test server
--------------------------------

Write the following code and save it as rpcserver.py::

    import bjsonrpc
    from bjsonrpc.handlers import BaseHandler
    
    class MyServerHandler(BaseHandler):
        def hello(self, txt):
            response = "hello, %s!." % txt
            print "*", response
            return response
    
    s = bjsonrpc.createserver( handler_factory = MyServerHandler )
    s.debug_socket(True)
    s.serve()

Execute it and leave it running on other window.

Creating a test client
---------------------------------

Write the following code and save it as rpcclient.py::

    import bjsonrpc
    c = bjsonrpc.connect()
    print "::>", c.call.hello("john")
    print "::>", c.call.hello("arnold")
    
Execute it and you should see the following output in the server part::

    >:43: {"params":["john"],"method":"hello","id":1}
    * hello, john!.
    <:46: {"id":1,"result":"hello, john!.","error":null}
    >:45: {"params":["arnold"],"method":"hello","id":2}
    * hello, arnold!.
    <:48: {"id":2,"result":"hello, arnold!.","error":null}

And this output on the client part::

    ::> hello, john!.
    ::> hello, arnold!.

That is! you have a working server and client rpc. Refer to the tutorial for 
more information.

