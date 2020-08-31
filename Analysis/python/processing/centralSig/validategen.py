#!/usr/bin/env python
import math

from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *

class MyEvents(SignalEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']

        for p in aux['dp']:
            rho = (p.dauvtx-p.vtx).Rho()
            l3d = (p.dauvtx-p.vtx).R()
            self.Histos['{}/dplxy'.format(chan)].Fill(rho)
            self.Histos['{}/dpl3d'.format(chan)].Fill(l3d)

            daus = []
            for d in event.gens:
                if abs(d.pid) not in [11, 13]: continue
                if (d.vtx-p.dauvtx).R()<1e-2: daus.append(d)
            if len(daus)==2:
                dpmass = (daus[0].p4+daus[1].p4).M()
                pairdr = DeltaR(daus[0].p4, daus[1].p4)
                self.Histos['{}/dpmass'.format(chan)].Fill(dpmass)
                if abs(daus[0].pid)==11: # electron pair
                    self.Histos['{}/electronpairdr'.format(chan)].Fill(pairdr)
                if abs(daus[0].pid)==13: # muon pair
                    self.Histos['{}/muonpairdr'.format(chan)].Fill(pairdr)

        if len(aux['dp'])==2:
            psmass = (aux['dp'][0].p4+aux['dp'][1].p4).M()
            dphi = abs(DeltaPhi(aux['dp'][0].p4, aux['dp'][1].p4))
            self.Histos['{}/psmass'.format(chan)].Fill(psmass)
            self.Histos['{}/dpdphi'.format(chan)].Fill(dphi)

        muons = [p for p in event.gens if abs(p.pid)==13]
        electrons = [p for p in event.gens if abs(p.pid)==11]

        self.Histos['{}/ndp'.format(chan)].Fill(len(aux['dp']))
        self.Histos['{}/nmu'.format(chan)].Fill(len(muons))
        self.Histos['{}/nel'.format(chan)].Fill(len(electrons))
        self.Histos['{}/nlep'.format(chan)].Fill(len(muons)+len(electrons))

        self.Histos['{}/mu0pt'.format(chan)].Fill(max([p.p4.pt() for p in muons]))
        if electrons:
            self.Histos['{}/el0pt'.format(chan)].Fill(max([p.p4.pt() for p in electrons]))
        for dp in aux['dp']:
            self.Histos['%s/dppt'%chan].Fill(dp.p4.pt())

    def postProcess(self):
        super(MyEvents, self).postProcess()

        for k in self.Histos:
            if 'phi' not in k: continue
            xax = self.Histos[k].axis(0)
            decorate_axis_pi(xax)

histCollection = [
    {
        'name': 'dplxy',
        'binning': (500, 0, 500),
        'title': 'dark photon lxy;Lxy [cm];counts/1cm'
    },
    {
        'name': 'dpl3d',
        'binning': (750, 0, 750),
        'title': 'dark photon l3d;L3d [cm];counts/1cm'
    },
    {
        'name': 'dpmass',
        'binning': (750, 0, 7.5),
        'title': 'dark photon invariant mass;mass [GeV];counts/0.01GeV'
    },
    {
        'name': 'psmass',
        'binning': (1500, 0, 1500),
        'title': 'DM bound state invariant mass;mass [GeV];counts/1GeV'
    },
    {
        'name': 'ndp',
        'binning': (5, 0, 5),
        'title': 'Number of dark photons;N;counts'
    },
    {
        'name': 'nmu',
        'binning': (5, 0, 5),
        'title': 'Number of muons;N;counts'
    },
    {
        'name': 'nel',
        'binning': (5, 0, 5),
        'title': 'Number of electrons;N;counts'
    },
    {
        'name': 'nlep',
        'binning': (5, 0, 5),
        'title': 'Number of leptons(electrons+muons);N;counts'
    },
    {
        'name': 'dpdphi',
        'binning': (20, 0, M_PI),
        'title': '|#Delta#phi| of dark photon pair;|#Delta#phi|;counts'
    },
    {
        'name': 'electronpairdr',
        'binning': (50, 0, 1),
        'title': '#DeltaR between electron pair;#DeltaR(ee);counts'
    },
    {
        'name': 'muonpairdr',
        'binning': (50, 0, 1),
        'title': '#DeltaR between muon pair;#DeltaR(#mu#mu);counts'
    },
    {
        'name': 'mu0pt',
        'binning': (1000, 0, 1000),
        'title': 'leading #mu p_{T};#mu p_{T} [GeV];counts/1GeV'
    },
    {
        'name': 'el0pt',
        'binning': (1000, 0, 1000),
        'title': 'leading electron p_{T};e p_{T} [GeV];counts/1GeV'
    },
    {
        'name': 'dppt',
        'binning': (1000, 0, 1000),
        'title': 'Z_{d} p_{T};Z_{d} p_{T} [GeV];counts/1GeV'
    },

]