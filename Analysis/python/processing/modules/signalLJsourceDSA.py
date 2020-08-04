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

        gmus = [p for p in event.gens \
            if abs(p.pid)==13 \
                and p.p4.pt()>10\
                and abs(p.p4.eta())<2.4\
                and p.vtx.Rho()<700]
        if len(gmus)<2: return

        dsaToGenmuMap = {}
        for i, dsa in enumerate(event.ljsources):
            if dsa.type!=8: continue
            pairs = [(g, DeltaR(gmu.p4, dsa.p4)) for g, gmu in enumerate(gmus)]
            pairs.sort(key=lambda x: x[1])
            if pairs and pairs[0][1]<0.3:
                dsaToGenmuMap[i] = pairs[0][0]

        for i, j in dsaToGenmuMap.items():
            dsa, genmu = event.ljsources[i], gmus[j]
            metric = (dsa.p4.pt()-genmu.p4.pt())/genmu.p4.pt()
            self.Histos['{}/ljsrcdsa'.format(chan)].Fill(metric, aux['wgt'])
            if dsa.charge==genmu.charge:
                self.Histos['{}/ljsrcdsasameq'.format(chan)].Fill(metric, aux['wgt'])

        self.Histos['%s/pfmet'%chan].Fill(event.pfMet.r(), aux['wgt'])


histCollection = [
    {
        'name': 'ljsrcdsa',
        'binning': (50, -1, 1),
        'title': 'DSA in lepton-jet source;(p_{T}^{reco}-p_{T}^{gen})/p_{T}^{gen};norm. counts/0.04'
    },
    {
        'name': 'ljsrcdsasameq',
        'binning': (50, -1, 1),
        'title': 'DSA in lepton-jet source;(p_{T}^{reco}-p_{T}^{gen})/p_{T}^{gen};norm. counts/0.04'
    },
    {
        'name': 'pfmet',
        'binning': (50, 0, 500),
        'title': 'PF MET;MET [GEV];counts/10'
    },
]