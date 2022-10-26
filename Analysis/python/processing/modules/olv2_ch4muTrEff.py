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
        dR_thr = 0.2

        self.Histos['%s/ljmass' % chan].Fill((LJ0.p4+LJ1.p4).M())
        pf, dsa, Reco_Mu = ([] for i in range (3))
        
        for lj in [LJ0, LJ1]:
            if not lj.isMuonType():continue
            for i in lj.pfcand_pfmuonIdx:
                pf.append(event.muons[i])
            for i in lj.pfcand_dsamuonIdx:
                dsa.append(event.dsamuons[i])

        print (len(pf)+len(dsa))
        
        '''for dsamu in dsa:
            self.Histos['%s/dsaMu_do' % chan].Fill(dsamu.d0)
            self.Histos['%s/dsaMu_dz' % chan].Fill(dsamu.dz)
        for pfmu in pf:
            self.Histos['%s/pfMu_do' % chan].Fill(pfmu.d0)
            self.Histos['%s/pfMu_dz' % chan].Fill(pfmu.dz)

        lpf, ldsa = len(pf),len(dsa)
        self.Histos['%s/nMuons' % chan].Fill(lpf+ldsa)
        
        if lpf ==1:
            Reco_Mu.append(pf[0])
            Reco_Mu.append(dsa[0])
            self.Histos['%s/dr1' % chan].Fill(DeltaR(Reco_Mu[0].p4,Reco_Mu[1].p4))
        elif lpf == 2:
            Reco_Mu.append(pf[0])
            Reco_Mu.append(pf[1])
            self.Histos['%s/dr2' % chan].Fill(DeltaR(Reco_Mu[0].p4,Reco_Mu[1].p4))
        elif lpf == 0:
            Reco_Mu.append(dsa[0])
            Reco_Mu.append(dsa[1])
            self.Histos['%s/dr0' % chan].Fill(DeltaR(Reco_Mu[0].p4,Reco_Mu[1].p4))

        self.Histos['%s/mumass' % chan].Fill((Reco_Mu[0].p4+Reco_Mu[1].p4).M())
        for mu in Reco_Mu:
            self.Histos['%s/ReMu_do' % chan].Fill(mu.d0)
            self.Histos['%s/ReMu_dz' % chan].Fill(mu.dz)
            self.Histos['%s/ReMu_rho' % chan].Fill(mu.p4.Rho())

        TriObj = [TO for TO in event.trigobjs] # trigger objects in the event
        if lpf == 2:
        #using both muon separately for now
            mindr, to1 = 999, 999
            if len(TriObj) >1:
                for j, TO in enumerate (TriObj):
                    #print TO.p4.Rho()
                    if TO.bit != 0 and (
                        abs(TO.bit) & (1<<0) > 0 or abs(TO.bit) & (1<<1) > 0 or abs(TO.bit) & (1<<2) > 0 or abs(TO.bit) & (1<<3) > 0 or abs(TO.bit) & (1<<4) > 0
                            or abs(TO.bit) & (1<<5)  > 0 or abs(TO.bit) & (1<<6)  > 0 or abs(TO.bit) & (1<<7)  > 0 or abs(TO.bit) & (1<<8)  > 0 or abs(TO.bit) & (1<<9)  > 0 
                            or abs(TO.bit) & (1<<10) > 0 or abs(TO.bit) & (1<<11) > 0 or abs(TO.bit) & (1<<12) > 0 or abs(TO.bit) & (1<<13) > 0 or abs(TO.bit) & (1<<14) > 0 
                            or abs(TO.bit) & (1<<15) > 0 or abs(TO.bit) & (1<<16) > 0 or abs(TO.bit) & (1<<17) > 0 or abs(TO.bit) & (1<<18) > 0 or abs(TO.bit) & (1<<19) > 0 
                            or abs(TO.bit) & (1<<20) > 0 or abs(TO.bit) & (1<<21) > 0 or abs(TO.bit) & (1<<22) > 0 or abs(TO.bit) & (1<<23) > 0):

                        drmt = DeltaR(TriObj[j].p4,Reco_Mu[0].p4)
                        if drmt < mindr:
                            mindr = drmt
                            if mindr < dR_thr:
                                to1 = j
                                mupt = Reco_Mu[0].p4.pt()
                                mueta = Reco_Mu[0].p4.eta()
                                mud0 = Reco_Mu[0].d0
                                #lxy = Reco_Mu[0].klmvtx_lxy
                        
                        if to1 != 999:
                            self.Histos['%s/TO_Den_dR'  %chan].Fill(mindr)
                            self.Histos['%s/TO_Den_pT'  %chan].Fill(mupt)        
                            self.Histos['%s/TO_Den_eta' %chan].Fill(mueta)
                            self.Histos['%s/TO_Den_d0' %chan].Fill(mud0)
                            #self.Histos['%s/TO_Den_lxy' %chan].Fill(lxy)
                            for j, to in enumerate (TriObj):
                                if j != to1:
                                    dr2 = DeltaR(TriObj[j].p4,Reco_Mu[1].p4)
                                    if dr2 < dR_thr:
                                        self.Histos['%s/TO_Num_dR' % chan].Fill(mindr)
                                        self.Histos['%s/TO_Num_pT' % chan].Fill(mupt)
                                        self.Histos['%s/TO_Num_eta' % chan].Fill(mueta)
                                        self.Histos['%s/TO_Num_d0' %chan].Fill(mud0)
                                        #self.Histos['%s/TO_Num_lxy' %chan].Fill(lxy)
                                        break
                                    
                        mindr, to1 = 999, 999
                        for j, to in enumerate (TriObj):
                            drmt = DeltaR(TriObj[j].p4,Reco_Mu[1].p4)
                            if drmt < mindr:
                                mindr = drmt
                                if mindr < dR_thr:
                                    to1 = j
                                    mupt = Reco_Mu[1].p4.pt()
                                    mueta = Reco_Mu[0].p4.eta()
                                    mud0 = Reco_Mu[0].d0

                        if to1 != 999:
                            self.Histos['%s/TO_Den_dR'  %chan].Fill(mindr)
                            self.Histos['%s/TO_Den_pT'  %chan].Fill(mupt)
                            self.Histos['%s/TO_Den_eta' %chan].Fill(mueta)
                            self.Histos['%s/TO_Den_d0' %chan].Fill(mud0)
                            for j, to in enumerate (TriObj):
                                if j != to1:
                                    dr2 = DeltaR(TriObj[j].p4,Reco_Mu[0].p4)
                                    if dr2 < dR_thr:
                                        self.Histos['%s/TO_Num_dR' % chan].Fill(mindr)
                                        self.Histos['%s/TO_Num_pT' % chan].Fill(mupt)
                                        self.Histos['%s/TO_Num_eta' % chan].Fill(mueta)
                                        self.Histos['%s/TO_Num_d0' %chan].Fill(mud0)
                                        break'''


