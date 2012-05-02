#!/usr/bin/env python

from __future__ import division
import sys, struct
import numpy as np
import matplotlib.pyplot as plt

UGLY_HEADER = '>HHHHHHLHHHHHLH'

class UGLY():
    '''Netstation Unsegmented Simple Binary File Header''' 
    
    def __init__(self, verNum, header):
        self.verNum = verNum
        self.year = header[0]
        self.month = header[1]
        self.day = header[2]
        self.hour = header[3]
        self.minute = header[4]
        self.second = header[5]
        self.millisec = header[6]
        self.smplFreq = header[7]
        self.nChan = header[8]
        self.boardGain = header[9]
        self.nConvbit = header[10]
        self.ampRange = header[11]
        self.nSmpl = header[12]
        self.nEvt = header[13]
        self.eventCodes = []
        self.perc = get_percision( self.verNum )
        self.magic = '>%s' % ( self.perc * ( self.nChan + self.nEvt ) )
    
    def __str__(self):
        return 'verNum: %d\nperc: %s\nyear: %d\nmonth: %d\nday: %d\n' \
                'hour: %d\nminute: %d\nsecond: %d\nmillisec: %d\n' \
                'smplFreq: %d\nnChan: %d\nboardGain: %d\nnConvbit: %d\n' \
                'ampRange: %d\nnSmpl: %d\nnEvt: %d\neventCodes: %s' % \
                (self.verNum, self.perc, self.year, self.month, self.day,
                 self.hour, self.minute, self.second, self.millisec,
                 self.smplFreq, self.nChan, self.boardGain, self.nConvbit,
                 self.ampRange, self.nSmpl, self.nEvt, self.eventCodes)
                
def get_percision(verNum):
    if verNum == 2 or verNum == 3:
        return 'h'
    elif verNum == 4 or verNum == 5:
        return 'f'
    elif verNum == 6 or verNum == 7:
        return 'd'
    
def is_segmented(verNum):
    '''Version number will be odd if the data is segmented.'''
    return verNum % 2

def has_zeros(nChan):
    '''The number of channels will be odd if the calibration channel exists.'''
    return nChan % 2

def is_microvolts(header):
    '''If the bits and range header fields are 0 then the data are in microvolts.'''
    if not header.nConvbit and not header.ampRange:
        return True
    else:
        return False

def convert_to_microvolts(header, data):
    '''Convert data from A/D units to microvolts.'''
    if not is_microvolts(header):
        if has_zeros(header.nChan) and header.boardGain:
            '''Use the more accurate formula'''
            f = lambda x: ( x[0] - x[1] ) * 400 / header.boardGain
            for i in range( 1, len(data) ):
                data[i] = map( f, zip( data[i], data[0] ) )
        else:
            '''Use the less accurate formula'''
            f = lambda x: ( header.ampRange / 2 ** header.nConvbit ) / x
            for i in range( 1, len(data) ):
                data[i] = map( f, data[i] )
    return data

def get_unsegmented_data(file, header):
    data = []
    for i in range(0, header.nSmpl):
        data.append(struct.unpack(header.magic, file.read(struct.calcsize(header.magic))))
    return zip(*data)

def read(file):
    
    verNum = struct.unpack('>L', file.read(struct.calcsize('>L')))[0]
    assert verNum > 1 and verNum < 8
    
    if is_segmented(verNum):
        pass
    else:
        header = UGLY(verNum, struct.unpack(UGLY_HEADER, file.read(struct.calcsize(UGLY_HEADER))))
        for i in range(0, header.nEvt):
            header.eventCodes.append(''.join(struct.unpack('>cccc', file.read(struct.calcsize('>cccc')))))
        data = get_unsegmented_data(file, header)

    """

    MAGIC = '>%s' % (perc * header['nSmpl'])
    
    print
       
    data = [None] * header['nChan']
    for i in range(0, header['nChan']):
        data[i] = struct.unpack(MAGIC, file.read(struct.calcsize(MAGIC)))
        print data[i][:20]
        
    print
    MAGIC = '>%s' % ('f' * header['nSmpl'])
    evtData = [None] * header['nEvt']
    for i in range(0, header['nEvt']):
        evtData[i] = struct.unpack(MAGIC, file.read(struct.calcsize(MAGIC)))
        
    print len(file.read())
    """
    
    return header, data[:header.nChan], data[header.nChan:]
    
if __name__ == '__main__':
    
    for arg in sys.argv[1:]:
        f = open(arg,'r')
        read(f)
        f.close()