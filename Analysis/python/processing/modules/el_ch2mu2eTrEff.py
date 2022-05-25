#!/usr/bin/env python
# RM: reco muon
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
                
        #Reco_Mu = [remu for i, remu in enumerate(event.ljsources)]
        #Reco_Mu = [remu for i, remu in enumerate(event.dsamuons)]
        Reco_Mu = [remu for i, remu in enumerate(event.muons)]
        matched_Reco = []
        dR_thr = 0.3
        RMix, TOix = [], []
        
        if len(Reco_Mu)>2:
            TriObj = [TO for TO in event.trigobjs]  # trigger objects in the event
            #print len(TriObj)
            for y in range(len(TriObj)):
                for z in range (y+1,len(TriObj)):
                    TOdR = DeltaR(TriObj[y].p4,TriObj[z].p4)
                    self.Histos['%s/TOdRall' % chan].Fill(TOdR)
                    if TOdR < 0.3:
                        self.Histos['%s/TOdR0p3' % chan].Fill(TOdR)
                #print y,TriObj[y].p4.pt(),y,y+1,DeltaR(TriObj[y].p4,TriObj[y+1].p4)
                #if y == (len(TriObj)-2):break
            #for i, j in enumerate (TriObj):
                #for m,n in enumerate (TriObj):
                    #print 'triobj',len(TriObj),i,m, DeltaR(j.p4,n.p4)
            #self.Histos['%s/TO_n' % chan].Fill(len(TriObj))

            for x, TO in enumerate(TriObj):
                self.Histos['%s/TO_bit' % chan].Fill(TO.bit)
                self.Histos['%s/TO_pT' % chan].Fill(TO.p4.pt())
                
                if TO.bit != 0 and (abs(TO.bit) & (1<<0) > 0 or abs(TO.bit) & (1<<1) > 0 or abs(TO.bit) & (1<<2) > 0 or abs(TO.bit) & (1<<3) > 0 or abs(TO.bit) & (1<<4) > 0 or abs(TO.bit)& (1<<5) > 0 or abs(TO.bit) & (1<<6) > 0 or abs(TO.bit) & (1<<7) > 0 or abs(TO.bit) & (1<<8) > 0 or abs(TO.bit) & (1<<9) > 0):     
                    
                    min_dR = 999
                    RMi = -1
                    #print '----------------------------',len(Reco_Mu), len(TriObj)
                    for i, j in enumerate(Reco_Mu):
                        dR_TO = DeltaR(TO.p4,j.p4)
                        #print i, x, dR_TO
                        if dR_TO > min_dR: continue
                        if dR_TO < min_dR:
                            #print len(Reco_Mu), len(TriObj),x, i, dR_TO
                            min_dR = dR_TO
                            RMi = i #muon index
                    if min_dR < dR_thr and i not in RMix:
                        #print 'muon index',i
                        RMix.append(i)
                        matched_Reco.append(RMi)
                        #print i, x, min_dR, len(matched_Reco)
            #print 'len',len(matched_Reco)
                        #self.Histos['%s/min_dR_RMTO' % chan].Fill(min_dR)
                #self.Histos['%s/RMTO_match' % chan].Fill(len(matched_Reco))
            
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
                            #mulxy = RM1.p4.d0()
                            mud0 = RM1.d0
                        else:
                            mupt = RM2.p4.pt()
                            re_mu1 = i2
                            mueta = RM2.p4.pt()
                            re_mu2 = i1
                            #mulxy = RM2.p4.d0
                            mud0 = RM2.d0
                    if mupt!= 0: self.Histos['%s/RM_pT'%chan].Fill(mupt)
                self.Histos['%s/RM_dR'  %chan].Fill(min_dR)
                
                if min_dR<dR_thr:
                    self.Histos['%s/TO_Den_dR'  %chan].Fill(min_dR)
                    self.Histos['%s/TO_Den_pT'  %chan].Fill(mupt)
                    self.Histos['%s/TO_Den_eta' %chan].Fill(mueta)
                    #self.Histos['%s/TO_Den_lxy' %chan].Fill(mulxy)
                    self.Histos['%s/TO_Den_d0' %chan].Fill(mud0)
                    #numerator
                    if (re_mu1 in matched_Reco and re_mu2 in matched_Reco):
                        self.Histos['%s/TO_Num_dR' % chan].Fill(min_dR)
                        self.Histos['%s/TO_Num_pT' % chan].Fill(mupt)
                        self.Histos['%s/TO_Num_eta' % chan].Fill(mueta)
                        #self.Histos['%s/TO_Num_lxy' % chan].Fill(mulxy)
                        self.Histos['%s/TO_Num_d0' %chan].Fill(mud0)


