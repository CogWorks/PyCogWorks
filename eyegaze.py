from __future__ import division
import socket, math, string, pygame, struct, time
import numpy as np
from threading import Thread
from fixation import *

"""
    import pygame
    pygame.display.init()
    pygame.font.init()
    from pycogworks.eyegaze import *
    eg = EyeGaze()
    eg.connect('1.0.0.31')
    eg.trace_test()
eg.calibrate(pygame.display.set_mode((1280,1024), pygame.FULLSCREEN))
"""

class EyeGaze(object):
    """This is a simple package for connecting with LC Technologies EGServer"""
    
    GAZEINFO = 0
    VERGENCE = 5
    IMAGEDATA = 81
    
    CALIBRATE = 10
    WORKSTATION_QUERY = 11
    WORKSTATION_RESPONSE = 12
    CLEAR_SCREEN = 13
    SET_COLOR = 14
    SET_DIAMETER = 15
    DRAW_CIRCLE = 16
    DRAW_CROSS = 17
    DISPLAY_TEXT = 18
    CALIBRATION_COMPLETE = 19
    CALIBRATION_ABORTED = 20
    TRACKING_ACTIVE = 22
    TRACKING_INACTIVE = 23
    
    BEGIN_SENDING_DATA = 30
    STOP_SENDING_DATA = 31
    CALIBRATE_ABORT = 21
    BEGIN_SENDING_VERGENCE = 40
    STOP_SENDING_VERGENCE = 41
    
    #EgDataStruct = '<3i6fQ2did'
    EgDataStruct = '3i6fI2did'
    
    def __init__(self, display_w_mm=340, display_h_mm=272):
        super(EyeGaze, self).__init__()
        
        self.display_w_mm = display_w_mm
        self.display_h_mm = display_h_mm
        self.display_w_px = None
        self.display_h_px = None
                
        self.fp = None
        self.s = None
        self.do_calibration = False
        self.bg_color = (51, 51, 153)
        self.eg_color = (0, 0, 0)
        self.eg_diameter = 0
        self.eg_font = None
        self.eg_data = None
        self.fix_data = None
        self.fix_count = 0
        self.process_fixations = True
        self.gaze_log_fn = None
        self.fix_log_fn = None
        self.gaze_log = None
        self.fix_log = None
        
        self.gaze_callback = None
        self.fixation_callback = None

    def _update_display_info(self):
        
        pygame.display.init()
        info = pygame.display.Info()
        self.display_w_px = info.current_w
        self.display_h_px = info.current_h
        
    def _read_message(self):
        ret = None
        try:
            header = map(ord, self.s.recv(4))
            body_len = (header[0] * 65536) + (header[1] * 256) + header[2] - 4
            body = None
            accum = sum(header)
            if body_len > 1:
                body = map(ord, self.s.recv(body_len - 1))
                accum += sum(body)
            chksum = ord(self.s.recv(1))
            if chksum == (255 & accum):
                ret = (header[3], body)
        except IndexError:
            pass
        return ret
            
    def _read_loop(self):
        while self.read_messages:
            val = self._read_message()	
            code = None
            if val:
                if val[0] == self.GAZEINFO:
                    d = "".join(map(chr, val[1]))
                    if len(val[1]) == 24:
                        self.eg_data = {'timestamp': int(d[14:24]),
                                         'camera': int(d[12:14]),
                                         'status': int(d[11:12]),
                                         'pupil': int(d[8:11]),
                                         'x': int(d[0:4]),
                                         'y': int(d[4:8])}
                        if self.gaze_log:
                            self.gaze_log.write('%f\t%f\t%d\t%d\t%d\t%d\t%d\t%d\t%d\n' % (time.time(), time.clock(), pygame.time.get_ticks(), int(d[14:24]), int(d[12:14]), int(d[11:12]), int(d[8:11]), int(d[0:4]), int(d[4:8])))                            
                    elif len(val[1]) == 78:
                        tmp = struct.unpack(self.EgDataStruct, d[1:-5])
                        self.eg_data = {'camera': ord(d[0]),
                                         'status': tmp[0],
                                         'x': tmp[1],
                                         'y': tmp[2],
                                         'pupil': tmp[3],
                                         'xEyeOffset': tmp[4],
                                         'yEyeOffset': tmp[5],
                                         'focusRange': tmp[6],
                                         'focusRangeOffset': tmp[7],
                                         'lensExtOffset': tmp[8],
                                         'fieldcount': tmp[9],
                                         'timestamp': tmp[10],
                                         'gazetime': tmp[10],
                                         'appmarkTime': tmp[11],
                                         'appmarkCount': tmp[12],
                                         'reportTime': tmp[13]}
                        if self.gaze_log:
                            self.gaze_log.write('%f\t%f\t%d\t%d\t%d\t%d\t%d\t%f\t%f\t%f\t%f\t%f\t%f\t%d\t%f\t%f\t%d\t%f\n' % (time.time(), time.clock(), pygame.time.get_ticks(), ord(d[0]), tmp[0], tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], tmp[12], tmp[13]))
                    if self.gaze_callback:
                        self.gaze_callback(self.eg_data)
                    if self.fp:
                        self.fix_data = self.fp.detect_fixation(self.eg_data['status'], self.eg_data['x'], self.eg_data['y'])
                        self.fix_data.timestamp = self.eg_data['timestamp']
                        if self.fix_log:
                            self.fix_log.write('%f\t%f\t%d\t%f\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\n' % (time.time(), time.clock(), pygame.time.get_ticks(), self.fix_data.timestamp, self.fix_data.gaze_found, self.fix_data.gaze_x, self.fix_data.gaze_y, self.fix_data.eye_motion_state, self.fix_data.fix_x, self.fix_data.fix_y, self.fix_data.gaze_deviation, self.fix_data.sac_duration, self.fix_data.fix_duration))
                        if self.fix_data.eye_motion_state == 2:
                            self.fix_count += 1
                        if self.fixation_callback:
                            self.fixation_callback(self.fix_data)
                elif val[0] == self.WORKSTATION_QUERY:
                    body = "%4d,%4d,%4d,%4d,%4d,%4d,%4d,%4d" % (self.display_w_mm,
                                                                self.display_h_mm,
                                                                self.display_w_px,
                                                                self.display_h_px,
                                                                self.display_w_px,
                                                                self.display_h_px,
                                                                0,
                                                                0)               
                    self._send_message(self._format_message(12, body))
                elif val[0] == self.CLEAR_SCREEN:
                    code = {'code': val[0]}
                elif val[0] == self.SET_COLOR:
                    self.eg_color = (val[1][2], val[1][1], val[1][0])
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
                            'text': "".join(map(chr, val[1][4:]))
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
    
    def connect(self, host):
        """Connect to EGServer"""
        ret = None
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((host, 3999))
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
    
    def calibrate(self, screen=pygame.display.get_surface(), bgcolor=(51, 51, 153)):
        """Start calibration procedure"""
        self.bg_color = bgcolor
        standalone = False
        self._update_display_info()
        if screen:
            self.screen = screen
        else:
            standalone = True
            self.screen = pygame.display.set_mode((self.display_w_px, self.display_h_px), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.mouse.set_visible(False)
        self.surf = pygame.Surface((self.display_w_px, self.display_h_px))
        self.surf_rect = self.surf.get_rect()
        pygame.font.init()
        self.eg_font = pygame.font.SysFont('courier', 18, bold=True)
        self._send_message(self._format_message(10))
        ret = True
        self.do_calibration = True
        circles = []
        self.clock = pygame.time.Clock()
        while self.do_calibration:
            tick_time = self.clock.tick(30)
            tmp = self.surf.copy()
            i = 0
            while i < len(circles):
                pygame.draw.circle(tmp, circles[i][0], (circles[i][1], circles[i][2]), circles[i][3])
                pygame.draw.circle(tmp, circles[i][0], (circles[i][1], circles[i][2]), 1)
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
                        self.calibrate_abort()
                elif event.type == pygame.USEREVENT:
                    if event.code == self.CLEAR_SCREEN:
                        self.surf.fill(self.bg_color)
                    elif event.code == self.DRAW_CIRCLE:
                        if event.save == 0:
                            circles[:] = []
                        circles.append((event.color, event.x, event.y, event.diameter, event.save))
                    elif event.code == self.DRAW_CROSS:
                        pygame.draw.line(self.surf, event.color,
                                         (event.x - event.diameter / 2, event.y),
                                         (event.x + event.diameter / 2, event.y))
                        pygame.draw.line(self.surf, event.color,
                                         (event.x, event.y - event.diameter / 2),
                                         (event.x, event.y + event.diameter / 2))
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
    
    def calibrate_abort(self):
        """Abort calibration"""
        self._send_message(self._format_message(self.CALIBRATE_ABORT))
        
    def data_start(self):
        """Start data logging"""
        if self.process_fixations:
            self.fp = FixationProcessor(self.display_w_px / self.display_w_mm)
        self._send_message(self._format_message(self.BEGIN_SENDING_DATA))
        
    def data_stop(self):
        """Stop data logging"""
        self._send_message(self._format_message(self.STOP_SENDING_DATA))
        self.fp = None
        
    def start_logging(self):
        if self.gaze_log_fn:
            self.gaze_log = open(self.gaze_log_fn, "w")
        if self.fix_log_fn:
            self.fix_log = open(self.fix_log_fn, "w")
        
    def stop_logging(self):
        if self.gaze_log:
            self.gaze_log.close()
        if self.fix_log:
            self.fix_log.close()
        
    def trace_test(self, fullscreen=True):
        pygame.display.init()
        pygame.font.init()
        pygame.mouse.set_visible(False)
        self._update_display_info()
        if fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        else:
            self.screen = pygame.display.set_mode((800, 600), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.width, self.height = self.screen.get_size()
        self.surf = pygame.Surface((self.width, self.height))
        self.surf_rect = self.surf.get_rect()
        self.clock = pygame.time.Clock()
        
        self.data_start()
        cont = True
        while cont:
            tick_time = self.clock.tick(60)
            self.screen.fill((0, 0, 0))
            if self.eg_data:
                self.surf.fill((0, 0, 0))
                if self.process_fixations:
                    if self.fix_data and self.fix_data.eye_motion_state > 0:
                        pygame.draw.line(self.surf, (255, 0, 0),
                                         (self.fix_data.fix_x - 10, self.fix_data.fix_y),
                                         (self.fix_data.fix_x + 10, self.fix_data.fix_y))
                        pygame.draw.line(self.surf, (255, 0, 0),
                                         (self.fix_data.fix_x, self.fix_data.fix_y - 10),
                                         (self.fix_data.fix_x, self.fix_data.fix_y + 10))
                else:
                    pygame.draw.line(self.surf, (255, 0, 0),
                                     (self.eg_data['x'] - 10, self.eg_data['y']),
                                     (self.eg_data['x'] + 10, self.eg_data['y']))
                    pygame.draw.line(self.surf, (255, 0, 0),
                                     (self.eg_data['x'], self.eg_data['y'] - 10),
                                     (self.eg_data['x'], self.eg_data['y'] + 10))
                self.screen.blit(self.surf, self.surf_rect)
            pygame.display.flip()
            if pygame.event.peek():
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            cont = False
        self.data_stop()
        pygame.display.quit()
        
    def __del__(self):
        if self.s:
            self.disconnect()
