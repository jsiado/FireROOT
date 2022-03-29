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

        Reco_Mu = [ remu for remu in event.muons]# if abs(p.pid) == 13]
        self.Histos['%s/num_RM' % chan].Fill(len(Reco_Mu))
        #print len(Reco_Mu)
        
        matched_Reco = []

        if getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha") or getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha_NoL2Matched") or getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed") or getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched") or getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha_Eta2p4") or getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4"):
            
            TriObj = [TO for TO in event.trigobjs]  # trigger objects in the event
            self.Histos['%s/num_TO' % chan].Fill(len(TriObj))
            for TO in TriObj:
                #if TO.p4.pt()<23: continue
                self.Histos['%s/TO_pid' % chan].Fill(TO.pid)
                self.Histos['%s/TO_pT' % chan].Fill(TO.p4.pt())
                
                if TO.pid == 0: continue
                if TO.pid != 0 and abs(TO.pid) & (1<<2) > 0:
                #if abs(TO.pid) == 13:
                    #print 'in if',TO.pid, abs(TO.pid) & (1<<2)
                    min_dR = 999
                    RMi = -1
                    for i, RM in enumerate(Reco_Mu):
                        if abs(RM.p4.pt() - TO.p4.pt())<0.001:continue 
                        dR_TO = DeltaR(TO.p4,RM.p4)
                        if dR_TO > min_dR: continue
                        if dR_TO < min_dR:
                            min_dR = dR_TO
                            RMi = i
                            if min_dR < 0.4:
                                matched_Reco.append(RMi)
                                #print 'one'
                    self.Histos['%s/dR_TO_reco' % chan].Fill(dR_TO)
                                
            for i, RM in enumerate (Reco_Mu):
                ## cuts
                if RM.p4.pt()<30 and abs(RM.p4.eta())>2.4: 
                    continue
                else:
                    min_dR = 999
                    for i2, RM2 in enumerate(Reco_Mu):
                        if i2 == i: continue
                        if DeltaR(RM.p4, RM2.p4) < min_dR: 
                            min_dR = DeltaR(RM.p4, RM2.p4)
                if min_dR<0.4:
                    self.Histos['%s/f_TO_Den'%chan].Fill(min_dR)
                    if (i2 in matched_Reco):
                        self.Histos['%s/f_TO_Num'%chan].Fill(min_dR)

histCollection = [
    #{  'name': 'hist',         'binning' : (100, 0.0, 10.00),		       'title': 'histry'},#not used
    {  'name': 'dR_TO_reco',   'binning' : (50,  0.0, 1.500),                  'title': '#Delta R: TO and muon; #Delta R; Number of entries'},
    {  'name': 'TO_pid',       'binning' : (100, -20.0, 20.0),                 'title': 'Trigger object id; id; # of entries'},
    {  'name': 'TO_pT',	       'binning' : (100, 0.0, 1000.0),		       'title': 'Trigger object p_{t}; p_{T}; number of entries'},
    {  'name': 'f_TO_Den',     'binning' : (50,  0.0, 0.500),		       'title': 'Reco muons; #Delta R; Number of entries'},
    {  'name': 'f_TO_Num',     'binning' : (50,  0.0, 0.500),		       'title': 'Matched Muons; #Delta R; Number of entries'},
    {  'name': 'num_TO',       'binning' : (100, 0.0, 20.0),                  'title': 'Number of trigger objects; # of trigger objects; number of entries'},
    {  'name': 'num_RM',       'binning' : (100, 0.0, 20.0),                  'title': 'Number of Reco Muons; Reco Muons; number of entries'},
]


