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
        passLjMass = all(map(lambda lj: lj.isEgmType() or lj.isMuonType() and lj.p4.M()<8, [LJ0, LJ1]))
        if not passLjMass: return

        Njet = 0
        NjetCleaned = 0
        for j in event.ak4jets:
            if not j.jetid: continue
            if j.p4.pt()<50: continue
            if abs(j.p4.eta())>2.4: continue

            Njet+=1

            mindist = min([DeltaR(j.p4, LJ0.p4), DeltaR(j.p4, LJ1.p4)])
            self.Histos['{}/ljdist'.format(chan)].Fill(mindist, aux['wgt'])
            if mindist<0.4: continue
            NjetCleaned+=1
            self.Histos['{}/jetpt'.format(chan)].Fill(j.p4.pt(), aux['wgt'])

        self.Histos['{}/njet'.format(chan)].Fill(Njet, aux['wgt'])
        self.Histos['{}/ncleanedjet'.format(chan)].Fill(NjetCleaned, aux['wgt'])

        invm = (LJ0.p4+LJ1.p4).M()
        self.Histos['{}/invm'.format(chan)].Fill(invm, aux['wgt'])


histCollection = [
    {
        'name': 'njet',
        'binning': (8, 0, 8),
        'title': 'Number of ak4jets;N;Events'
    },
    {
        'name': 'ncleanedjet',
        'binning': (8, 0, 8),
        'title': 'Number of cleaned ak4jets;N;Events'
    },
    {
        'name': 'ljdist',
        'binning': (50, 0, 5),
        'title': 'min dist btw ak4jet and lepton-jet;distance;Events'
    },
    {
        'name': 'jetpt',
        'binning': (50, 0, 500),
        'title': 'AK4Jet p_{T};pT [GeV];Events'
    },
    {
        'name': 'invm',
        'binning': (100, 0, 250),
        'title': 'inv mass;mass [GeV];Events'
    },
]