histCollection = [
    {  'name': 'TOdRall',      'binning' : (100, 0.0,5.0),                   'title': '#Delta R of all trigger objects; #Delta R; Number of entries'},
    {  'name': 'TOdR0p3',      'binning' : (100, 0.0,0.5),                   'title': '#Delta R of trigger objects w/in 0.3; #Delta R; Number of entries'},
    
    {  'name': 'RM_dR',
       'binning' : [[0,0.02,0.04,0.06,0.08,0.1,0.15,0.2,.3,.4,]],
       'title': '#Delta R of Reco muons; #Delta R; Number of entries'},

    {  'name': 'RM_pT',          'binning' : (100, 0.0,500),                   'title': 'Reco muon p_{T} distribution; p_{T} [GeV]; Number of entries'},
    {  'name': 'RM_n',           'binning' : (20, 0.0,20),                     'title': 'Number of Reco #mu ; #mu ; Number of entries'},
    {  'name': 'TO_n',           'binning' : (30, 0.0,30),                     'title': 'Number of trigger objects; #mu ; Number of entries'},
    {  'name': 'TO_bit',         'binning' : (100, -50.0,50),                  'title': 'Trigger object ID ; TO ID; Number of entries'},
    {  'name': 'TO_pT',          'binning' : (50, 0.0,500),                    'title': 'TO p_{T} distribution;  p_{T} [GeV]; Number of entries'},
    {  'name': 'RMTO_match',     'binning' : (50, 0.0,50),                     'title': '# of muon matched to a TO; # of muons; Number of entries'},
    
    {  'name': 'min_dR_RMTO',  
       'binning' : [[0,0.1,0.2,0.3,0.4]],  
       'title': '# of muon matched to a TO; # of muons; Number of entries'},
    
    {  'name': 'TO_Num_dR',
       'binning' : (50, 0.0, 0.5),
  #     'binning' : [[0,0.005,0.01,0.015,0.02,0.03,0.04,0.06,0.08,0.11,0.14,0.17,0.2,0.25,0.4]],
       'title' : 'Leading #mu; #Delta R; Number of entries'},
    
    {  'name': 'TO_Den_dR',
       'binning' : (50, 0.0, 0.5),
       #'binning' : [[0,0.005,0.01,0.015,0.02,0.03,0.04,0.06,0.08,0.11,0.14,0.17,0.2,0.25,0.4]],
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
       'binning' : [[0,0.5,1.0,1.5,2.0,3,4,5,6,7,8,9,10,15,20]],
   #    'binning' : [[0,2,4,6,8,10,12,14,20,50]],
    #   'binning' : (10,0,5),
       'title': 'Leading #mu d_{0}; d_{0}; Number of entries'
   },
    
    {  'name': 'TO_Den_d0',
       'binning' : [[0,0.5,1.0,1.5,2.0,3,4,5,6,7,8,9,10,15,20]],
    #   'binning' : [[0,2,4,6,8,10,12,14,20,50]],
       #'binning' : (10,0,5),
       'title': 'Leading #mu d_{0}; d_{0}; Number of entries'
   },
]
