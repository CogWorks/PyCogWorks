#!/usr/bin/env python

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
    print (header,events)
    
    if header['verNum'] == 2:
        prec = 'h'
    elif header['verNum'] == 4:
        perc = 'f'
    if header['verNum'] == 6:
        perc = 'd'
    MAGIC = '>ff'
    print struct.unpack(MAGIC, file.read(struct.calcsize(MAGIC)))
if __name__ == '__main__':
    
    for arg in sys.argv[1:]:
        print arg
        f = open(arg,'r')
        read(f)
        f.close()