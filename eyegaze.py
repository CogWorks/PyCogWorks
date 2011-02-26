import socket, math, string
from threading import Thread

class EyeGaze(object):
    """This is a simple package for connecting with LC Technologies EGServer"""
    
    def __init__(self, host, port):
        super(EyeGaze, self).__init__()
        self.host = host
        self.port = port
        
    def _read_loop(self):
        pass   
        
    def connect(self):
        """Connect to EGServer"""
        ret = None
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.host, self.port))
            self.thread = Thread(target=self._read_loop)
            self.thread.run()
        except socket.error, msg:
            ret = msg
        return ret
    
    def _sendCommand(self, msg):
        self.s.send(msg)
    
    def _mod(self, x, y):
        return int(x / y), int(math.fmod(x, y))
    
    def _checksum(self, msg):
        chksum = 0
        for c in msg:
            chksum += ord(c)
        return chr(chksum & 0xff)
    
    def _format_message(self, command, body=""):
        msg_len = 5 + len(body)
        i1, r1 = self._mod(msg_len, 65536)
        i2, r2 = self._mod(r1, 256)
        header = chr(i1) + chr(i2) + chr(r2) + chr(command)
        msg = header + body
        msg = msg + self._checksum(msg)
        l = len(msg)
        s = 8 - l % 8 + l
        return string.ljust(msg,s,'\x00')
    
    def test_message(self, command, body=""):
        return self._format_message(command, body)
    
    def calibrate(self):
        """Start calibration procedure"""
        msg = self._format_message(10)
        self._sendCommand(msg)
        
    def data_start(self):
        """Start data logging"""
        msg = self._format_message(30)
        self._sendCommand(msg)
        
    def data_stop(self):
        """Stop data logging"""
        msg = self._format_message(31)
        self._sendCommand(msg)
        
    def __del__(self):
        pass