#!/usr/bin/env python
import math
from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *


class MyEvents(SignalEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu']):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel)

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']

        gmus = [p for p in event.gens \
            if abs(p.pid)==13 \
                and p.p4.pt()>10\
                and abs(p.p4.eta())<2.4\
                and p.vtx.Rho()<700]
        if len(gmus)<2: return
        dsaToGenmuMap = {}
        for i, dsa in enumerate(event.dsamuons):
            if dsa.p4.pt()<10 or abs(dsa.p4.eta())>2.4: continue
            pairs = [(g, DeltaR(gmu.p4, dsa.p4)) for g, gmu in enumerate(gmus)]
            pairs.sort(key=lambda x: x[1])
            if pairs and pairs[0][1]<0.3:
                dsaToGenmuMap[i] = pairs[0][0]

        for i, j in dsaToGenmuMap.items():
            dsa, genmu = event.dsamuons[i], gmus[j]
            if dsa.charge!=genmu.charge: continue
            metric = (dsa.p4.pt()-genmu.p4.pt())/genmu.p4.pt()
            # reco cuts
            if (dsa.CSCStations+dsa.DTStations)>=2:
                self.Histos['{}/nstas'.format(chan)].Fill(metric, aux['wgt'])
            else:
                self.Histos['{}/nstasInv'.format(chan)].Fill(metric, aux['wgt'])

            if (dsa.DTHits+dsa.CSCHits)>=12:
                self.Histos['{}/nhits'.format(chan)].Fill(metric, aux['wgt'])
            else:
                self.Histos['{}/nhitsInv'.format(chan)].Fill(metric, aux['wgt'])

            if dsa.ptErrorOverPt<1:
                self.Histos['{}/pterr'.format(chan)].Fill(metric, aux['wgt'])
            else:
                self.Histos['{}/pterrInv'.format(chan)].Fill(metric, aux['wgt'])

            if dsa.normChi2<4:
                self.Histos['{}/normchi2'.format(chan)].Fill(metric, aux['wgt'])
            else:
                self.Histos['{}/normchi2Inv'.format(chan)].Fill(metric, aux['wgt'])

            if dsa.CSCHits==0:
                if dsa.DTHits>18:
                    self.Histos['{}/dthits'.format(chan)].Fill(metric, aux['wgt'])
                else:
                    self.Histos['{}/dthitsInv'.format(chan)].Fill(metric, aux['wgt'])

            # inclusive:
            if (dsa.CSCStations+dsa.DTStations)>=2 \
                and (dsa.DTHits+dsa.CSCHits)>=12 \
                and dsa.ptErrorOverPt<1 \
                and dsa.normChi2<4 \
                and (dsa.CSCHits>0 or dsa.DTHits>18):
                self.Histos['{}/inc'.format(chan)].Fill(metric, aux['wgt'])
            else:
                self.Histos['{}/incInv'.format(chan)].Fill(metric, aux['wgt'])



histCollection = [
    {
        'name': 'nstas',
        'binning': (50, -1, 1),
        'title': 'N(DT+CSC) stations;(p_{T}^{reco}-p_{T}^{gen})/p_{T}^{gen};norm. counts/0.04'
    },
    {
        'name': 'nstasInv',
        'binning': (50, -1, 1),
        'title': 'N(DT+CSC) stations;(p_{T}^{reco}-p_{T}^{gen})/p_{T}^{gen};norm. counts/0.04'
    },

    {
        'name': 'nhits',
        'binning': (50, -1, 1),
        'title': 'N(DT+CSC) hits;(p_{T}^{reco}-p_{T}^{gen})/p_{T}^{gen};norm. counts/0.04'
    },
    {
        'name': 'nhitsInv',
        'binning': (50, -1, 1),
        'title': 'N(DT+CSC) hits;(p_{T}^{reco}-p_{T}^{gen})/p_{T}^{gen};norm. counts/0.04'
    },

    {
        'name': 'pterr',
        'binning': (50, -1, 1),
        'title': '#sigma_{p_{T}}/p_{T};(p_{T}^{reco}-p_{T}^{gen})/p_{T}^{gen};norm. counts/0.04'
    },
    {
        'name': 'pterrInv',
        'binning': (50, -1, 1),
        'title': '#sigma_{p_{T}}/p_{T};(p_{T}^{reco}-p_{T}^{gen})/p_{T}^{gen};norm. counts/0.04'
    },

    {
        'name': 'normchi2',
        'binning': (50, -1, 1),
        'title': '#chi^{2}/ndof;(p_{T}^{reco}-p_{T}^{gen})/p_{T}^{gen};norm. counts/0.04'
    },
    {
        'name': 'normchi2Inv',
        'binning': (50, -1, 1),
        'title': '#chi^{2}/ndof;(p_{T}^{reco}-p_{T}^{gen})/p_{T}^{gen};norm. counts/0.04'
    },

    {
        'name': 'dthits',
        'binning': (50, -1, 1),
        'title': 'N(DT) hits;(p_{T}^{reco}-p_{T}^{gen})/p_{T}^{gen};norm. counts/0.04'
    },
    {
        'name': 'dthitsInv',
        'binning': (50, -1, 1),
        'title': 'N(DT) hits;(p_{T}^{reco}-p_{T}^{gen})/p_{T}^{gen};norm. counts/0.04'
    },

    {
        'name': 'inc',
        'binning': (50, -1, 1),
        'title': 'inclusive cuts;(p_{T}^{reco}-p_{T}^{gen})/p_{T}^{gen};norm. counts/0.04'
    },
    {
        'name': 'incInv',
        'binning': (50, -1, 1),
        'title': 'inclusive cuts;(p_{T}^{reco}-p_{T}^{gen})/p_{T}^{gen};norm. counts/0.04'
    },
]