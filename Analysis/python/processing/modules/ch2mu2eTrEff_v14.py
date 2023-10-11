#!/usr/bin/env python
# Reco_Mu: reco muon, TO: trigger object, LJ: lepton jet

'''
Tr eff after the jamboree and redefine the efficiency:
Match reco to gen and then reco to TO. Using ljsources collection 
Eff = gen-mathed reco muons matched to TO / gen
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

        gmus = [mu for mu in event.gens \
            if abs(mu.pid)==13 \
                and mu.p4.pt()>10\
                and abs(mu.p4.eta())<2.4\
                and mu.vtx.Rho()<700]

        self.Histos['%s/gen_n' % chan].Fill(len(gmus))
        gmus.sort(key=lambda mu: mu.p4.pt(), reverse=True) # sort gen muons by pt
        if len(gmus) < 2: return
        
        #Dark photon
        for p in aux['dp']:
            if p.p4.pt() < 30 or abs(p.p4.eta()) > 2.4: return
            if abs(p.daupid) == 13:
                zdlxy = (p.dauvtx-p.vtx).Rho()
                #if zdlxy > 500: return
                zdpt = p.p4.pt()
                mud0 = p.dauvtx.Rho()
        
        gendr = DeltaR(gmus[0].p4,gmus[1].p4)
        ptg1, ptg2 = gmus[0].p4.pt(), gmus[1].p4.pt()
        etag1, etag2 = gmus[0].p4.eta(), gmus[1].p4.eta()
        self.Histos['%s/gen_dR'%chan].Fill(gendr)
        self.Histos['%s/gen_pTl'%chan].Fill(ptg1)
        self.Histos['%s/gen_pTs'%chan].Fill(ptg2)
		
        reco_mu, dsa_mu, pf_mu = [], [], []
        for i, mu in enumerate(event.ljsources):
            if abs(mu.p4.eta()) > 2.4: continue
            if mu.type == 3:
                if mu.p4.pt() < 5: continue
                if mu.p4.pt() > 1000: continue
                pf_mu.append(mu)
                reco_mu.append(mu)
            elif mu.type == 8:
                if mu.p4.pt() < 10: continue
                if mu.p4.pt() > 1000: continue
                dsa_mu.append(mu)
                reco_mu.append(mu)
            else:
                pass

        self.Histos['%s/dsa_n'%chan].Fill(len(dsa_mu))
        self.Histos['%s/pf_n'%chan].Fill(len(pf_mu))
        self.Histos['%s/reco_n'%chan].Fill(len(reco_mu))
            
        reco_mu.sort(key=lambda mu: mu.p4.pt(), reverse=True) # sort reco (pf and dsa) muons by pt

        ############################################################
        drthr_gm = 0.4 #dr between reco and gen muons
        drthr_tm = 0.2 #dr between to and reco muons

        #matching gen(mu1) to its closest reco muon
        min1, m1  = 999, None
        for r, rmu in enumerate(reco_mu):
            dr = DeltaR(gmus[0].p4,rmu.p4)
            self.Histos['%s/g1all_dR'%chan].Fill(dr)
            ptr = rmu.p4.pt()
            if dr < min1:# ptr > 0.9*ptg1 and ptr < 1.1*ptg1
                min1 = dr
                if min1 < drthr_gm:
                    m1 = r # index of reco muon matched to the leading gen muon
                    ptr1 = ptr

        if m1 is not None:
            self.Histos['%s/lindex'%chan].Fill(m1)
            self.Histos['%s/reco_pTl'%chan].Fill(ptr1)
            ptdiff1 = 1- (ptr1/ptg1)            
            self.Histos['%s/diff1_pT'%chan].Fill(ptdiff1)
            
        #matching gen(mu2) to its closest reco muon discarting reco1
        min2, m2 = 999, None
        for r, rmu in enumerate(reco_mu):
            dr = DeltaR(gmus[1].p4,rmu.p4)
            self.Histos['%s/g2all_dR'%chan].Fill(dr)
            ptr = rmu.p4.pt()
            if dr < min2 and r != m1: #and ptr > 0.5*ptg2 and ptr < 1.5*ptg2
                min2 = dr
                if min2 < drthr_gm:
                    m2 = r # index of reco muon matched to the sub-leading gen muon
                    ptr2 = ptr

        if m2 is not None:
            self.Histos['%s/sindex'%chan].Fill(m2)
            self.Histos['%s/reco_pTs'%chan].Fill(ptr2)
            ptdiff2 = 1- (ptr2/ptr2)
            self.Histos['%s/diff2_pT'%chan].Fill(ptdiff2)
            

        #### Variables for efficiency
        effpt = ptg1
        effdr = gendr
        effeta = etag1
        effd0 = mud0

        ########################################
        self.Histos['%s/Total_ID' % chan].Fill(effpt)
        self.Histos['%s/Total_dR' % chan].Fill(effdr)
        self.Histos['%s/Total_pT' % chan].Fill(effpt)
        self.Histos['%s/Total_eta' % chan].Fill(effeta)
        self.Histos['%s/Total_d0' % chan].Fill(mud0)
        self.Histos['%s/Total_zdlxy' % chan].Fill(zdlxy)
        self.Histos['%s/Total_zdpt' % chan].Fill(zdpt)
    
        if m1 is not None and m2 is not None: #both rmu matched to the two gmu 
            recodr = DeltaR(reco_mu[m1].p4,reco_mu[m2].p4)
            leaddr = DeltaR(gmus[0].p4,reco_mu[m1].p4)
            subdr = DeltaR(gmus[1].p4,reco_mu[m2].p4)

            self.Histos['%s/Passed_ID'%chan].Fill(effpt) # # of events with two reco muons
            self.Histos['%s/reco_dR'%chan].Fill(recodr)
            self.Histos['%s/lead_dR'%chan].Fill(leaddr)
            self.Histos['%s/sub_dR'%chan].Fill(subdr)

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
            
            #matching reco 1 to a trigger object
            mindr, to1 = 999, None
            for k, t in enumerate(TO_pass):
                drt =  DeltaR(TO_pass[k].p4,reco_mu[m1].p4)
                if drt < mindr:
                    mindr = drt
                    if mindr < drthr_tm:
                        to1 = k # trigger object at position k was matched to reco mu 1

            #matching reco 2 to a trigger object different than the first 1
            mindr, to2 = 999, None
            for k, t in enumerate(TO_pass):
                drt =  DeltaR(TO_pass[k].p4,reco_mu[m2].p4)
                if drt < mindr:
                    mindr = drt
                    if mindr < drthr_tm and k != to1: #remove TO that was matched to reco 0
                        to2 = k # trigger object at position k was matched to reco mu 1 

            if to1 is not None and to2 is not None:
                self.Histos['%s/Passed_dR' % chan].Fill(effdr)
                self.Histos['%s/Passed_pT' % chan].Fill(effpt)
                self.Histos['%s/Passed_eta' % chan].Fill(effeta)
                self.Histos['%s/Passed_d0' % chan].Fill(effd0)
                self.Histos['%s/Passed_zdlxy' % chan].Fill(zdlxy)
                self.Histos['%s/Passed_zdpt' % chan].Fill(zdpt)

histCollection = [
    { 'name': 'test',             'binning': (10, -0.5,9.5),                'title': 'muon type; type; Counts'},

    { 'name': 'ljmu_n',           'binning': (10, -0.5,9.5),                'title': 'Number of reco muons; muons; Counts'}, 
    { 'name': 'ljall_n',          'binning': (10, -0.5,9.5),               'title': 'Number of all objects; muons; Counts'},
    { 'name': 'gen_n',            'binning': (6, -0.5,5.5),                'title': 'Number of gen muons; muons; Entries'},
    { 'name': 'pf_n',             'binning': (30, -0.5,29.5),              'title': 'Number of pf muons; muons; Entries'},
    { 'name': 'dsa_n',            'binning': (30, -0.5,29.5),              'title': 'Number of dsa muons; muons; Entries'},
    { 'name': 'reco_n',           'binning': (30, -0.5,29.5),              'title': 'Number of reco (pf+dsa) muons; muons; Entries'},
    { 'name': 'lindex',      'binning': (13, -0.5,12.5),              'title': 'leading muons postition; Index; Events'},
    { 'name': 'sindex',      'binning': (13, -0.5,12.5),              'title': 'sub-leading muons postition; Index; Events'},
    #{ 'name': 'reco_gen0p4',      'binning': (13, -0.5,12.5),              'title': 'Number of reco muons within 0.4 of gen 1; number of muons; Events'},
    #{ 'name': 'reco_gen0p3',      'binning': (13, -0.5,12.5),              'title': 'Number of reco muons within 0.3 of gen 1; number of muons; Events'},
    #{ 'name': 'reco_gen0p2',      'binning': (13, -0.5,12.5),              'title': 'Number of reco muons within 0.2 of gen 1; number of muons; Events'},
    
    { 'name': 'gen_dR',      'binning': [[0,.005,.01,.015,.02,.025,.03,.04,.05,.06,.07,.08,.09,.1,.12,.14,.16,.18,.2,.24,.28]], 'title': '#Delta R gen muons; #Delta R (g1,g2); Entries'},
    { 'name': 'reco_dR',     'binning': [[0,.005,.01,.015,.02,.025,.03,.04,.05,.06,.07,.08,.09,.1,.12,.14,.16,.18,.2,.24,.28]], 'title': '#Delta R reco muons; #Delta R(r1, r2); Entries'},
    { 'name': 'lead_dR',     'binning': [[0,.005,.01,.015,.02,.025,.03,.04,.05,.06,.07,.08,.09,.1,.12,.14,.16,.18,.2,.24,.28]], 'title': 'Matched #Delta R(g1,r1);#Delta R(g1, r1);Events'},
    { 'name': 'sub_dR',      'binning': [[0,.005,.01,.015,.02,.025,.03,.04,.05,.06,.07,.08,.09,.1,.12,.14,.16,.18,.2,.24,.28]], 'title': 'Matched #Delta R(g2, r2);#Delta R(g2, r2);Events'},

    #{ 'name': 'gen_Mass',         'binning': (40, -0.75,9.75),             'title': 'Mass of the gen muons pairs; p_{T} [GeV]; Entries'},
    
    { 'name': 'gen_pTl',          'binning': (100, 0,800),                 'title': 'Leading gen p_{T}; p_{T, lea}^{gen} [GeV]; Events'},
    { 'name': 'gen_pTs',          'binning': (100, 0,800),                 'title': 'Sub-leading gen p_{T} ; p_{T, sub}^{gen} [GeV]; Events'},
    { 'name': 'reco_pTl',          'binning': (100, 0,800),                 'title': 'Leading reco p_{T}; p_{T, lea}^{gen} [GeV]; Events'},
    { 'name': 'reco_pTs',          'binning': (100, 0,800),                 'title': 'Sub-leading reco p_{T} ; p_{T, sub}^{gen} [GeV]; Events'},
    { 'name': 'diff1_pT',         'binning': (100, -10,10),              'title': 'p_{T} diff of leading muons; 1- #frac{p_{T}^{reco}}{p_{T}^{gen}}; Events'},
    { 'name': 'diff2_pT',         'binning': (100, -10,10),              'title': 'p_{T} diff of sub-leading muons; |p_{T}^{gen} - p_{T}^{reco}| p_{T}^{gen} [GeV]; Events'},
    #{ 'name': 'gen_diff_pT',      'binning': (100, 0.,800.),               'title': 'p_{T} diff of gen muons; |p_{T}^{lead} - p_{T}^{sub}| [GeV]; Events'},

    { 'name': 'Passed_ID',         'binning': (100, 0,800),                 'title': '; p_{T} [GeV]; Entries'},
    { 'name': 'Total_ID',          'binning': (100, 0,800),                 'title': '; p_{T} [GeV]; Entries'},

    { 'name': 'Passed_pT',         'binning': (100, 0,800),                 'title': '; Passed p_{T} muons; p_{T} [GeV]; Entries'},
    { 'name': 'Total_pT',          'binning': (100, 0,800),                 'title': '; Total  p_{T} muons; p_{T} [GeV]; Entries'},


    #{ 'name': 'Passed_pT',   'binning': [[0, 10, 20, 30, 40, 50, 60, 70, 80, 100, 120, 140, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800]], 'title': 'Passed p_{T} muons; p_{T} [GeV]; Entries'},
    #{ 'name': 'Total_pT',   'binning': [[0, 10, 20, 30, 40, 50, 60, 70, 80, 100, 120, 140, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800]], 'title': 'Total p_{T} muons; p_{T} [GeV]; Entries'},
    { 'name': 'Passed_dR',   'binning': [[0,.005,.01,.015,.02,.025,.03,.04,.05,.06,.07,.08,.09,.1,.12,.14,.16,.18,.2,.24,.28]],   'title': '#Delta R (to,reco); #Delta R; Entries'},
    { 'name': 'Total_dR',   'binning': [[0,.005,.01,.015,.02,.025,.03,.04,.05,.06,.07,.08,.09,.1,.12,.14,.16,.18,.2,.24,.28]],   'title': '#Delta R (to,reco); #Delta R; Entries'},
    { 'name': 'Passed_eta',       'binning': (30, -3.,3.),                 'title': 'Passed #eta; #eta; Entries'},
    { 'name': 'Total_eta',        'binning': (30, -3.,3.),                 'title': 'Total #eta; #eta; Entries'},
    { 'name': 'Passed_d0',       'binning': (50, 0.,200.),                 'title': 'Passed d_0; d_0 [cm]; Entries'},
    { 'name': 'Total_d0',        'binning': (50, 0.,200.),                 'title': 'Total d_0; d_0 [cm]; Entries'},
    { 'name': 'Passed_zdpt',      'binning': (100, 0., 1200.),             'title': '; Dark photon p_{T}; #eta; Entries'},
    { 'name': 'Total_zdpt',       'binning': (100, 0., 1200.),             'title': '; Dark photon p_{T}; Entries'},
    { 'name': 'Passed_zdlxy',     'binning': (100, 0., 1200.),             'title': '; Dark photon L_{xy} [cm]; Entries'},
    { 'name': 'Total_zdlxy',      'binning': (100, 0., 1200.),             'title': '; Dark photon L_{xy} [cm]; Entries'},
 
    { 'name': 'g1all_dR',         'binning': (70, 0., 0.45),               'title': '#Delta R (g1,all reco); #Delta R all; Entries'},
    { 'name': 'g10p4_dR',         'binning': (70, 0., 0.45),               'title': '#Delta R (g1,all reco); #Delta R < 0.4; Entries'},
    { 'name': 'g10p3_dR',         'binning': (70, 0., 0.45),               'title': '#Delta R (g1,all reco); #Delta R < 0.3; Entries'},
    { 'name': 'g10p2_dR',         'binning': (70, 0., 0.45),               'title': '#Delta R (g1,all reco); #Delta R < 0.2; Entries'},
    { 'name': 'g2all_dR',         'binning': (70, 0., 0.45),               'title': '#Delta R (g2,all reco); #Delta R all; Entries'},
    { 'name': 'g20p4_dR',         'binning': (70, 0., 0.45),               'title': '#Delta R (g2,all reco); #Delta R < 0.4; Entries'},
    { 'name': 'g20p3_dR',         'binning': (70, 0., 0.45),               'title': '#Delta R (g2,all reco); #Delta R < 0.3; Entries'},
    { 'name': 'g20p2_dR',         'binning': (70, 0., 0.45),               'title': '#Delta R (g2,all reco); #Delta R < 0.2; Entries'},
]

