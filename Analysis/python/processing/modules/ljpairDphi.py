#!/usr/bin/env python
import math

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

        dphi = abs(DeltaPhi(LJ0.p4, LJ1.p4))

        ## displacement cut
        mind0s = []
        for lj in [LJ0, LJ1]:
            if lj.isMuonType() and not math.isnan(lj.pfcand_tkD0Min):
                mind0s.append( lj.pfcand_tkD0Min*1e4 )

        if self.Type=='DATA' and dphi>2.2: return

        metric = {'2mu2e': 500, '4mu': 500}
        if max(mind0s)<metric[chan]: return
        self.Histos['{}/dphipre'.format(chan)].Fill(dphi, aux['wgt'])

        metric = {'2mu2e': 1500, '4mu': 1000}
        if max(mind0s)<metric[chan]: return

        self.Histos['{}/dphi'.format(chan)].Fill(dphi, aux['wgt'])

    def postProcess(self):
        super(MyEvents, self).postProcess()

        for k in self.Histos:
            if 'phi' not in k: continue
            xax = self.Histos[k].axis(0)
            decorate_axis_pi(xax)



histCollection = [
    {
        'name': 'dphipre',
        'binning': (20, 0, M_PI),
        'title': '|#Delta#phi| of lepton-jet pair;|#Delta#phi|;counts/#pi/20'
    },
    {
        'name': 'dphi',
        'binning': (20, 0, M_PI),
        'title': '|#Delta#phi| of lepton-jet pair;|#Delta#phi|;counts/#pi/20'
    },
]

