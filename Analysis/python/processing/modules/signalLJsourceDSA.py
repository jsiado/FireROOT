#!/usr/bin/env python
import math
from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *

class MyEvents(SignalEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)
        nLJcero = 0
    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']

        gmus = [p for p in event.gens \
            if abs(p.pid)==13 \
                and p.p4.pt()>5\
                and abs(p.p4.eta())<2.4\
                and p.vtx.Rho()<700]
        if len(gmus)<2: return

        ########################
        self.Histos['%s/ngenmu'%chan].Fill(len(gmus),aux['wgt'])#js
        self.Histos['%s/nljet'%chan].Fill(len(event.leptonjets),aux['wgt'])# hist with # of LJ
    
        if len(event.leptonjets)>2:
            dR12 = DeltaR(event.leptonjets[0].p4, event.leptonjets[1].p4)
            self.Histos['%s/dRLJ12'%chan].Fill(dR12,aux['wgt'])
            
            dR13 = DeltaR(event.leptonjets[0].p4, event.leptonjets[2].p4)
            self.Histos['%s/dRLJ13'%chan].Fill(dR13,aux['wgt'])

            dR23 = DeltaR(event.leptonjets[1].p4, event.leptonjets[2].p4)
            self.Histos['%s/dRLJ23'%chan].Fill(dR23,aux['wgt'])


            dphi12 = abs(DeltaPhi(event.leptonjets[0].p4, event.leptonjets[1].p4))
            self.Histos['%s/delphi12'%chan].Fill(dphi12,aux['wgt'])
            
            dphi13 = abs(DeltaPhi(event.leptonjets[0].p4, event.leptonjets[2].p4))
            self.Histos['%s/delphi13'%chan].Fill(dphi13,aux['wgt'])

            dphi23 = abs(DeltaPhi(event.leptonjets[1].p4, event.leptonjets[2].p4))
            self.Histos['%s/delphi23'%chan].Fill(dphi23,aux['wgt'])
            

            for p in aux['dp']:
                zdlj2 = DeltaR(p.p4, event.leptonjets[2].p4)
                self.Histos['%s/zdljdR'%chan].Fill(zdlj2,aux['wgt'])
                if zdlj2<0.4:
                    self.Histos['%s/matchLJ'%chan].Fill(-1,aux['wgt'])
                else:
                    self.Histos['%s/matchLJ'%chan].Fill(1,aux['wgt'])
        
        dsaToGenmuMap = {}
        for i, dsa in enumerate(event.ljsources):
            if dsa.type!=8: continue
            pairs = [(g, DeltaR(gmu.p4, dsa.p4)) for g, gmu in enumerate(gmus)]
            pairs.sort(key=lambda x: x[1])
            if pairs and pairs[0][1]<0.3:
                dsaToGenmuMap[i] = pairs[0][0]

        for i, j in dsaToGenmuMap.items():
            dsa, genmu = event.ljsources[i], gmus[j]
            metric = (dsa.p4.pt()-genmu.p4.pt())/genmu.p4.pt()
            self.Histos['{}/ljsrcdsa'.format(chan)].Fill(metric, aux['wgt'])
            if dsa.charge==genmu.charge:
                self.Histos['{}/ljsrcdsasameq'.format(chan)].Fill(metric, aux['wgt'])

        self.Histos['%s/pfmet'%chan].Fill(event.pfMet.r(), aux['wgt'])

histCollection = [
    {
        'name': 'ljsrcdsa',
        'binning': (50, -1, 1),
        'title': 'DSA in lepton-jet source;(p_{T}^{reco}-p_{T}^{gen})/p_{T}^{gen};norm. counts/0.04'
    },
    {
        'name': 'ljsrcdsasameq',
        'binning': (50, -1, 1),
        'title': 'DSA in lepton-jet source;(p_{T}^{reco}-p_{T}^{gen})/p_{T}^{gen};norm. counts/0.04'
    },
    {
        'name': 'pfmet',
        'binning': (50, 0, 500),
        'title': 'PF MET;MET [GEV];counts/10'
    },

    {'name': 'ngenmu', 'binning':(50,0,110), 'title': 'number of gen muons'},

    {'name': 'nljet', 'binning':(50,0,10), 'title': 'number of lepton jets'},
    {'name': 'zdljdR', 'binning':(50,-5,5), 'title': '#DeltaR zdlj3'},
    {'name': 'matchLJ', 'binning':(50,-3,3), 'title': 'matching LJ3'},

    {'name': 'dRLJ12', 'binning':(50,-10,10), 'title': '#DeltaR LJ12'},
    {'name': 'dRLJ13', 'binning':(50,-10,10), 'title': '#DeltaR LJ13'},
    {'name': 'dRLJ23', 'binning':(50,-10,10), 'title': '#DeltaR LJ23'},
    
    {'name': 'delphi12', 'binning':(50,-5.0,5.0), 'title': '#Delta #phi LJ12'},
    {'name': 'delphi13', 'binning':(50,-5.0,5.0), 'title': '#Delta #phi LJ13'},
    {'name': 'delphi23', 'binning':(50,-5.0,5.0), 'title': '#Delta #phi LJ23'},
]
