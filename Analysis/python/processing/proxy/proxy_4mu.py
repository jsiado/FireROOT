#!/usr/bin/env python
import math, json
import numpy as np

from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *

class MyEvents(ProxyEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']
        cutflowbin = 5

        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1

        lj, proxy = aux['lj'], aux['proxy']
        if not lj.passCosmicVeto(event): return
        if abs(proxy.dz(event))>40: return
        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1

        nbtight = 0
        for s, j in zip(event.hftagscores, event.ak4jets):
            if not (j.jetid and j.p4.pt()>30 and abs(j.p4.eta())<2.5): continue
            if (s.DeepCSV_b&(1<<2))!=(1<<2): continue
            nbtight += 1


        mind0s = []
        if lj.isMuonType() and not math.isnan(lj.pfcand_tkD0Min):
            mind0s.append( lj.pfcand_tkD0Min*1e4 )
        mind0s.append( abs(proxy.d0(event))*1e4 )


        ljact = lj.p4.energy()*lj.pfiso()/(1-lj.pfiso())
        proxyact = proxy.p4.energy()*proxy.pfiso()/(1-proxy.pfiso())

        dphi = abs(DeltaPhi(lj.p4, proxy.p4))

        self.Histos['{}/proxyd0'.format(chan)].Fill( abs(proxy.d0(event))*1e4, aux['wgt'])
        self.Histos['{}/muljd0'.format(chan)].Fill( lj.pfcand_tkD0Min*1e4, aux['wgt'])
        self.Histos['{}/maxd0'.format(chan)].Fill( max(mind0s), aux['wgt'])

        if max(mind0s)<400: return
        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1

        self.Histos['{}/nbtight'.format(chan)].Fill(nbtight, aux['wgt'])
        if nbtight==0: return
        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1

        self.Histos['{}/proxyact'.format(chan)].Fill(proxyact, aux['wgt'])
        self.Histos['{}/muljact'.format(chan)].Fill(ljact, aux['wgt'])
        self.Histos['{}/maxact'.format(chan)].Fill(max(ljact, proxyact), aux['wgt'])

        self.Histos['{}/dphi'.format(chan)].Fill(dphi, aux['wgt'])

        self.Histos['{}/dphiAct2D'.format(chan)].Fill(dphi, max(ljact, proxyact), aux['wgt'])


    def postProcess(self):
        super(MyEvents, self).postProcess()

        for ch in self.Channel:
            xaxis = self.Histos['{}/cutflow'.format(ch)].axis(0)

            labels = [ch, 'ljcosmicveto_pass', 'd0sig_pass', 'bjet_ge1', 'proxyiso_pass', 'maxljiso_pass', 'ljpairdphi_pass']

            for i, s in enumerate(labels, start=6):
                xaxis.SetBinLabel(i, s)
                # binNum., labAngel, labSize, labAlign, labColor, labFont, labText
                xaxis.ChangeLabel(i, 315, -1, 11, -1, -1, s)

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
        'name': 'muljd0',
        'binning': [[0,2,4,6,8,10,20,50,]+list(np.arange(100,2100,100))],
        'title': 'muon type lepton-jet minimum |d_{0}|;|d_{0}| [#mum];Events'
    },

    {
        'name': 'maxd0',
        'binning': [[0,2,4,6,8,10,20,50,]+list(np.arange(100,2100,100))],
        'title': 'max(proxy,lj) |d_{0}|;|d_{0}| [#mum];Events'
    },
    {
        'name': 'proxyact',
        'binning': (100, 0, 100),
        'title': 'proxy activity;PF activity [GeV];counts/1GeV'
    },
    {
        'name': 'muljact',
        'binning': (100, 0, 100),
        'title': 'lepton-jet activity;PF activity [GeV];counts/1GeV'
    },
    {
        'name': 'maxact',
        'binning': (100, 0, 100),
        'title': 'max activity(lepton-jet, proxy muon);PF activity [GeV];counts/1GeV'
    },
    {
        'name': 'dphi',
        'binning': (30, 0, M_PI),
        'title': '|#Delta#phi|(lepton-jet, proxy muon);|#Delta#phi|;counts/#pi/30'
    },
    {
        'name': 'dphiAct2D',
        'binning': (30, 0, M_PI, 50, 0, 100),
        'title': '|#Delta#phi| vs max activity;|#Delta#phi|;max activity',
    },
]