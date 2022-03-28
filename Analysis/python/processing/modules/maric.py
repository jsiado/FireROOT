#!/usr/bin/env python
import math

from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *

class MyEvents(SignalEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']
        
        Reco_Mu = [ p for p in event.muons]# if abs(p.pid) == 13]
        matched_Reco = []
        min_dR = 1000
        matched = -1
        
        if getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha") or getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha_NoL2Matched") or getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed") or getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched") or getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha_Eta2p4") or getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4"):
            #print 'ok'
            TriObj = [TO for TO in event.trigobjs]
            print '-------->>>>>>>>>',len (TriObj)
            for TO in TriObj:
                if TO.pid == 0: continue
                print TO.pid
                #if (TO.bit == 0) or (TO.bit == 1):
                   # print TO
                #if (TO.bit & 23) !=0:
                   # print 'ok 2'#O.pid, TO.bit & 23
 #           if event.hltL2DoubleMu23NoVertexL2Filtered2Cha == 1:
  #              print 'ok'
                
                


            '''for i, p in enumerate(Reco_Mu):
            #print 'marico'
            for lj in event.leptonjets:
                if not lj.isMuonType(): continue
                if not lj.passSelection(event): continue
                dR_TO = DeltaR(p.p4, lj.p4)

                if dR_TO > min_dR: continue
                if dR_TO <min_dR:
                    mindr = dR_TO
                    matched = i
                    if min_dR < 0.4:
                        matched_Reco.append(matched)
                        
        for i, p in enumerate(Reco_Mu):
            #cuts
            min_dR = 1000
            for j, q in enumerate(Reco_Mu):
                if i == j: continue
                dR_TO = DeltaR(p.p4, q.p4)
                if dR_TO < min_dR:
                    min_dR = DeltaR(p.p4, p.p4)
                    self.Histos['%s/TO_Den'%chan].Fill(min_dR)                                                                                            
                    if (i in matched_Reco):
                        self.Histos['%s/TO_Num'%chan].Fill(min_dR)'''

histCollection = [
	{	'name': 'TO_pT',				'binning': (100,0.0, 500.0),				'title': 'number of trigger objects'},
	{	'name': 'TO_Den',				'binning': (100,0.0, 500.0),				'title': 'all reco muons'},
	{	'name': 'TO_Num',				'binning': (100,0.0, 500.0),				'title': 'Matched'},
]
