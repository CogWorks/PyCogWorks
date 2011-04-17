#!/usr/bin/env python

import sys, math, simpleBinary

import numpy as np
import matplotlib.pyplot as plt
from scikits.talkbox.spectral.basic import periodogram, arspec

GSN32 = [(3,3),(3,5),(4,3),(4,5),(5,3),(5,5),(6,3),(6,5),(7,3),(7,5),
         (4,2),(4,6),(5,2),(5,6),(6,2),(6,6),(4,4),(2,4),(6,4),(8,4),
         (4,1),(4,7),(6,1),(6,7),(8,2),(8,6),(3,4),(5,4),(1,3),(1,5),
         (2,2),(2,6)]

if __name__ == '__main__':
 
    for arg in sys.argv[1:]:
        f = open(arg,'r')
        header, data, events = simpleBinary.read(f)
        f.close()
        print header
        print
        print 'nEEGData: %d' % (len(data))
        print 'nEventData: %d' % (len(events))
                
        #plt.plot(events[1])
        #plt.show()
        
        fig = plt.figure(1)
        fig.subplots_adjust(hspace=.5,wspace=.3)

        overlap = 0.5
        window = 2 * header.smplFreq
        taper = np.hanning(window)

        mod = header.nChan % 2
        for i in range(0,header.nChan-mod):
            power = []
            fgrid = []
            for game in np.nonzero(events[1])[0]:
                offset = game
                max = offset + 300 * header.smplFreq
                tmp = []
                while offset + window <= max:
                    #sp = arspec(np.multiply(data[i][offset:offset+window], taper), 12, fs=header.smplFreq)
                    sp = periodogram(np.multiply(data[i][offset:offset+window], taper), fs=header.smplFreq)
                    tmp.append(sp[0])
                    fgrid = sp[1]
                    offset += int(window * overlap)
                print len(tmp)
                power.append(np.mean(tmp,0))
            print len(power)
            plt.subplot2grid((8,7),(GSN32[i][0]-1,GSN32[i][1]-1))
            plt.plot(fgrid, np.mean(power,0))
            plt.title(str(i+1))
            plt.axis('tight')
            plt.xlim([45,75])
            #plt.xlim([3,15])
            plt.ylim([0,32])
        plt.show()
        
