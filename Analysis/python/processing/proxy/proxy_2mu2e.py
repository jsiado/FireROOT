#!/usr/bin/env python
import math
import numpy as np

from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *


class MyEvents(ProxyEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']

        lj, proxy = aux['lj'], aux['proxy']
        if not lj.passCosmicVeto(event): return


        njet = sum([
            1 for j in event.ak4jets if \
                j.jetid \
                and j.p4.pt() > max([lj.p4.pt(), proxy.p4.pt()]) \
                and abs(j.p4.eta()) < 2.4
            ])

        nbtight = 0
        for s, j in zip(event.hftagscores, event.ak4jets):
            if not (j.jetid and j.p4.pt()>30 and abs(j.p4.eta())<2.5): continue
            if (s.DeepCSV_b&(1<<2))!=(1<<2): continue
            nbtight += 1

        proxyd0 = abs(proxy.d0(event))*1e4

        maxpfiso = lj.pfiso()
        dphi = abs(DeltaPhi(lj.p4, proxy.p4))
        invm = (lj.p4+proxy.p4).M()

        self.Histos['{}/proxyd0'.format(chan)].Fill(proxyd0, aux['wgt'])
        if proxyd0<1600: return
        self.Histos['{}/nbtight'.format(chan)].Fill(nbtight, aux['wgt'])
        if nbtight==0: return
        self.Histos['{}/proxyiso'.format(chan)].Fill(proxy.pfiso(), aux['wgt'])
        self.Histos['{}/njet'.format(chan)].Fill(njet, aux['wgt'])
        self.Histos['{}/dphi'.format(chan)].Fill(dphi, aux['wgt'])
        self.Histos['{}/ljiso'.format(chan)].Fill(maxpfiso, aux['wgt'])
        hadact = lj.p4.energy()*lj.hadIsolationNoPU05/(1-lj.hadIsolationNoPU05)
        self.Histos['{}/hadactivity'.format(chan)].Fill(hadact, aux['wgt'])
        self.Histos['{}/dphiIso2D'.format(chan)].Fill(dphi, maxpfiso, aux['wgt'])

    def postProcess(self):
        super(MyEvents, self).postProcess()

        for k in self.Histos:
            if 'phi' not in k: continue
            xax = self.Histos[k].axis(0)
            xax.SetNdivisions(-310)
            xax.ChangeLabel(2,-1,-1,-1,-1,-1,"#frac{#pi}{10}")
            xax.ChangeLabel(3,-1,-1,-1,-1,-1,"#frac{#pi}{5}")
            xax.ChangeLabel(4,-1,-1,-1,-1,-1,"#frac{3#pi}{10}")
            xax.ChangeLabel(5,-1,-1,-1,-1,-1,"#frac{2#pi}{5}")
            xax.ChangeLabel(6,-1,-1,-1,-1,-1,"#frac{#pi}{2}")
            xax.ChangeLabel(7,-1,-1,-1,-1,-1,"#frac{3#pi}{5}")
            xax.ChangeLabel(8,-1,-1,-1,-1,-1,"#frac{7#pi}{10}")
            xax.ChangeLabel(9,-1,-1,-1,-1,-1,"#frac{4#pi}{5}")
            xax.ChangeLabel(10,-1,-1,-1,-1,-1,"#frac{9#pi}{10}")
            xax.ChangeLabel(11,-1,-1,-1,-1,-1,"#pi")


histCollection = [
    {
        'name': 'nbtight',
        'binning': (5, 0, 5),
        'title': 'Num. tight bjets;Num.bjets;counts'
    },
    {
        'name': 'proxyd0',
        'binning': [[0,2,4,6,8,10,20,50,]+list(np.arange(100,2100,100))],
        'title': 'proxy muon |d_{0}|;|d_{0}| [#mum];Events'
    },
    {
        'name': 'njet',
        'binning': (5, 0, 5),
        'title': 'num. of AK4Jets (p_{T}>LJ0 p_{T}, proxy p_{T});N;counts/1'
    },
    {
        'name': 'proxyiso',
        'binning': (50, 0, 1),
        'title': 'proxy muon isolation;isolation;counts/0.02'
    },
    {
        'name': 'ljiso',
        'binning': (50, 0, 1),
        'title': 'lepton-jet isolation;isolation;counts/0.02'
    },
    {
        'name': 'dphi',
        'binning': (30, 0, M_PI),
        'title': '|#Delta#phi| between lepton-jet and proxy muon;|#Delta#phi|;counts/#pi/30'
    },
    {
        'name': 'hadactivity',
        'binning': (100, 0, 100),
        'title': 'lepton-jet isolation hadronic PFcand activity;hadronic activity [GeV];Events/1GeV',
    },
    {
        'name': 'dphiIso2D',
        'binning': (30, 0, M_PI, 30, 0, 0.3),
        'title': '|#Delta#phi| vs maxiso;|#Delta#phi|;maxIso',
    },
]
