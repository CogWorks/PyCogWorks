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
    
    def _sendCommand(self, msg):
        self.t.write(msg)
    
    def _mod(self, x, y):
        return int(x / y), int(math.fmod(x, y))
    
    def _checksum(self, header, body):
        chksum = 0
        msg = "%s%s" % (header, body)
        for c in msg:
            chksum += ord(c)
        return "%c" % (chksum & 0xff)
    
    def _format_message(self, command, body=""):
        message_length = 5 + len(body)
        i1, r1 = self._mod(message_length, 65536)
        i2, r2 = self._mod(r1, 256)
        header = "%c%c%c%c" % (i1, i2, r2, command)
        return "%s%s%s" % (header, body, self._checksum(header, body))
    
    def calibrate(self):
        msg = self._format_message(10)
        self._sendCommand(msg)
        
    def start(self):
        msg = self._format_message(30)
        self._sendCommand(msg)
        
    def stop(self):
        msg = self._format_message(31)
        self._sendCommand(msg)
