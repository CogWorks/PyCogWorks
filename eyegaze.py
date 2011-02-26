import socket, math, string
from threading import Thread

class EyeGaze(object):
    """This is a simple package for connecting with LC Technologies EGServer"""
    
    def __init__(self, host, port):
        super(EyeGaze, self).__init__()
        self.host = host
        self.port = port
        self.s = None
        
    def _read_message(self):
        ret = None
        header = map(ord,self.s.recv(4))
        body_len = (header[0] * 65536) + (header[1] * 256) + header[2] - 4
        body = None
        accum = sum(header)
        if body_len > 1:
            body = map(ord,self.s.recv(body_len - 1))
            accum += sum(body)
        chksum = ord(self.s.recv(1))
        if chksum == ('\xff' & accum):
            ret = (header[3],body)
        return ret
            
    def _read_loop(self):
        while self.read_messages:
            val = self.read_message()
            if val:
                if val[0] == 0: # eg-gaze-info
                    pass
                elif val[0] == 11: # eg-ws-query
                    pass
                elif val[0] == 13: # eg-clear-screen
                    pass
                elif val[0] == 14: # eg-set-color
                    pass
                elif val[0] == 15: # eg-set-diameter
                    pass
                elif val[0] == 16: # eg-draw-circle
                    pass
                elif val[0] == 17: # eg-draw-cross
                    pass
                elif val[0] == 18: # eg-draw-text
                    pass
                elif val[0] == 19: # eg-cal-complete
                    pass
                elif val[0] == 20: # eg-cal-aborted
                    pass
        
    def _send_message(self, msg):
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
               
    def connect(self):
        """Connect to EGServer"""
        ret = None
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.host, self.port))
            self.read_messages = True
            self.thread = Thread(target=self._read_loop)
            self.thread.run()
        except socket.error, msg:
            ret = msg
        return ret
    
    def disconnect(self):
        """Disconnect from EGServer"""
        self._send_message(self._format_message(32))
        self.s.close()
        self.s = None
    
    def calibrate(self):
        """Start calibration procedure"""
        self._send_message(self._format_message(10))
        
    def data_start(self):
        """Start data logging"""
        self._send_message(self._format_message(30))
        
    def data_stop(self):
        """Stop data logging"""
        self._send_message(self._format_message(31))
        
    def test_message(self, command, body=""):
        return self._send_message(command, body)
    
    def __del__(self):
        if self.s:
            self.disconnect()