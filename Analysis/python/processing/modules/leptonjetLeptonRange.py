#!/usr/bin/env python
import math
import numpy as np

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

        for lj in [LJ0, LJ1]:
            for ctype, pt, eta in zip(lj.pfcand_type, lj.pfcand_pt, lj.pfcand_eta):
                if ctype==2:
                    self.Histos['{}/electronPt'.format(chan)].Fill(pt, aux['wgt'])
                    self.Histos['{}/electronEta'.format(chan)].Fill(eta, aux['wgt'])
                if ctype==3:
                    self.Histos['{}/muonPt'.format(chan)].Fill(pt, aux['wgt'])
                    self.Histos['{}/muonEta'.format(chan)].Fill(eta, aux['wgt'])
                if ctype==4:
                    self.Histos['{}/photonPt'.format(chan)].Fill(pt, aux['wgt'])
                    self.Histos['{}/photonEta'.format(chan)].Fill(eta, aux['wgt'])
                if ctype==8:
                    self.Histos['{}/dsamuonPt'.format(chan)].Fill(pt, aux['wgt'])
                    self.Histos['{}/dsamuonEta'.format(chan)].Fill(eta, aux['wgt'])

        # displacement
        mind0s = []
        for lj in [LJ0, LJ1]:
            if lj.isMuonType() and not math.isnan(lj.pfcand_tkD0Min):
                mind0s.append(lj.pfcand_tkD0Min*1e4)
        metric_d0 = {'2mu2e': 1000, '4mu': 100}
        if max(mind0s)<metric_d0[chan]: return

        vetoLowPtElectron = False
        vetoLowPtPhoton = False
        vetoLowPtMuon = False
        for lj in [LJ0, LJ1]:
            if lj.isEgmType():
                for ctype, pt in zip(lj.pfcand_type, lj.pfcand_pt):
                    if ctype==2:
                        if pt<10: vetoLowPtElectron = True
                    if ctype==4:
                        if pt<20: vetoLowPtPhoton = True
            if lj.isMuonType():
                for ctype, pt in zip(lj.pfcand_type, lj.pfcand_pt):
                    if ctype==3:
                        if pt<15: vetoLowPtMuon = True

        self.Histos['{}/vetoLowPtElectron'.format(chan)].Fill(int(vetoLowPtElectron), aux['wgt'])
        self.Histos['{}/vetoLowPtPhoton'.format(chan)].Fill(int(vetoLowPtPhoton), aux['wgt'])
        self.Histos['{}/vetoLowPtEgm'.format(chan)].Fill(int(vetoLowPtElectron or vetoLowPtPhoton), aux['wgt'])

        self.Histos['{}/vetoLowPtMuon'.format(chan)].Fill(int(vetoLowPtMuon), aux['wgt'])
        self.Histos['{}/vetoLowPtPFCand'.format(chan)].Fill(int(vetoLowPtElectron or vetoLowPtMuon or vetoLowPtPhoton), aux['wgt'])

histCollection = [
    {
        'name': 'electronPt',
        'binning': [[0,5,10,20,50,]+list(np.arange(100,501,50))],
        'title': 'electron p_{T};p_{T} [GeV];counts',
    },
    {
        'name': 'electronEta',
        'binning': (24, -2.4, 2.4),
        'title': 'electron #eta;#eta;counts',
    },
    {
        'name': 'muonPt',
        'binning': [[0,5,10,15,20,50,]+list(np.arange(100,501,50))],
        'title': 'muon p_{T};p_{T} [GeV];counts',
    },
    {
        'name': 'muonEta',
        'binning': (24, -2.4, 2.4),
        'title': 'muon #eta;#eta;counts',
    },
    {
        'name': 'photonPt',
        'binning': [[0,5,10,20,50,]+list(np.arange(100,501,50))],
        'title': 'photon p_{T};p_{T} [GeV];counts',
    },
    {
        'name': 'photonEta',
        'binning': (24, -2.4, 2.4),
        'title': 'photon #eta;#eta;counts',
    },
    {
        'name': 'dsamuonPt',
        'binning': [[0,5,10,15,20,50,]+list(np.arange(100,501,50))],
        'title': 'dsamuon p_{T};p_{T} [GeV];counts',
    },
    {
        'name': 'dsamuonEta',
        'binning': (24, -2.4, 2.4),
        'title': 'dsamuon #eta;#eta;counts',
    },
    {
        'name': 'vetoLowPtElectron',
        'binning': (2, 0, 2),
        'title': 'signal loss due to PF electron p_{T}<10GeV;;events',
    },
    {
        'name': 'vetoLowPtPhoton',
        'binning': (2, 0, 2),
        'title': 'signal loss due to PF photon p_{T}<20GeV;;events',
    },
    {
        'name': 'vetoLowPtEgm',
        'binning': (2, 0, 2),
        'title': 'signal loss due to low p_{T} e#gamma;;events',
    },
    {
        'name': 'vetoLowPtMuon',
        'binning': (2, 0, 2),
        'title': 'signal loss due to PF muon p_{T}<15GeV;;events',
    },
    {
        'name': 'vetoLowPtPFCand',
        'binning': (2, 0, 2),
        'title': 'signal loss due to low p_{T} e#gamma#mu;;events',
    },
]