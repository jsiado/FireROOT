#!/usr/bin/env python
import math

from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *

class MyEvents(SignalEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e','4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']
        
        gmus = [p for p in event.gens \
            if abs(p.pid)==13 \
                and p.p4.pt()>22 \
                and abs(p.p4.eta())<2.4\
                and p.vtx.Rho()<700]
        if len(gmus) < 2 : return
        if len(gmus) == 2:
            dR12 = DeltaR(gmus[0].p4, gmus[1].p4)
            self.Histos['%s/dR12'%chan].Fill(dR12)
            if getattr(event.hlt, "IsoMu24"):
                self.Histos['%s/iso24'%chan].Fill(dR12)
                if getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha"):
                    self.Histos['%s/Dimu'%chan].Fill(dR12)

        #LJ0, LJ1 = aux['lj0'], aux['lj1']
        #passCosmic = all(map(lambda lj: lj.passCosmicVeto(event), [LJ0, LJ1]))

        #if not passCosmic: return

        #muInLjIdx = []
        #for lj in [LJ0, LJ1]:
         #   if not lj.isMuonType(): continue
          #  for i in lj.pfcand_pfmuonIdx:
           #     muInLjIdx.append(i)
        #print len(muInLjIdx)
       # muInLjIdx = list(set(muInLjIdx))

            # two muons
           # if len(gmus) == 2:
               # self.Histos['%s/mu1pt'%chan].Fill(gmus[0].p4.pt())#tag
               # self.Histos['%s/mu2pt'%chan].Fill(gmus[1].p4.pt())#probe
               # self.Histos['%s/dR12'%chan].Fill(DeltaR(gmus[0].p4, gmus[1].p4))
                
             #   if gmus[0].p4.pt()>24:
                    #print "tag"
            #        self.Histos['%s/tagpt'%chan].Fill(gmus[1].p4.pt())
                    #print gmus[0].p4.pt(),' ',gmus[1].p4.pt()

              #      if gmus[1].p4.pt()>30:
                        #print "probe"
               #         self.Histos['%s/probept'%chan].Fill(gmus[1].p4.pt())
                        #self.Histos['%s/tagpt'%chan].Fill(gmus[0].p4.pt())
                        #print gmus[0].p4.pt(),' ',gmus[1].p4.pt()
                    #else: self.Histos['%s/probept'%chan].Fill(0)


            # two lepton jets
            #if len(gmus) == 4:
             #   for i in range (len(gmus)):
              #      for j in range (len(gmus)-1):
                        #self.Histos['%s/tagpt'%chan].Fill(gmus[i].p4.pt()) #0 tag
                        #if 
                    
histCollection = [
    #{'name': 'dRclose',        'binning': (10, 0, 1.0),        'title': '#Delta R between muons; #Delta R;counts'},
    {'name': 'dR12',        'binning': (50, 0, 1),         'title': '#Delta R between muons; #Delta R;counts'},
    #{'name': 'tagpt',       'binning': (500, 0.0, 50.0),    'title': 'tag p_{T} ;p_{T} [GeV] ;counts'},
    #{'name': 'probept',     'binning': (500, 0.0, 50.0),    'title': 'Probe p_{T} ;p_{T} [GeV] ;counts'},
    {'name': 'iso24',       'binning': (100, 0.0, 5.0),    'title': 'IsoMu24 p_{T} ;p_{T} [GeV] ;counts'},
    {'name': 'Dimu',     'binning': (100, 0.0, 5.0),    'title': 'DoubleL2Mu23NoVtx_2Cha p_{T} ;p_{T} [GeV] ;counts'},
    #{'name': 'mu1pt',       'binning': (500, 0.0, 500.0),    'title': 'muon 1 p_{T} ;p_{T} [GeV] ;counts'},
    #{'name': 'mu2pt',       'binning': (500, 0.0, 500.0),    'title': 'muon 2 p_{T} ;p_{T} [GeV] ;counts'},
]
