#!/usr/bin/env python
# Reco_Mu: reco muon, TO: trigger object, LJ: lepton jet

''' output as out_60.root
4mu channel efficiency 
copy from 2mu2e and modify to include all
permutatiions for 4 mu channel'''


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
        dR_thr, pt_thr, d0_thr = 0.2, 30, .05 # Matching threshold between TO and reco muon, min pt for reco muons
        #self.Histos['%s/ljmass' % chan].Fill((LJ0.p4+LJ1.p4).M())#lepton jet mass
        
        pf, dsa, Reco_Mu = ([] for i in range (3))
        
        #Get the muons from the pf and dsa candidates collection 
        for lj in [LJ0, LJ1]:
            if not lj.isMuonType():continue
            for i in lj.pfcand_pfmuonIdx:
                pf.append(event.muons[i])
            for j in lj.pfcand_dsamuonIdx:
                dsa.append(event.dsamuons[j])
        #print('bef here')
        ###################
        #fill hist for != variables for dsa and pf muons
        for dsamu in dsa:
            self.Histos['%s/dsaMu_d0' % chan].Fill(abs(dsamu.d0))
            self.Histos['%s/dsaMu_pT' % chan].Fill(dsamu.p4.pt())
            self.Histos['%s/dsaMu_eta' % chan].Fill(dsamu.p4.eta())
            
        for pfmu in pf:
            self.Histos['%s/pfMu_d0' % chan].Fill(abs(pfmu.d0))
            self.Histos['%s/pfMu_pT' % chan].Fill(pfmu.p4.pt())
            self.Histos['%s/pfMu_eta' % chan].Fill(pfmu.p4.eta())

        lpf, ldsa = len(pf),len(dsa)
        self.Histos['%s/npfMuons' % chan].Fill(lpf)
        self.Histos['%s/ndsaMuons' % chan].Fill(ldsa)
        self.Histos['%s/nMuons' % chan].Fill(lpf + ldsa)
        
        #############################################################################################
        #Join pf and dsa muons in a single list, Reco_Mu
        #############################################################################################
        if lpf ==4:
            Reco_Mu.append(pf[0])
            Reco_Mu.append(pf[1])
            Reco_Mu.append(pf[2])
            Reco_Mu.append(pf[3])

        elif lpf == 3:
            Reco_Mu.append(pf[0])
            Reco_Mu.append(pf[1])
            Reco_Mu.append(pf[2])
            Reco_Mu.append(dsa[0])
        
        elif lpf == 2:
            Reco_Mu.append(pf[0])
            Reco_Mu.append(pf[1])
            Reco_Mu.append(dsa[0])
            Reco_Mu.append(dsa[1])
        
        elif ldsa == 1:
            Reco_Mu.append(pf[0])
            Reco_Mu.append(dsa[0])
            Reco_Mu.append(dsa[1])
            Reco_Mu.append(dsa[2])
        
        elif ldsa == 4:
            Reco_Mu.append(dsa[0])
            Reco_Mu.append(dsa[1])
            Reco_Mu.append(dsa[2])
            Reco_Mu.append(dsa[3])
        ############################################################################################################
        
        Reco_Mu.sort(key=lambda mu: mu.p4.pt(), reverse=True) # order list by muon pt

        ##Reco muon variables
        drlist = []
        if len(Reco_Mu) == 4: #Reco_Mu[0] is the leading muon
            pt1, pt2, pt3, pt4 = Reco_Mu[0].p4.pt(), Reco_Mu[1].p4.pt(), Reco_Mu[2].p4.pt(), Reco_Mu[3].p4.pt() # leading and sub pt
            d01, d02, d03, d04 = abs(Reco_Mu[0].d0), abs(Reco_Mu[1].d0), abs(Reco_Mu[2].d0), abs(Reco_Mu[3].d0)
            eta1, eta2, eta3, eta4 = Reco_Mu[0].p4.eta(), Reco_Mu[1].p4.eta(), Reco_Mu[2].p4.eta(), Reco_Mu[3].p4.eta()
            
            #get the pt of the muons
            self.Histos['%s/ptmu1'%chan].Fill(pt1)
            self.Histos['%s/ptmu2'%chan].Fill(pt2)
            self.Histos['%s/ptmu3'%chan].Fill(pt3)
            self.Histos['%s/ptmu4'%chan].Fill(pt4)            
            
            #dR between the combination of muons
            dr12 = DeltaR(Reco_Mu[0].p4,Reco_Mu[1].p4)
            dr13 = DeltaR(Reco_Mu[0].p4,Reco_Mu[2].p4)
            dr14 = DeltaR(Reco_Mu[0].p4,Reco_Mu[3].p4)
            dr23 = DeltaR(Reco_Mu[1].p4,Reco_Mu[2].p4)
            dr24 = DeltaR(Reco_Mu[1].p4,Reco_Mu[3].p4)
            dr34 = DeltaR(Reco_Mu[2].p4,Reco_Mu[3].p4)

            self.Histos['%s/dr12' % chan].Fill(dr12)
            self.Histos['%s/dr13' % chan].Fill(dr13)
            self.Histos['%s/dr14' % chan].Fill(dr14)
            self.Histos['%s/dr23' % chan].Fill(dr23)
            self.Histos['%s/dr24' % chan].Fill(dr24)
            self.Histos['%s/dr34' % chan].Fill(dr34)
            
            drlist.append(dr12)
            drlist.append(dr13)
            drlist.append(dr14)
            drlist.append(dr23)
            drlist.append(dr24)
            drlist.append(dr34)
            
            #minimum dR between the two pair of leptons in a lepton jet
            drmu =  min(drlist)
            self.Histos['%s/drmu' % chan].Fill(drmu)
            
            # trigger objects in the event
            TriObj = [TO for TO in event.trigobjs]
            #self.Histos['%s/nTOs' % chan].Fill(len(TriObj))
            TO_pass = []#list with TO passing a trigger
                
            # loop over all trigger objects in the event. If a trigger object pass a trigger filter append it to TO_pass 
            for j, TO in enumerate (TriObj):
                if TO.bit != 0 and (
                        abs(TO.bit) & (1<<0) > 0 or abs(TO.bit) & (1<<1) > 0 or abs(TO.bit) & (1<<2) > 0 or abs(TO.bit) & (1<<3) > 0 or abs(TO.bit) & (1<<4) > 0
                        or abs(TO.bit) & (1<<5)  > 0 or abs(TO.bit) & (1<<6)  > 0 or abs(TO.bit) & (1<<7)  > 0 or abs(TO.bit) & (1<<8)  > 0 or abs(TO.bit) & (1<<9)  > 0
                        or abs(TO.bit) & (1<<10) > 0 or abs(TO.bit) & (1<<11) > 0 or abs(TO.bit) & (1<<12) > 0 or abs(TO.bit) & (1<<13) > 0 or abs(TO.bit) & (1<<14) > 0
                        or abs(TO.bit) & (1<<15) > 0 or abs(TO.bit) & (1<<16) > 0 or abs(TO.bit) & (1<<17) > 0 or abs(TO.bit) & (1<<18) > 0 or abs(TO.bit) & (1<<19) > 0
                        or abs(TO.bit) & (1<<20) > 0 or abs(TO.bit) & (1<<21) > 0 or abs(TO.bit) & (1<<22) > 0 or abs(TO.bit) & (1<<23) > 0):
                    TO_pass.append(TriObj[j])
            self.Histos['%s/nTOspass' % chan].Fill(len(TO_pass))                        
            #########################################################################
            # At this point there are two lists: Reco_Mu contains the reco muons and TO_pass contains the TO that passed a trigger filter
            ####################################################################
            
            mu1, mu2, mu3, mu4 = 0, 1, 2, 3# index of the muons
            #mud0, to1, to2 = None, 9999, 9999
            
            #find delta R between reco mu "0" and its closest TO
            mindr1,to1 = 9999,9999
            for i, TO1 in enumerate(TO_pass):
                dr_to1mu1 = DeltaR(TO_pass[i].p4,Reco_Mu[mu1].p4) #calculate delra R between trigger object "k" and reco mu "1"
                if dr_to1mu1 < mindr1:
                    mindr1 = dr_to1mu1
                    if mindr1 < dR_thr:#matched
                        to1 = i   # TO at index i was matched to a RM[1]
                        mupt = pt1
                        mueta = eta1
                        mud0 = d01

            #find if muon2 was matched to TO                                                                                                                                              
            mindr2, to2 = 9999, 9999
            for j, TO2 in enumerate(TO_pass):                                                                       
                dr_to2mu2 = DeltaR(TO_pass[j].p4,Reco_Mu[mu2].p4)
                if dr_to2mu2 < mindr2:
                    mindr2 = dr_to2mu2
                    if mindr2 < dR_thr and j != to1:
                        to2 = j

            #find if muon3 was matched to TO
            mindr3, to3 = 9999, 9999
            for k, TO3 in enumerate(TO_pass):
                dr_to3mu3 = DeltaR(TO_pass[k].p4,Reco_Mu[mu3].p4)
                if dr_to3mu3 < mindr3:
                    mindr3 = dr_to3mu3
                    if mindr3 < dR_thr and k!=to1 and k!=to2:
                        to3 = k

            #find if muon4 was matched to TO
            mindr4, to4 = 9999, 9999
            for l, TO4 in enumerate(TO_pass):
                dr_to4mu4 = DeltaR(TO_pass[l].p4,Reco_Mu[mu4].p4)
                if dr_to4mu4 < mindr4:
                    mindr4 = dr_to4mu4
                    if mindr4 < dR_thr and l!=to1 and l!=to2 and l!=to3:
                        to3 = l
                        
            #Fill the Denominator and numerator
            if to1 != 9999:# muon 1 was matched to a TO
                self.Histos['%s/Tot_dR' % chan].Fill(drmu)
                self.Histos['%s/Tot_pT' % chan].Fill(mupt)
                self.Histos['%s/Tot_eta' % chan].Fill(mueta)
                self.Histos['%s/Tot_d0' % chan].Fill(mud0)

                if (to2 != 9999 and to2 != to1): #check if mu4 was matched to a TO
                    self.Histos['%s/Mat_dR'  % chan].Fill(drmu)
                    self.Histos['%s/Mat_pT'  % chan].Fill(mupt)
                    self.Histos['%s/Mat_eta' % chan].Fill(mueta)
                    self.Histos['%s/Mat_d0'  % chan].Fill(mud0)
                    
                    self.Histos['%s/Mat12' % chan].Fill(dr12)

                elif (to3!=9999 and to3!=to1): #check if mu4 was matched to a TO
                    self.Histos['%s/Mat_dR'  % chan].Fill(drmu)
                    self.Histos['%s/Mat_pT'  % chan].Fill(mupt)
                    self.Histos['%s/Mat_eta' % chan].Fill(mueta)
                    self.Histos['%s/Mat_d0'  % chan].Fill(mud0)
                    
                    self.Histos['%s/Mat13' % chan].Fill(dr13)

                elif (to4!=9999 and to4!=to1): #check if mu4 was matched to a TO
                    self.Histos['%s/Mat_dR'  % chan].Fill(drmu)
                    self.Histos['%s/Mat_pT'  % chan].Fill(mupt)
                    self.Histos['%s/Mat_eta' % chan].Fill(mueta)
                    self.Histos['%s/Mat_d0'  % chan].Fill(mud0)
                    
                    self.Histos['%s/Mat14' % chan].Fill(dr14)
                    
