"""
    bjson/main.py
    
    Copyright (c) 2015 Miriam Ruiz
    All rights reserved.

    Licensed under 3-clause BSD License. 
    See LICENSE.txt for the full license text.

"""

#import serial

class SerialSocket:
    def __init__(self, serial_port):
        self.serialport = serial_port
        self.conn = None
        self.timeout = None

    def connect(self, address):
        self._address = (self._host, self._port) = address

    def setsockopt(self, family, type, protocol):
        self.family = family
        self.protocol = protocol
        self.type = type

    def recv(self, bufsize, flags=None):
        data = self.serialport.read()
        return data

    def fileno(self):
        return self.serialport.fileno()

    def settimeout(self, timeout):
        if timeout is None:
            self.timeout = None
        else:
            self.timeout = timeout

    def gettimeout(self):
        return self.timeout

    def setsockopt(self, level, optname, value):
        pass

    def getsockopt(self, level, optname, buflen=None):
        return 0

    def bind(self, address):
        pass

    def accept(self):
        return self, 'c'

    def getsockname(self):
        return ('0.0.0.0', 0)

    def setblocking(self, flag):
        pass

    def listen(self, backlog):
        pass

    def sendall(self, buffer, flags=None):
        return len(data)

    def send(self, data, flags=None):
        self.serialport.write(data)
        return len(data)

    def getpeername(self):
        return 'peer'

    def shutdown(self, how):
        #print(self.serialport.name + " shutdown")
        pass

    def close(self):
        #print(self.serialport.name + " close")
        self.serialport.close()
