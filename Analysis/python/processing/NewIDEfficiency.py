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

        gmus = [p for p in event.gens \
            if abs(p.pid)==13 \
                and p.p4.pt()>5\
                and abs(p.p4.eta())<2.4\
                and p.vtx.Rho()<700]
        if len(gmus)<2: return
        
        #pt of dsa
        for i, dsa in enumerate(event.dsamuons):
            if dsa.p4.pt()<5 or abs(dsa.p4.eta())>2.4: continue
            if dsa.p4.pt()>5:
                self.Histos['%s/DsaPt5'%chan].Fill(dsa.p4.pt(), aux['wgt'])
                if dsa.p4.pt()>7:
                    self.Histos['%s/DsaPt7'%chan].Fill(dsa.p4.pt(), aux['wgt'])
                    if dsa.p4.pt()>10:
                        self.Histos['%s/DsaPt10'%chan].Fill(dsa.p4.pt(), aux['wgt'])

        #lepton jets using new pt
        if len(event.leptonjets) == 2:
            dRlj = DeltaR(event.leptonjets[0].p4, event.leptonjets[1].p4)
            dphilj = abs(DeltaPhi(event.leptonjets[0].p4, event.leptonjets[1].p4))
            
            self.Histos['%s/dRLJ'%chan].Fill(dRlj,aux['wgt'])
            self.Histos['%s/dPhiLJ'%chan].Fill(dphilj,aux['wgt'])
            

        #leading pt
        for p in aux['dp']:
            rho = (p.dauvtx-p.vtx).Rho()
            l3d = (p.dauvtx-p.vtx).R()
            daus = []
            for d in event.gens:
                if abs(d.pid) not in [11, 13]: continue
                if (d.vtx-p.dauvtx).R()<1e-2: daus.append(d)
                if len(daus)==2:
                    dpmass = (daus[0].p4+daus[1].p4).M()
                    dpdR = DeltaR(daus[0].p4, daus[1].p4)
                    self.Histos['{}/dpmass'.format(chan)].Fill(dpmass)
                    self.Histos['{}/dpdR'.format(chan)].Fill(dpdR)
                    
                    if abs(daus[0].pid) == 11:
                        self.Histos['{}/electronpairdr'.format(chan)].Fill(dpdR)
                        if daus[0].p4.pt()>daus[1].p4.pt():
                            self.Histos['{}/leaelpt'.format(chan)].Fill(daus[0].p4.pt())
                        else: 
                            self.Histos['{}/leaelpt'.format(chan)].Fill(daus[1].p4.pt())
                    elif abs(daus[0].pid) == 13:
                        self.Histos['{}/muonpairdr'.format(chan)].Fill(dpdR)
                        if daus[0].p4.pt()>daus[1].p4.pt():
                            self.Histos['{}/leamupt'.format(chan)].Fill(daus[0].p4.pt())
                        else: 
                            self.Histos['{}/leamupt'.format(chan)].Fill(daus[1].p4.pt())
        
        #mass and dphi for the dark photon
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
    {'name': 'DsaPt5',           'binning': (50, 0, 250.0),    'title': 'DSA p_{T} >5;p_{T};counts'},
    {'name': 'DsaPt7',           'binning': (50, 0, 250.0),    'title': 'DSA p_{T} >7;p_{T};counts'},
    {'name': 'DsaPt10',          'binning': (50, 0, 250.0),    'title': 'DSA p_{T} >10;p_{T};counts'},
    #{'name': 'dpmass',           'binning': (500, 0, 6.5),     'title': 'dark photon invariant mass;mass [GeV];counts/0.01GeV'},
    {'name': 'leamupt',          'binning': (100, 0, 500.0),   'title': 'Leading muon; p_{T} [GeV];counts/1GeV'},
    {'name': 'leaelpt',          'binning': (100, 0, 500.0),   'title': 'leading ele;  p_{T} [GeV];counts/1GeV'},
    #{'name': 'dplxy',            'binning': (500, 0, 500),     'title': 'dark photon lxy;Lxy [cm];counts/1cm'},
    #{'name': 'dpl3d',            'binning': (750, 0, 750),     'title': 'dark photon l3d;L3d [cm];counts/1cm'},
    {'name': 'dpmass',           'binning': (750, 0, 7.5),     'title': 'dark photon invariant mass;mass [GeV];counts/0.01GeV'},
    {'name': 'psmass',           'binning': (1500, 0, 1500),   'title': 'DM bound state invariant mass;mass [GeV];counts/1GeV'},
    {'name': 'ndp',              'binning': (5, 0, 5),         'title': 'Number of dark photons;N;counts'},
    {'name': 'nmu',              'binning': (5, 0, 5),         'title': 'Number of muons;N;counts'},
    {'name': 'nel',              'binning': (5, 0, 5),         'title': 'Number of electrons;N;counts'},
    {'name': 'nlep',             'binning': (5, 0, 5),         'title': 'Number of leptons(electrons+muons);N;counts'},
    {'name': 'dpdphi',           'binning': (20, 0, M_PI),     'title': '|#Delta#phi| of dark photon pair;|#Delta#phi|;counts'},
    {'name': 'electronpairdr',   'binning': (50, 0, 1),        'title': '#DeltaR between electron pair;#DeltaR(ee);counts'},
    {'name': 'muonpairdr',       'binning': (50, 0, 1),        'title': '#DeltaR between muon pair;#DeltaR(#mu#mu);counts'},
    {'name': 'mu0pt',            'binning': (1000, 0, 1000),   'title': 'leading #mu p_{T};#mu p_{T} [GeV];counts/1GeV'},
    {'name': 'el0pt',            'binning': (1000, 0, 1000),   'title': 'leading electron p_{T};e p_{T} [GeV];counts/1GeV'},
    {'name': 'dppt',             'binning': (1000, 0, 1000),   'title': 'Z_{d} p_{T};Z_{d} p_{T} [GeV];counts/1GeV'},
    {'name': 'dpdR',             'binning': (50, -1,5),        'title': '#DeltaR between dark photon pair;#DeltaR(Z_{d}Z_{d});counts'},
    {'name': 'dRLJ',             'binning': (50, -1,5),        'title': '#DeltaR between lepton jet pair;#DeltaR(LJ0LJ1);counts'},
    {'name': 'dPhiLJ',           'binning': (50, -5.0,5.0),    'title': '|#Delta#phi| between the lepton jet pair;#Delta#phi(LJ0LJ1);counts'},
]
