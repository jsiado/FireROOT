#!/usr/bin/env python
import math

from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *

class MyEvents(Events):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']

        LJ0, LJ1 = aux['lj0'], aux['lj1']
        passCosmic = all(map(lambda lj: lj.passCosmicVeto(event), [LJ0, LJ1]))

        if not passCosmic: return

        muInLjIdx = []
        for lj in [LJ0, LJ1]:
            if not lj.isMuonType(): continue
            for i in lj.pfcand_pfmuonIdx:
                muInLjIdx.append(i)
        muInLjIdx = list(set(muInLjIdx))

        NlooseMu, NmediumMu, NtightMu = 0, 0, 0
        NlooseIsoMu, NmediumIsoMu, NtightIsoMu = 0, 0, 0
        NmediumPromptMu = 0
        for i, mu in enumerate(event.muons):
            if mu.p4.pt()<5: continue
            if abs(mu.p4.eta())>2.4: continue
            if i in muInLjIdx: continue
            if mu.selectors&(1<<0)==(1<<0): NlooseMu+=1
            if mu.selectors&(1<<1)==(1<<1): NmediumMu+=1
            if mu.selectors&(1<<3)==(1<<3): NtightMu+=1

            if mu.selectors&(1<<7)==(1<<7): NlooseIsoMu+=1
            if mu.selectors&(1<<8)==(1<<8): NmediumIsoMu+=1
            if mu.selectors&(1<<9)==(1<<9): NtightIsoMu+=1

            if mu.selectors&(1<<2)==(1<<2): NmediumPromptMu+=1

            self.Histos['{}/pt'.format(chan)].Fill(mu.p4.pt(), aux['wgt'])


        self.Histos['{}/nloose'.format(chan)].Fill(NlooseMu, aux['wgt'])
        self.Histos['{}/nmedium'.format(chan)].Fill(NmediumMu, aux['wgt'])
        self.Histos['{}/ntight'.format(chan)].Fill(NtightMu, aux['wgt'])

        self.Histos['{}/nlooseIso'.format(chan)].Fill(NlooseIsoMu, aux['wgt'])
        self.Histos['{}/nmediumIso'.format(chan)].Fill(NmediumIsoMu, aux['wgt'])
        self.Histos['{}/ntightIso'.format(chan)].Fill(NtightIsoMu, aux['wgt'])

        self.Histos['{}/nmediumprompt'.format(chan)].Fill(NmediumPromptMu, aux['wgt'])


histCollection = [
    {
        'name': 'nloose',
        'binning': (8, 0, 8),
        'title': 'Number of additional loose ID muons;N;Events'
    },
    {
        'name': 'nmedium',
        'binning': (8, 0, 8),
        'title': 'Number of additional medium ID muons;N;Events'
    },
    {
        'name': 'ntight',
        'binning': (8, 0, 8),
        'title': 'Number of additional tight ID muons;N;Events'
    },
    {
        'name': 'nlooseIso',
        'binning': (8, 0, 8),
        'title': 'Number of additional loose Iso muons;N;Events'
    },
    {
        'name': 'nmediumIso',
        'binning': (8, 0, 8),
        'title': 'Number of additional medium Iso muons;N;Events'
    },
    {
        'name': 'ntightIso',
        'binning': (8, 0, 8),
        'title': 'Number of additional tight Iso muons;N;Events'
    },
    {
        'name': 'nmediumprompt',
        'binning': (8, 0, 8),
        'title': 'Number of additional medium prompt ID muons;N;Events'
    },
    {
        'name': 'pt',
        'binning': (100, 0, 200),
        'title': 'muon p_{T};p_{T} [GeV];Events'
    },
]