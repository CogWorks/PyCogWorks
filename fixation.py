from __future__ import division
import pickle, math, json

class FixationData(object):
    iStartCount     = 0
    iEndCount       = 0
    iNSamples       = 0
    fXSum           = 0.0
    fYSum           = 0.0
    fX              = 0.0
    fY              = 0.0
    
    def __str__(self):
        return json.dumps({'iStartCount': self.iStartCount,
                           'iEndCount': self.iEndCount,
                           'iNSamples': self.iNSamples,
                           'fXSum': self.fXSum,
                           'fYSum': self.fYSum,
                           'fX': self.fX,
                           'fY': self.fY})
    
class GazeData(object):
    fXGaze          =  0.0
    fYGaze          =  0.0
    bGazeFound      =  0
    iEyeMotionState =  0
    fXFix           =  0.0
    fYFix           =  0.0
    fGazeDeviation  = -0.1
    iSacDuration    =  0
    iFixDuration    =  0
    
    def __str__(self):
        return json.dumps({'Gaze': [self.fXGaze, self.fYGaze],
                           'bGazeFound': self.bGazeFound,
                           'iEyeMotionState': self.iEyeMotionState,
                           'Fix': [self.fXFix, self.fYFix],
                           'fGazeDeviation': self.fGazeDeviation,
                           'iSacDuration': self.iSacDuration,
                           'iFixDuration': self.iFixDuration})
        

