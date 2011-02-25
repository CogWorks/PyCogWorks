import socket, telnetlib, math

class EyeGaze(object):
    """This is a simple package for connecting with LC Technologies EGServer"""
    
    def __init__(self, host, port):
        super(EyeGaze, self).__init__()
        self.host = host
        self.port = port
        
    def connect(self):
        ret = None
        try:
            self.t = telnetlib.Telnet(self.host, self.port)
        except socket.error, msg:
            ret = msg
        return ret
    
    def __sendCommand(self, msg):
        self.t.write(msg)
    
    def __mod(self, x, y):
        return int(x / y), int(math.fmod(x, y))
    
    def __checksum(self, header, body):
        chksum = 0
        msg = "%s%s" % (header, body)
        for c in msg:
            chksum += ord(c)
        return "%c" % (chksum & 0xff)
    
    def __format_message(self, command, body=""):
        message_length = 5 + len(body)
        i1, r1 = self.__mod(message_length, 65536)
        i2, r2 = self.__mod(r1, 256)
        header = "%c%c%c%c" % (i1, i2, r2, command)
        return "%s%s%s" % (header, body, self.__checksum(header, body))
    
    def calibrate(self):
        msg = self.__format_message(10)
        print "%s" % (msg)
        self.__sendCommand(msg)
