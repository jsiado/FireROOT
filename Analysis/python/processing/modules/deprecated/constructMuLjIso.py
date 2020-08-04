#!/usr/bin/env python
import math
import numpy as np

from rootpy.plotting import Profile
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

        mind0s = []
        for lj in [LJ0, LJ1]:
            if lj.isMuonType() and not math.isnan(lj.pfcand_tkD0Min):
                mind0s.append( lj.pfcand_tkD0Min*1e4 )

        # njet = sum([
        #     1 for j in event.ak4jets if \
        #         j.jetid \
        #         and j.p4.pt() > max([LJ0.p4.pt(), LJ1.p4.pt()]) \
        #         and abs(j.p4.eta()) < 2.4
        #     ])

        pfiso = [LJ0.pfiso(), LJ1.pfiso()]
        pfact = [
            LJ0.p4.energy()*LJ0.pfiso()/(1-LJ0.pfiso()),
            LJ1.p4.energy()*LJ1.pfiso()/(1-LJ1.pfiso()),
        ]
        dphi = abs(DeltaPhi(LJ0.p4, LJ1.p4))


        self.Histos['{}/maxiso'.format(chan)].Fill(max(pfiso), aux['wgt'])
        self.Histos['{}/maxact'.format(chan)].Fill(max(pfact), aux['wgt'])
        for iso in pfiso: self.Histos['{}/ljiso'.format(chan)].Fill(iso, aux['wgt'])
        for act in pfact: self.Histos['{}/ljact'.format(chan)].Fill(act, aux['wgt'])
        self.Histos['{}/dphi'.format(chan)].Fill(dphi, aux['wgt'])
        for lj in [LJ0, LJ1]:
            self.Histos['{}/ljisoenergy'.format(chan)].Fill(lj.p4.energy(), lj.pfiso(),)

        if max(mind0s)<400: return

    def postProcess(self):
        super(MyEvents, self).postProcess()

        for k in self.Histos:
            if 'phi' not in k: continue
            xax = self.Histos[k].axis(0)
            xax.SetNdivisions(-310)
            xax.ChangeLabel(2,-1,-1,-1,-1,-1,"#frac{#pi}{10}")
            xax.ChangeLabel(3,-1,-1,-1,-1,-1,"#frac{#pi}{5}")
            xax.ChangeLabel(4,-1,-1,-1,-1,-1,"#frac{3#pi}{10}")
            xax.ChangeLabel(5,-1,-1,-1,-1,-1,"#frac{2#pi}{5}")
            xax.ChangeLabel(6,-1,-1,-1,-1,-1,"#frac{#pi}{2}")
            xax.ChangeLabel(7,-1,-1,-1,-1,-1,"#frac{3#pi}{5}")
            xax.ChangeLabel(8,-1,-1,-1,-1,-1,"#frac{7#pi}{10}")
            xax.ChangeLabel(9,-1,-1,-1,-1,-1,"#frac{4#pi}{5}")
            xax.ChangeLabel(10,-1,-1,-1,-1,-1,"#frac{9#pi}{10}")
            xax.ChangeLabel(11,-1,-1,-1,-1,-1,"#pi")


histCollection = [
    {
        'name': 'maxiso',
        'binning': (50, 0, 1),
        'title': 'max lepton-jet isolation;isolation;counts'
    },
    {
        'name': 'ljiso',
        'binning': (50, 0, 1),
        'title': 'lepton-jet isolation;isolation;counts'
    },
    {
        'name': 'maxact',
        'binning': (100, 0, 100),
        'title': 'max lepton-jet activity;PF activity [GeV];counts'
    },
    {
        'name': 'ljact',
        'binning': (100, 0, 100),
        'title': 'lepton-jet activity;PF activity [GeV];counts'
    },
    {
        'name': 'dphi',
        'binning': (30, 0, M_PI),
        'title': '|#Delta#phi|(lepton-jet pair);|#Delta#phi|;counts/#pi/30'
    },
    {
        'name': 'ljisoenergy',
        'class': Profile,
        'binning': (list(np.arange(0,500,20))+list(np.arange(500,1001,100)), 0, 1),
        'title': 'lepton-jet isolation vs. energy;lepton-jet energy [GeV];isolation'
    },
]