class FixationProcessor(object):
    
    MOVING              = 0
    FIXATING            = 1
    FIXATION_COMPLETED  = 2
    
    NEW_FIX             = 0
    PRES_FIX            = 1
    PREV_FIX            = 2
    
    RING_SIZE           = 121
    
    def __init__(self, fHorzPixPerMm, fMinFixMs=100,
                 fGazeDeviationThreshMm=6.35, iSamplePerSec=120):
        super(FixationProcessor, self).__init__()
        
        self.iMinimumFixSamples = int(fMinFixMs * iSamplePerSec / 1000.0)
        if self.iMinimumFixSamples < 3: self.iMinimumFixSamples = 3
        print '--> Minimum Fixation Samples: %d <--' % (self.iMinimumFixSamples)
    
        self.fGazeDeviationThreshPix = fGazeDeviationThreshMm * fHorzPixPerMm
        print '--> Gaze Deviation Threshold: %f px <--' % (self.fGazeDeviationThreshPix)
        
        self.iMaxMissedSamples = 3
        self.iMaxOutSamples = 1
    
        self.stRingBuf = [GazeData() for i in range(0,self.RING_SIZE)]
        self.iRingIndex = 0
        self.iRingIndexDelay = self.RING_SIZE - self.iMinimumFixSamples
    
        self.iCallCount = 0
        self.stFix = [FixationData() for i in range(0,3)]
        
        '''Debug Shit'''
        self.devCalcs = 0
        self.resets = 0
        self.startfixes = 0
        self.updates = 0
        self.checks = 0
        self.moves = 0
        self.completes = 0
        self.restores = 0
        
        self.ResetFixation(self.PRES_FIX)
        
        self.ResetFixation(self.NEW_FIX)
        
        print
        
    def CalcGazeDeviationFromFix(self, iNewPresPrev, fXGaze, fYGaze):
        
        self.devCalcs += 1
        
        fDx = fXGaze - self.stFix[iNewPresPrev].fX
        fDy = fYGaze - self.stFix[iNewPresPrev].fY
        
        dDrSq = fDx * fDx + fDy * fDy
        
        if dDrSq < 0.0: dDrSq = 0.0
        fDr = math.sqrt(dDrSq)
            
        if iNewPresPrev == self.PRES_FIX:
            self.stRingBuf[self.iRingIndex].fGazeDeviation = fDr
            
        print '@@ %f' % (fDr) 
            
        return fDr
        
    def ResetFixation(self, iNewPresPrev):
        
        self.resets += 1
        
        self.stFix[iNewPresPrev].iStartCount    = 0
        self.stFix[iNewPresPrev].iEndCount      = 0
        self.stFix[iNewPresPrev].iNSamples      = 0
        self.stFix[iNewPresPrev].fXSum          = 0.0
        self.stFix[iNewPresPrev].fYSum          = 0.0
        self.stFix[iNewPresPrev].fX             = 0.0
        self.stFix[iNewPresPrev].fY             = 0.0
        
        if iNewPresPrev == self.PRES_FIX:
            self.iNPresOut = 0
            
    def StartFixAtGazepoint(self, iNewPresPrev, fXGaze, fYGaze):
        
        self.startfixes += 1
        
        self.stFix[iNewPresPrev].iNSamples      = 1
        self.stFix[iNewPresPrev].fXSum          = fXGaze
        self.stFix[iNewPresPrev].fYSum          = fYGaze
        self.stFix[iNewPresPrev].fX             = fXGaze
        self.stFix[iNewPresPrev].fY             = fYGaze
        self.stFix[iNewPresPrev].iStartCount    = self.iCallCount
        self.stFix[iNewPresPrev].iEndCount      = self.iCallCount
    
        if iNewPresPrev == self.PRES_FIX:
            self.iNPresOut = 0
            self.ResetFixation(self.NEW_FIX)

    def UpdateFixation(self, iNewPresPrev, fXGaze, fYGaze):
        
        self.updates += 1
        
        self.stFix[iNewPresPrev].iNSamples     += 1
        self.stFix[iNewPresPrev].fXSum         += fXGaze
        self.stFix[iNewPresPrev].fYSum         += fYGaze
        self.stFix[iNewPresPrev].fX             = self.stFix[iNewPresPrev].fXSum / self.stFix[iNewPresPrev].iNSamples
        self.stFix[iNewPresPrev].fY             = self.stFix[iNewPresPrev].fYSum / self.stFix[iNewPresPrev].iNSamples
        self.stFix[iNewPresPrev].iEndCount      = self.iCallCount
        
        if iNewPresPrev == self.PRES_FIX:
            self.iNPresOut = 0
            self.CheckIfFixating()
            self.ResetFixation(self.NEW_FIX)
            
    def CheckIfFixating(self):
        
        self.checks += 1
        
        if self.stFix[self.PRES_FIX].iNSamples >= self.iMinimumFixSamples:
            for i in range(0, self.iMinimumFixSamples):
                ii = self.iRingIndex - i
                if ii < 0: ii += self.RING_SIZE
                
                self.stRingBuf[ii].iEyeMotionState = self.FIXATING
                self.stRingBuf[ii].fXFix = self.stFix[self.PRES_FIX].fX
                self.stRingBuf[ii].fYFix = self.stFix[self.PRES_FIX].fY
                
                self.stRingBuf[ii].iSacDuration = self.stFix[self.PRES_FIX].iStartCount - self.stFix[self.PREV_FIX].iEndCount - 1
                self.stRingBuf[ii].iFixDuration = self.stFix[self.PRES_FIX].iEndCount - i - self.stFix[self.PRES_FIX].iStartCount + 1

    def MoveNewFixToPresFix(self):
        
        self.moves += 1
        
        self.iNPresOut = 0
        
        self.stFix[self.PRES_FIX] = self.stFix[self.NEW_FIX]
        
        self.ResetFixation(self.NEW_FIX)
        
        self.CheckIfFixating()
        
    def DeclareCompletedFixation(self, iSamplesAgo):
        
        self.completes += 1
        
        iRingIndexFixCompleted = self.iRingIndex - iSamplesAgo
        if iRingIndexFixCompleted < 0: iRingIndexFixCompleted += self.RING_SIZE
        
        self.stRingBuf[iRingIndexFixCompleted].iEyeMotionState = self.FIXATION_COMPLETED
        
        self.stFix[self.PREV_FIX] = self.stFix[self.PRES_FIX]
        
        self.MoveNewFixToPresFix()
        
    def RestoreOutPoints(self):
        
        self.restores += 1
        
        if self.iNSamplesSinceLastGoodFixPoint > 1:
            
            for i in range(1,self.iNSamplesSinceLastGoodFixPoint):
                ii = self.iRingIndex - i
                if ii < 0: ii += self.RING_SIZE
                
                if self.stRingBuf[ii].bGazeFount == True:
                    self.stFix[self.PRES_FIX].iNSamples += 1
                    self.stFix[self.PRES_FIX].fXSum += self.stRingBuf[ii].fXGaze
                    self.stFix[self.PRES_FIX].fYSum += self.stRingBuf[ii].fYGaze
                    self.stRingBuf[ii].iEyeMotionState = self.FIXATING
                    
            self.iNPresOut = 0
            
    def DetectFixation(self, bGazepointFound, fXGaze, fYGaze):
        
        self.iCallCount += 1
        self.iRingIndex += 1
        if self.iRingIndex >= self.RING_SIZE: self.iRingIndex = 0
        self.iRingIndexDelay = self.iRingIndex - self.iMinimumFixSamples
        if self.iRingIndexDelay < 0: self.iRingIndexDelay += self.RING_SIZE
        
        self.stRingBuf[self.iRingIndex].fXGaze          = fXGaze
        self.stRingBuf[self.iRingIndex].fYGaze          = fYGaze
        self.stRingBuf[self.iRingIndex].bGazepointFound = bGazepointFound
        
        self.stRingBuf[self.iRingIndex].iEyeMotionState = self.MOVING
        self.stRingBuf[self.iRingIndex].fXFix           = -0.0
        self.stRingBuf[self.iRingIndex].fYFix           = -0.0
        self.stRingBuf[self.iRingIndex].fGazeDeviation  = -0.1
        self.stRingBuf[self.iRingIndex].iSacDuration    = 0
        self.stRingBuf[self.iRingIndex].iFixDuration    = 0
        
        
        if self.stFix[self.PRES_FIX].iEndCount > 0:
            self.iNSamplesSinceLastGoodFixPoint = self.iCallCount - self.stFix[self.PRES_FIX].iEndCount
        else:
            self.iNSamplesSinceLastGoodFixPoint = 1
        
        #A1    
        if bGazepointFound:
            #B1
            if self.stFix[self.PRES_FIX].iNSamples > 0:
                self.fPresDr = self.CalcGazeDeviationFromFix(self.PRES_FIX, fXGaze, fYGaze)
                #C1
                if self.fPresDr <= self.fGazeDeviationThreshPix:
                    self.RestoreOutPoints()
                    self.UpdateFixation(self.PRES_FIX, fXGaze, fYGaze)
                #C2
                else:
                    self.iNPresOut += 1
                    #D1
                    if self.iNPresOut <= self.iMaxOutSamples:
                        #E1
                        if self.stFix[self.NEW_FIX].iNSamples > 0:
                            self.fNewDr = self.CalcGazeDeviationFromFix(self.NEW_FIX, fXGaze, fYGaze)
                            #F1
                            if self.fNewDr <= self.fGazeDeviationThreshPix:
                                self.UpdateFixation(self.NEW_FIX, fXGaze, fYGaze)
                            #F2
                            else:
                                self.StartFixAtGazepoint(self.NEW_FIX, fXGaze, fYGaze)
                        #E2
                        else:
                            self.StartFixAtGazepoint(self.NEW_FIX, fXGaze, fYGaze)
                    #D2
                    else:    
                        #G1
                        if self.stFix[self.PRES_FIX].iNSamples >= self.iMinimumFixSamples:
                            self.DeclareCompletedFixation(self.iNSamplesSinceLastGoodFixPoint)
                        #G2
                        else:
                            self.MoveNewFixToPresFix()
                        #H1
                        if self.stFix[self.PRES_FIX].iNSamples > 0:
                            self.fPresDr = self.CalcGazeDeviationFromFix(self.PRES_FIX, fXGaze, fYGaze)
                            if self.fPresDr <= self.fGazeDeviationThreshPix:
                                self.UpdateFixation(self.PRES_FIX, fXGaze, fYGaze)
                            else:
                                self.StartFixAtGazepoint(self.NEW_FIX, fXGaze, fYGaze)
                        #H2
                        else:
                            self.StartFixAtGazepoint(self.PRES_FIX, fXGaze, fYGaze)
            #B2
            else:
                self.StartFixAtGazepoint(self.PRES_FIX, fXGaze, fYGaze)
        #A2
        else:
            #I1
            if self.iNSamplesSinceLastGoodFixPoint <= self.iMaxMissedSamples:
                pass
            #I2
            else:
                #J1
                if self.stFix[self.PRES_FIX].iNSamples >= self.iMinimumFixSamples:
                    self.DeclareCompletedFixation(self.iNSamplesSinceLastGoodFixPoint)
                #J2
                else:
                    self.MoveNewFixToPresFix()
                    
        return self.stRingBuf[self.iRingIndexDelay]
                
def load_data():
    f = open('/Users/ryan/Downloads/eg_data.dat', 'rb')
    eg_data = pickle.load(f)
    f.close
    return eg_data


#data = load_data()
#pixPerMM = 1280 / 340
#fp = FixationProcessor(pixPerMM)
#print
#for g in data:
#    f = fp.DetectFixation(g['status'], g['x'], g['y'])
#    if f.iEyeMotionState > 0: print f.iEyeMotionState
#    
#print
#print fp.devCalcs
#print fp.resets
#print fp.startfixes
#print fp.updates
#print fp.checks
#print fp.moves
#print fp.completes
#print fp.restores
#print
#for p in fp.stFix:
#    print p