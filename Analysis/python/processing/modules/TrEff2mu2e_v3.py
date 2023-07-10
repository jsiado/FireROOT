#!/usr/bin/env python
# Reco_Mu: reco muon, TO: trigger object, LJ: lepton jet

''' output as out_53.root
change d0 to cm in all plots
and make all new plots'''


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
        
        ############
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
        #self.Histos['%s/nMuons' % chan].Fill(-3)
        #print(lpf+ldsa)
        

        #############################################################################################
        #Join pf and dsa muons in a single list, Reco_Mu
        #############################################################################################
        if lpf ==2:
            Reco_Mu.append(pf[0])
            Reco_Mu.append(pf[1])
            self.Histos['%s/drpf' % chan].Fill(DeltaR(Reco_Mu[0].p4,Reco_Mu[1].p4))

        elif lpf == 1:#order by pt instead of which collection the muon is drawn from
            if pf[0].p4.pt()> dsa[0].p4.pt():
                Reco_Mu.append(pf[0])
                Reco_Mu.append(dsa[0])
            else:
                Reco_Mu.append(dsa[0])
                Reco_Mu.append(pf[0])
            self.Histos['%s/drboth' % chan].Fill(DeltaR(Reco_Mu[0].p4,Reco_Mu[1].p4))
            
        elif ldsa == 2:
            Reco_Mu.append(dsa[0])
            Reco_Mu.append(dsa[1])
            self.Histos['%s/drdsa' % chan].Fill(DeltaR(Reco_Mu[0].p4,Reco_Mu[1].p4))
        ############################################################################################################
        
        #if lpf == 
        
        ##Reco muon variables
        if len(Reco_Mu) == 2:#Reco_Mu[0] is the leading muon
            pt1, pt2 = Reco_Mu[0].p4.pt(), Reco_Mu[1].p4.pt() # leading and sub pt
            d01, d02 = abs(Reco_Mu[0].d0), abs(Reco_Mu[1].d0)
            eta1, eta2 = Reco_Mu[0].p4.eta(), Reco_Mu[1].p4.eta()

            self.Histos['%s/leadpt'%chan].Fill(pt1) #leading pt
            self.Histos['%s/leadptrb'%chan].Fill(pt1) #rebin the pt plot for leading
            self.Histos['%s/subleadpt'%chan].Fill(pt2) #subleading pt
            
            if pt1 < 30:
                self.Histos['%s/leadptl30'%chan].Fill(pt1) #check how many leading mu with pt < 10
            elif pt1 < 100: #check how many leading mu with 30 <= pt < 100
                self.Histos['%s/leadptl100'%chan].Fill(pt1)
            else: #check how many leading mu with pt > 100
                self.Histos['%s/leadptm100'%chan].Fill(pt1)

            self.Histos['%s/Mumass' % chan].Fill((Reco_Mu[0].p4+Reco_Mu[1].p4).M())#invariant mass of the two muons
            
            #d0 dist for the two muons
            self.Histos['%s/ReMu_d0' % chan].Fill(d01) 
            self.Histos['%s/ReMu_d0' % chan].Fill(d02)
            
            drmu = DeltaR(Reco_Mu[0].p4,Reco_Mu[1].p4)#Delta R between the two muons
            self.Histos['%s/drmu' % chan].Fill(drmu)
            
            # get the trigger objects in the event
            TriObj = [TO for TO in event.trigobjs]
            self.Histos['%s/nTOs' % chan].Fill(len(TriObj))
            TO_pass = []#iniatialize list with TO passing a trigger
                
            # loop over all trigger objects in the event. If a trigger object pass a trigger filter append it to TO_pass 
            for j, TO in enumerate (TriObj):
                if TO.bit != 0 and (
                        abs(TO.bit) & (1<<0) > 0 or abs(TO.bit) & (1<<1) > 0 or abs(TO.bit) & (1<<2) > 0 or abs(TO.bit) & (1<<3) > 0 or abs(TO.bit) & (1<<4) > 0
                        or abs(TO.bit) & (1<<5)  > 0 or abs(TO.bit) & (1<<6)  > 0 or abs(TO.bit) & (1<<7)  > 0 or abs(TO.bit) & (1<<8)  > 0 or abs(TO.bit) & (1<<9)  > 0
                        or abs(TO.bit) & (1<<10) > 0 or abs(TO.bit) & (1<<11) > 0 or abs(TO.bit) & (1<<12) > 0 or abs(TO.bit) & (1<<13) > 0 or abs(TO.bit) & (1<<14) > 0
                        or abs(TO.bit) & (1<<15) > 0 or abs(TO.bit) & (1<<16) > 0 or abs(TO.bit) & (1<<17) > 0 or abs(TO.bit) & (1<<18) > 0 or abs(TO.bit) & (1<<19) > 0
                        or abs(TO.bit) & (1<<20) > 0 or abs(TO.bit) & (1<<21) > 0 or abs(TO.bit) & (1<<22) > 0 or abs(TO.bit) & (1<<23) > 0):
                    TO_pass.append(TriObj[j])
                    
            ##### calculate dR between all trigger objects
            for i, to in enumerate(TO_pass):
                for j, tov in enumerate (TO_pass):
                    if i != j:
                        drto = DeltaR(TO_pass[i].p4,TO_pass[j].p4)
                        self.Histos['%s/drto' % chan].Fill(drto) #check that not same TO are used 

            #########################################################################
            # At this point there are two lists: Reco_Mu contains the reco muons and TO_pass contains the TO that passed a trigger filter
            ####################################################################

            # To calculate the efficiecny Take the a muon a match it to TO 
            # Then take the second muon and match it to a different TO
            #        # of both muons matched
            # eff = --------------------------
            #        # of events with 1mu matched
            #

            mu1, mu2 = 1, 0 # index of the muons
            mud0, to1, to2 = None, 9999, 9999
            
            #find delta R between reco mu "0" and its closest TO
            mindr,to1 = 9999,9999
            for k, TO in enumerate(TO_pass):
                dr_to1mu1 = DeltaR(TO_pass[k].p4,Reco_Mu[mu1].p4) #calculate delra R between trigger object "k" and reco mu "1"
                if dr_to1mu1 < mindr:
                    mindr = dr_to1mu1
                    if mindr < dR_thr:# matched
                        to1 = k   # TO at index k was matched to a RM[1]
                        mupt = pt1
                        mueta = eta1
                        mud0 = d01
                        dr11 = mindr #dr(to1,mu1)
                        
            if to1 != 9999:#store variables related to muon 1
                dr12 = DeltaR(TO_pass[to1].p4,Reco_Mu[mu2].p4) #dr(to1,mu2)
                self.Histos['%s/Tot_dR'  %chan].Fill(drmu)
                self.Histos['%s/Tot_pT'  %chan].Fill(mupt)
                self.Histos['%s/Tot_eta' %chan].Fill(mueta)
                self.Histos['%s/Tot_d0'  %chan].Fill(mud0)
                self.Histos['%s/dr_to1mu1'  %chan].Fill(drmu,dr11) #dr matched (to1,mu1) vs dr(mu1,mu2)
                
                if mud0 < 10000:
                    self.Histos['%s/Tot_dRfbin' % chan].Fill(drmu)
                
                #fill different ranges of dR
                if mud0 < 0.02:
                    self.Histos['%s/Tot_dRd0l2' % chan].Fill(drmu)
                    self.Histos['%s/Tot_pTd0l2' % chan].Fill(mupt)
                    
                elif mud0 < 0.05:
                    self.Histos['%s/Tot_dRd0l5' % chan].Fill(drmu)
                    self.Histos['%s/Tot_pTd0l5' % chan].Fill(mupt)
                else:
                    self.Histos['%s/Tot_dRd0m5' % chan].Fill(drmu)
                    self.Histos['%s/Tot_pTd0m5' % chan].Fill(mupt) 

                    
                #find min dr between the second muon and its closest TO
                mindr2, to2 = 9999, 9999
                for l, to in enumerate(TO_pass): #loop over all TO_pass again now with RM[2] to see if there is a match
                    dr_to2mu2 = DeltaR(TO_pass[l].p4,Reco_Mu[mu2].p4)
                    if dr_to2mu2 < mindr2:
                        mindr2 = dr_to2mu2
                        if mindr2 < dR_thr and l != to1: #making sure TO1 is different than TO2
                            to2 = l
                            dr22 = mindr2 #dR(to2,mu2)
                            
                if to2 != 9999 and to1 != to2: #check if the index of the second loop is different that 'to1' index of the TO matched to RM[1]
                    dr_to1to2 = DeltaR(TO_pass[to1].p4,TO_pass[to2].p4)  #dR(to1,to2)
                    dr21 = DeltaR(TO_pass[to2].p4,Reco_Mu[mu1].p4) #dr(to2,mu1)
                    self.Histos['%s/Mat_dR'  % chan].Fill(drmu)
                    self.Histos['%s/Mat_pT'  % chan].Fill(mupt)
                    self.Histos['%s/Mat_eta' % chan].Fill(mueta)
                    self.Histos['%s/Mat_d0'  % chan].Fill(mud0)
                    self.Histos['%s/dr_to2mu2'  % chan].Fill(drmu,dr22) #to2 match to mu2 vs dr (mu1,mu2)
                    self.Histos['%s/dr_to1to2'  % chan].Fill(dr_to1to2) #1d hist
                    self.Histos['%s/dr_to1mu1vto2mu2'  % chan].Fill(dr11,dr22) #dr(to1mu1) vs dr(to2mu2)
                    self.Histos['%s/dr_to1mu2vto2mu1'  % chan].Fill(dr12,dr21) #
                    
                    if mud0< 10000:
                        self.Histos['%s/Mat_dRfbin' % chan].Fill(drmu)

                    if mud0 < 0.02:
                        self.Histos['%s/Mat_dRd0l2' % chan].Fill(drmu)
                        self.Histos['%s/Mat_pTd0l2' % chan].Fill(mupt)
                    elif mud0 < 0.05:
                        self.Histos['%s/Mat_dRd0l5' % chan].Fill(drmu)
                        self.Histos['%s/Mat_pTd0l5' % chan].Fill(mupt)
                    else:
                        self.Histos['%s/Mat_dRd0m5' % chan].Fill(drmu)
                        self.Histos['%s/Mat_pTd0m5' % chan].Fill(mupt)




