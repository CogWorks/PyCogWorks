import time, random
from collections import deque

class NBack(object):
    
    NUMERIC = 0
    ALPHA1 = 1
    ALPHA2 = 2
    ALPHA3 = 3

    def __init__(self, p=None, n=1, type=ALPHA1):
        super(NBack, self).__init__()
        
        self.p = p
        self.n = n
        self.buffer = deque()
        self.pool = self._generate_stimuli_pool(type)
        
    def _generate_stimuli_pool(self, type):
        
        pool = None
        
        if type == self.NUMERIC:
            pool = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        
        elif type == self.ALPHA1:
            pool = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
            
        elif type == self.ALPHA2:
            pool = ['b', 'c', 'd', 'g', 'j', 'k', 'l', 'm',
                    'n', 'p', 'r', 's', 't', 'x', 'y', 'z']            
        
        elif type == self.ALPHA3:
            pool = ['b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
                    'n', 'o', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z']
            
        return pool
    
    def next(self):
        new = random.choice(self.pool)
        if len(self.buffer) == self.n + 1:
            while new == self.buffer[-2]:
                new = random.choice(self.pool)
            if self.p == None:
                self.buffer.appendleft(new)
            elif 0 <= self.p and self.p <= 1:
                if random.random() < self.p:
                    self.buffer.appendleft(self.buffer[-2])
                else:
                    self.buffer.appendleft(new)
            self.buffer.pop()
        else:
            self.buffer.appendleft(new)
        return self.buffer[0]
    
    def respond(self, ans):
        ret = None
        if len(self.buffer) == self.n + 1:
            match = self.buffer[0] == self.buffer[-1]
            if match == ans:
                ret = True
            else:
                ret = False        
        return ret