from bjsonrpc.handlers import BaseHandler
from bjsonrpc import createserver
import threading

class ServerHandler(BaseHandler):
    def ping(self):
        return "pong"
    
    def add2(self, num1 ,  num2):
        return num1 + num2
        
    def addN(self, *args):
        return sum(args)
    
    def addnlist(self, nlist):
        tot = 0
        for xlist in nlist:
            tot += sum(xlist)
            
        return tot
    
    def getabc(self, a=None, b=None, c=None):
        return (a, b, c)
        


def start():
    global server,  server_thread
    server = createserver(handler_factory=ServerHandler)
    server_thread = threading.Thread(target=server.serve)
    server_thread.start()

def stop():
    global server,  server_thread
    server.stop()
    server_thread.join(timeout=5)
    if server_thread.is_alive():
        raise IOError("Server Still Alive!!!")
    
    del server_thread
    del server
