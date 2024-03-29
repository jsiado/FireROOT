#!/usr/bin/env python
# RM: reco muon, TO: trigger object

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
        dR_thr = 0.2 # Matching threshold between TO and reco muon

        self.Histos['%s/ljmass' % chan].Fill((LJ0.p4+LJ1.p4).M())#lepton jet mass
        pf, dsa, Reco_Mu = ([] for i in range (3))
        ########
        #Get the two muons from the pf and dsa candidates collection 
        for lj in [LJ0, LJ1]:
            if not lj.isMuonType():continue
            for i in lj.pfcand_pfmuonIdx:
                pf.append(event.muons[i])
            for i in lj.pfcand_dsamuonIdx:
                dsa.append(event.dsamuons[i])
        
        ############
        #fill hist for d0 and dz
        for dsamu in dsa:
            self.Histos['%s/dsaMu_do' % chan].Fill(dsamu.d0)
            self.Histos['%s/dsaMu_dz' % chan].Fill(dsamu.dz)
        for pfmu in pf:
            self.Histos['%s/pfMu_do' % chan].Fill(pfmu.d0)
            self.Histos['%s/pfMu_dz' % chan].Fill(pfmu.dz)

        lpf, ldsa = len(pf),len(dsa)
        self.Histos['%s/nMuons' % chan].Fill(lpf+ldsa)
        

        ########
        #Join pf and dsa muons in a single list, Reco_Mu 
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

        self.Histos['%s/mumass' % chan].Fill((Reco_Mu[0].p4+Reco_Mu[1].p4).M())#invariant mass of the two muons
        for mu in Reco_Mu:
            self.Histos['%s/ReMu_do' % chan].Fill(mu.d0)
            self.Histos['%s/ReMu_dz' % chan].Fill(mu.dz)
            self.Histos['%s/ReMu_rho' % chan].Fill(mu.p4.Rho())
        
        drmu = DeltaR(Reco_Mu[0].p4,Reco_Mu[1].p4)#Delta R of the two muons
        self.Histos['%s/drmus' % chan].Fill(drmu)
        if drmu < 0.2:
             self.Histos['%s/drmus0p2' % chan].Fill(drmu)
        TriObj = [TO for TO in event.trigobjs] # trigger objects in the event
        self.Histos['%s/nTOs' % chan].Fill(len(TriObj))

        TO_pass = []#list with TO passing a trigger

        for j, TO in enumerate (TriObj):# loop over all trigger objects in the event                                                                                                  
            if TO.bit != 0 and (
                    abs(TO.bit) & (1<<0) > 0 or abs(TO.bit) & (1<<1) > 0 or abs(TO.bit) & (1<<2) > 0 or abs(TO.bit) & (1<<3) > 0 or abs(TO.bit) & (1<<4) > 0
                    or abs(TO.bit) & (1<<5)  > 0 or abs(TO.bit) & (1<<6)  > 0 or abs(TO.bit) & (1<<7)  > 0 or abs(TO.bit) & (1<<8)  > 0 or abs(TO.bit) & (1<<9)  > 0
                    or abs(TO.bit) & (1<<10) > 0 or abs(TO.bit) & (1<<11) > 0 or abs(TO.bit) & (1<<12) > 0 or abs(TO.bit) & (1<<13) > 0 or abs(TO.bit) & (1<<14) > 0
                    or abs(TO.bit) & (1<<15) > 0 or abs(TO.bit) & (1<<16) > 0 or abs(TO.bit) & (1<<17) > 0 or abs(TO.bit) & (1<<18) > 0 or abs(TO.bit) & (1<<19) > 0
                    or abs(TO.bit) & (1<<20) > 0 or abs(TO.bit) & (1<<21) > 0 or abs(TO.bit) & (1<<22) > 0 or abs(TO.bit) & (1<<23) > 0):
                TO_pass.append(TriObj[j])
        
        for i, to in enumerate(TO_pass):
            for j, tov in enumerate (TO_pass):
                if i != j:
                    drtoall = DeltaR(TO_pass[i].p4,TO_pass[j].p4)
                    self.Histos['%s/drtoall' % chan].Fill(drtoall)
                    if drtoall<0.2:
                    	self.Histos['%s/drtoall0p2' % chan].Fill(drtoall)
        
        ###################
        #Reco_Mu is the list with the reco muons and TO_pass is the TO that passed a trigger
        
        ######################
        #find the min delta R between reco mu "0" and all TO_pass
        mindr,to1 = 999,999
        for k, TO in enumerate(TO_pass):
            drtm = DeltaR(TO_pass[k].p4,Reco_Mu[0].p4) #calculate delta R between trigger object "k" and reco mu "0"
            if drtm < mindr:
                mindr = drtm
                if mindr < dR_thr:#matched
                    to1 = k   # TO at index k was matched to a RM[0]
                    mupt = Reco_Mu[0].p4.pt()
                    mueta = Reco_Mu[0].p4.eta()
                    mud0 = Reco_Mu[0].d0
                    var = drtm
                    self.Histos['%s/drtm1'  %chan].Fill(drmu,drtm)
        
        #if to1 != 999 means RM[0] was matched a TO
        if to1 != 999:
            self.Histos['%s/TO_Den_dR'  %chan].Fill(drmu)
            self.Histos['%s/TO_Den_pT'  %chan].Fill(mupt)        
            self.Histos['%s/TO_Den_eta' %chan].Fill(mueta)
            self.Histos['%s/TO_Den_d0' %chan].Fill(mud0)

            for l, to in enumerate(TO_pass): #loop over all TO_pass again now with RM[1] to see if there is a match
                drtm2 = DeltaR(TO_pass[l].p4,Reco_Mu[1].p4)
                if l != to1 and drtm2 < dR_thr: #check if the index of the second loop is different that 'to1' index of the TO matched to RM[0]
                	drt12 = DeltaR(TO_pass[to1].p4,TO_pass[l].p4)
                	self.Histos['%s/TO_Num_dR'  %chan].Fill(drmu)
                	self.Histos['%s/TO_Num_pT' % chan].Fill(mupt)
                	self.Histos['%s/TO_Num_eta' % chan].Fill(mueta)
                	self.Histos['%s/TO_Num_d0' %chan].Fill(mud0)
                	self.Histos['%s/drtm2'  %chan].Fill(drmu,drtm2)
                	#self.Histos['%s/drt12'  %chan].Fill(drt12)
                	self.Histos['%s/drtm12'  %chan].Fill(var,drtm2)
                	self.Histos['%s/drt12'  %chan].Fill(drt12)
                	break

        #####
        ## loop for the inversion starting with Muon2 now and looping with mu1
        #mindr,to1 = 999,999
        mindr,to1 = 999,999
        for k, to in enumerate (TO_pass):
            drtm = DeltaR(TO_pass[k].p4,Reco_Mu[1].p4)
            if drtm < mindr:
                mindr = drtm
                if mindr < dR_thr:
                    to1 = k
                    mupt = Reco_Mu[1].p4.pt()
                    mueta = Reco_Mu[1].p4.eta()
                    mud0 = Reco_Mu[1].d0
                    var = drtm
                    self.Histos['%s/drtm1'  %chan].Fill(drmu,drtm)

        if to1 != 999:
            self.Histos['%s/TO_Den_dR'  %chan].Fill(drmu)
            self.Histos['%s/TO_Den_pT'  %chan].Fill(mupt)
            self.Histos['%s/TO_Den_eta' %chan].Fill(mueta)
            self.Histos['%s/TO_Den_d0' %chan].Fill(mud0)
            
            for l, to in enumerate(TO_pass):
                drtm2 = DeltaR(TO_pass[l].p4,Reco_Mu[0].p4)
                if l != to1 and drtm2 < dR_thr:
                    drt12 = DeltaR(TO_pass[to1].p4,TO_pass[l].p4)
                    self.Histos['%s/TO_Num_dR'  %chan].Fill(drmu)
                    self.Histos['%s/TO_Num_pT' % chan].Fill(mupt)
                    self.Histos['%s/TO_Num_eta' % chan].Fill(mueta)
                    self.Histos['%s/TO_Num_d0' %chan].Fill(mud0)
                    self.Histos['%s/drtm2'  %chan].Fill(drmu,drtm2)
                    self.Histos['%s/drtm12'  %chan].Fill(var,drtm2)
                    self.Histos['%s/drt12'  %chan].Fill(drt12)
                    break


