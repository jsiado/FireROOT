#!/usr/bin/env python
import math
import numpy as np
from rootpy.plotting import Profile

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
        if abs(proxy.dz(event))>40: return

        mind0 = lj.pfcand_tkD0Min*1e4

        ljiso = lj.pfiso()
        proxyiso = proxy.pfiso()
        ljact = lj.p4.energy()*lj.pfiso()/(1-lj.pfiso())
        proxyact = proxy.p4.energy()*proxy.pfiso()/(1-proxy.pfiso())

        dphi = abs(DeltaPhi(lj.p4, proxy.p4))

        self.Histos['{}/ljiso'.format(chan)].Fill(ljiso, aux['wgt'])
        self.Histos['{}/proxyiso'.format(chan)].Fill(proxyiso, aux['wgt'])
        self.Histos['{}/scaledproxyiso'.format(chan)].Fill(proxyiso*0.765, aux['wgt'])
        self.Histos['{}/maxiso'.format(chan)].Fill(max(ljiso, proxyiso), aux['wgt'])
        self.Histos['{}/ljact'.format(chan)].Fill(ljact, aux['wgt'])
        self.Histos['{}/proxyact'.format(chan)].Fill(proxyact, aux['wgt'])
        self.Histos['{}/maxact'.format(chan)].Fill(max(ljact, proxyact), aux['wgt'])
        self.Histos['{}/dphi'.format(chan)].Fill(dphi, aux['wgt'])
        self.Histos['{}/ljisoenergy'.format(chan)].Fill(lj.p4.energy(), ljiso, aux['wgt'])
        self.Histos['{}/proxyisoenergy'.format(chan)].Fill(proxy.p4.energy(), proxyiso,)

        if mind0<400: return

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
        'name': 'maxiso',
        'binning': (50, 0, 1),
        'title': 'max (lepton-jet,proxy) isolation;isolation;counts'
    },
    {
        'name': 'ljiso',
        'binning': (50, 0, 1),
        'title': 'lepton-jet isolation;isolation;counts'
    },
    {
        'name': 'proxyiso',
        'binning': (50, 0, 1),
        'title': 'proxy muon isolation;isolation;counts'
    },
    {
        'name': 'scaledproxyiso',
        'binning': (50, 0, 1),
        'title': 'scaled proxy muon isolation;isolation;counts'
    },
    {
        'name': 'maxact',
        'binning': (100, 0, 100),
        'title': 'max (lepton-jet,proxy) activity;PF activity [GeV];counts'
    },
    {
        'name': 'ljact',
        'binning': (100, 0, 100),
        'title': 'lepton-jet activity;PF activity [GeV];counts'
    },
    {
        'name': 'proxyact',
        'binning': (100, 0, 100),
        'title': 'proxy muon activity;PF activity [GeV];counts'
    },
    {
        'name': 'dphi',
        'binning': (30, 0, M_PI),
        'title': '|#Delta#phi|(lepton-jet, proxy muon);|#Delta#phi|;counts/#pi/30'
    },
    {
        'name': 'ljisoenergy',
        'class': Profile,
        'binning': (list(np.arange(0,500,20))+list(np.arange(500,1001,100)), 0, 1),
        'title': 'lepton-jet isolation vs. energy;lepton-jet energy [GeV];isolation'
    },
    {
        'name': 'proxyisoenergy',
        'class': Profile,
        'binning': (list(np.arange(0,500,20))+list(np.arange(500,1001,100)), 0, 1),
        'title': 'proxy muon isolation vs. energy;proxy muon energy [GeV];isolation'
    },
]