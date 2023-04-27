#!/usr/bin/env python
# Reco_Mu: reco muon, TO: trigger object, LJ: lepton jet

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
        dR_thr, pt_thr = 0.2, 30 # Matching threshold between TO and reco muon, min pt for reco muons

        self.Histos['%s/ljmass' % chan].Fill((LJ0.p4+LJ1.p4).M())#lepton jet mass
        
        pf, dsa, Reco_Mu = ([] for i in range (3))
        
        #Get the muons from the pf and dsa candidates collection 
        #for lj in [LJ0, LJ1]:
         #   if not lj.isMuonType():continue
          #  for i in lj.pfcand_pfmuonIdx:
           #     pf.append(event.muons[i])
            #for j in lj.pfcand_dsamuonIdx:
             #   dsa.append(event.dsamuons[j])
        
        ############
        #fill hist of d0 for pf and dsa muons
        for dsamu in dsa:
            self.Histos['%s/dsaMu_d0' % chan].Fill(abs(dsamu.d0))
            
        for pfmu in pf:
            self.Histos['%s/pfMu_d0' % chan].Fill(abs(pfmu.d0)*10000)

        lpf, ldsa = len(pf),len(dsa)
        self.Histos['%s/nMuons' % chan].Fill(lpf+ldsa)
        

        ########
        #Join pf and dsa muons in a single list, Reco_Mu
        ########
        '''if lpf ==2:
            Reco_Mu.append(pf[0])
            Reco_Mu.append(pf[1])
            self.Histos['%s/drpf' % chan].Fill(DeltaR(Reco_Mu[0].p4,Reco_Mu[1].p4))'''

        '''elif lpf == 1:#order by pt instead of which collection the muon is drawn from
            if pf[0].p4.pt()> dsa[0].p4.pt():
                Reco_Mu.append(pf[0])
                Reco_Mu.append(dsa[0])
            else:
                Reco_Mu.append(dsa[0])
                Reco_Mu.append(pf[0])
            self.Histos['%s/drboth' % chan].Fill(DeltaR(Reco_Mu[0].p4,Reco_Mu[1].p4))
            self.Histos['%s/ptboth' % chan].Fill(Reco_Mu[0].p4.pt() - Reco_Mu[1].p4.pt())'''
            
        if ldsa == 2:
            Reco_Mu.append(dsa[0])
            Reco_Mu.append(dsa[1])
            #print(Reco_Mu[0].d0)
            self.Histos['%s/drdsa' % chan].Fill(DeltaR(Reco_Mu[0].p4,Reco_Mu[1].p4))
            self.Histos['%s/ptdsa' % chan].Fill( Reco_Mu[0].p4.pt() - Reco_Mu[1].p4.pt() )

        
        #self.Histos['%s/leadingpt'%chan].Fill(Reco_Mu[0].p4.pt())
        #self.Histos['%s/sleadingpt'%chan].Fill(Reco_Mu[1].p4.pt())
        #d0_1, d0_2 = 10000*abs(Reco_Mu[0].d0), 10000* abs(Reco_Mu[1].d0)

        ##Reco muon variables
        if len(Reco_Mu) == 2:
            self.Histos['%s/leadingpt'%chan].Fill(Reco_Mu[0].p4.pt())
            self.Histos['%s/sleadingpt'%chan].Fill(Reco_Mu[1].p4.pt())
            d0_1, d0_2 = 1*abs(Reco_Mu[0].d0), 1* abs(Reco_Mu[1].d0)
            if Reco_Mu[0].p4.pt()>pt_thr and Reco_Mu[1].p4.pt()>pt_thr and d0_1>0 and d0_2>0: #impose cuts on # of muons and muon pt and d0
            
                self.Histos['%s/mumass' % chan].Fill((Reco_Mu[0].p4+Reco_Mu[1].p4).M())#invariant mass of the two muons
                for mu in Reco_Mu:
                    self.Histos['%s/ReMu_d0' % chan].Fill(abs(mu.d0)*1)


                drmu = DeltaR(Reco_Mu[0].p4,Reco_Mu[1].p4)#Delta R of the two muons
                self.Histos['%s/drmus' % chan].Fill(drmu)
                if drmu <0.2: self.Histos['%s/drmus0p2' % chan].Fill(drmu)

                # trigger objects in the event
                TriObj = [TO for TO in event.trigobjs]
                self.Histos['%s/nTOs' % chan].Fill(len(TriObj))
                TO_pass = []#list with TO passing a trigger
                
                # loop over all trigger objects in the event. If a trigger object pass a trigger filter append it to TO_pass 
                for j, TO in enumerate (TriObj):
                    if TO.bit != 0 and (
                            abs(TO.bit) & (1<<0) > 0 or abs(TO.bit) & (1<<1) > 0 or abs(TO.bit) & (1<<2) > 0 or abs(TO.bit) & (1<<3) > 0 or abs(TO.bit) & (1<<4) > 0
                            or abs(TO.bit) & (1<<5)  > 0 or abs(TO.bit) & (1<<6)  > 0 or abs(TO.bit) & (1<<7)  > 0 or abs(TO.bit) & (1<<8)  > 0 or abs(TO.bit) & (1<<9)  > 0
                            or abs(TO.bit) & (1<<10) > 0 or abs(TO.bit) & (1<<11) > 0 or abs(TO.bit) & (1<<12) > 0 or abs(TO.bit) & (1<<13) > 0 or abs(TO.bit) & (1<<14) > 0
                            or abs(TO.bit) & (1<<15) > 0 or abs(TO.bit) & (1<<16) > 0 or abs(TO.bit) & (1<<17) > 0 or abs(TO.bit) & (1<<18) > 0 or abs(TO.bit) & (1<<19) > 0
                            or abs(TO.bit) & (1<<20) > 0 or abs(TO.bit) & (1<<21) > 0 or abs(TO.bit) & (1<<22) > 0 or abs(TO.bit) & (1<<23) > 0):
                        #if TO.p4.pt()>23:
                        TO_pass.append(TriObj[j])
                    
                ##### calculate dR between all trigger objects
                for i, to in enumerate(TO_pass):
                    for j, tov in enumerate (TO_pass):
                        if i != j:
                            drtoall = DeltaR(TO_pass[i].p4,TO_pass[j].p4)
                            self.Histos['%s/drtoall' % chan].Fill(drtoall)
                            if drtoall < 0.2: self.Histos['%s/drtoall0p2' % chan].Fill(drtoall)
                        
                ########################
                # At this point there are two lists: Reco_Mu is the contains the reco muons and TO_pass contains the TO that passed a trigger filter
                ########################
            
                mu1, mu2 = 0,1# index of the muons in the list to test their order

                #find the min delta R between reco mu "0" and all TO_pass
            
                #testing efficiency for different displacemnet
                #if displacement grater than a value
                if mu1 == 0: #place holder for now
                    mindr,to1 = 999,999
                    for k, TO in enumerate(TO_pass):
                        drtm = DeltaR(TO_pass[k].p4,Reco_Mu[mu1].p4) #calculate delra R between trigger object "k" and reco mu "1"
                        if drtm < mindr:
                            mindr = drtm
                            if mindr < dR_thr:#matched
                                to1 = k   # TO at index k was matched to a RM[0]
                                #vaviables refering to the first muon
                                mupt = Reco_Mu[mu1].p4.pt()
                                mueta = Reco_Mu[mu1].p4.eta()
                                mud0 = abs(Reco_Mu[mu1].d0)*1
                                var = drtm
                            
                            #if to1 != 999 means RM[1] was matched a TO
                            if to1 != 999:
                                self.Histos['%s/TO_Den_dR'  %chan].Fill(drmu)
                                self.Histos['%s/TO_Den_pT'  %chan].Fill(mupt)
                                self.Histos['%s/TO_Den_eta' %chan].Fill(mueta)
                                self.Histos['%s/TO_Den_d0' %chan].Fill(mud0)
                                self.Histos['%s/drtm1'  %chan].Fill(drmu,var)
                            
                                #find min dr between the second muon and its closest TO
                                mindr, to2 = 999, 999
                                for l, to in enumerate(TO_pass): #loop over all TO_pass again now with RM[1] to see if there is a match
                                    drtm2 = DeltaR(TO_pass[l].p4,Reco_Mu[mu2].p4)
                                    if drtm2 < mindr:
                                        mindr = drtm2
                                        if mindr < dR_thr and l != to1:
                                            to2 = l
                                        
                                if to2 != 999:
                                    if to1 != to2: #check if the index of the second loop is different that 'to1' index of the TO matched to RM[0]
                                        drt12 = DeltaR(TO_pass[to1].p4,TO_pass[l].p4)
                                        self.Histos['%s/TO_Num_dR'  %chan].Fill(drmu)
                                        self.Histos['%s/TO_Num_pT' % chan].Fill(mupt)
                                        self.Histos['%s/TO_Num_eta' % chan].Fill(mueta)
                                        self.Histos['%s/TO_Num_d0' %chan].Fill(mud0)
                                        self.Histos['%s/drtm2'  %chan].Fill(drmu,drtm2)
                                        self.Histos['%s/drtm12'  %chan].Fill(var,drtm2)
                                        self.Histos['%s/drt12'  %chan].Fill(drt12)
                        
                        
