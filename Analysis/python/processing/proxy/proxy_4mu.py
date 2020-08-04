#!/usr/bin/env python
import math
import numpy as np

from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *

class MyEvents(ProxyEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)
        self.KeepCutFlow=True

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']
        cutflowbin = 5

        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1

        lj, proxy = aux['lj'], aux['proxy']
        if not lj.passCosmicVeto(event): return
        if abs(proxy.dz(event))>40: return
        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1

        mind0s = []
        if lj.isMuonType() and not math.isnan(lj.pfcand_tkD0Min):
            mind0s.append( lj.pfcand_tkD0Min*1e4 )
        mind0s.append( abs(proxy.d0(event))*1e4 )

        self.Histos['{}/proxyd0inc'.format(chan)].Fill( abs(proxy.d0(event))*1e4, aux['wgt'])
        self.Histos['{}/muljd0inc'.format(chan)].Fill( lj.pfcand_tkD0Min*1e4, aux['wgt'])
        self.Histos['{}/maxd0inc'.format(chan)].Fill( max(mind0s), aux['wgt'])

        nbtight, nbmedium = 0, 0
        for s, j in zip(event.hftagscores, event.ak4jets):
            if not (j.jetid and j.p4.pt()>30 and abs(j.p4.eta())<2.5): continue
            if (s.DeepCSV_b&(1<<2))==(1<<2): nbtight += 1
            if (s.DeepCSV_b&(1<<1))==(1<<1): nbmedium += 1


        dphi = abs(DeltaPhi(lj.p4, proxy.p4))


        self.Histos['{}/nbtight'.format(chan)].Fill(nbtight, aux['wgt'])
        self.Histos['{}/nbmedium'.format(chan)].Fill(nbmedium, aux['wgt'])
        if nbtight==0: return
        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1


        self.Histos['{}/proxyd0'.format(chan)].Fill( abs(proxy.d0(event))*1e4, aux['wgt'])
        self.Histos['{}/muljd0'.format(chan)].Fill( lj.pfcand_tkD0Min*1e4, aux['wgt'])
        self.Histos['{}/maxd0'.format(chan)].Fill( max(mind0s), aux['wgt'])

        if lj.pfcand_tkD0Min*1e4 > 100:
            self.Histos['{}/dphi_100'.format(chan)].Fill(dphi, aux['wgt'])
            self.Histos['{}/dphiIso2Dpre'.format(chan)].Fill(dphi, lj.pfiso(), aux['wgt'])
        if lj.pfcand_tkD0Min*1e4 > 200:
            self.Histos['{}/dphi_200'.format(chan)].Fill(dphi, aux['wgt'])
        if lj.pfcand_tkD0Min*1e4 > 300:
            self.Histos['{}/dphi_300'.format(chan)].Fill(dphi, aux['wgt'])
        if lj.pfcand_tkD0Min*1e4 > 400:
            self.Histos['{}/dphi_400'.format(chan)].Fill(dphi, aux['wgt'])
        if lj.pfcand_tkD0Min*1e4 > 500:
            self.Histos['{}/dphi_500'.format(chan)].Fill(dphi, aux['wgt'])
            self.Histos['{}/dphiIso2Dinit'.format(chan)].Fill(dphi, lj.pfiso(), aux['wgt'])

        if lj.pfcand_tkD0Min*1e4 < 1000: return
        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1

        self.Histos['{}/proxyiso'.format(chan)].Fill(proxy.pfiso(), aux['wgt'])
        self.Histos['{}/muljiso'.format(chan)].Fill(lj.pfiso(), aux['wgt'])
        self.Histos['{}/maxiso'.format(chan)].Fill(max(lj.pfiso(), proxy.pfiso()), aux['wgt'])

        self.Histos['{}/dphi'.format(chan)].Fill(dphi, aux['wgt'])

        self.Histos['{}/dphiIso2D'.format(chan)].Fill(dphi, lj.pfiso(), aux['wgt'])


    def postProcess(self):
        super(MyEvents, self).postProcess()

        for ch in self.Channel:
            xaxis = self.Histos['{}/cutflow'.format(ch)].axis(0)

            labels = [ch, 'ljcosmicveto_pass', 'bjet_ge1', 'mind0_pass',]

            for i, s in enumerate(labels, start=6):
                xaxis.SetBinLabel(i, s)
                # binNum., labAngel, labSize, labAlign, labColor, labFont, labText
                xaxis.ChangeLabel(i, 315, -1, 11, -1, -1, s)

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
        'name': 'nbmedium',
        'binning': (5, 0, 5),
        'title': 'Num. medium bjets;Num.bjets;counts'
    },
    {
        'name': 'proxyd0inc',
        'binning': (50, 0, 2500),
        'title': 'proxy muon |d_{0}|;|d_{0}| [#mum];Events'
    },
    {
        'name': 'muljd0inc',
        'binning': (50, 0, 2500),
        'title': 'muon type lepton-jet minimum |d_{0}|;|d_{0}| [#mum];Events'
    },
    {
        'name': 'maxd0inc',
        'binning': (50, 0, 2500),
        'title': 'max(proxy,lj) |d_{0}|;|d_{0}| [#mum];Events'
    },
    {
        'name': 'proxyd0',
        'binning': (50, 0, 2500),
        'title': 'proxy muon |d_{0}|(N_{bjet}#geq1);|d_{0}| [#mum];Events'
    },
    {
        'name': 'muljd0',
        'binning': (50, 0, 2500),
        'title': 'muon type lepton-jet minimum |d_{0}|(N_{bjet}#geq1);|d_{0}| [#mum];Events'
    },
    {
        'name': 'maxd0',
        'binning': (50, 0, 2500),
        'title': 'max(proxy,lj) |d_{0}|(N_{bjet}#geq1);|d_{0}| [#mum];Events'
    },
    {
        'name': 'proxyiso',
        'binning': (20, 0, 0.5),
        'title': 'proxy isolation;iso;counts'
    },
    {
        'name': 'muljiso',
        'binning': (20, 0, 0.5),
        'title': 'lepton-jet isolation;iso;counts'
    },
    {
        'name': 'maxiso',
        'binning': (20, 0, 0.5),
        'title': 'max iso(lepton-jet, proxy muon);iso;counts'
    },
    {
        'name': 'dphi_100',
        'binning': (20, 0, M_PI),
        'title': '|#Delta#phi|(lepton-jet, proxy muon) (LJ |d_{0}|>100#mum);|#Delta#phi|;counts/#pi/20'
    },
    {
        'name': 'dphi_200',
        'binning': (20, 0, M_PI),
        'title': '|#Delta#phi|(lepton-jet, proxy muon) (LJ |d_{0}|>200#mum);|#Delta#phi|;counts/#pi/20'
    },
    {
        'name': 'dphi_300',
        'binning': (20, 0, M_PI),
        'title': '|#Delta#phi|(lepton-jet, proxy muon) (LJ |d_{0}|>300#mum);|#Delta#phi|;counts/#pi/20'
    },
    {
        'name': 'dphi_400',
        'binning': (20, 0, M_PI),
        'title': '|#Delta#phi|(lepton-jet, proxy muon) (LJ |d_{0}|>400#mum);|#Delta#phi|;counts/#pi/20'
    },
    {
        'name': 'dphi_500',
        'binning': (20, 0, M_PI),
        'title': '|#Delta#phi|(lepton-jet, proxy muon) (LJ |d_{0}|>500#mum);|#Delta#phi|;counts/#pi/20'
    },
    {
        'name': 'dphi',
        'binning': (20, 0, M_PI),
        'title': '|#Delta#phi|(lepton-jet, proxy muon);|#Delta#phi|;counts/#pi/20'
    },
    {
        'name': 'dphiIso2Dpre',
        'binning': (20, 0, M_PI, 20, 0, 0.5),
        'title': '|#Delta#phi| vs muon-type lepton-jet isolation;|#Delta#phi|;iso',
    },
    {
        'name': 'dphiIso2Dinit',
        'binning': (20, 0, M_PI, 20, 0, 0.5),
        'title': '|#Delta#phi| vs muon-type lepton-jet isolation;|#Delta#phi|;iso',
    },
    {
        'name': 'dphiIso2D',
        'binning': (20, 0, M_PI, 20, 0, 0.5),
        'title': '|#Delta#phi| vs muon-type lepton-jet isolation;|#Delta#phi|;iso',
    },
]