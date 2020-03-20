#!/usr/bin/env python

from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *


class MyEvents(CosmicEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu']):
        super(MyEvents, self).__init__(files=files,
                                       type=type, maxevents=maxevents, channel=channel)

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel:
            return
        chan = aux['channel']
        LJ0, LJ1 = aux['lj0'], aux['lj1']
        for lj in [LJ0, LJ1]:
            if lj.isEgmType(): continue
            drcosmicdsa = lj.dRcosmicDSA(event)
            drcosmicseg = lj.dRcosmicSeg(event)
            if drcosmicdsa:
                self.Histos['{}/drdsa'.format(chan)].Fill(min(drcosmicdsa), aux['wgt'])
            if drcosmicseg:
                self.Histos['{}/drseg'.format(chan)].Fill(min(drcosmicseg), aux['wgt'])

histCollection = [
    {
        'name': 'drdsa',
        'binning': (50, 0, 0.5),
        'title': r'#DeltaR_{cosmic}(DSA_{i}, DSA_{j});#DeltaR_{cosmic};counts/0.01',
    },
    {
        'name': 'drseg',
        'binning': (50, 0, 0.5),
        'title': r'#DeltaR_{cosmic}(DSA_{i}, segment);#DeltaR_{cosmic};counts/0.01',
    },
]