histCollection = [
    {  'name': 'dr0',        'binning' : (50, 0.0,0.5),                   'title': '#Delta R dsa muons; #Delta R; Number of entries'},
    {  'name': 'dr1',        'binning' : (50, 0.0,0.5),                   'title': '#Delta R pf and dsa muons; #Delta R; Number of entries'},
    {  'name': 'dr2',        'binning' : (50, 0.0,0.5),                   'title': '#Delta R pf  muons; #Delta R; Number of entries'},
    {  'name': 'ReMu_do',    'binning' : (10, 0, 50),                     'title': 'd_{o} distribution for reco muons; d_{o}; number of entries'},
    {  'name': 'nMuons',     'binning' : (10, -5.0,5.0),                  'title': 'number of Muons; nMuons; Number of entries'},
    {  'name': 'ReMu_dz',    'binning' : (50, 0, 20),                     'title': 'd_{z} distribution for reco muons; d_{z}; number of entries'},
    {  'name': 'ReMu_rho',   'binning' : (50, 0, 50),                     'title': '#Rho distribution for reco muons; #Rho; number of entries'},
    {  'name': 'dsaMu_do',   'binning' : (50, 0, 50),                     'title': 'd_{0} distribution for dsa muons; d_{0}; number of entries'},
    {  'name': 'dsaMu_dz',   'binning' : (50, 0, 50),                     'title': 'd_{z} distribution for dsa muons; d_{z}; number of entries'},
    {  'name': 'pfMu_do',    'binning' : (50, 0, 50),                     'title': 'd_{0} distribution for pf muons; d_{0}; number of entries'},
    {  'name': 'pfMu_dz',    'binning' : (50, 0, 50),                     'title': 'd_{z} distribution for pf muons; d_{z}; number of entries'},
    {  'name': 'mumass',     'binning' : (30, 0, 10),                      'title': 'mass distribution for reco  muons; m [GeV]; number of entries'},
    {  'name': 'ljmass',     'binning' : (100, 50, 1200),                      'title': 'mass distribution for lj; m [GeV]; number of entries'},
    
    #{  'name': 'RM_dR',
    #  'binning' : [[0,0.02,0.04,0.06,0.08,0.1,0.15,0.2,.3,.4,]],
    # 'title': '#Delta R of Reco muons; #Delta R; Number of entries'},

    #{  'name': 'RM_pT',          'binning' : (100, 0.0,500),                   'title': 'Reco muon p_{T} distribution; p_{T} [GeV]; Number of entries'},
    #{  'name': 'RM_n',           'binning' : (20, 0.0,20),                     'title': 'Number of Reco #mu ; #mu ; Number of entries'},
    #{  'name': 'TO_n',           'binning' : (30, 0.0,30),                     'title': 'Number of trigger objects; #mu ; Number of entries'},
    #{  'name': 'TO_bit',         'binning' : (100, -50.0,50),                  'title': 'Trigger object ID ; TO ID; Number of entries'},
    #{  'name': 'TO_pT',          'binning' : (50, 0.0,500),                    'title': 'TO p_{T} distribution;  p_{T} [GeV]; Number of entries'},
    #{  'name': 'RMTO_match',     'binning' : (50, 0.0,50),                     'title': '# of muon matched to a TO; # of muons; Number of entries'},
    
    #{  'name': 'min_dR_RMTO',  
     #  'binning' : [[0,0.1,0.2,0.3,0.4]],  
      # 'title': '# of muon matched to a TO; # of muons; Number of entries'},

    #{  'name': 'ReMu_d0',
     #  'binning' : [[0,0.001,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.12,0.14,0.16,0.18,0.2,0.25,0.3,0.4,2,5,10,20,50,200,1000]],
      # 'title' : 'd0 for all reco muons; d_0; Number of entries'
    #},    
    {  'name': 'TO_Num_dR',
       #'binning' : (20, 0.0, 0.5),
       'binning' : [[0,0.02,0.04,0.06,0.08,0.1,0.13,0.16,0.19,0.23,0.27,0.3,0.35,0.4]],
       'title' : '#mu; #Delta R; Number of entries'},
    
    {  'name': 'TO_Den_dR',
       #'binning' : (20, 0.0, 0.5),
       'binning' : [[0,0.02,0.04,0.06,0.08,0.1,0.13,0.16,0.19,0.23,0.27,0.3,0.35,0.4]],
       'title': '#mu; #Delta R; Number of entries'},

    {  'name': 'TO_Num_pT',     
       'binning' :  [[0,2,4,6,8,10,15,20,30,40,60,80,100,150,200,250,300,350,400,450,500,600]],
       'title' : '#mu p_{T}; p_{T} [GeV]; Number of entries'},

    {  'name': 'TO_Den_pT',
       'binning' :  [[0,2,4,6,8,10,15,20,30,40,60,80,100,150,200,250,300,350,400,450,500,600]],  
       'title' : '#mu p_{T}; p_{T} [GeV]; Number of entries'},

    {  'name': 'TO_Num_eta',
       'binning' : (30,-3.5,3.5),#[[-3.5,-3.0,-2.6,-2.2,-1.8,-1.4,-1.0,-0.6,0.2,0.6,1.0,1.4,1.8,2.2,2.6,3.0,3.5]],
       'title': '#mu #eta; #eta; Number of entries'
   },
    
    {  'name': 'TO_Den_eta', 
       'binning' : (30,-3.5,3.5),#[[-3.5,-3.0,-2.6,-2.2,-1.8,-1.4,-1.0,-0.6,0.2,0.6,1.0,1.4,1.8,2.2,2.6,3.0,3.5]],
       'title': '#mu #eta; #eta; Number of entries'
   },

    {  'name': 'TO_Num_d0',
       'binning' : [[0,0.1,0.2,0.4,0.6,0.8,1.0,1.5,2.0,3,4,5]],
       'title': '#mu d_{0}; d_{0}; Number of entries'
   },
    {  'name': 'TO_Den_d0',
       'binning' : [[0,0.1,0.2,0.4,0.6,0.8,1.0,1.5,2.0,3,4,5]],
       'title': ' #mu d_{0}; d_{0}; Number of entries'
   },
    {  'name': 'TO_Num_lxy',
       'binning' : [[0,5,10,13,17,20,30,50,80,120,200]],
       'title': 'Probe #mu L_{xy}; L_{xy} [cm]; Number of entries'
   },
    {  'name': 'TO_Den_lxy',
       'binning' : [[0,5,10,13,17,20,30,50,80,120,200]],
       'title': 'Probe #mu L_{xy}; L_{xy} [cm]; Number of entries'
   },
]
