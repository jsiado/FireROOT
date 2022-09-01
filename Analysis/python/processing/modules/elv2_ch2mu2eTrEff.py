#!/usr/bin/env python
# RM: reco muon, 
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

        #include new collections of muons
        dR_thr = 0.3

        pf, dsa, Reco_Mu = ([] for i in range (3))
        for lj in [LJ0, LJ1]:
            if not lj.isMuonType():continue
            for i in lj.pfcand_pfmuonIdx:
                pf.append(event.muons[i])
            for i in lj.pfcand_dsamuonIdx:
                dsa.append(event.dsamuons[i])

        lpf, ldsa = len(pf),len(dsa)

        #lpf, ldsa = len(pf), len(dsa)
        if lpf ==1:
            Reco_Mu.append(pf[0])
            Reco_Mu.append(dsa[0])
        elif lpf == 2:
            Reco_Mu.append(pf[0])
            Reco_Mu.append(pf[1])
        elif lpf == 0:
            Reco_Mu.append(dsa[0])
            Reco_Mu.append(dsa[1])

        Reco_Mu2 = Reco_Mu[:]

        if len(Reco_Mu)==2:
            for ii in Reco_Mu:
                self.Histos['%s/ReMu_d0' % chan].Fill(ii.d0)
                #print ii.d0
            TriObj = [TO for TO in event.trigobjs]  # trigger objects in the event
            for y in range(len(TriObj)):
                for z in range (y+1,len(TriObj)):
                    TOdR = DeltaR(TriObj[y].p4,TriObj[z].p4)
                    self.Histos['%s/TOdRall' % chan].Fill(TOdR)
                    if TOdR < 0.3:    self.Histos['%s/TOdR0p3' % chan].Fill(TOdR)
            matched_Reco = []
            for x, TO in enumerate(TriObj):
                self.Histos['%s/TO_bit' % chan].Fill(TO.bit)
                #self.Histos['%s/TO_pT' % chan].Fill(TO.p4.pt())

                #print TO.bit, abs(TO.bit), #Type(TO)
                #muon match to a trigger objects cjhange and to &
                if TO.bit != 0 and (
                        abs(TO.bit) & (1<<0) > 0
                        or abs(TO.bit) & (1<<1) > 0 or abs(TO.bit) & (1<<2) > 0 or abs(TO.bit) & (1<<3) > 0 or abs(TO.bit) & (1<<4) > 0 or abs(TO.bit) & (1<<5) > 0
                        or abs(TO.bit) & (1<<6) > 0 or abs(TO.bit) & (1<<7) > 0 or abs(TO.bit) & (1<<8) > 0 or abs(TO.bit) & (1<<9) > 0 or abs(TO.bit) & (1<<10) > 0
                        or abs(TO.bit) & (1<<11) > 0 or abs(TO.bit) & (1<<12) > 0 or abs(TO.bit) & (1<<13) > 0 or abs(TO.bit) & (1<<14) > 0 or abs(TO.bit) & (1<<15) > 0
                        or abs(TO.bit) & (1<<16) > 0 or abs(TO.bit) & (1<<17) > 0 or abs(TO.bit) & (1<<18) > 0 or abs(TO.bit) & (1<<19) > 0 or abs(TO.bit) & (1<<20) > 0
                        or abs(TO.bit) & (1<<21) > 0 or abs(TO.bit) & (1<<22) > 0 or abs(TO.bit) & (1<<23) > 0):   
                    
                    min_dR, RMi = 999, -1
                    for i, j in enumerate(Reco_Mu):
                        dR_TO = DeltaR(TO.p4,j.p4)
                        if dR_TO > min_dR: continue
                        if dR_TO < min_dR:
                            min_dR = dR_TO
                            RMi = i #muon index
                    if min_dR < dR_thr and RMi not in matched_Reco:
                        matched_Reco.append(RMi)
                        Reco_Mu.pop(RMi)
                        #self.Histos['%s/min_dR_RMTO' % chan].Fill(min_dR)
                #self.Histos['%s/RMTO_match' % chan].Fill(len(matched_Reco))

            #loop 1 reco muons 
            for i1, RM1 in enumerate (Reco_Mu2):
                if RM1.p4.pt()<30:continue
                if abs(RM1.p4.eta())>2.4: continue

                #2nd loop over reco muons 
                min_dR, mupt, mueta, mulxy = 999, 0, 0, 0
                for i2 in range (i1+1,len(Reco_Mu2)):
                    if Reco_Mu2[i2].p4.pt()<30: continue
                    if abs(Reco_Mu2[i2].p4.eta())>2.4: continue
                    #if i2 == i1: continue
                    if DeltaR(RM1.p4, Reco_Mu2[i2].p4) < min_dR:
                        min_dR = DeltaR(RM1.p4, Reco_Mu2[i2].p4)

                        if RM1.p4.pt()>Reco_Mu2[i2].p4.pt(): 
                            re_mu1 = i1
                            mupt = RM1.p4.pt()
                            mueta = RM1.p4.eta()
                            re_mu2 = i2
                            mud0 = RM1.d0
                        else:
                            mupt = Reco_Mu2[i2].p4.pt()
                            re_mu1 = i2
                            mueta = Reco_Mu2[i2].p4.pt()
                            re_mu2 = i1
                            mud0 = Reco_Mu2[i2].d0
                    #if mupt!= 0: self.Histos['%s/RM_pT'%chan].Fill(mupt)
                #self.Histos['%s/RM_dR'  %chan].Fill(min_dR)

                if min_dR<dR_thr:
                    self.Histos['%s/TO_Den_dR'  %chan].Fill(min_dR)
                    self.Histos['%s/TO_Den_pT'  %chan].Fill(mupt)
                    self.Histos['%s/TO_Den_eta' %chan].Fill(mueta)
                    self.Histos['%s/TO_Den_d0' %chan].Fill(mud0)
                    #numerator
                    if (re_mu1 in matched_Reco and re_mu2 in matched_Reco):
                        self.Histos['%s/TO_Num_dR' % chan].Fill(min_dR)
                        self.Histos['%s/TO_Num_pT' % chan].Fill(mupt)
                        self.Histos['%s/TO_Num_eta' % chan].Fill(mueta)
                        self.Histos['%s/TO_Num_d0' %chan].Fill(mud0)

