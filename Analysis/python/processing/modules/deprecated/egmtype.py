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

        for lj in [LJ0, LJ1]:
            if not lj.isEgmType(): continue
            if lj.nPFElectron()==1:
                self.Histos['{}/ndau'.format(chan)].Fill(
                    lj.nDaughters(), aux['wgt']
                )
            self.Histos['{}/tocut'.format(chan)].Fill(0, aux['wgt'])
            if lj.nPFElectron()==1 and lj.nDaughters()==1:
                self.Histos['{}/tocut'.format(chan)].Fill(1, aux['wgt'])

    def postProcess(self):
        super(MyEvents, self).postProcess()

        for ch in self.Channel:
            xaxis = self.Histos['{}/tocut'.format(ch)].axis(0)
            xaxis.SetBinLabel(1, 'total')
            xaxis.SetBinLabel(2, 'only 1 electron')



histCollection = [
    {
        'name': 'ndau',
        'binning': (5, 0, 5),
        'title': 'electron-type lepton-jet nDaughters;nDaughters;Events',
    },
    {
        'name': 'tocut',
        'binning': (2, 0, 2),
        'title': 'EGM-type lepton-jet;;Events',
    },

]