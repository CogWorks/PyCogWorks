import socket, math, string, pygame
from threading import Thread

"""
from eyegaze import *
eg = EyeGaze('1.0.0.21',3999)
eg.connect()
eg.calibrate()
"""

class EyeGaze(object):
    """This is a simple package for connecting with LC Technologies EGServer"""
    
    GAZEINFO                = 0
    VERGENCE                = 5
    IMAGEDATA               = 81
    
    CALIBRATE               = 10
    WORKSTATION_QUERY       = 11
    WORKSTATION_RESPONSE    = 12
    CLEAR_SCREEN            = 13
    SET_COLOR               = 14
    SET_DIAMETER            = 15
    DRAW_CIRCLE             = 16
    DRAW_CROSS              = 17
    DISPLAY_TEXT            = 18
    CALIBRATION_COMPLETE    = 19
    CALIBRATION_ABORTED     = 20
    TRACKING_ACTIVE         = 22
    TRACKING_INACTIVE       = 23
    
    BEGIN_SENDING_DATA      = 30
    STOP_SENDING_DATA       = 31
    CALIBRATE_ABORT         = 21
    BEGIN_SENDING_VERGENCE  = 40
    STOP_SENDING_VERGENCE   = 41
    
    def __init__(self, host, port):
        super(EyeGaze, self).__init__()
        self.host = host
        self.port = port
        self.s = None
        self.do_calibration = False
        self.bg_color = (51,51,153)
        self.eg_color = (0,0,0)
        self.eg_diameter = 0
        self.eg_font = None
        
    def _read_message(self):
        ret = None
        try:
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
        except IndexError:
            pass
        return ret
            
    def _read_loop(self):
        while self.read_messages:
            val = self._read_message()
            code = None
            if val:
                if val[0] == self.GAZEINFO:
                    if len(val[1]) == 24:
                        d = map(chr,val[1])
                        eg_data = {'timestamp': int("".join(d[14:24])),
                                   'camera': int("".join(d[12:14])),
                                   'status': int("".join(d[11:12])),
                                   'pupil': int("".join(d[8:11])),
                                   'x': int("".join(d[0:4])),
                                   'y': int("".join(d[4:8]))}
                        print eg_data
                    else:
                        print val[1]
                elif val[0] == self.WORKSTATION_QUERY:
                    body = "%4d,%4d,%4d,%4d,%4d,%4d,%4d,%4d" % (340, 272,
                                                                self.width,
                                                                self.height,
                                                                self.width,
                                                                self.height,
                                                                0, 0)               
                    self._send_message(self._format_message(12, body))
                elif val[0] == self.CLEAR_SCREEN:
                    code = {'code': val[0]}
                elif val[0] == self.SET_COLOR:
                    self.eg_color = (val[1][2],val[1][1],val[1][0])
                elif val[0] == self.SET_DIAMETER:
                    self.eg_diameter = (val[1][0] * 256) + val[1][1]
                elif val[0] == self.DRAW_CIRCLE:
                    code = {
                            'code': val[0],
                            'x': (val[1][0] * 256) + val[1][1],
                            'y': (val[1][2] * 256) + val[1][3],
                            'diameter': self.eg_diameter,
                            'color': self.eg_color,
                            'save': val[1][4]
                            }
                elif val[0] == self.DRAW_CROSS:
                    code = {
                            'code': val[0],
                            'x': (val[1][0] * 256) + val[1][1],
                            'y': (val[1][2] * 256) + val[1][3],
                            'diameter': self.eg_diameter,
                            'color': self.eg_color
                            }
                elif val[0] == self.DISPLAY_TEXT:
                    code = {
                            'code': val[0],
                            'x': (val[1][0] * 256) + val[1][1],
                            'y': (val[1][2] * 256) + val[1][3],
                            'color': self.eg_color,
                            'text': "".join(map(chr,val[1][4:]))
                            }
                elif val[0] == self.CALIBRATION_COMPLETE:
                    code = {'code': val[0]}
                elif val[0] == self.CALIBRATION_ABORTED:
                    pygame.event.clear(pygame.USEREVENT)
                    code = {'code': val[0]}             
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
        return msg + self._checksum(msg)
    
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
        self.read_messages = False
        self._send_message(self._format_message(32))
        self.s.close()
        self.s = None
    
    def calibrate(self, screen=pygame.display.get_surface(), bgcolor=(51,51,153)):
        """Start calibration procedure"""
        self.bg_color = bgcolor
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
        self.surf = pygame.Surface((self.width, self.height))
        self.surf_rect = self.surf.get_rect()
        self.eg_font = pygame.font.SysFont('courier', 18, bold=True)
        self._send_message(self._format_message(10))
        ret = True
        self.do_calibration = True
        circles = []
        while self.do_calibration:
            tmp = self.surf.copy()
            i = 0
            while i < len(circles):
                pygame.draw.circle(tmp, circles[i][0],(circles[i][1],circles[i][2]), circles[i][3])
                pygame.draw.circle(tmp, circles[i][0], (circles[i][1],circles[i][2]), 1)
                if circles[i][4] == 0:
                    circles.pop(i)
                else:
                    i += 1 
            self.screen.blit(tmp, self.surf_rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        ret = False
                        self.do_calibration = False
                elif event.type == pygame.USEREVENT:
                    if event.code == self.CLEAR_SCREEN:
                        self.surf.fill(self.bg_color)
                    elif event.code == self.DRAW_CIRCLE:
                        if event.save == 0:
                            circles[:] = []
                        circles.append((event.color, event.x, event.y, event.diameter, event.save))
                    elif event.code == self.DRAW_CROSS:
                        pygame.draw.line(self.surf, event.color,
                                         (event.x-event.diameter/2, event.y),
                                         (event.x+event.diameter/2, event.y))
                        pygame.draw.line(self.surf, event.color,
                                         (event.x, event.y-event.diameter/2),
                                         (event.x, event.y+event.diameter/2))
                    elif event.code == self.DISPLAY_TEXT:
                        text = self.eg_font.render(event.text, True, event.color)
                        text_rect = text.get_rect()
                        text_rect.bottomleft = (event.x, event.y)
                        self.surf.blit(text, text_rect)
                    elif event.code == self.CALIBRATION_COMPLETE:
                        self.do_calibration = False
                    elif event.code == self.CALIBRATION_ABORTED:
                        ret = False
                        self.do_calibration = False
        if standalone:
            pygame.display.quit()   
        return ret
        
    def data_start(self):
        """Start data logging"""
        self._send_message(self._format_message(self.BEGIN_SENDING_DATA))
        
    def data_stop(self):
        """Stop data logging"""
        self._send_message(self._format_message(self.STOP_SENDING_DATA))
        
    def __del__(self):
        if self.s:
            self.disconnect()
