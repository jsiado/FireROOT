#!/usr/bin/env python
import math

from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *


class MyEvents(Events):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu']):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel)

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']

        LJ0, LJ1 = aux['lj0'], aux['lj1']
        passCosmic = all(map(lambda lj: lj.passCosmicVeto(event), [LJ0, LJ1]))

        if not passCosmic: return

        dphi = abs(DeltaPhi(LJ0.p4, LJ1.p4))
        invm = (LJ0.p4+LJ1.p4).M()
        maxpfiso = max([LJ0.pfiso(), LJ1.pfiso()])
        njet = sum([1 for j in event.ak4jets if j.jetid and j.p4.pt()>max([LJ0.p4.pt(), LJ1.p4.pt()]) and abs(j.p4.eta())<2.4])

        ## displacement cut
        mind0sigs = []
        for lj in [LJ0, LJ1]:
            if lj.isMuonType() and not math.isnan(lj.pfcand_tkD0SigMin):
                mind0sigs.append(lj.pfcand_tkD0SigMin)

        metric_d0sig = {'2mu2e': 2, '4mu': 0.5}
        metric_pfiso = {'2mu2e': 0.15, '4mu': 0.15}

        if max(mind0sigs)<metric_d0sig[chan]: return

        if chan=='2mu2e' and njet>0: return

        mf = event.metfilters
        ## before ABCD
        self.Histos['{}/invm_b100'.format(chan)].Fill(invm, aux['wgt'])
        self.Histos['{}/invm_b150'.format(chan)].Fill(invm, aux['wgt'])
        self.Histos['{}/invm_b200'.format(chan)].Fill(invm, aux['wgt'])
        self.Histos['{}/invm_b500'.format(chan)].Fill(invm, aux['wgt'])
        self.Histos['{}/invm_b800'.format(chan)].Fill(invm, aux['wgt'])
        self.Histos['{}/invm_b1000'.format(chan)].Fill(invm, aux['wgt'])
        self.Histos['{}/bmf_b'.format(chan)].Fill(int(mf.BadMuonFilter), aux['wgt'])


        if maxpfiso>metric_pfiso[chan] or dphi<math.pi/2: return
        ## signal region
        self.Histos['{}/invm_e100'.format(chan)].Fill(invm, aux['wgt'])
        self.Histos['{}/invm_e150'.format(chan)].Fill(invm, aux['wgt'])
        self.Histos['{}/invm_e200'.format(chan)].Fill(invm, aux['wgt'])
        self.Histos['{}/invm_e500'.format(chan)].Fill(invm, aux['wgt'])
        self.Histos['{}/invm_e800'.format(chan)].Fill(invm, aux['wgt'])
        self.Histos['{}/invm_e1000'.format(chan)].Fill(invm, aux['wgt'])
        self.Histos['{}/bmf_e'.format(chan)].Fill(int(mf.BadMuonFilter), aux['wgt'])


histCollection = [
    {
        'name': 'invm_b100',
        'binning': (100, 0, 200),
        'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/2GeV'
    },
    {
        'name': 'invm_b150',
        'binning': (100, 0, 300),
        'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/3GeV'
    },
    {
        'name': 'invm_b200',
        'binning': (100, 0, 400),
        'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/4GeV'
    },
    {
        'name': 'invm_b500',
        'binning': (100, 0, 1000),
        'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/10GeV'
    },
    {
        'name': 'invm_b800',
        'binning': (100, 0, 1600),
        'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/16GeV'
    },
    {
        'name': 'invm_b1000',
        'binning': (100, 0, 2000),
        'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/20GeV'
    },
    {
        'name': 'invm_e100',
        'binning': (100, 0, 200),
        'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/2GeV'
    },
    {
        'name': 'invm_e150',
        'binning': (100, 0, 300),
        'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/3GeV'
    },
    {
        'name': 'invm_e200',
        'binning': (100, 0, 400),
        'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/4GeV'
    },
    {
        'name': 'invm_e500',
        'binning': (100, 0, 1000),
        'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/10GeV'
    },
    {
        'name': 'invm_e800',
        'binning': (100, 0, 1600),
        'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/16GeV'
    },
    {
        'name': 'invm_e1000',
        'binning': (100, 0, 2000),
        'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/20GeV'
    },
    {
        'name': 'bmf_b',
        'binning': (2, 0, 2),
        'title': 'BadMuonFilter;result;counts',
    },
    {
        'name': 'bmf_e',
        'binning': (2, 0, 2),
        'title': 'BadMuonFilter;result;counts',
    },
]