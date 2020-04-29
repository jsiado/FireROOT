#!/usr/bin/env python

from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *


class MyEvents(CosmicEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files,
                                       type=type, maxevents=maxevents, channel=channel, **kwargs)

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        flag = False
        if aux['hasCosmicShower'] and self.Type=='DATA': flag=True
        if not aux['hasCosmicShower'] and self.Type!='DATA': flag=True
        if flag is False: return

        chan = aux['channel']
        LJ0, LJ1 = aux['lj0'], aux['lj1']
        for lj in [LJ0, LJ1]:
            if lj.isEgmType(): continue
            drcosmicdsa = lj.dRcosmicDSA(event)
            drcosmicseg = lj.dRcosmicSeg(event)
            if drcosmicdsa:
                self.Histos['{}/drdsa'.format(chan)].Fill(min(drcosmicdsa), aux['wgt'])
                if min(drcosmicdsa)>0.05 and drcosmicseg:
                    self.Histos['{}/drseg'.format(chan)].Fill(min(drcosmicseg), aux['wgt'])

histCollection = [
    {
        'name': 'drdsa',
        'binning': (50,0,0.5),
        'title': r'#DeltaR_{cosmic}(DSA_{i}, DSA_{j});#DeltaR_{cosmic};counts',
    },
    {
        'name': 'drseg',
        'binning': (50,0,0.5),
        'title': r'#DeltaR_{cosmic}(DSA_{i}, segment) (#DeltaR_{cosmic}(DSA_{i}, DSA_{j})>0.05);#DeltaR_{cosmic};counts',
    },
]
