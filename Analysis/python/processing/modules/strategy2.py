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
        cutflowbin = 5

        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1

        LJ0, LJ1 = aux['lj0'], aux['lj1']
        passCosmic = all(map(lambda lj: lj.passCosmicVeto(event), [LJ0, LJ1]))

        if not passCosmic: return
        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1

        # displacement variable
        mind0s = []
        for lj in [LJ0, LJ1]:
            if not lj.isMuonType(): continue
            if not math.isnan(lj.pfcand_tkD0Min): mind0s.append(lj.pfcand_tkD0Min)
        if max(mind0s)*1e4<10: return # max mind0<10um
        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1

        ## isolation variables
        isoval = []
        for lj in [LJ0, LJ1]:
            if not math.isnan(lj.pfIsolation05):
                isoval.append(lj.pfIsolation05)

        maxiso = max(isoval)
        dphi = abs(DeltaPhi(LJ0.p4, LJ1.p4))
        njet = sum([1 for j in event.ak4jets if j.jetid and j.p4.pt()>max([LJ0.p4.pt(), LJ1.p4.pt()]) and abs(j.p4.eta())<2.4])

        self.Histos['{}/maxiso'.format(chan)].Fill(maxiso, aux['wgt'])
        self.Histos['{}/dphi'.format(chan)].Fill(dphi, aux['wgt'])
        self.Histos['{}/njet'.format(chan)].Fill(njet, aux['wgt'])
        if dphi>math.pi/2:
            self.Histos['{}/maxiso_njetT'.format(chan)].Fill(maxiso, njet, aux['wgt'])
        else:
            self.Histos['{}/maxiso_njetF'.format(chan)].Fill(maxiso, njet, aux['wgt'])

histCollection = [
    {
        'name': 'maxiso',
        'binning': [list(np.arange(0,0.1,0.01))+[0.1,0.15,0.2,0.25,0.3,0.4,0.5,1.0]],
        'title': 'max lepton-jet pfIso05;max pfIso05;Events',
    },
    {
        'name': 'dphi',
        'binning': (20, 0, M_PI),
        'title': '|#Delta#phi| of lepton-jet pair;|#Delta#phi|;Events/#pi/20'
    },
    {
        'name': 'njet',
        'binning': (5, 0, 5),
        'title': 'num. of AK4Jets p_T>p_{T leading lj};num.AK4jet;Events/1'
    },
    {
        'name': 'maxiso_njetT',
        'binning': [list(np.arange(0,0.1,0.01))+[0.1,0.15,0.2,0.25,0.3,0.4,0.5,1.0],5,0,5],
        'title': 'njet vs. maxiso, |#Delta#phi|>#pi/2;max pfiso05;njet'
    },
    {
        'name': 'maxiso_njetF',
        'binning': [list(np.arange(0,0.1,0.01))+[0.1,0.15,0.2,0.25,0.3,0.4,0.5,1.0],5,0,5],
        'title': 'njet vs. maxiso, |#Delta#phi|<=#pi/2;max pfiso05;njet'
    },
]