Basic Tutorial 
=================================

Here we'll show the basic things you can do with **bjsonrpc**. 

Create basic client and server programs
-----------------------------------------

The most basic client and server have only two lines each one. Let's see the 
server part::

    import bjsonrpc
    bjsonrpc.createserver().serve()
    
And the client code::

    import bjsonrpc
    c = bjsonrpc.connect()

That code already handles the connections and does all for you. You only have to
add the methods to publish and make use of them.

*createserver()* method returns a Server instance, and *connect()* method returns
a Connection instance. Server instance is useful to configure how the clients 
and new connections will be handled. Connection instance is the main tool for
calling remote methods.

Host and port are by default 127.0.0.1:10123 both for client and server examples.

Let's see a example with method calling from client to server. There is the 
server code::

    from bjsonrpc.handlers import BaseHandler
    from bjsonrpc import createserver
    import time
    
    class ServerHandler(BaseHandler):
        def time(self):
            return time.time()
        
        def delta(self,start):
            return time.time() - start
    
    s = createserver(host="0.0.0.0", handler_factory=ServerHandler)
    s.serve()

Here we have created a Handler for server methods, and we ve declared a method
called *time*, which returns the current time as a floating point. Another method 
called *delta* expects a time argument and returns a quantity of seconds elapsed 
from start. Very simple, isn't it?

Notice that we've specified a host for the server, is where the socket will bind
to for incoming connections. "0.0.0.0" is meant for listening to all interfaces.

Now, here's a client example using those methods::

    from bjsonrpc import connect
    
    c = connect()
    time1 = c.call.time()
    # do something here ...
    print "Time:", time1
    print "Delta:", c.call.delta(time1)
    
As you can see, calling remote methods is fairly simple. Just use the *call* 
attribute of the Connection instance, and call the function as it were local.

Call is a connection proxy: it will send your request to the connection 
internals, and the connection will convert it to JSON. When a response is 
received from the channel, call will return the value received or raise a
ServerException.

Connection Proxies
----------------------

A connection proxy is a class that makes it easier to call a remote function.
By default a connection comes with three connection proxies: *call*, *method* and
*notice*.

Here's a short description for each one:

*connection* . **call** . methodname(...)
    Calls a remote method named *methodname* with the args given. It **will wait
    and block** until a response for this method is received. The result is 
    returned as a value or a ServerError is raised if there were errors.
    
*connection* . **method** . methodname(...)
    Calls a remote method named *methodname* with the args given. Writes to the
    socket and **returns without waiting**. It returns a Request object which is 
    useful to retrieve the return value later.
    
*connection* . **notify** . methodname(...)
    Calls a remote method named *methodname* with the args given. Writes to the
    socket and returns without waiting. It tells to the server to **discard the
    returning value** or errors produced by the call.
    
Any server method can be called with any of these 3 proxies. If you don't know
what you should use, start using the *call* proxy because is simpler. When 
you need more performance you'll should take a look to the other two. *Method* 
proxy virtually removes the network lag on multiple calls that aren't required 
to be executed in serial order. *Notify* proxy doubles bandwidth the eficiency 
of *method* removing the return value.

You can also make *call* proxy to go as fast as *method* proxy using python 
threads. This will create concurrent calls and avoids using complex methods.
But sometimes threads are complex than the *method* proxy, so is your choice.

    

Stateful server
----------------------------------

In addition of standard stateless servers you can code very easily a server
where a state is hold for the connection. Stateful connections are very good
for some cases, but try to reduce them at a minimum, because with an eventual 
disconnection you will lose all changes you've made to the handler. So, if you 
need persistence, you should write to disk or to global variables. That is left
to the developer.

Here is another server example with states::

    from bjsonrpc.handlers import BaseHandler
    from bjsonrpc import createserver
    
    class ServerHandler(BaseHandler):
        def _setup(self):
            self.fifo = []
            self.maxitems = 32
        
        def write(self, element):
            if len(self.fifo) >= self.maxitems:
                raise ValueError("FIFO maximum capacity reached")
            self.fifo.append(element)
        
        def read(self): return self.fifo.pop(0)
        
    s = createserver(host="0.0.0.0", handler_factory=ServerHandler).serve()

There is a special *_setup()* method to make easier the inheritance. This function
is called just after *__init__()* and you don't have to call the super function.
It is the recomended place to write your initialization statements. Every attribute
you change for the handler instance will be accessible for every method of the
same connection. Another connection will get another handler instance with different
values inside.

An example client for this one could be::

    from bjsonrpc import connect
    
    c = connect()
    request_list = []
    for i in range(15): # this is done in paralell
        request_list.append(c.method.write(i))
    
    # Wait for every request
    for request in request_list: request.wait() 
    
    for i in range(10): 
        print c.call.read(),
    print
    
    # there are 5 entries left in the fifo buffer.

You will see that even with 5 entries left, repeated calls to the RPC server 
produce the same output. The initial state is the same for every connection.

If you play with values you could see in the client several exceptions blaming 
about end of capacity on the FIFO (could not write), or no elements to pop from
the list (could not read). These exceptions can be handled in a general 
try/except clause::

    from bjsonrpc import connect
    from bjsonrpc.exceptions import ServerError
    c = connect()
    while True:
        try:
            c.call.read()
        except ServerError:
            break


Exceptions
----------------------------------------

Exceptions on the server are propagated to the client. There are two kind of 
exceptions: expected exceptions and unexpected ones. Expected exceptions are 
those raised by the developer, meant to be catched at the client code. 
Unexpected ones are those exceptions that should be catched by python code at
the server but they weren't. The second ones may hide a bug on your code, so
by default, bjsonrpc masks them as a ServerError. In some future could be a mode
indicating wether the server should tell anything about the error to the client
or not. By now, it's a text indicating the basics of the error.

The library knows that the exception is expected by the programmer because it
is a subclass of bjsonrpc.exceptions.ServerError. So, you can subclass this to
create your own server exceptions. 

Actually is impossible to tell the library that all exceptions are expected, or
which ones (for example is impossible to send a TypeError to the client). This
may be addressed in the future.



   
    

    
    



 