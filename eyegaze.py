import socket, math, string, pygame
from threading import Thread

class EyeGaze(object):
    """This is a simple package for connecting with LC Technologies EGServer"""
    
    def __init__(self, host, port):
        super(EyeGaze, self).__init__()
        self.host = host
        self.port = port
        self.s = None
        self.do_calibration = False
        self.eg_color = (0,0,0)
        self.eg_diameter = 0
        self.eg_font = None
        
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
        if chksum == (255 & accum):
            ret = (header[3],body)
        return ret
            
    def _read_loop(self):
        while self.read_messages:
            val = self._read_message()
            code = None
            if val:
                if val[0] == 0: # eg-gaze-info
                    pass
                elif val[0] == 11: # eg-ws-query
                    body = "%4d,%4d,%4d,%4d,%4d,%4d,%4d,%4d" % (340, 272, self.width, self.height, self.width, self.height, 0, 0)               
                    self._send_message(self._format_message(12, body))
                elif val[0] == 13: # eg-clear-screen
                    code = {'code': 'clear', 'color': self.eg_color}
                elif val[0] == 14: # eg-set-color
                    self.eg_color = (val[1][2],val[1][1],val[1][0])
                elif val[0] == 15: # eg-set-diameter
                    self.eg_diameter = (val[1][0] * 256) + val[1][1]
                elif val[0] == 16: # eg-draw-circle
                    code = {
                            'code': 'circle',
                            'x': (val[1][0] * 256) + val[1][1],
                            'y': (val[1][2] * 256) + val[1][3],
                            'diameter': self.eg_diameter,
                            'color': self.eg_color
                            }
                elif val[0] == 17: # eg-draw-cross
                    code = {
                            'code': 'cross',
                            'x': (val[1][0] * 256) + val[1][1],
                            'y': (val[1][2] * 256) + val[1][3],
                            'diameter': self.eg_diameter,
                            'color': self.eg_color
                            }
                elif val[0] == 18: # eg-draw-text
                    code = {
                            'code': 'text',
                            'x': (val[1][0] * 256) + val[1][1],
                            'y': (val[1][2] * 256) + val[1][3],
                            'color': self.eg_color,
                            'text': "".join(map(chr,val[1][4:]))
                            }
                elif val[0] == 19: # eg-cal-complete
                    code = {'code': 'complete'}
                elif val[0] == 20: # eg-cal-aborted
                    pygame.event.clear(pygame.USEREVENT)
                    code = {'code': 'abort'}             
                if code and self.do_calibration:
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT, dict(code)))
        
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
            self.thread.start()
        except socket.error, msg:
            ret = msg
        return ret
    
    def disconnect(self):
        """Disconnect from EGServer"""
        self._send_message(self._format_message(32))
        self.s.close()
        self.s = None
    
    def calibrate(self, screen=pygame.display.get_surface()):
        """Start calibration procedure"""
        standalone = False
        if screen:
            self.screen = screen
        else:
            standalone = True
            pygame.display.init()
            pygame.font.init()
            pygame.mouse.set_visible(False)
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)
            self.width, self.height = self.screen.get_size()
            self.eg_font = pygame.font.Font(None, 24)
            self.surf = pygame.Surface((self.width, self.height))
            self.surf_rect = self.surf.get_rect()
        self._send_message(self._format_message(10))
        ret = True
        self.do_calibration = True
        while self.do_calibration:
            self.screen.blit(self.surf, self.surf_rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        ret = False
                        self.do_calibration = False
                elif event.type == pygame.USEREVENT:
                    print event
                    if event.code == 'clear':
                        self.surf.fill(event.color)
                    elif event.code == 'circle':
                        pygame.draw.circle(self.surf, event.color, 
                                           (event.x,event.y),
                                           event.diameter)
                    elif event.code == 'cross':
                        pygame.draw.line(self.surf, event.color,
                                         ((event.x-event.diameter/2), event.y),
                                         ((event.x+event.diameter/2), event.y))
                        pygame.draw.line(self.surf, event.color,
                                         (event.x, (event.y-event.diameter/2)),
                                         (event.x, (event.y+event.diameter/2)))
                    elif event.code == 'text':
                        text = self.eg_font.render(event.text, True, event.color)
                        text_rect = text.get_rect()
                        text_rect.center = (event.x, event.y)
                        self.surf.blit(text, text_rect)
                    elif event.code == 'complete':
                        self.do_calibration = False
                    elif event.code == 'abort':
                        ret = False
                        self.do_calibration = False
        if standalone:
            pygame.display.quit()   
        return ret
        
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
