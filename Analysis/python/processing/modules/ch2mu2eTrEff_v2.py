#!/usr/bin/env python
# Reco_Mu: reco muon, TO: trigger object, LJ: lepton jet

'''
Tr eff after the jamboree and redefine the efficiency
1. get reco and gen muons. plot some quantities to check their distributions
'''


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

        reco_mu, dsa_mu, pf_mu = [], [], []

        gmus = [mu for mu in event.gens \
            if abs(mu.pid)==13 \
                and mu.p4.pt()>10\
                and abs(mu.p4.eta())<2.4\
                and mu.vtx.Rho()<700]

        self.Histos['%s/ngenall' % chan].Fill(len(gmus))
        if len(gmus) < 2: return
        self.Histos['%s/ngen' % chan].Fill(len(gmus))
        self.Histos['%s/gen_dR'%chan].Fill(DeltaR(gmus[0].p4,gmus[1].p4))
        self.Histos['%s/gen_Mass'%chan].Fill((gmus[0].p4 + gmus[1].p4).M())
        
        r1, r2 = None, None #match reco muons to gen muons
        self.Histos['%s/gen_pT'%chan].Fill(gmus[0].p4.pt())
        self.Histos['%s/gen_pT'%chan].Fill(gmus[1].p4.pt())
            
        for mu in event.muons: #pf muons
            if mu.p4.pt() < 5: continue
            if abs(mu.p4.eta()) > 2.4: continue
            pf_mu.append(mu)
            reco_mu.append(mu)
            self.Histos['%s/pf_pT'%chan].Fill(mu.p4.pt())

        for dsa in event.dsamuons: #dsamuons
            if dsa.p4.pt() < 10: continue
            if abs(dsa.p4.eta()) > 2.4: continue
            dsa_mu.append(dsa)
            reco_mu.append(dsa)
            self.Histos['%s/dsa_pT'%chan].Fill(dsa.p4.pt())

        self.Histos['%s/ndsa'%chan].Fill(len(dsa_mu))
        self.Histos['%s/npf'%chan].Fill(len(pf_mu))
        self.Histos['%s/nreco'%chan].Fill(len(reco_mu))
            
        reco_mu.sort(key=lambda mu: mu.p4.pt(), reverse=True) # sort muons by pt
        
        #start matching all those reco muons to gen muons
        drthr, min1, ptg1, ptg2, m1 = 0.4, 999, gmus[0].p4.pt(), gmus[1].p4.pt(), None
        for r, rmu in enumerate(reco_mu):
            dr = DeltaR(gmus[0].p4,rmu.p4)
            ptr = rmu.p4.pt()
            if ptr > 0.9*ptg1 and ptr < 1.1*ptg1 and dr < min1:
                min1 = dr
                if min1 < drthr:
                    m1 = r # index of reco muon matched to the leading gen muon
                    ptr1 = ptr
                    #print(min1, pt_r, ptg1)

        if m1 is not None: # there was a matched
            #print(m1)
            self.Histos['%s/lgen_pT_matched'%chan].Fill(ptg1)
            #self.Histos['%s/lreco_pT_matched'%chan].Fill(ptr1)
        

        min2, m2 = 999, None
        for r, rmu in enumerate(reco_mu):
            dr = DeltaR(gmus[1].p4,rmu.p4)
            ptr = rmu.p4.pt()
            if ptr > 0.9*ptg2 and ptr < 1.1*ptg2 and dr < min2:
                min2 = dr
                if min2< drthr:
                    m2 = r # index of reco muon matched to the leading gen muon
                    ptr2 = ptr

        if m2 is not None:
            self.Histos['%s/sgen_pT_matched'%chan].Fill(ptg2)
            self.Histos['%s/sreco_pT_matched'%chan].Fill(ptr2)
        
        ########################################
        #histogram for matching efficiency#
        #######################################
        self.Histos['%s/eff_den' % chan].Fill(ptg2)
        if m1 is not None and m2 is not None:
            self.Histos['%s/eff_num' % chan].Fill(ptg2)
            
            #################################################
            ###  get trigger object in the events ##
            #################################################

            TriObj = [TO for TO in event.trigobjs]
            TO_pass = []
            for j, TO in enumerate (TriObj):
                if TO.bit != 0 and (
                        abs(TO.bit) & (1<<0) > 0 or abs(TO.bit) & (1<<1) > 0 or abs(TO.bit) & (1<<2) > 0 or abs(TO.bit) & (1<<3) > 0 or abs(TO.bit) & (1<<4) > 0
                        or abs(TO.bit) & (1<<5)  > 0 or abs(TO.bit) & (1<<6)  > 0 or abs(TO.bit) & (1<<7)  > 0 or abs(TO.bit) & (1<<8)  > 0 or abs(TO.bit) & (1<<9)  > 0
                        or abs(TO.bit) & (1<<10) > 0 or abs(TO.bit) & (1<<11) > 0 or abs(TO.bit) & (1<<12) > 0 or abs(TO.bit) & (1<<13) > 0 or abs(TO.bit) & (1<<14) > 0
                        or abs(TO.bit) & (1<<15) > 0 or abs(TO.bit) & (1<<16) > 0 or abs(TO.bit) & (1<<17) > 0 or abs(TO.bit) & (1<<18) > 0 or abs(TO.bit) & (1<<19) > 0
                        or abs(TO.bit) & (1<<20) > 0 or abs(TO.bit) & (1<<21) > 0 or abs(TO.bit) & (1<<22) > 0 or abs(TO.bit) & (1<<23) > 0):
                    TO_pass.append(TriObj[j])
        
        
            #matched reco 1 to trigger objects
            mindr, to1, to2 = 999, None, None
            for k, t in enumerate(TO_pass):
                drt =  DeltaR(TO_pass[k].p4,reco_mu[m1].p4)
                if drt < mindr:
                    mindr = drt
                    if mindr < drthr:
                        to1 = k # trigger object at position k was matched to reco mu 1

            #matched reco 2 to trigger objects
            mindr = 999
            for k, t in enumerate(TO_pass):
                drt =  DeltaR(TO_pass[k].p4,reco_mu[m2].p4)
                if drt < mindr:
                    mindr = drt
                    if mindr < drthr and k != to1:
                        to2 = k # trigger object at position k was matched to reco mu 1 

            #if to1 is not None or to2 is not None:
                #self.Histos['%s/Total_pT' % chan].Fill(ptg2)
            if to1 is not None and to2 is not None:
                    self.Histos['%s/Matched_pT' % chan].Fill(ptg2)
                    


