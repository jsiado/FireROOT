#!/usr/bin/env python
# RM: reco muon, TO:trigger object

import math
import numpy as np

from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *

class MyEvents(SignalEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']
        
        gen_mus = [p for p in event.gens \
            if abs(p.pid)==13 \
                and p.p4.pt()>10\
                and abs(p.p4.eta())<2.4\
                and p.vtx.Rho()<700]
        #for i, gen in enumerate(gen_mus):
            #self.Histos['%s/geM_pT' % chan].Fill(gen.p4.pt())
            
        # RM: reco muon, TO: trigger object             
        matched_Reco = []

        Reco_Mu = [remu for i, remu in enumerate(event.ljsources)]# if abs(remu.pid)==13]                                                                                 
        #self.Histos['%s/RM_n' % chan].Fill(len(Reco_Mu))
        dR_thr = 0.3
                    
        if len(Reco_Mu)>2:

            TriObj = [TO for TO in event.trigobjs]  # trigger objects in the event
            #self.Histos['%s/TO_n' % chan].Fill(len(TriObj))
            
            for TO in TriObj:
                self.Histos['%s/TO_bit' % chan].Fill(TO.bit)
                #print TO.bit
                self.Histos['%s/TO_pT' % chan].Fill(TO.p4.pt())
                
                '''if TO.pid == 0: continue
                if TO.pid != 0 and (abs(TO.pid) & (1<<0) > 0 or abs(TO.pid) & (1<<1) > 0 or abs(TO.pid) & (1<<2) > 0 or abs(TO.pid) & (1<<3) > 0):
                    
                    min_dR = 999
                    RMi = -1
                    for i, j in enumerate(Reco_Mu):
                        dR_TO = DeltaR(TO.p4,j.p4)
                        if dR_TO > min_dR: continue
                        if dR_TO < min_dR:
                            min_dR = dR_TO
                            RMi = i #muon index
                            if min_dR < dR_thr:
                                matched_Reco.append(RMi)
            
            #loop 1 reco muons 
            for i1, RM1 in enumerate (Reco_Mu):
                if RM1.p4.pt()<30:continue
                if abs(RM1.p4.eta())>2.4: continue
                
                min_dR = 999
                mupt = 0
                mueta = 0
                mulxy = 0
                
                #loop 2 reco muons
                for i2, RM2 in enumerate(Reco_Mu):
                    if RM2.p4.pt()<30: continue
                    if abs(RM2.p4.eta())>2.4: continue
                    if i2 == i1: continue
                    if DeltaR(RM1.p4, RM2.p4) < min_dR:
                        min_dR = DeltaR(RM1.p4, RM2.p4)
                        
                        if RM1.p4.pt()>RM2.p4.pt(): 
                            re_mu1 = i1
                            mupt = RM1.p4.pt()
                            mueta = RM1.p4.eta()
                            re_mu2 = i2
                            mulxy = RM1.p4.Rho()
                        else:
                            mupt = RM2.p4.pt()
                            re_mu1 = i2
                            mueta = RM2.p4.pt()
                            re_mu2 = i1
                            mulxy = RM2.p4.Rho()
                    if mupt!= 0: self.Histos['%s/RM_pT'%chan].Fill(mupt)
                self.Histos['%s/RM_dR'  %chan].Fill(min_dR)
                
                if min_dR<dR_thr:
                    self.Histos['%s/TO_Den_dR'  %chan].Fill(min_dR)
                    self.Histos['%s/TO_Den_pT'  %chan].Fill(mupt) 
                    self.Histos['%s/TO_Den_eta' %chan].Fill(mueta)
                    self.Histos['%s/TO_Den_lxy' %chan].Fill(mulxy)
                    if (re_mu1 in matched_Reco and re_mu2 in matched_Reco):
                        self.Histos['%s/TO_Num_dR' % chan].Fill(min_dR)
                        self.Histos['%s/TO_Num_pT' % chan].Fill(mupt)
                        self.Histos['%s/TO_Num_eta' % chan].Fill(mueta)
                        self.Histos['%s/TO_Num_lxy' % chan].Fill(mulxy)'''
                        

histCollection = [
    #{  'name': 'geM_pT',      'binning' : (100, 0.0,500),                   'title': 'Gen muons p_{T}; p_{T} [GeV]; Number of entries'},
    #{  'name': 'RM_dR',
     #  'binning' : [[0,0.02, 0.04,0.06, 0.08, 0.1,0.15,0.2,.3,.4,]+list(np.arange(.08,.02,.01))],
      # 'title': '#Delta R of Reco muons; #Delta R; Number of entries'},

    #{  'name': 'RM_pT',     'binning' : (100, 0.0,500),                   'title': 'Reco muon p_{T} distribution; p_{T} [GeV]; Number of entries'},
    #{  'name': 'RM_n',     'binning' : (20, 0.0,20),                   'title': 'Number of Reco #mu ; #mu ; Number of entries'},
    {  'name': 'TO_n',     'binning' : (30, 0.0,30),                   'title': 'Number of trigger objects; #mu ; Number of entries'},
    {  'name': 'TO_bit',     'binning' : (100, -50.0,5000),                   'title': 'Trigger object ID ; TO ID; Number of entries'},
    {  'name': 'TO_pT',     'binning' : (50, 0.0,500),                   'title': 'TO p_{T} distribution;  p_{T} [GeV]; Number of entries'},

    #{  'name': 'TO_Num_dR',     
     #  'binning' : [[0,0.02, 0.04,0.06, 0.08, 0.1,0.15,0.2,.3,.4,]+list(np.arange(.08,.02,.01))],
      # 'title' : 'Leading #mu; #Delta R; Number of entries'},
    
    #{  'name': 'TO_Den_dR',     
     #  'binning' : [[0,0.02, 0.04,0.06, 0.08, 0.1,0.15,0.2,.3,.4,]+list(np.arange(.08,.02,.01))],
      # 'title': 'Leading #mu; #Delta R; Number of entries'},

    #{  'name': 'TO_Num_pT',     
     #  'binning' :  [[0, 5, 10, 15, 20, 25, 30, 35, 40, 50,70, 100, 150, 200, 250, 300, 400, 500,]+list(np.arange(1,.100,1))],
      # 'title' : 'Leading #mu p_{T}; p_{T} [GeV]; Number of entries'},

    #{  'name': 'TO_Den_pT',     
     #  'binning' :  [[0, 5, 10, 15, 20, 25, 30, 35, 40, 50, 70, 100, 150, 200, 250, 300, 400, 500]+list(np.arange(.08,.02,.01))],  
      # 'title' : 'Leading #mu p_{T}; p_{T} [GeV]; Number of entries'},

    #{  'name': 'TO_Num_eta',     'binning' : (30,  -3.0, 3.0),                    'title': 'Leading #mu #eta; #eta; Number of entries'},
    #{  'name': 'TO_Den_eta',     'binning' : (30,  -3.0, 3.0),                    'title': 'Leading #mu #eta; #eta; Number of entries'},

    #{  'name': 'TO_Num_lxy',
    #   'binning' : [[0, 5, 10, 15, 20, 25, 30, 35, 40, 50,70, 100, 150, 200, 250, 300, 400, 500, 600, 700,]+list(np.arange(1,.100,1))],
     #  'title': 'Leading #mu displacement; l_{xy}; Number of entries'},
    #{  'name': 'TO_Den_lxy',  
     #  'binning' : [[0, 5, 10, 15, 20, 25, 30, 35, 40, 50,70, 100, 150, 200, 250, 300, 400, 500, 600, 700,]+list(np.arange(1,.100,1))],
      # 'title': 'Leading #mu displacement; l_{xy}; Number of entries'},
]


