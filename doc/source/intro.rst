Introduction to bjsonrpc
=================================

About
------
*bjsonrpc* is a pure-python module that ships an implementation of the 
well-known JSON-RPC protocol over raw TCP sockets with more features. It is 
aimed at speed and simplicity and it adds some other extensions to JSON-RPC 
that makes *bjsonrpc* a very powerful tool as a IPC mechanism over 
low bandwidth.


Basic design principles
--------------------------

Imagine two computers connected through a network. It could be a reasonably fast 
network (10mbps LAN), a probably faulty network (3mbps WiFi), or maybe a very
slow connection (1000/300kbps Internet connection). And we want to be able to
communicate and interact between two programs one on each party. 

Which one is the server (has the listening port) and which one is the client 
(will try to connect the other one) is a decision that matters for most installations.

For example, a portable device that connects through a Wireless network is better
to configure it as a client, and a server should be something more reliable 
(a machine with a cable connection, which is running the most of the time).

But most of the client-server protocol schemes will force you to put the server
to one specific device, and the client in the other. To be more specific, in 
RPC-like protocols, the server usually must be the one that recieves calls, 
and the client is the one that sends them. This limitation that seems logic,
isn't enough on most professional RPC systems, there are lots of RPC uses that
require a *"reversed configuration"*, and some other uses require the both things
at the same time.

**bjsonrpc** is designed from scratch with some of this ideas in mind to overcome 
this limitations (there are several others i'll explain later). It uses the 
JSON-RPC protocol over TCP/IP sockets (does not handle nor creates HTTP 
connections), and should be fairly compatible with other JSON (1.0, 1.1) clients 
and servers. In **bjsonrpc** there are two basic rules that aren't in the basic 
JSON protocol specification:

* Client and Server concepts are things about sockets, not about the protocol. 
  The *only* difference between a client and a server is that a client should 
  connect to, and a server waits for connections. The rest is *exactly the same*.
  This is known as bidirectionality. The same message types can be sent from 
  both ends.

* There is no guarantee on the return or processing order of RPC calls. That means
  that peers never rely on assumptions like *"if i sent request A and later B, 
  i'll get A response first, and B will be the next"*. That's untrue. Requests
  can be handled in any order, with any priority, and optionally in parallel.
  If you need to execute a request B after a request A is done, you should wait 
  for A result. (or at least indicate to the server that this call should wait
  to A request to complete before proceding)
  
* It is not stateless. *bjsonrpc* can create stateless peers, but makes it easier
  to create stateful peers, which will be configurable per connection, or will
  require several commands to complete one operation.
  

The messages sent are simple JSON objects followed by a newline *'\\n'* separator.
You should keep messages as short as you can. That will give you better response
speed with slow connections. If you plan to send lots of data through a message
consider dividing them in small parts (about 4K of data per message). With one 
big packet, the entire stream will be blocked until it is sucessfully sent and
no other queries can be sent while this is happening. 

*bjsonrpc* implementation aims to:

* Have a complete bidirectional protocol.

* Virtually remove the network lag. 

* Enhance parallel querys (parallel method querying, parallel method dispatching, etc)

* Make very easy to use it as a general IPC mechanism, to control the state of 
  the objects of the other peer, to create authentication mechanisms, syncing 
  data or lists... 
  
* Minimize the network bandwidth used.


Disavantages of bjsonrpc
-----------------------------

* The implementation differs from standard, it tries to be compatible, but is not
  always possible. 
  
* At this moment there is only a Pure-python implementation (it would be good to 
  have Java, C# and Ruby ones)

* Doesn't has any HTTP implementation (but there are already lots of json-rpc 
  libraries with HTTP). Some features are clearly incompatible with HTTP.
  
Examples of uses of bjsonrpc
--------------------------------

* PDA and handheld communication with a central server. Is faster than xmlrpc 
  and it allows the server to notify the client if updates of the data are available.
  
* As a standard communication system between several processes that could be 
  on the same machine, or connected somewhere in the net.
  
* As a notification system (for updates, syslog, etc)

* As a syncronization system (send files, rows, actions, and get files, rows, ...)  

* As a remote control for your services. (start, stop, restart .. )

* As a cloud-computing solution.