histCollection = [
    { 'name': 'dsaMu_d0',           'binning': (20, 0, 70),            'title': '|d_{0}| dsa muons; |d_{0}|[cm]; Events'},
    { 'name': 'dsaMu_pT',           'binning': (100, 0,800),           'title': 'p_{T}  dsa muons; p_{T} [GeV]; Entries'},
    { 'name': 'dsaMu_eta',          'binning': (30,-3.5,3.5),          'title': '#eta dsa muons; #eta_{dsa}; Entries'},
    { 'name': 'pfMu_d0',            'binning': (10, 0, 25),            'title': '|d_{0}| pf muons; |d_{0}|[cm]; Entries'},
    { 'name': 'pfMu_pT',            'binning': (100, 0,800),           'title': 'p_{T}  pf muons; p_{T} [GeV]; Entries'},
    { 'name': 'pfMu_eta',           'binning': (25,-3.5,3.5),          'title': '#eta pf muons; #eta_{pf}; Entries'},
    #{ 'name': 'nMuons',             'binning': (5, -5.0,5.0),          'title': 'number of Muons; nMuons; Entries'},
    { 'name': 'drdsa',              'binning': (30, 0.0,0.4),          'title': '#Delta R dsa muons; #Delta R(dsa,dsa); Entries'},
    { 'name': 'drboth',             'binning': (30, 0.0,0.4),          'title': '#Delta R pf and dsa muons; #Delta R(pf,dsa); Entries'},
    { 'name': 'drpf',               'binning': (30, 0.0,0.4),          'title': '#Delta R pf  muons; #Delta R(pf,pf); Entries'},
    { 'name': 'leadpt',             'binning': (100, 0,600),           'title': 'p_{T} Leading muon; p_{T} [GeV]; Entries'},
    { 'name': 'subleadpt',          'binning': (100, 0,600),           'title': 'p_{T} subleading muon; p_{T} [GeV]; Entries'},
    { 'name': 'Mumass',             'binning': (30, 0, 10),            'title': 'mass distribution for reco  muons; m [GeV]; Entries'},
    { 'name': 'ReMu_d0',            'binning': (20, 0, 70),            'title': '|d_{0}| reco muons; |d_{0}|[cm]; Entries'},
    { 'name': 'drmu',               'binning': (100, 0, 0.4),          'title': '#Delta R between #mu; #Delta R(#mu_{1},#mu_{2}); Entries'},
    { 'name': 'nTOs',               'binning': (20, 0,50),             'title': 'number of trigger objects; nTOs; Entries'},
    { 'name': 'drto',               'binning': (50,0,0.4),  	       'title': '#Delta R between all TOs; #Delta R(TO_{i},TO_{j}); #Delta R (TO,#mu_{1})'},
     

    { 'name': 'Mat_pT',          'binning': [[0,30,60,90,120,160,200, 300, 400, 500, 600, 700]],         'title': 'p_{T} matched; p_{T} [GeV]; Entries'},
    { 'name': 'Tot_pT',          'binning': [[0,30,60,90,120,160,200, 300, 400, 500, 600, 700]],         'title': 'p_{T} total; p_{T} [GeV]; Entries'},
    { 'name': 'Mat_eta',         'binning': (25,-3.5,3.5),          'title': '#eta matched ; #eta; Entries'},
    { 'name': 'Tot_eta',         'binning': (25,-3.5,3.5),          'title': '#eta total; #eta; Entries'},
    { 'name': 'Mat_d0',   	    'binning': (20, 0, 70),          'title': '|d_{0}| matched; |d_{0}|[cm]; Entries'},
    { 'name': 'Tot_d0',          'binning': (20, 0, 70),          'title': '|d_{0}| total; |d_{0}|[cm]; Entries'},
    
    { 'name': 'Mat_dR',        'binning': [[0.,0.02,0.04, 0.06,0.08,0.1, 0.15,0.2,0.25, 0.3,0.4,]],  'title':'#Delta R matched; #Delta R(#mu_{1},#mu_{2}); Entries'},
    { 'name': 'Tot_dR',        'binning': [[0.,0.02,0.04, 0.06,0.08,0.1, 0.15,0.2,0.25, 0.3,0.4,]],  'title':'#Delta R total; #Delta R(#mu_{1},#mu_{2}); Entries'},
    { 'name': 'Mat_dRd0l2',    'binning': [[0.,0.02,0.04, 0.06,0.08,0.1, 0.15,0.2,0.25, 0.3,0.4,]],  'title':'#Delta R matched d_{0}<200; #Delta R(#mu_{1},#mu_{2}); Entries'},
    { 'name': 'Tot_dRd0l2',    'binning': [[0.,0.02,0.04, 0.06,0.08,0.1, 0.15,0.2,0.25, 0.3,0.4,]],  'title':'#Delta R total d_{0}<200; #Delta R(#mu_{1},#mu_{2}); Entries'},
    { 'name': 'Mat_dRd0l5',    'binning': [[0.,0.02,0.04, 0.06,0.08,0.1, 0.15,0.2,0.25, 0.3,0.4,]],  'title':'#Delta R matched d_{0} > 200 and <500; #Delta R(#mu_{1},#mu_{2}); Entries'},
    { 'name': 'Tot_dRd0l5',    'binning': [[0.,0.02,0.04, 0.06,0.08,0.1, 0.15,0.2,0.25, 0.3,0.4,]],  'title':'#Delta R total d_{0} > 200 and <500; #Delta R(#mu_{1},#mu_{2}); Entries'},
    { 'name': 'Mat_dRd0m5',    'binning': [[0.,0.02,0.04, 0.06,0.08,0.1, 0.15,0.2,0.25, 0.3,0.4,]],  'title':'#Delta R matched d_{0}>500; #Delta R(#mu_{1},#mu_{2}); Entries'},
    { 'name': 'Tot_dRd0m5',    'binning': [[0.,0.02,0.04, 0.06,0.08,0.1, 0.15,0.2,0.25, 0.3,0.4,]],  'title':'#Delta R total d_{0}>500; #Delta R(#mu_{1},#mu_{2}); Entries'},
    { 'name': 'Mat_dRfbin',    'binning': [[0.,0.02,0.04, 0.06,0.08,0.1, 0.15,0.2,0.25, 0.3,0.4,]],  'title':'#Delta R matched d_{0} extended; #Delta R(#mu_{1},#mu_{2}); Entries'},
    { 'name': 'Tot_dRfbin',    'binning': [[0.,0.02,0.04, 0.06,0.08,0.1, 0.15,0.2,0.25, 0.3,0.4,]],  'title':'#Delta R total d_{0} extended; #Delta R(#mu_{1},#mu_{2}); Entries'},

    { 'name': 'Mat_pTd0l2',          'binning': [[0,5,10,15,20,25,30,35,40,50,60,70,80, 90, 100, 150, 200]],         'title': 'p_{T} matched for d_{0}<200; p_{T} [GeV]; Entries'},
    { 'name': 'Tot_pTd0l2',          'binning': [[0,5,10,15,20,25,30,35,40,50,60,70,80, 90, 100, 150, 200]],         'title': 'p_{T} total for d_{0}<200; p_{T} [GeV]; Entries'},
    { 'name': 'Mat_pTd0l5',          'binning': [[0,5,10,15,20,25,30,35,40,50,60,70,80, 90, 100, 150, 200]],         'title': 'p_{T} matched for d_{0}<500; p_{T} [GeV]; Entries'},
    { 'name': 'Tot_pTd0l5',          'binning': [[0,5,10,15,20,25,30,35,40,50,60,70,80, 90, 100, 150, 200]],         'title': 'p_{T} total for d_{0}<500; p_{T} [GeV]; Entries'},
    { 'name': 'Mat_pTd0m5',          'binning': [[0,5,10,15,20,25,30,35,40,50,60,70,80, 90, 100, 150, 200]],         'title': 'p_{T} matched for d_{0}>500; p_{T} [GeV]; Entries'},
    { 'name': 'Tot_pTd0m5',          'binning': [[0,5,10,15,20,25,30,35,40,50,60,70,80, 90, 100, 150, 200]],         'title': 'p_{T} total for d_{0}>500; p_{T} [GeV]; Entries'},

    { 'name': 'leadptrb',              'binning': [[0, 10, 15, 20, 30, 40, 60, 80, 100]],           'title': 'p_{T} Leading muon; p_{T} [GeV]; Entries'},
    { 'name': 'leadptl30',             'binning': (10, 0.0, 35), 'title': 'p_{T} < 30 Leading muon; p_{T} [GeV]; Entries'},
    { 'name': 'leadptl100',            'binning': (10, 20.0, 120), 'title': 'p_{T} > 30 and < 100 Leading muon; p_{T} [GeV]; Entries'},
    { 'name': 'leadptm100',            'binning': (30, 90.0, 600), 'title': 'p_{T} > 100 Leading muon; p_{T} [GeV]; Entries'},
    
    { 'name': 'dr_to1mu1',          'binning': (50,0,0.5, 50,0,0.4),   'title': '#Delta R between TO and #mu_{1}; #Delta R(#mu_{1},#mu_{2}); #Delta R (TO1,#mu_{1})'},
    { 'name': 'dr_to2mu2',          'binning': (50,0,0.5, 50,0,0.4),    'title': '#Delta R between TO and #mu_{2}; #Delta R(#mu_{1},#mu_{2}); #Delta R (TO2,#mu_{2})'},
    { 'name': 'dr_to1mu1vto2mu2',   'binning': (50,0,0.5, 50,0,0.4),   'title': '#Delta R to1mu1 vs #Delta R (to2,mu2) matched; #Delta R(to1,#mu_{1}); #Delta R(to2,#mu_{2})'},
    { 'name': 'dr_to1to2',          'binning': (50, 0, 0.4),           'title': '#Delta R between matched TO; #Delta R(TO_{1},TO_{2}); Entries'},
    { 'name': 'dr_to1mu2vto2mu1',   'binning': (50,0,0.5, 50,0,0.4),   'title': '#Delta R (to1,mu2) vs #Delta R (to2,mu1) matched; #Delta R(to1,#mu_{2}); #Delta R(to2,#mu_{1})'},
    
    #{ 'name': 'ptpf',         'binning': (100, -100,100),       'title': 'pf muon p_{T} difference; p_{T} [GeV]; Number of entries'},
    #{ 'name': 'ptboth',       'binning': (100, -100,100),       'title': 'both muon p_{T} difference; p_{T} [GeV]; Number of entries'},
    #{ 'name': 'ptdsa',        'binning': (100, -100,100),       'title': 'dsa muon p_{T} difference; p_{T} [GeV]; Number of entries'},
    #{ 'name': 'ljmass',       'binning': (100, 50, 1200),       'title': 'mass distribution for lj; m [GeV]; number of entries'},
    #{ 'name': 'RM_dR',        'binning': [[0,0.02,0.04,0.06,0.08,0.1,0.15,0.2,.3,.4,]],     'title': '#Delta R of Reco muons; #Delta R; Number of entries'},
    #{ 'name': 'TO_bit',       'binning': (100, -50.0,50),                  'title': 'Trigger object ID ; TO ID; Number of entries'},
    #{ 'name': 'TO_pT',        'binning': (50, 0.0,500),                    'title': 'TO p_{T} distribution;  p_{T} [GeV]; Number of entries'},
]