histCollection = [
    { 'name': 'ngenall',           'binning': (10, -0.5,9.5),          'title': 'n gen muons; n muons; Entries'},
    { 'name': 'ngen',           'binning': (10, -0.5,9.5),          'title': 'n gen muons; n muons; Entries'},
    { 'name': 'gen_dR',         'binning': (24, 0,0.4),             'title': 'p_{T}  gen muons; p_{T} [GeV]; Entries'},
    { 'name': 'gen_pT',         'binning': (100, 0,1000),           'title': 'p_{T}  gen muons; p_{T} [GeV]; Entries'},
    { 'name': 'lgen_pT',        'binning': (100, 0,1000),           'title': 'p_{T}  leading gen muons; p_{T} [GeV]; Entries'},
    { 'name': 'gen_Mass',       'binning': (40, -0.75,9.75),        'title': 'Mass of the gen muons pairs; p_{T} [GeV]; Entries'},
    
    
    { 'name': 'npf',            'binning': (30, -0.5,29.5),              'title': 'n pf muons; n muons; Entries'},
    { 'name': 'pf_pT',          'binning': (100, 0,1000),           'title': 'p_{T}  pf muons; p_{T} [GeV]; Entries'},

    { 'name': 'ndsa',           'binning': (30, -0.5,29.5),              'title': 'n dsa muons; n muons; Entries'},
    { 'name': 'dsa_pT',         'binning': (100, 0,1000),           'title': 'p_{T}  dsa muons; p_{T} [GeV]; Entries'},

    { 'name': 'nreco',          'binning': (30, -0.5,29.5),              'title': 'n pf + dsa muons; n muons; Entries'},
    { 'name': 'lreco_pT',       'binning': (100, 0,1000),           'title': 'p_{T}  leading reco pf muons; p_{T} [GeV]; Entries'},

    { 'name': 'lgen_pT_matched',         'binning': (100, 0,1000),           'title': 'Leading p_{T}  gen muons; p_{T} [GeV]; Entries'},
    { 'name': 'sgen_pT_matched',         'binning': (100, 0,1000),           'title': 'Sub-leading p_{T}  gen muons; p_{T} [GeV]; Entries'},
    { 'name': 'lreco_pT_matched',         'binning': (100, 0,1000),           'title': 'Leading p_{T}  reco muons; p_{T} [GeV]; Entries'},
    { 'name': 'sreco_pT_matched',         'binning': (100, 0,1000),           'title': 'Sub-leading p_{T}  reco muons; p_{T} [GeV]; Entries'},

    { 'name': 'eff_num',        'binning': (100, 0,1000),           'title': 'p_{T}  num muons; p_{T} [GeV]; Entries'},
    { 'name': 'eff_den',        'binning': (100, 0,1000),           'title': 'p_{T}  den muons; p_{T} [GeV]; Entries'},

    { 'name': 'Matched_pT',     'binning': (100, 0,1000),           'title': 'p_{T}  matched muons; p_{T} [GeV]; Entries'},
    { 'name': 'Total_pT',       'binning': (100, 0,1000),           'title': 'p_{T}  total muons; p_{T} [GeV]; Entries'},



    
     

    #{ 'name': 'Mat_pT',          'binning': [[0,30,60,90,120,160,200, 300, 400, 500, 600, 700]],         'title': 'p_{T} matched; p_{T} [GeV]; Entries'},
    #{ 'name': 'Tot_pT',          'binning': [[0,30,60,90,120,160,200, 300, 400, 500, 600, 700]],         'title': 'p_{T} total; p_{T} [GeV]; Entries'},
    #{ 'name': 'Mat_eta',         'binning': (25,-3.5,3.5),          'title': '#eta matched ; #eta; Entries'},
    #{ 'name': 'Mat_d0',   	    'binning': (20, 0, 70),          'title': '|d_{0}| matched; |d_{0}|[cm]; Entries'},
    #{ 'name': 'Tot_d0',          'binning': (20, 0, 70),          'title': '|d_{0}| total; |d_{0}|[cm]; Entries'},
    
    #{ 'name': 'Mat_dR',        'binning': [[0.,0.02,0.04, 0.06,0.08,0.1, 0.15,0.2,0.25, 0.3,0.4,]],  'title':'#Delta R matched; #Delta R(#mu_{1},#mu_{2}); Entries'},
    #{ 'name': 'Tot_dR',        'binning': [[0.,0.02,0.04, 0.06,0.08,0.1, 0.15,0.2,0.25, 0.3,0.4,]],  'title':'#Delta R total; #Delta R(#mu_{1},#mu_{2}); Entries'},
    #{ 'name': 'Mat_dRd0l2',    'binning': [[0.,0.02,0.04, 0.06,0.08,0.1, 0.15,0.2,0.25, 0.3,0.4,]],  'title':'#Delta R matched d_{0}<200; #Delta R(#mu_{1},#mu_{2}); Entries'},
    #{ 'name': 'Tot_dRd0l2',    'binning': [[0.,0.02,0.04, 0.06,0.08,0.1, 0.15,0.2,0.25, 0.3,0.4,]],  'title':'#Delta R total d_{0}<200; #Delta R(#mu_{1},#mu_{2}); Entries'},
    #{ 'name': 'Mat_dRd0l5',    'binning': [[0.,0.02,0.04, 0.06,0.08,0.1, 0.15,0.2,0.25, 0.3,0.4,]],  'title':'#Delta R matched d_{0} > 200 and <500; #Delta R(#mu_{1},#mu_{2}); Entries'},
    #{ 'name': 'Tot_dRd0l5',    'binning': [[0.,0.02,0.04, 0.06,0.08,0.1, 0.15,0.2,0.25, 0.3,0.4,]],  'title':'#Delta R total d_{0} > 200 and <500; #Delta R(#mu_{1},#mu_{2}); Entries'},
    #{ 'name': 'Mat_dRd0m5',    'binning': [[0.,0.02,0.04, 0.06,0.08,0.1, 0.15,0.2,0.25, 0.3,0.4,]],  'title':'#Delta R matched d_{0}>500; #Delta R(#mu_{1},#mu_{2}); Entries'},
    #{ 'name': 'Tot_dRd0m5',    'binning': [[0.,0.02,0.04, 0.06,0.08,0.1, 0.15,0.2,0.25, 0.3,0.4,]],  'title':'#Delta R total d_{0}>500; #Delta R(#mu_{1},#mu_{2}); Entries'},
    #{ 'name': 'Mat_dRfbin',    'binning': [[0.,0.02,0.04, 0.06,0.08,0.1, 0.15,0.2,0.25, 0.3,0.4,]],  'title':'#Delta R matched d_{0} extended; #Delta R(#mu_{1},#mu_{2}); Entries'},
    #{ 'name': 'Tot_dRfbin',    'binning': [[0.,0.02,0.04, 0.06,0.08,0.1, 0.15,0.2,0.25, 0.3,0.4,]],  'title':'#Delta R total d_{0} extended; #Delta R(#mu_{1},#mu_{2}); Entries'},
    
    #{ 'name': 'Mat_pTd0l2',          'binning': [[0,5,10,15,20,25,30,35,40,50,60,70,80, 90, 100, 150, 200]],         'title': 'p_{T} matched for d_{0}<200; p_{T} [GeV]; Entries'},
    #{ 'name': 'Tot_pTd0l2',          'binning': [[0,5,10,15,20,25,30,35,40,50,60,70,80, 90, 100, 150, 200]],         'title': 'p_{T} total for d_{0}<200; p_{T} [GeV]; Entries'},
    #{ 'name': 'Mat_pTd0l5',          'binning': [[0,5,10,15,20,25,30,35,40,50,60,70,80, 90, 100, 150, 200]],         'title': 'p_{T} matched for d_{0}<500; p_{T} [GeV]; Entries'},
    #{ 'name': 'Tot_pTd0l5',          'binning': [[0,5,10,15,20,25,30,35,40,50,60,70,80, 90, 100, 150, 200]],         'title': 'p_{T} total for d_{0}<500; p_{T} [GeV]; Entries'},
    #{ 'name': 'Mat_pTd0m5',          'binning': [[0,5,10,15,20,25,30,35,40,50,60,70,80, 90, 100, 150, 200]],         'title': 'p_{T} matched for d_{0}>500; p_{T} [GeV]; Entries'},
    #{ 'name': 'Tot_pTd0m5',          'binning': [[0,5,10,15,20,25,30,35,40,50,60,70,80, 90, 100, 150, 200]],         'title': 'p_{T} total for d_{0}>500; p_{T} [GeV]; Entries'},

    #{ 'name': 'leadptrb',              'binning': [[0, 10, 15, 20, 30, 40, 60, 80, 100]],           'title': 'p_{T} Leading muon; p_{T} [GeV]; Entries'},
    #{ 'name': 'leadptl30',             'binning': (10, 0.0, 35), 'title': 'p_{T} < 30 Leading muon; p_{T} [GeV]; Entries'},
    #{ 'name': 'leadptl100',            'binning': (10, 20.0, 120), 'title': 'p_{T} > 30 and < 100 Leading muon; p
    
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

