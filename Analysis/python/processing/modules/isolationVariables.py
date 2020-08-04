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
        if self.Type=='DATA' and dphi>2.2: return

        # displacement variable
        mind0s = []
        for lj in [LJ0, LJ1]:
            if lj.isMuonType() and not math.isnan(lj.pfcand_tkD0Min):
                mind0s.append( lj.pfcand_tkD0Min*1e4 )

        egmljiso = []
        muljiso = []

        for lj in [LJ0, LJ1]:
            if math.isnan(lj.pfIsolationNoPU05): continue
            if lj.isMuonType(): muljiso.append(lj.pfIsolationNoPU05)
            if lj.isEgmType(): egmljiso.append(lj.pfIsolationNoPU05)

        if not egmljiso and not muljiso: return

        maxljiso = max(muljiso+egmljiso)

        metric = {'2mu2e': 500, '4mu': 500}
        if max(mind0s)<metric[chan]: return

        self.Histos['{}/maxljisopre'.format(chan)].Fill(maxljiso, aux['wgt'])
        for iso in egmljiso: self.Histos['{}/egmljisopre'.format(chan)].Fill(iso, aux['wgt'])
        for iso in muljiso:  self.Histos['{}/muljisopre'.format(chan)].Fill(iso, aux['wgt'])

        metric = {'2mu2e': 1500, '4mu': 1000}
        if max(mind0s)<metric[chan]: return

        self.Histos['{}/maxljiso'.format(chan)].Fill(maxljiso, aux['wgt'])
        for iso in egmljiso: self.Histos['{}/egmljiso'.format(chan)].Fill(iso, aux['wgt'])
        for iso in muljiso:  self.Histos['{}/muljiso'.format(chan)].Fill(iso, aux['wgt'])



histCollection = [
    {
        'name': 'maxljisopre',
        'binning': (20, 0, 0.5),
        'title': 'max lepton-jet isolation;isolation;counts/0.025',
    },
    {
        'name': 'egmljisopre',
        'binning': (20, 0, 0.5),
        'title': 'Egm-type lepton-jet isolation;isolation;counts/0.025',
    },
    {
        'name': 'muljisopre',
        'binning': (20, 0, 0.5),
        'title': 'muon-type lepton-jet isolation;isolation;counts/0.025',
    },
    {
        'name': 'maxljiso',
        'binning': (20, 0, 0.5),
        'title': 'max lepton-jet isolation;isolation;counts/0.025',
    },
    {
        'name': 'egmljiso',
        'binning': (20, 0, 0.5),
        'title': 'Egm-type lepton-jet isolation;isolation;counts/0.025',
    },
    {
        'name': 'muljiso',
        'binning': (20, 0, 0.5),
        'title': 'muon-type lepton-jet isolation;isolation;counts/0.025',
    },
]