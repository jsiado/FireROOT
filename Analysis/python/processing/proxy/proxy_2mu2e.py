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
        if abs(proxy.dz(event))>40: return

        nbtight = 0
        for s, j in zip(event.hftagscores, event.ak4jets):
            if not (j.jetid and j.p4.pt()>30 and abs(j.p4.eta())<2.5): continue
            if (s.DeepCSV_b&(1<<2))!=(1<<2): continue
            nbtight += 1

        proxyd0 = abs(proxy.d0(event))*1e4

        maxpfiso = lj.pfiso()
        dphi = abs(DeltaPhi(lj.p4, proxy.p4))

        self.Histos['{}/nbtight'.format(chan)].Fill(nbtight, aux['wgt'])
        self.Histos['{}/proxyd0inc'.format(chan)].Fill(proxyd0, aux['wgt'])
        if nbtight==0: return

        if proxyd0 > 100:
            self.Histos['{}/dphi_100'.format(chan)].Fill(dphi, aux['wgt'])
            self.Histos['{}/dphiIso2Dpre'.format(chan)].Fill(dphi, maxpfiso, aux['wgt'])
        if proxyd0 > 200:
            self.Histos['{}/dphi_200'.format(chan)].Fill(dphi, aux['wgt'])
        if proxyd0 > 300:
            self.Histos['{}/dphi_300'.format(chan)].Fill(dphi, aux['wgt'])
        if proxyd0 > 400:
            self.Histos['{}/dphi_400'.format(chan)].Fill(dphi, aux['wgt'])
        if proxyd0 > 500:
            self.Histos['{}/dphi_500'.format(chan)].Fill(dphi, aux['wgt'])
            self.Histos['{}/dphiIso2Dinit'.format(chan)].Fill(dphi, maxpfiso, aux['wgt'])

        self.Histos['{}/proxyd0'.format(chan)].Fill(proxyd0, aux['wgt'])
        if proxyd0<1500: return

        self.Histos['{}/proxyiso'.format(chan)].Fill(proxy.pfiso(), aux['wgt'])
        self.Histos['{}/dphi'.format(chan)].Fill(dphi, aux['wgt'])
        self.Histos['{}/ljiso'.format(chan)].Fill(maxpfiso, aux['wgt'])
        self.Histos['{}/dphiIso2D'.format(chan)].Fill(dphi, maxpfiso, aux['wgt'])

    def postProcess(self):
        super(MyEvents, self).postProcess()

        for k in self.Histos:
            if 'phi' not in k: continue
            xax = self.Histos[k].axis(0)
            decorate_axis_pi(xax)
            if '2D' in k:
                self.Histos[k].yaxis.SetNdivisions(-210)


histCollection = [
    {
        'name': 'nbtight',
        'binning': (5, 0, 5),
        'title': 'Num. tight bjets;Num.bjets;counts'
    },
    {
        'name': 'proxyd0inc',
        # 'binning': [[0,2,4,6,8,10,20,50,]+list(np.arange(100,2501,100))],
        'binning': (40, 0, 2000),
        'title': 'proxy muon |d_{0}|;|d_{0}| [#mum];Events'
    },
    {
        'name': 'proxyd0',
        'binning': (40, 0, 2000),
        'title': 'proxy muon |d_{0}|(N_{bjet}#geq1);|d_{0}| [#mum];Events'
    },
    {
        'name': 'proxyiso',
        'binning': (20, 0, 0.5),
        'title': 'proxy muon isolation;isolation;counts'
    },
    {
        'name': 'ljiso',
        'binning': (20, 0, 0.5),
        'title': 'lepton-jet isolation;isolation;counts'
    },
    {
        'name': 'dphi_100',
        'binning': (20, 0, M_PI),
        'title': '|#Delta#phi|(lepton-jet, proxy muon) (proxy muon |d_{0}|>100#mum);|#Delta#phi|;counts/#pi/20'
    },
    {
        'name': 'dphi_200',
        'binning': (20, 0, M_PI),
        'title': '|#Delta#phi|(lepton-jet, proxy muon) (proxy muon |d_{0}|>200#mum);|#Delta#phi|;counts/#pi/20'
    },
    {
        'name': 'dphi_300',
        'binning': (20, 0, M_PI),
        'title': '|#Delta#phi|(lepton-jet, proxy muon) (proxy muon |d_{0}|>300#mum);|#Delta#phi|;counts/#pi/20'
    },
    {
        'name': 'dphi_400',
        'binning': (20, 0, M_PI),
        'title': '|#Delta#phi|(lepton-jet, proxy muon) (proxy muon |d_{0}|>400#mum);|#Delta#phi|;counts/#pi/20'
    },
    {
        'name': 'dphi_500',
        'binning': (20, 0, M_PI),
        'title': '|#Delta#phi|(lepton-jet, proxy muon) (proxy muon |d_{0}|>500#mum);|#Delta#phi|;counts/#pi/20'
    },

    {
        'name': 'dphi',
        'binning': (20, 0, M_PI),
        'title': '|#Delta#phi|(lepton-jet, proxy muon);|#Delta#phi|;counts/#pi/20'
    },
    {
        'name': 'dphiIso2Dpre',
        'binning': (20, 0, M_PI, 20, 0, 0.5),
        'title': '|#Delta#phi| vs lepton-jet isolation;|#Delta#phi|;iso',
    },
    {
        'name': 'dphiIso2Dinit',
        'binning': (20, 0, M_PI, 20, 0, 0.5),
        'title': '|#Delta#phi| vs lepton-jet isolation;|#Delta#phi|;iso',
    },
    {
        'name': 'dphiIso2D',
        'binning': (20, 0, M_PI, 20, 0, 0.5),
        'title': '|#Delta#phi| vs lepton-jet isolation;|#Delta#phi|;iso',
    },
]