histCollection = [
    {  'name': 'TOdRall',      'binning' : (100, 0.0,5.0),                   'title': '#Delta R of all trigger objects; #Delta R; Number of entries'},
    {  'name': 'TOdR0p3',      'binning' : (100, 0.0,0.5),                   'title': '#Delta R of trigger objects w/in 0.3; #Delta R; Number of entries'},
    
    #{  'name': 'RM_dR',
     #  'binning' : [[0,0.02,0.04,0.06,0.08,0.1,0.15,0.2,.3,.4,]],
      # 'title': '#Delta R of Reco muons; #Delta R; Number of entries'},

    #{  'name': 'RM_pT',          'binning' : (100, 0.0,500),                   'title': 'Reco muon p_{T} distribution; p_{T} [GeV]; Number of entries'},
    #{  'name': 'RM_n',           'binning' : (20, 0.0,20),                     'title': 'Number of Reco #mu ; #mu ; Number of entries'},
    #{  'name': 'TO_n',           'binning' : (30, 0.0,30),                     'title': 'Number of trigger objects; #mu ; Number of entries'},
    {  'name': 'TO_bit',         'binning' : (100, -50.0,50),                  'title': 'Trigger object ID ; TO ID; Number of entries'},
    #{  'name': 'TO_pT',          'binning' : (50, 0.0,500),                    'title': 'TO p_{T} distribution;  p_{T} [GeV]; Number of entries'},
    #{  'name': 'RMTO_match',     'binning' : (50, 0.0,50),                     'title': '# of muon matched to a TO; # of muons; Number of entries'},
    
    #{  'name': 'min_dR_RMTO',  
     #  'binning' : [[0,0.1,0.2,0.3,0.4]],  
      # 'title': '# of muon matched to a TO; # of muons; Number of entries'},

    {  'name': 'ReMu_d0',
       'binning' : [[0,0.001,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.12,0.14,0.16,0.18,0.2,0.25,0.3,0.4,2,5,10,20,50,200,1000]],
       'title' : 'd0 for all reco muons; d_0; Number of entries'
   },    
    {  'name': 'TO_Num_dR',
       #'binning' : (20, 0.0, 0.5),
       'binning' : [[0,0.001,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.12,0.14,0.16,0.18,0.2,0.25,0.3,0.4]],
       'title' : 'Leading #mu; #Delta R; Number of entries'},
    
    {  'name': 'TO_Den_dR',
       #'binning' : (20, 0.0, 0.5),
       'binning' : [[0,0.001,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.12,0.14,0.16,0.18,0.2,0.25,0.3,0.4]],
       'title': 'Leading #mu; #Delta R; Number of entries'},

    {  'name': 'TO_Num_pT',     
       'binning' :  [[0,2,4,6,8,10,15,20,30,40,60,80,100,150,200,250,300,350,400,450,500,600]],
       'title' : 'Leading #mu p_{T}; p_{T} [GeV]; Number of entries'},

    {  'name': 'TO_Den_pT',     
       'binning' :  [[0,2,4,6,8,10,15,20,30,40,60,80,100,150,200,250,300,350,400,450,500,600]],  
       'title' : 'Leading #mu p_{T}; p_{T} [GeV]; Number of entries'},

    {  'name': 'TO_Num_eta',
       'binning' : (30,-3.5,3.5),#[[-3.5,-3.0,-2.6,-2.2,-1.8,-1.4,-1.0,-0.6,0.2,0.6,1.0,1.4,1.8,2.2,2.6,3.0,3.5]],
       'title': 'Leading #mu #eta; #eta; Number of entries'
   },
    
    {  'name': 'TO_Den_eta', 
       'binning' : (30,-3.5,3.5),#[[-3.5,-3.0,-2.6,-2.2,-1.8,-1.4,-1.0,-0.6,0.2,0.6,1.0,1.4,1.8,2.2,2.6,3.0,3.5]],
       'title': 'Leading #mu #eta; #eta; Number of entries'
   },

    {  'name': 'TO_Num_d0',
       'binning' : [[0,0.5,1.0,1.5,2.0,3,4,5,6,7,8,9,10,15]],#dsa
       #'binning' : [[0,0.1,0.2,0.3,0.4,0.6,0.8,1,1.3,1.6,1.9,3,4,5]],#pf
    #   'binning' : (10,0,5),
       'title': 'Leading #mu d_{0}; d_{0}; Number of entries'
   },
    
    {  'name': 'TO_Den_d0',
       'binning' : [[0,0.5,1.0,1.5,2.0,3,4,5,6,7,8,9,10,15]],#dsa
       #'binning' : [[0,0.1,0.2,0.3,0.4,0.6,0.8,1,1.3,1.6,1.9,3,4,5]],#pf
       #'binning' : (10,0,5),
       'title': 'Leading #mu d_{0}; d_{0}; Number of entries'
   },
]
