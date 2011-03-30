#!/usr/bin/env python

from __future__ import division
import sys, struct, pprint

HEADER_MAGIC = '>IHHHHHHIHHHHHIH'
EVENT_MAGIC = '>CCCC'

def read(file):
    header = struct.unpack(HEADER_MAGIC, file.read(struct.calcsize(HEADER_MAGIC)))
    header = {
              'verNum': header[0],
              'year': header[1],
              'month': header[2],
              'day': header[3],
              'hour': header[4],
              'minute': header[5],
              'second': header[6],
              'millisec': header[7],
              'smplFreq': header[8],
              'nChan': header[9],
              'boardGain': header[10],
              'nConvbit': header[11],
              'ampRange': header[12],
              'nSmpl': header[13],
              'nEvt': header[14]}
    events = []
    for i in range(0, header['nEvt']):
        events.append(struct.unpack(EVENT_MAGIC, file.read(struct.calcsize(EVENT_MAGIC))))
    
    if header['verNum'] == 2:
        prec = 'h'
    elif header['verNum'] == 4:
        perc = 'f'
    elif header['verNum'] == 6:
        perc = 'd'
    MAGIC = '>%s' % (perc * header['nSmpl'])
    
    data = [None] * header['nChan']
    for i in range(0, header['nChan']-1):
        data[i] = struct.unpack(MAGIC, file.read(struct.calcsize(MAGIC)))
        file.read(1)
        
    return (header, events, data)
    
if __name__ == '__main__':
    
    for arg in sys.argv[1:]:
        f = open(arg,'r')
        read(f)
        f.close()