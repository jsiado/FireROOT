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

        isonopu = []
        iso = []
        isonopu_pt = []
        iso_pt = []

        for lj in [LJ0, LJ1]:
            if not math.isnan(lj.pfIsolationNoPU05):
                isonopu.append(lj.pfIsolationNoPU05)
            if not math.isnan(lj.pfIsolation05):
                iso.append(lj.pfIsolation05)
            if not math.isnan(lj.pfIsolationPtNoPU05):
                isonopu_pt.append(lj.pfIsolationPtNoPU05)
            if not math.isnan(lj.pfIsolationPt05):
                iso_pt.append(lj.pfIsolationPt05)
            if lj.isEgmType():
                self.Histos['{}/egmljisonopu'.format(chan)].Fill(lj.pfiso(), aux['wgt'])
                self.Histos['{}/egmljiso'.format(chan)].Fill(lj.pfIsolation05, aux['wgt'])

        self.Histos['{}/maxisonopu'.format(chan)].Fill(max(isonopu), aux['wgt'])
        self.Histos['{}/maxiso'.format(chan)].Fill(max(iso), aux['wgt'])
        self.Histos['{}/maxisoptnopu'.format(chan)].Fill(max(isonopu_pt), aux['wgt'])
        self.Histos['{}/maxisopt'.format(chan)].Fill(max(iso_pt), aux['wgt'])

        # self.Histos['{}/rho'.format(chan)].Fill(event.fixedGridRho, aux['wgt'])
        pupt = event.fixedGridRho*math.pi*0.5**2
        # correct = lambda lj: 1-1/(1/(1-lj.pfIsolationPt05)-pupt/lj.p4.pt())
        def correct(lj):
            if lj.pfIsolationPt05==0: return 0
            activity = lj.p4.pt()/(1./lj.pfIsolationPt05-1)
            activity = max(0, activity-pupt)
            return activity/(activity+lj.p4.pt())
        correct_iso = []
        for lj in [LJ0, LJ1]:
            correct_iso.append( correct(lj) )
            if lj.isEgmType():
                self.Histos['{}/egmljcorriso'.format(chan)].Fill( correct(lj), aux['wgt'])

        self.Histos['{}/maxcorriso'.format(chan)].Fill(max(correct_iso), aux['wgt'])


        mind0s = []
        for lj in [LJ0, LJ1]:
            if lj.isMuonType() and not math.isnan(lj.pfcand_tkD0Min):
                mind0s.append(lj.pfcand_tkD0Min*1e4)
        metric_d0 = {'2mu2e': 1000, '4mu': 100}
        if max(mind0s)<metric_d0[chan]: return
        self.Histos['{}/maxcorriso_d0'.format(chan)].Fill(max(correct_iso), aux['wgt'])
        self.Histos['{}/maxisonopu_d0'.format(chan)].Fill(max(isonopu), aux['wgt'])
        for lj in [LJ0, LJ1]:
            if lj.isEgmType():
                self.Histos['{}/egmljisonopu_d0'.format(chan)].Fill(lj.pfiso(), aux['wgt'])
                self.Histos['{}/egmljcorriso_d0'.format(chan)].Fill( correct(lj), aux['wgt'])


histCollection = [
    {
        'name': 'maxisonopu',
        'binning': (50, 0, 0.5),
        'title': 'max lepton-jet isolation (no PU);isolation;counts',
    },
    {
        'name': 'maxiso',
        'binning': (50, 0, 0.5),
        'title': 'max lepton-jet isolation (w/ PU);isolation;counts',
    },
    {
        'name': 'maxisoptnopu',
        'binning': (50, 0, 0.5),
        'title': 'max lepton-jet p_{T} isolation (no PU);isolation;counts',
    },
    {
        'name': 'maxisopt',
        'binning': (50, 0, 0.5),
        'title': 'max lepton-jet p_{T} isolation (w/ PU);isolation;counts',
    },
    {
        'name': 'maxcorriso',
        'binning': (50, 0, 0.5),
        'title': 'max lepton-jet p_{T} corrected isolation (w/ PU);isolation;counts',
    },
    # {
    #     'name': 'rho',
    #     'binning': (50, 0, 50),
    #     'title': 'fixed grid rho;#rho;counts',
    # },
    {
        'name': 'maxcorriso_d0',
        'binning': (50, 0, 0.5),
        'title': 'max lepton-jet p_{T} corrected isolation (w/ PU, after displacement cut);isolation;counts',
    },
    {
        'name': 'maxisonopu_d0',
        'binning': (50, 0, 0.5),
        'title': 'max lepton-jet isolation (no PU, after displacement cut);isolation;counts',
    },

    {
        'name': 'egmljiso',
        'binning': (50, 0, 0.5),
        'title': 'egm-type lepton-jet isolation (w/ PU);isolation;counts',
    },
    {
        'name': 'egmljisonopu',
        'binning': (50, 0, 0.5),
        'title': 'egm-type lepton-jet isolation (no PU);isolation;counts',
    },
    {
        'name': 'egmljisonopu_d0',
        'binning': (50, 0, 0.5),
        'title': 'egm-type lepton-jet isolation (no PU, after displacement cut);isolation;counts',
    },
    {
        'name': 'egmljcorriso',
        'binning': (50, 0, 0.5),
        'title': 'egm-type lepton-jet p_{T} corrected isolation (w/ PU);isolation;counts',
    },
    {
        'name': 'egmljcorriso_d0',
        'binning': (50, 0, 0.5),
        'title': 'egm-type lepton-jet p_{T} corrected isolation (w/ PU, after displacement cut);isolation;counts',
    },

]