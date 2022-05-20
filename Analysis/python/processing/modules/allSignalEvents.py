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

        for i,j in enumerate(gmus):
            self.Histos['{}/MuPt'.format(chan)].Fill(j.p4.pt(),aux['wgt'])
        
        #leptons
        muons = [p for p in event.gens if abs(p.pid)==13]
        electrons = [p for p in event.gens if abs(p.pid)==11]
        self.Histos['{}/nMu'.format(chan)].Fill(len(muons))
        self.Histos['{}/nEle'.format(chan)].Fill(len(electrons))
        self.Histos['{}/nLepton'.format(chan)].Fill(len(muons)+len(electrons))
        
        #pt of dsa
        for i, dsa in enumerate(event.dsamuons):
            if dsa.p4.pt()<5 or abs(dsa.p4.eta())>2.4: continue
            self.Histos['%s/DsaPt'%chan].Fill(dsa.p4.pt(), aux['wgt'])
            if dsa.p4.pt()<50:
                self.Histos['%s/DsaPtzoom2'%chan].Fill(dsa.p4.pt(), aux['wgt'])
        
        #dark photons
        for p in aux['dp']:
            rho = (p.dauvtx-p.vtx).Rho()
            self.Histos['{}/dplxy'.format(chan)].Fill(rho,aux['wgt'])
            
        #lepton jets
        self.Histos['%s/nljet'%chan].Fill(len(event.leptonjets),aux['wgt'])
        if len(event.leptonjets) == 2:
            dRLJ = DeltaR(event.leptonjets[0].p4, event.leptonjets[1].p4)
            dphiLJ = abs(DeltaPhi(event.leptonjets[0].p4, event.leptonjets[1].p4))
            self.Histos['%s/dRLJ'%chan].Fill(dRLJ,aux['wgt'])
            self.Histos['%s/delPhiLJ'%chan].Fill(dphiLJ,aux['wgt'])
        
histCollection = [

    {'name': 'nMu',            'binning': (100, 0.0, 5.0),    'title': 'Number of muons ;N ;counts'},
    {'name': 'nEle',            'binning': (100, 0.0, 5.0),    'title': 'Number of electrons ;N ;counts'},
    {'name': 'nLepton',            'binning': (100, 0.0, 8.0),    'title': 'Number of leptons ;N ;counts'},
    {'name': 'DsaPt',            'binning': (100, 0.0, 500.0),    'title': 'DSA #mu p_{T}  ;p_{T} ;counts'},
    {'name': 'DsaPtzoom2',       'binning': (100, 0.0, 80.0),    'title': 'DSA #mu p_{T} zoom ;p_{T} ;counts'},
    {'name': 'nljet',            'binning': (100, 0.0, 3.0),    'title': 'Number of Lepton jets ;N ;counts'},
    {'name': 'dRLJ',            'binning': (100, 0.0, 5.5),    'title': '#Delta R between lepton jets ;#Delta R ;counts'},
    {'name': 'delPhiLJ',         'binning': (100, 0.0, 3.5),    'title': '#Delta #phi between lepton jets ;#Delta #phi ;counts'},
    {'name': 'dplxy',        'binning': (100, 0, 500),        'title': 'darkphoton lxy;Lxy [cm];counts/1cm'},
    {'name': 'MuPt',        'binning': (100, 0, 500.0),        'title': 'all Muons;p_{T} [GeV]; counts'    },

                 ]
