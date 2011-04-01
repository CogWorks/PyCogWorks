#!/usr/bin/env python

from __future__ import division
import sys, struct, pprint

HEADER_MAGIC = '>IHHHHHHIHHHHHIH'
EVENT_MAGIC = '>cccc'

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
    print header
    
    events = []
    for i in range(0, header['nEvt']):
        events.append(''.join(struct.unpack(EVENT_MAGIC, file.read(struct.calcsize(EVENT_MAGIC)))))
    print events
    
    print
    MAGIC = '>%s' % ('bbbb' * header['nSmpl'])
    evtData = [None] * header['nEvt']
    for i in range(0, header['nEvt']):
        evtData[i] = struct.unpack(MAGIC, file.read(struct.calcsize(MAGIC)))
        print evtData[i][:20]
    
    if header['verNum'] == 2:
        prec = 'h'
    elif header['verNum'] == 4:
        perc = 'f'
    elif header['verNum'] == 6:
        perc = 'd'
    MAGIC = '>%s' % (perc * header['nSmpl'])
    
    print
       
    data = [None] * header['nChan']
    for i in range(0, header['nChan']):
        data[i] = struct.unpack(MAGIC, file.read(struct.calcsize(MAGIC)))
        print data[i][:20]
        
    print
        
    print len(file.read())
        
    return (header, events, data, evtData)
    
if __name__ == '__main__':
    
    for arg in sys.argv[1:]:
        f = open(arg,'r')
        read(f)
        f.close()