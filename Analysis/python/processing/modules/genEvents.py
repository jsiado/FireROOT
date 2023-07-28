#!/usr/bin/env python
# RM: reco muon, TO:trigger object

import math
import numpy as np

from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *

class MyEvents(SignalEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']
        
        gen_mus = [p for p in event.gens \
            if abs(p.pid)==13 \
                and p.p4.pt()>10\
                and abs(p.p4.eta())<2.4\
                and p.vtx.Rho()<700]

        dp_toMu = [p for p in aux['dp'] if p.daupid==13] #select muons from Zd                                                                                                    
        dp_toEl = [p for p in aux['dp'] if p.daupid==11] #select electron from Zd
        
        for dp in dp_toMu:
            if dp.p4.pt()<30 or abs(dp.p4.eta())>2.4: continue
            lxy = (dp.dauvtx - dp.vtx).Rho()
            lz  = (dp.dauvtx - dp.vtx).Z()
            # if abs(lz)>800: continue
            self.Histos['%s/lxyDpToMu' % chan].Fill(lxy)
            self.Histos['%s/lepDrDpToMu' % chan].Fill(dp.daudr)
            self.Histos['%s/lzDpToMu' % chan].Fill(dp.daudr)
        
        for lj in enumerate(event.leptonjets):                                                                                                                                           
            LJ0 = event.leptonjets[0]                                                                                                                                                    
            zdlj =  DeltaR(l.p4, LJ0.p4)                                                                                                                                               
            #if DeltaR<0.4:
                


histCollection = [
    {  'name': 'lxyDpToMu',       'binning' : (100, 0.0,1000),                   'title': 'l_{xy} Z_{d} -> #mu#mu; l_{xy}; Number of entries'},
    {  'name': 'lepDrDpToMu',     'binning' : (50, 0.0,0.25),                    'title': '#Delta R (Z_{d},#mu) ; #Delta R (Z_{d},#mu) ; Number of entries'},
    {  'name': 'lzDpToMu',        'binning' : (100, 0.0,1),                      'title': 'l_{z} Z_{d} -> #mu#mu; l_{z} ; Number of entries'},
]


