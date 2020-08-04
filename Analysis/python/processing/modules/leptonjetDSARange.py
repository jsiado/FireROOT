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

        for lj in [LJ0, LJ1]:
            if not lj.isMuonType(): continue
            for i in lj.pfcand_dsamuonIdx:
                dsa = event.dsamuons[i]
                self.Histos['{}/dsapt'.format(chan)].Fill(dsa.p4.pt(), aux['wgt'])
                self.Histos['{}/dsaeta'.format(chan)].Fill(dsa.p4.eta(), aux['wgt'])
                self.Histos['{}/dsaphi'.format(chan)].Fill(dsa.p4.phi(), aux['wgt'])
                self.Histos['{}/dsad0'.format(chan)].Fill(abs(dsa.d0), aux['wgt'])
                self.Histos['{}/dsadz'.format(chan)].Fill(abs(dsa.dz), aux['wgt'])
                self.Histos['{}/normchi2'.format(chan)].Fill(dsa.normChi2, aux['wgt'])

histCollection = [
    {
        'name': 'dsapt',
        'binning': [[0,5,10,20,50,]+list(np.arange(100,501,50))],
        'title': 'DSA p_{T};p_{T} [GeV];counts',
    },
    {
        'name': 'dsaeta',
        'binning': (24, -2.4, 2.4),
        'title': 'DSA #eta;#eta;counts',
    },
    {
        'name': 'dsaphi',
        'binning': (24, -math.pi, math.pi),
        'title': 'DSA #phi;#phi;counts',
    },
    {
        'name': 'dsad0',
        'binning': (50, 0, 150),
        'title': 'DSA |d_{0}|;|d_{0}| [cm];counts',
    },
    {
        'name': 'dsadz',
        'binning': (50, 0, 50),
        'title': 'DSA |d_{z}|;|d_{z}| [cm];counts',
    },
    {
        'name': 'normchi2',
        'binning': (50, 0, 20),
        'title': 'DSA #chi^{2}/ndof;#chi^{2}/ndof;counts',
    },

]