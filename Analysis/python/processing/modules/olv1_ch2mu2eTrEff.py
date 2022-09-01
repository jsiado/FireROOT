#!/usr/bin/env python
import math
import numpy as np
from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *

class MyEvents(Events):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']

        LJ0, LJ1 = aux['lj0'], aux['lj1']
        passCosmic = all(map(lambda lj: lj.passCosmicVeto(event), [LJ0, LJ1]))
        if not passCosmic: return
        passLjMass = all(map(lambda lj: lj.isEgmType() or lj.isMuonType() and lj.p4.M()<8, [LJ0, LJ1]))
        if not passLjMass: return

        for lj in [LJ0,LJ1]:
            if lj.p4.pt()<30 or abs(lj.p4.eta())>2.4: continue
        
        Reco_Mu = [remu for i, remu in enumerate(event.ljsources)]# if abs(remu.pid)==13]
        self.Histos['%s/RM_n' % chan].Fill(len(Reco_Mu))
        
        dR_thr = 0.3
        if len(Reco_Mu)>2:
            
            TriObj = [TO for TO in event.trigobjs]  # trigger objects in the event
            self.Histos['%s/TO_n' % chan].Fill(len(TriObj))
            
            for i1, rm1 in enumerate(Reco_Mu):
                for i2, rm2 in enumerate(Reco_Mu):
                    dR = DeltaR(rm1.p4,rm2.p4)
                    if dR < dR_thr and i1 != i2:
                        #self.Histos['%s/mu_total' % chan].Fill(rm1.p4.pt())
                        for m, mu in enumerate([rm1,rm2]):
                            self.Histos['%s/mu_total' % chan].Fill(mu.p4.pt())
                            for n, to in enumerate(TriObj):
                                dRmt = DeltaR(mu.p4,to.p4)
                                if dRmt < dR_thr:
                                    
                                    print len(TriObj),m,n
                                    self.Histos['%s/mu_matched' % chan].Fill(mu.p4.pt())
                                    
histCollection = [
    { 'name': 'RM_n',             'binning' : (20, 0.0,20),                     'title': 'Number of Reco #mu ; #mu ; Number of entries'},
    { 'name': 'TO_n',             'binning' : (30, 0.0,30),                     'title': 'Number of trigger objects; #mu ; Number of entries'},
    
    { 'name': 'mu_total',         
      'binning' : [[0, 5, 10, 15, 20, 25, 30, 35, 40, 50,70, 100, 150, 200, 250, 300, 400, 500,]+list(np.arange(1,.100,1))], 
      'title': 'Reco muon p_{T} distribution; p_{T} [GeV]; Number of entries'},
    
    { 'name': 'mu_matched', 
      'binning' : [[0, 5, 10, 15, 20, 25, 30, 35, 40, 50,70, 100, 150, 200, 250, 300, 400, 500,]+list(np.arange(1,.100,1))],
      'title': 'Reco muon p_{T} distribution; p_{T} [GeV]; Number of entries'},
]