histCollection = [
    { 'name': 'dsaMu_d0',           'binning': (20, 0, 70),          'title': '|d_{0}| dsa muons; |d_{0}|[cm]; Events'},
    { 'name': 'dsaMu_pT',           'binning': (100, 0,800),         'title': 'p_{T}  dsa muons; p_{T} [GeV]; Entries'},
    { 'name': 'dsaMu_eta',          'binning': (30,-3.5,3.5),        'title': '#eta dsa muons; #eta_{dsa}; Entries'},
    
    { 'name': 'pfMu_d0',            'binning': (10, 0, 25),          'title': '|d_{0}| pf muons; |d_{0}|[cm]; Entries'},
    { 'name': 'pfMu_pT',            'binning': (100, 0,800),         'title': 'p_{T}  pf muons; p_{T} [GeV]; Entries'},
    { 'name': 'pfMu_eta',           'binning': (25,-3.5,3.5),        'title': '#eta pf muons; #eta_{pf}; Entries'},

    { 'name': 'npfMuons',           'binning': (8, -2.0,6.0),        'title': 'number of pf Muons; nMuons; Entries'},
    { 'name': 'ndsaMuons',          'binning': (8, -2.0,6.0),        'title': 'number of dsa Muons; nMuons; Entries'},
    { 'name': 'nMuons',             'binning': (8, -2.0,6.0),        'title': 'number of Muons; nMuons; Entries'},

    #{ 'name': 'drdsa',              'binning': (30, 0.0,0.4),        'title': '#Delta R dsa muons; #Delta R(dsa,dsa); Entries'},
    #{ 'name': 'drboth',             'binning': (30, 0.0,0.4),        'title': '#Delta R pf and dsa muons; #Delta R(pf,dsa); Entries'},
    #{ 'name': 'drpf',               'binning': (30, 0.0,0.4),        'title': '#Delta R pf  muons; #Delta R(pf,pf); Entries'},

    { 'name': 'ptmu1',              'binning': (100, 0,600),         'title': 'p_{T} Leading muon; p_{T} [GeV]; Entries'},
    { 'name': 'ptmu2',              'binning': (100, 0,600),         'title': 'p_{T} Second muon; p_{T} [GeV]; Entries'},
    { 'name': 'ptmu3',              'binning': (100, 0,600),         'title': 'p_{T} Third muon; p_{T} [GeV]; Entries'},
    { 'name': 'ptmu4',              'binning': (100, 0,600),         'title': 'p_{T} Fourth muon; p_{T} [GeV]; Entries'},

    { 'name': 'dr12',               'binning': (25, 0, 5),           'title': '#Delta R (1,2); #Delta R; Entries'},
    { 'name': 'dr13',               'binning': (25, 0, 5),           'title': '#Delta R (1,3); #Delta R; Entries'},
    { 'name': 'dr14',               'binning': (25, 0, 5),           'title': '#Delta R (1,4); #Delta R; Entries'},
    { 'name': 'dr23',               'binning': (25, 0, 5),           'title': '#Delta R (2,3); #Delta R; Entries'},
    { 'name': 'dr24',               'binning': (25, 0, 5),           'title': '#Delta R (2,4); #Delta R; Entries'},
    { 'name': 'dr34',               'binning': (25, 0, 5),           'title': '#Delta R (3,4); #Delta R; Entries'},
    { 'name': 'drmu',               'binning': (25, 0, 0.5),         'title': 'Min #Delta R; #Delta R; Entries'},

    { 'name': 'Mat12',              'binning': (25, 0, 5),           'title': '#Delta R (1,2); #Delta R; Entries'},
    { 'name': 'Mat13',              'binning': (25, 0, 5),           'title': '#Delta R (1,3); #Delta R; Entries'},
    { 'name': 'Mat14',              'binning': (25, 0, 5),           'title': '#Delta R (1,4); #Delta R; Entries'},

    { 'name': 'nTOspass',           'binning': (20, 0,50),           'title': 'number of trigger objects; nTOs; Entries'},

    #{ 'name': 'subleadpt',          'binning': (100, 0,600),           'title': 'p_{T} subleading muon; p_{T} [GeV]; Entries'},
    #{ 'name': 'Mumass',             'binning': (30, 0, 10),            'title': 'mass distribution for reco  muons; m [GeV]; Entries'},
    #{ 'name': 'ReMu_d0',            'binning': (20, 0, 70),          'title': '|d_{0}| reco muons; |d_{0}|[cm]; Entries'},
    #{ 'name': 'drmu',               'binning': (100, 0, 0.4),          'title': '#Delta R between #mu; #Delta R(#mu_{1},#mu_{2}); Entries'},
    #{ 'name': 'nTOs',               'binning': (20, 0,50),             'title': 'number of trigger objects; nTOs; Entries'},
    #{ 'name': 'drto',               'binning': (50,0,0.4),  	       'title': '#Delta R between all TOs; #Delta R(TO_{i},TO_{j}); #Delta R (TO,#mu_{1})'},
     
    { 'name': 'Mat_dR',          'binning': [[0.0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4,]],         'title': '#Delta R matched; #Delta R(#mu_{1},#mu_{2}); Entries'},
    { 'name': 'Tot_dR',          'binning': [[0.0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4,]],         'title': '#Delta R total; #Delta R(#mu_{1},#mu_{2}); Entries'},
    { 'name': 'Mat_pT',          'binning': [[0,30,60,90,120,160,200, 300, 400, 500, 600, 700]],         'title': 'p_{T} matched; p_{T} [GeV]; Entries'},
    { 'name': 'Tot_pT',          'binning': [[0,30,60,90,120,160,200, 300, 400, 500, 600, 700]],         'title': 'p_{T} total; p_{T} [GeV]; Entries'},
    { 'name': 'Mat_eta',         'binning': (25,-3.5,3.5),          'title': '#eta matched ; #eta; Entries'},
    { 'name': 'Tot_eta',         'binning': (25,-3.5,3.5),          'title': '#eta total; #eta; Entries'},
    { 'name': 'Mat_d0',   	 'binning': (20, 0, 70),          'title': '|d_{0}| matched; |d_{0}|[cm]; Entries'},
    { 'name': 'Tot_d0',          'binning': (20, 0, 70),          'title': '|d_{0}| total; |d_{0}|[cm]; Entries'},
    
    #{ 'name': 'TO_Num_dRd0l2',          'binning': (16, 0.0, 0.4),         'title': '#Delta R matched for d_{0}<200; #Delta R(#mu_{1},#mu_{2}); Entries'},
    #{ 'name': 'TO_Den_dRd0l2',          'binning': (16, 0.0, 0.4),         'title': '#Delta R total for d_{0}<200; #Delta R(#mu_{1},#mu_{2}); Entries'},
    #{ 'name': 'TO_Num_dRd0l5',          'binning': (16, 0.0, 0.4),         'title': '#Delta R matched for d_{0} > 200 and <500; #Delta R(#mu_{1},#mu_{2}); Entries'},
    #{ 'name': 'TO_Den_dRd0l5',          'binning': (16, 0.0, 0.4),         'title': '#Delta R total for d_{0} > 200 and <500; #Delta R(#mu_{1},#mu_{2}); Entries'},
    #{ 'name': 'TO_Num_dRd0m5',          'binning': (16, 0.0, 0.4),         'title': '#Delta R matched for d_{0}>500; #Delta R(#mu_{1},#mu_{2}); Entries'},
    #{ 'name': 'TO_Den_dRd0m5',          'binning': (16, 0.0, 0.4),         'title': '#Delta R total for d_{0}>500; #Delta R(#mu_{1},#mu_{2}); Entries'},

    #{ 'name': 'TO_Num_pTd0l2',          'binning': [[0,5,10,15,20,25,30,35,40,50,60,70,80, 90, 100, 150, 200]],         'title': 'p_{T} matched for d_{0}<200; p_{T} [GeV]; Entries'},
    #{ 'name': 'TO_Den_pTd0l2',          'binning': [[0,5,10,15,20,25,30,35,40,50,60,70,80, 90, 100, 150, 200]],         'title': 'p_{T} total for d_{0}<200; p_{T} [GeV]; Entries'},
    #{ 'name': 'TO_Num_pTd0l5',          'binning': [[0,5,10,15,20,25,30,35,40,50,60,70,80, 90, 100, 150, 200]],         'title': 'p_{T} matched for d_{0}<500; p_{T} [GeV]; Entries'},
    #{ 'name': 'TO_Den_pTd0l5',          'binning': [[0,5,10,15,20,25,30,35,40,50,60,70,80, 90, 100, 150, 200]],         'title': 'p_{T} total for d_{0}<500; p_{T} [GeV]; Entries'},
    #{ 'name': 'TO_Num_pTd0m5',          'binning': [[0,5,10,15,20,25,30,35,40,50,60,70,80, 90, 100, 150, 200]],         'title': 'p_{T} matched for d_{0}>500; p_{T} [GeV]; Entries'},
    #{ 'name': 'TO_Den_pTd0m5',          'binning': [[0,5,10,15,20,25,30,35,40,50,60,70,80, 90, 100, 150, 200]],         'title': 'p_{T} total for d_{0}>500; p_{T} [GeV]; Entries'},

    #{ 'name': 'leadptrb',             'binning': [[0, 10, 15, 20, 30, 40, 60, 80, 100]],           'title': 'p_{T} Leading muon; p_{T} [GeV]; Entries'},
    #{ 'name': 'leadptl30',          'binning': (10, 0.0, 35), 'title': 'p_{T} < 30 Leading muon; p_{T} [GeV]; Entries'},
    #{ 'name': 'leadptl100',          'binning': (10, 20.0, 120), 'title': 'p_{T} > 30 and < 100 Leading muon; p_{T} [GeV]; Entries'},
    #{ 'name': 'leadptm100',          'binning': (30, 90.0, 600), 'title': 'p_{T} > 100 Leading muon; p_{T} [GeV]; Entries'},
    
    #{ 'name': 'dr_to1mu1',          'binning': (50,0,0.5, 50,0,0.4),   'title': '#Delta R between TO and #mu_{1}; #Delta R(#mu_{1},#mu_{2}); #Delta R (TO1,#mu_{1})'},
    #{ 'name': 'dr_to2mu2',          'binning': (50,0,0.5, 50,0,0.4),    'title': '#Delta R between TO and #mu_{2}; #Delta R(#mu_{1},#mu_{2}); #Delta R (TO2,#mu_{2})'},
    #{ 'name': 'dr_to1mu1vto2mu2',   'binning': (50,0,0.5, 50,0,0.4),   'title': '#Delta R to1mu1 vs #Delta R (to2,mu2) matched; #Delta R(to1,#mu_{1}); #Delta R(to2,#mu_{2})'},
    #{ 'name': 'dr_to1to2',          'binning': (50, 0, 0.4),           'title': '#Delta R between matched TO; #Delta R(TO_{1},TO_{2}); Entries'},
    #{ 'name': 'dr_to1mu2vto2mu1',   'binning': (50,0,0.5, 50,0,0.4),   'title': '#Delta R (to1,mu2) vs #Delta R (to2,mu1) matched; #Delta R(to1,#mu_{2}); #Delta R(to2,#mu_{1})'},
    
    #{ 'name': 'ptpf',         'binning': (100, -100,100),       'title': 'pf muon p_{T} difference; p_{T} [GeV]; Number of entries'},
    #{ 'name': 'ptboth',       'binning': (100, -100,100),       'title': 'both muon p_{T} difference; p_{T} [GeV]; Number of entries'},
    #{ 'name': 'ptdsa',        'binning': (100, -100,100),       'title': 'dsa muon p_{T} difference; p_{T} [GeV]; Number of entries'},
    #{ 'name': 'ljmass',       'binning': (100, 50, 1200),       'title': 'mass distribution for lj; m [GeV]; number of entries'},
    #{ 'name': 'RM_dR',        'binning': [[0,0.02,0.04,0.06,0.08,0.1,0.15,0.2,.3,.4,]],     'title': '#Delta R of Reco muons; #Delta R; Number of entries'},
    #{ 'name': 'TO_bit',       'binning': (100, -50.0,50),                  'title': 'Trigger object ID ; TO ID; Number of entries'},
    #{ 'name': 'TO_pT',        'binning': (50, 0.0,500),                    'title': 'TO p_{T} distribution;  p_{T} [GeV]; Number of entries'},
]