histCollection = [
    {  'name': 'dr0',        'binning' : (50, 0.0,0.5),                   'title': '#Delta R dsa muons; #Delta R; Number of entries'},
    {  'name': 'dr1',        'binning' : (50, 0.0,0.5),                   'title': '#Delta R pf and dsa muons; #Delta R; Number of entries'},
    {  'name': 'dr2',        'binning' : (50, 0.0,0.5),                   'title': '#Delta R pf  muons; #Delta R; Number of entries'},
    {  'name': 'ReMu_do',    'binning' : (10, 0, 50),                     'title': 'd_{o} distribution for reco muons; d_{o}; number of entries'},
    {  'name': 'nMuons',     'binning' : (10, -5.0,5.0),                  'title': 'number of Muons; nMuons; Number of entries'},
    {  'name': 'nTOs',        'binning' : (20, 0,50),                     'title': 'number of trigger objects; nTOs; Number of entries'},
    {  'name': 'ReMu_dz',    'binning' : (50, 0, 20),                     'title': 'd_{z} distribution for reco muons; d_{z}; number of entries'},
    {  'name': 'ReMu_rho',   'binning' : (50, 0, 50),                     'title': '#Rho distribution for reco muons; #Rho; number of entries'},
    {  'name': 'dsaMu_do',   'binning' : (50, 0, 50),                     'title': 'd_{0} distribution for dsa muons; d_{0}; number of entries'},
    {  'name': 'dsaMu_dz',   'binning' : (50, 0, 50),                     'title': 'd_{z} distribution for dsa muons; d_{z}; number of entries'},
    {  'name': 'pfMu_do',    'binning' : (50, 0, 50),                     'title': 'd_{0} distribution for pf muons; d_{0}; number of entries'},
    {  'name': 'pfMu_dz',    'binning' : (50, 0, 50),                     'title': 'd_{z} distribution for pf muons; d_{z}; number of entries'},
    {  'name': 'mumass',     'binning' : (30, 0, 10),                     'title': 'mass distribution for reco  muons; m [GeV]; number of entries'},
    {  'name': 'ljmass',     'binning' : (100, 50, 1200),                 'title': 'mass distribution for lj; m [GeV]; number of entries'},
    
    {  'name': 'drtm1',		'binning': (200,0,0.5, 20,0,0.5),  'title': '#Delta R between TO and #mu_{1}; #Delta R(#mu_{1},#mu_{2}); #Delta R (TO,#mu_{1})'},
    {  'name': 'drtm2',		'binning': (200,0,0.5, 20,0,0.5),  'title': '#Delta R between TO and #mu_{2}; #Delta R(#mu_{1},#mu_{2}); #Delta R (TO,#mu_{2})'},
    {  'name': 'drtm12',	'binning': (200,0,0.5, 20,0,0.5),  'title': '#Delta R for the two matches; #Delta R(to,#mu_{2}); #Delta R(to,#mu_{1})'},
    {  'name': 'drt12',		'binning': (200, 0, 0.5),          'title': '#Delta R between TO; #Delta R(TO_{1},TO_{2}); Number of entries'},
    {  'name': 'drtoall',	'binning': (200, 0, 0.5),          'title': '#Delta R between TOs; #Delta R(TO_{i},TO_{j}); Number of entries'},
    {  'name': 'drtoall0p2',       'binning': (200, 0, 0.22),          'title': '#Delta R between TOs; #Delta R(TO_{i},TO_{j}); Number of entries'},
    {  'name': 'drmus',       'binning': (200, 0, 0.5),          'title': '#Delta R between #mu; #Delta R(#mu_{1},#mu_{2}); Number of entries'},
    {  'name': 'drmus0p2',       'binning': (200, 0, 0.22),          'title': '#Delta R between #mu; #Delta R(#mu_{1},#mu_{2}); Number of entries'},
    
    #{  'name': 'RM_dR',
    #  'binning' : [[0,0.02,0.04,0.06,0.08,0.1,0.15,0.2,.3,.4,]],
    # 'title': '#Delta R of Reco muons; #Delta R; Number of entries'},

    #{  'name': 'RM_pT',          'binning' : (100, 0.0,500),                   'title': 'Reco muon p_{T} distribution; p_{T} [GeV]; Number of entries'},
    #{  'name': 'TO_n',           'binning' : (30, 0.0,30),                     'title': 'Number of trigger objects; #mu ; Number of entries'},
    #{  'name': 'TO_bit',         'binning' : (100, -50.0,50),                  'title': 'Trigger object ID ; TO ID; Number of entries'},
    #{  'name': 'RMTO_match',     'binning' : (50, 0.0,50),                     'title': '# of muon matched to a TO; # of muons; Number of entries'},
    
    #{  'name': 'min_dR_RMTO',  
     #  'binning' : [[0,0.1,0.2,0.3,0.4]],  
      # 'title': '# of muon matched to a TO; # of muons; Number of entries'},

    #{  'name': 'ReMu_d0',
     #  'binning' : [[0,0.001,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.12,0.14,0.16,0.18,0.2,0.25,0.3,0.4,2,5,10,20,50,200,1000]],
      # 'title' : 'd0 for all reco muons; d_0; Number of entries'
    #},    
    {  'name': 'TO_Num_dR',
       'binning' : [[0,0.0005,0.002,0.005,0.01,0.02,0.03,0.04,0.06,0.08,0.1,0.13,0.16,0.19,0.23,0.27,0.3,0.35,0.4,0.5]],
       'title' : '#mu; #Delta R(#mu_{1},#mu_{2}); Number of entries'},
    
    {  'name': 'TO_Den_dR',
       'binning' : [[0,0.0005,0.002,0.005,0.01,0.02,0.03,0.04,0.06,0.08,0.1,0.13,0.16,0.19,0.23,0.27,0.3,0.35,0.4,0.5]],
       'title': '#mu; #Delta R(#mu_{1},#mu_{2}); Number of entries'},

    {  'name': 'TO_Num_pT',
		'binning' : (30,0,600),
#       'binning' :  [[0,10,20,30,40,60,80,100,150,200,250,300,350,400,450,500,600]],
       'title' : '#mu p_{T}; p_{T} [GeV]; Number of entries'},

    {  'name': 'TO_Den_pT',
    	'binning' : (30,0,600),
#       'binning' :  [[0,10,20,30,40,60,80,100,150,200,250,300,350,400,450,500,600]],  
       'title' : '#mu p_{T}; p_{T} [GeV]; Number of entries'},

    {  'name': 'TO_Num_eta',
       'binning' : (20,-3.5,3.5),#[[-3.5,-3.0,-2.6,-2.2,-1.8,-1.4,-1.0,-0.6,0.2,0.6,1.0,1.4,1.8,2.2,2.6,3.0,3.5]],
       'title': '#mu #eta; #eta; Number of entries'},
    
    {  'name': 'TO_Den_eta', 
       'binning' : (20,-3.5,3.5),#[[-3.5,-3.0,-2.6,-2.2,-1.8,-1.4,-1.0,-0.6,0.2,0.6,1.0,1.4,1.8,2.2,2.6,3.0,3.5]],
       'title': '#mu #eta; #eta; Number of entries'},

    {  'name': 'TO_Num_d0',
    	'binning' : (15, 0, 50),
 #      'binning' : [[0,0.1,0.2,0.4,0.6,0.8,1.0,1.5,2.0,3,4,5,6,8,12,16,20]],
       'title': '#mu d_{0}; d_{0}; Number of entries'},
    {  'name': 'TO_Den_d0',
    	'binning' : (15, 0, 50),
#       'binning' : [[0,0.1,0.2,0.4,0.6,0.8,1.0,1.5,2.0,3,4,5,6,8,12,16,20]],
       'title': ' #mu d_{0}; d_{0}; Number of entries'},
       
    {  'name': 'TO_Num_lxy',
       'binning' : [[0,5,10,13,17,20,30,50,80,120,200]],
       'title': 'Probe #mu L_{xy}; L_{xy} [cm]; Number of entries'},
   
    {  'name': 'TO_Den_lxy',
       'binning' : [[0,5,10,13,17,20,30,50,80,120,200]],
       'title': 'Probe #mu L_{xy}; L_{xy} [cm]; Number of entries'
   },
]
