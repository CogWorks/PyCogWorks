import socket, telnetlib, json

class CogWorld(object):
    """This is a simple package for connecting with CogWorld"""
    
    def __init__(self, host, port, id):
        super(CogWorld, self).__init__()
        self.host = host
        self.port = port
        self.id = id
        
    def connect(self):
        ret = None
        try:
            self.t = telnetlib.Telnet(self.host, self.port)
        except socket.error, msg:
            ret = msg
        return ret
        
    def disconnect(self):
        self.t.close()
        
    def _sendCommand(self, command):
        self.t.write(command + '\n')
        return json.loads(self.t.read_until('\n'))['result']
    
    def cwGetVersion(self):
        cmd = {'method':'cwGetVersion', 'id':self.id}
        return self._sendCommand(json.dumps(cmd))
    
    def cwEegBeginRecord(self):
        cmd = {'method':'cwEegBeginRecord', 'id':self.id}
        return self._sendCommand(json.dumps(cmd))
    
    def cwEegEndRecord(self):
        cmd = {'method':'cwEegEndRecord', 'id':self.id}
        return self._sendCommand(json.dumps(cmd))
    
    def cwEegEventNotify(self, duration, type_code, label, data):
        cmd = {'method':'cwEegEventNotify', 'params':[duration, type_code, label, data], 'id':self.id}
        return self._sendCommand(json.dumps(cmd))
    
    def cwLogInfo(self, list):
        cmd = {'method':'cwLogInfo', 'params':[list], 'id':self.id}
        return self._sendCommand(json.dumps(cmd))
    
    def cwGetEyetrackerIp(self):
        cmd = {'method':'cwGetEyetrackerIp', 'id':self.id}
        return self._sendCommand(json.dumps(cmd))
