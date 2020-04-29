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


        invm = (LJ0.p4+LJ1.p4).M()

        ## displacement variables
        mind0s, maxd0s, aved0s = [], [], []
        mind0sigs, maxd0sigs, aved0sigs = [], [], []
        for lj in [LJ0, LJ1]:
            if not lj.isMuonType(): continue
            if not math.isnan(lj.pfcand_tkD0Max): maxd0s.append(lj.pfcand_tkD0Max)
            if not math.isnan(lj.pfcand_tkD0Min): mind0s.append(lj.pfcand_tkD0Min)
            if not math.isnan(lj.pfcand_tkD0SigMax): maxd0sigs.append(lj.pfcand_tkD0SigMax)
            if not math.isnan(lj.pfcand_tkD0SigMin): mind0sigs.append(lj.pfcand_tkD0SigMin)
            _d0 = [abs(x) for x in lj.pfcand_tkD0 if not math.isnan(x)]
            aved0s.append(sum(_d0)/len(_d0))
            _d0sig = [x for x in lj.pfcand_tkD0Sig if not math.isnan(x)]
            aved0sigs.append( sum(_d0sig)/len(_d0sig) )


        self.Histos['{}/mind0'.format(chan)].Fill(max(mind0s)*1e4, aux['wgt'])
        self.Histos['{}/maxd0'.format(chan)].Fill(max(maxd0s)*1e4, aux['wgt'])
        self.Histos['{}/aved0'.format(chan)].Fill(max(aved0s)*1e4, aux['wgt'])
        self.Histos['{}/mind0sig'.format(chan)].Fill(max(mind0sigs), aux['wgt'])
        self.Histos['{}/maxd0sig'.format(chan)].Fill(max(maxd0sigs), aux['wgt'])
        self.Histos['{}/aved0sig'.format(chan)].Fill(max(aved0sigs), aux['wgt'])




histCollection = [
    {
        'name': 'mind0',
        'binning': [[0,2,4,6,8,10,20,50,]+list(np.arange(100,2501,100))],
        'title': 'muon-type lepton-jet minimum |d_{0}|;|d_{0}| [#mum];Events',
    },
    {
        'name': 'maxd0',
        'binning': [[0,2,4,6,8,10,20,50,]+list(np.arange(100,2501,100))],
        'title': 'muon-type lepton-jet maximum |d_{0}|;|d_{0}| [#mum];Events',
    },
    {
        'name': 'aved0',
        'binning': [[0,2,4,6,8,10,20,50,]+list(np.arange(100,2501,100))],
        'title': 'muon-type lepton-jet average |d_{0}|;|d_{0}| [#mum];Events',
    },
    {
        'name': 'mind0sig',
        'binning': [list(np.arange(0,1,0.1))+list(np.arange(1,10,2))+list(np.arange(10,100,10))],
        'title': 'muon-type lepton-jet minimum |d_{0}| significance;|d_{0}|/#sigma_{d_{0}};Events',
    },
    {
        'name': 'maxd0sig',
        'binning': [list(np.arange(0,1,0.1))+list(np.arange(1,10,2))+list(np.arange(10,100,10))],
        'title': 'muon-type lepton-jet maximum |d_{0}| significance;|d_{0}|/#sigma_{d_{0}};Events',
    },
    {
        'name': 'aved0sig',
        'binning': [list(np.arange(0,1,0.1))+list(np.arange(1,10,2))+list(np.arange(10,100,10))],
        'title': 'muon-type lepton-jet average |d_{0}| significance;|d_{0}|/#sigma_{d_{0}};Events',
    },
]