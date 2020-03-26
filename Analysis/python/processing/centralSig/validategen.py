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
            self.Histos['{}/dplxy'.format(chan)].Fill(rho)
            self.Histos['{}/dpl3d'.format(chan)].Fill(l3d)

            daus = []
            for d in event.gens:
                if abs(d.pid) not in [11, 13]: continue
                if (d.vtx-p.dauvtx).R()<1e-2: daus.append(d)
            if len(daus)==2:
                dpmass = (daus[0].p4+daus[1].p4).M()
                self.Histos['{}/dpmass'.format(chan)].Fill(dpmass)

        if len(aux['dp'])==2:
            psmass = (aux['dp'][0].p4+aux['dp'][1].p4).M()
            self.Histos['{}/psmass'.format(chan)].Fill(psmass)

histCollection = [
    {
        'name': 'dplxy',
        'binning': (500, 0, 500),
        'title': 'darkphoton lxy;Lxy [cm];counts/1cm'
    },
    {
        'name': 'dpl3d',
        'binning': (750, 0, 750),
        'title': 'darkphoton l3d;L3d [cm];counts/1cm'
    },
    {
        'name': 'dpmass',
        'binning': (750, 0, 7.5),
        'title': 'dark photon invM;mass [GeV];counts/0.01GeV'
    },
    {
        'name': 'psmass',
        'binning': (1500, 0, 1500),
        'title': 'DM bound state invM;mass [GeV];counts/1GeV'
    }
]