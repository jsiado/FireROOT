#!/usr/bin/env python
import math

from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *

class MyEvents(ProxyEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu']):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel)

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']
        lj, proxy = aux['lj'], aux['proxy']
        if not lj.passCosmicVeto(event): return

        nbtight = 0
        for s, j in zip(event.hftagscores, event.ak4jets):
            if not (j.jetid and j.p4.pt()>30 and abs(j.p4.eta())<2.5): continue
            if (s.DeepCSV_b&(1<<2))!=(1<<2): continue
            nbtight += 1


        mind0sigs = []
        if lj.isMuonType() and not math.isnan(lj.pfcand_tkD0SigMin):
            mind0sigs.append(lj.pfcand_tkD0SigMin)
        mind0sigs.append(proxy.d0sig(event))

        njet = sum([
            1 for j in event.ak4jets if \
                j.jetid \
                and j.p4.pt() > max([lj.p4.pt(), proxy.p4.pt()]) \
                and abs(j.p4.eta()) < 2.4
            ])
        maxpfiso = lj.pfiso() #max([lj.pfiso(), proxy.pfiso()])
        dphi = abs(DeltaPhi(lj.p4, proxy.p4))

        self.Histos['{}/nbtight'.format(chan)].Fill(nbtight, aux['wgt'])
        if nbtight==0: return

        self.Histos['{}/proxyd0sig'.format(chan)].Fill(proxy.d0sig(event), aux['wgt'])
        self.Histos['{}/maxd0sig'.format(chan)].Fill(max(mind0sigs), aux['wgt'])
        # if max(mind0sigs)<1: return
        if max(mind0sigs)<0.5: return

        self.Histos['{}/proxyiso'.format(chan)].Fill(proxy.pfiso(), aux['wgt'])
        if proxy.pfiso()<0.1: return

        self.Histos['{}/njet'.format(chan)].Fill(njet, aux['wgt'])
        self.Histos['{}/iso'.format(chan)].Fill(maxpfiso, aux['wgt'])
        self.Histos['{}/dphi'.format(chan)].Fill(dphi, aux['wgt'])

        if njet==0:
            self.Histos['{}/dphi_0jet'.format(chan)].Fill(dphi, aux['wgt'])
        else:
            self.Histos['{}/dphi_0jetinv'.format(chan)].Fill(dphi, aux['wgt'])

        if maxpfiso<0.15:
            self.Histos['{}/dphi_siso'.format(chan)].Fill(dphi, aux['wgt'])
        else:
            self.Histos['{}/dphi_sisoinv'.format(chan)].Fill(dphi, aux['wgt'])


histCollection = [
    {
        'name': 'nbtight',
        'binning': (5, 0, 5),
        'title': 'Num. tight bjets;Num.bjets;counts'
    },
    {
        'name': 'proxyd0sig',
        'binning': (50, 0, 10),
        'title': 'proxy muon d0 significance;d0/#sigma_{d0};counts/0.2'
    },
    {
        'name': 'maxd0sig',
        'binning': (50, 0, 10),
        'title': 'max(proxy,lj) d0 significance;d0/#sigma_{d0};counts/0.2'
    },
    {
        'name': 'njet',
        'binning': (5, 0, 5),
        'title': 'num. of AK4Jets;num.AK4jet;counts/1'
    },
    {
        'name': 'proxyiso',
        'binning': (50, 0, 1),
        'title': 'proxy isolation;isolation;counts/0.02'
    },
    {
        'name': 'iso',
        'binning': (50, 0, 1),
        'title': 'lepton-jet isolation;isolation;counts/0.02'
    },
    {
        'name': 'dphi',
        'binning': (20, 0, M_PI),
        'title': '|#Delta#phi| between lepton-jet and proxy muon;|#Delta#phi|;counts/#pi/20'
    },
    {
        'name': 'dphi_0jet',
        'binning': (20, 0, M_PI),
        'title': '|#Delta#phi| between lepton-jet and proxy muon;|#Delta#phi|;counts/#pi/20'
    },
    {
        'name': 'dphi_0jetinv',
        'binning': (20, 0, M_PI),
        'title': '|#Delta#phi| between lepton-jet and proxy muon;|#Delta#phi|;counts/#pi/20'
    },
    {
        'name': 'dphi_siso',
        'binning': (20, 0, M_PI),
        'title': '|#Delta#phi| between lepton-jet and proxy muon;|#Delta#phi|;counts/#pi/20'
    },
    {
        'name': 'dphi_sisoinv',
        'binning': (20, 0, M_PI),
        'title': '|#Delta#phi| between lepton-jet and proxy muon;|#Delta#phi|;counts/#pi/20'
    },
]