histCollection = [

    {  'name': 'drdsa',      'binning' : (50, 0.0,0.5),         'title': '#Delta R dsa muons; #Delta R; Number of entries'},
    {  'name': 'drboth',     'binning' : (50, 0.0,0.5),         'title': '#Delta R pf and dsa muons; #Delta R; Number of entries'},
    {  'name': 'drpf',       'binning' : (50, 0.0,0.5),         'title': '#Delta R pf  muons; #Delta R; Number of entries'},
    {  'name': 'ptpf',       'binning' : (100, -100,100),       'title': 'pf muon p_{T} difference; p_{T} [GeV]; Number of entries'},
    {  'name': 'ptboth',     'binning' : (100, -100,100),       'title': 'both muon p_{T} difference; p_{T} [GeV]; Number of entries'},
    {  'name': 'ptdsa',      'binning' : (100, -100,100),       'title': 'dsa muon p_{T} difference; p_{T} [GeV]; Number of entries'},
    {  'name': 'leadingpt',  'binning' : (100, 0,1000),       'title': 'Leading muon p_{T}; p_{T} [GeV]; Number of entries'},
    {  'name': 'sleadingpt', 'binning' : (100, 0,1000),       'title': 'subleading muon p_{T}; p_{T} [GeV]; Number of entries'},


    {  'name': 'ReMu_d0',    'binning' : (50, 0, 100),           'title': '|d_{0}| distribution for reco muons; |d_{0}|[#mu m]; Events'},
    {  'name': 'dsaMu_d0',   'binning' : (50, 0, 100),           'title': '|d_{0}| distribution for dsa muons; |d_{0}|[cm]; number of entries'},
    {  'name': 'pfMu_d0',    'binning' : (50, 0, 2500),           'title': '|d_{0}| distribution for pf muons; |d_{0}|[#mu m]; number of entries'},

    {  'name': 'nMuons',     'binning' : (10, -5.0,5.0),        'title': 'number of Muons; nMuons; Number of entries'},
    {  'name': 'nTOs',       'binning' : (20, 0,50),            'title': 'number of trigger objects; nTOs; Number of entries'},

    {  'name': 'mumass',     'binning' : (30, 0, 10),           'title': 'mass distribution for reco  muons; m [GeV]; number of entries'},
    {  'name': 'ljmass',     'binning' : (100, 50, 1200),       'title': 'mass distribution for lj; m [GeV]; number of entries'},

    {  'name': 'drmus',      'binning': (100, 0, 0.5),          'title': '#Delta R between #mu; #Delta R(#mu_{1},#mu_{2}); Number of entries'},
    {  'name': 'drmus0p2',   'binning': (100, 0, 0.22),         'title': '#Delta R between #mu; #Delta R(#mu_{1},#mu_{2}); Number of entries'},    
    {  'name': 'drtoall',    'binning': (50,0,0.5),  	        'title': '#Delta R between TOs; #Delta R(TO_{i},TO_{j}); #Delta R (TO,#mu_{1})'},
    {  'name': 'drtoall0p2', 'binning': (200, 0, 0.22),         'title': '#Delta R between TOs; #Delta R(TO_{i},TO_{j}); Number of entries'},

    {  'name': 'drtm1',	     'binning': (50,0,0.5, 20,0,0.5),	'title': '#Delta R between TO and #mu_{1}; #Delta R(#mu_{1},#mu_{2}); #Delta R (TO,#mu_{1})'},
    {  'name': 'drtm2',	     'binning': (50,0,0.5, 20,0,0.5),	'title': '#Delta R between TO and #mu_{2}; #Delta R(#mu_{1},#mu_{2}); #Delta R (TO,#mu_{2})'},
    {  'name': 'drtm12',     'binning': (50,0,0.5, 20,0,0.5),	'title': '#Delta R for the two matches; #Delta R(to,#mu_{2}); #Delta R(to,#mu_{1})'},
    {  'name': 'drt12',	     'binning': (50, 0, 0.5),		'title': '#Delta R between matched TO; #Delta R(TO_{1},TO_{2}); Number of entries'},



    #{  'name': 'RM_dR',          'binning' : [[0,0.02,0.04,0.06,0.08,0.1,0.15,0.2,.3,.4,]],     'title': '#Delta R of Reco muons; #Delta R; Number of entries'},
    #{  'name': 'RM_pT',          'binning' : (100, 0.0,500),                   'title': 'Reco muon p_{T} distribution; p_{T} [GeV]; Number of entries'},
    #{  'name': 'RM_n',           'binning' : (20, 0.0,20),                     'title': 'Number of Reco #mu ; #mu ; Number of entries'},
    #{  'name': 'TO_n',           'binning' : (30, 0.0,30),                     'title': 'Number of trigger objects; #mu ; Number of entries'},
    #{  'name': 'TO_bit',         'binning' : (100, -50.0,50),                  'title': 'Trigger object ID ; TO ID; Number of entries'},
    #{  'name': 'TO_pT',          'binning' : (50, 0.0,500),                    'title': 'TO p_{T} distribution;  p_{T} [GeV]; Number of entries'},
    #{  'name': 'RMTO_match',     'binning' : (50, 0.0,50),                     'title': '# of muon matched to a TO; # of muons; Number of entries'},
    
    #{  'name': 'TO_Num_dR',     'binning' : [[0,0.001,0.005,0.01,0.02,0.03,0.04,0.06,0.08,0.1,0.13,0.16,0.19,0.23,0.27,0.3,0.35,0.4,0.5]], 'title' :'#mu;#Delta R(#mu_{1},#mu_{2});Events'},
    #{  'name': 'TO_Den_dR',     'binning' : [[0,0.001,0.005,0.01,0.02,0.03,0.04,0.06,0.08,0.1,0.13,0.16,0.19,0.23,0.27,0.3,0.35,0.4,0.5]], 'title':'#mu; #Delta R(#mu_{1},#mu_{2});Events'},

    {  'name': 'TO_Num_dR',     'binning': (16, 0.0, 0.3),     'title': '#Delta R matched; #Delta R(#mu_{1},#mu_{2}); Number of entries'},
    {  'name': 'TO_Den_dR',     'binning': (16, 0.0, 0.3),     'title': '#Delta R total; #Delta R(#mu_{1},#mu_{2}); Number of entries'},

    {  'name': 'TO_Num_pT',     'binning': (18, 0.0, 600),     'title': '#mu p_{T} matched; p_{T} [GeV]; Number of entries'},
    {  'name': 'TO_Den_pT',     'binning': (18, 0.0, 600),     'title': '#mu p_{T} total; p_{T} [GeV]; Number of entries'},

    {  'name': 'TO_Num_eta',    'binning': (25,-3.5,3.5),      'title': ' #eta matched ; #eta; Number of entries'},
    {  'name': 'TO_Den_eta',    'binning': (25,-3.5,3.5),      'title': ' #eta total; #eta; Number of entries'},

    {  'name': 'TO_Num_d0',   	'binning': (50, 0, 100),       'title': 'd_{0} matched; |d_{0}|[#mu m]; Number of entries'},
    {  'name': 'TO_Den_d0',     'binning': (50, 0, 100),       'title': 'd_{0} total; |d_{0}|[#mu m]; Number of entries'},

]
