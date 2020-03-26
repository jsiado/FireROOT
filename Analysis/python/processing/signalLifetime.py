#!/usr/bin/env python
import math
from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *


class MyEvents(SignalEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu']):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel)

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']

        for p in aux['dp']:
            rho = (p.dauvtx-p.vtx).Rho()
            l3d = (p.dauvtx-p.vtx).R()
            t = rho*(p.p4.mass()/p.p4.pt())
            self.Histos['{}/dplxy'.format(chan)].Fill(rho)
            self.Histos['{}/dpl3d'.format(chan)].Fill(l3d)
            self.Histos['{}/dptime'.format(chan)].Fill(t)

histCollection = [
    {
        'name': 'dplxy',
        'binning': (50, 0, 500),
        'title': 'darkphoton lxy;Lxy [cm];counts/10cm'
    },
    {
        'name': 'dpl3d',
        'binning': (50, 0, 500),
        'title': 'darkphoton l3d;L3d [cm];counts/10cm'
    },
    {
        'name': 'dptime',
        'binning': (50, 0, 5),
        'title': 'darkphoton time;t [cm];counts/10cm'
    },
]