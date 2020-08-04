#!/usr/bin/env python
import math
from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *

def SignalReWeight(cTauRef, cTauNew, t):
    tRef, tNew = float(cTauRef)/10., float(cTauNew)/10.
    return tRef/tNew * ROOT.TMath.Exp(t/tRef - t/tNew)

class MyEvents(SignalEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)

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

            cTauRef = self.Ctau
            self.Histos['{}/dplxy_0p1'.format(chan)].Fill(rho, SignalReWeight(cTauRef, cTauRef*0.1, t))
            self.Histos['{}/dplxy_0p5'.format(chan)].Fill(rho, SignalReWeight(cTauRef, cTauRef*0.5, t))
            self.Histos['{}/dplxy_2'.format(chan)].Fill(rho, SignalReWeight(cTauRef, cTauRef*2, t))
            self.Histos['{}/dplxy_10'.format(chan)].Fill(rho, SignalReWeight(cTauRef, cTauRef*10, t))

        muons = [p for p in event.gens if abs(p.pid)==13]
        electrons = [p for p in event.gens if abs(p.pid)==11]

        self.Histos['{}/ndp'.format(chan)].Fill(len(aux['dp']))
        self.Histos['{}/nmu'.format(chan)].Fill(len(muons))
        self.Histos['{}/nel'.format(chan)].Fill(len(electrons))
        self.Histos['{}/nlep'.format(chan)].Fill(len(muons)+len(electrons))

histCollection = [
    {
        'name': 'dplxy',
        'binning': (500, 0, 500),
        'title': 'darkphoton lxy;Lxy [cm];counts/1cm'
    },
    {
        'name': 'dplxy_0p1',
        'binning': (500, 0, 500),
        'title': 'darkphoton lxy (scaled #times0.1);Lxy [cm];counts/1cm'
    },
    {
        'name': 'dplxy_0p5',
        'binning': (500, 0, 500),
        'title': 'darkphoton lxy (scaled #times0.5);Lxy [cm];counts/1cm'
    },
    {
        'name': 'dplxy_2',
        'binning': (500, 0, 500),
        'title': 'darkphoton lxy (scaled #times2);Lxy [cm];counts/1cm'
    },
    {
        'name': 'dplxy_10',
        'binning': (500, 0, 500),
        'title': 'darkphoton lxy (scaled #times10);Lxy [cm];counts/1cm'
    },
    {
        'name': 'dpl3d',
        'binning': (750, 0, 750),
        'title': 'darkphoton l3d;L3d [cm];counts/1cm'
    },
    {
        'name': 'dptime',
        'binning': (50, 0, 5),
        'title': 'darkphoton time;t [cm];counts/10cm'
    },
    {
        'name': 'ndp',
        'binning': (5, 0, 5),
        'title': 'Number of dark photons;N;counts'
    },
    {
        'name': 'nmu',
        'binning': (5, 0, 5),
        'title': 'Number of muons;N;counts'
    },
    {
        'name': 'nel',
        'binning': (5, 0, 5),
        'title': 'Number of electrons;N;counts'
    },
    {
        'name': 'nlep',
        'binning': (5, 0, 5),
        'title': 'Number of leptons(electrons+muons);N;counts'
    },
]