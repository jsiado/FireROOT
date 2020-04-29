#!/usr/bin/env python

from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *


class MyEvents(CosmicEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']
        LJ0, LJ1 = aux['lj0'], aux['lj1']
        # passCosmic = all(map(lambda lj: lj.passCosmicVeto(event), [LJ0, LJ1]))
        # if not passCosmic: return

        self.Histos['{}/npair'.format(chan)].Fill(event.cosmicveto.parallelpairs, aux['wgt'])

histCollection = [
    {
        'name': 'npair',
        'binning': (20, 0, 20),
        'title': 'N(parallel pairs) of cosmic muons;N(pairs);counts/1',
    },
]