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

        isonopu = []
        iso = []

        for lj in [LJ0, LJ1]:
            # if not math.isnan(lj.pfIsolationNoPU05):
            isonopu.append(lj.pfIsolationNoPU05)
            # if not math.isnan(lj.pfIsolation05):
            iso.append(lj.pfIsolation05)
            if lj.isEgmType():
                self.Histos['{}/egmisonopu'.format(chan)].Fill(lj.pfIsolationNoPU05, aux['wgt'])
                self.Histos['{}/egmiso'.format(chan)].Fill(lj.pfIsolation05, aux['wgt'])

        self.Histos['{}/maxisonopu'.format(chan)].Fill(max(isonopu), aux['wgt'])
        self.Histos['{}/maxiso'.format(chan)].Fill(max(iso), aux['wgt'])


histCollection = [
    {
        'name': 'maxisonopu',
        'binning': (50, 0, 0.5),
        'title': 'max lepton-jet isolation (no PU);isolation;counts',
    },
    {
        'name': 'maxiso',
        'binning': (50, 0, 0.5),
        'title': 'max lepton-jet isolation (w/ PU);isolation;counts',
    },
    {
        'name': 'egmisonopu',
        'binning': (50, 0, 0.5),
        'title': 'egm-type lepton-jet isolation (no PU);isolation;counts',
    },
    {
        'name': 'egmiso',
        'binning': (50, 0, 0.5),
        'title': 'egm-type lepton-jet isolation (w/ PU);isolation;counts',
    },
]