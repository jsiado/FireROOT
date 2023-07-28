#!/usr/bin/env python
# RM: reco muon, TO:trigger object

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

        pf, dsa, remu = [], [], [] #list with the two muons
        for lj in [LJ0, LJ1]:
            if not lj.isMuonType():continue
            for i in lj.pfcand_pfmuonIdx:
                pf.append(event.muons[i])
            for i in lj.pfcand_dsamuonIdx:
                dsa.append(event.dsamuons[i])
        
        dp_toMu = [p for p in aux['dp'] if p.daupid==13] #select muons from Zd

        lpf, ldsa = len(pf),len(dsa)
        if lpf == 1:
            remu.append(pf[0])
            remu.append(dsa[0])
            #print remu[0].p4.pt(),"==========",pf[0].p4.pt()
            #print remu[1].p4.pt(),"==========",dsa[0].p4.pt()
        elif lpf ==2:
            remu.append(pf[0])
            remu.append(pf[1])
            #print remu[0].p4.pt(),"+++++",pf[0].p4.pt()
            #print remu[1].p4.pt(),"+++++",pf[1].p4.pt()
        elif lpf ==0:
            remu.append(dsa[0])
            remu.append(dsa[1])
            #print remu[0].p4.pt(),"-----",dsa[0].p4.pt()
            #print remu[1].p4.pt(),"-----",dsa[1].p4.pt()
        
        #if len(pf)==2:
         #   print pf[0].p4.M()+pf[1].p4.M()
        #for i in range(len(pf)):
         #   print len(pf),'=============',pf[i].p4.M()
        #3print 'bla'
        #for i in lj.pfcand_dsamuonIdx:
         #   dsa = event.dsamuons[i]
          #  self.Histos['%s/ptmudsa2' % chan].Fill(dsa.p4.pt())
           # #print dsa.p4.M()

        #pfmuons
        #for i, mu in enumerate (event.muons):
         #   if mu.p4.pt()<5: continue
          #  if abs(mu.p4.eta())>2.4: continue
           # if i not in mu_pf: continue
            #self.Histos['%s/ptmupf' % chan].Fill(mu.p4.pt())
            #self.Histos['%s/d0mupf' % chan].Fill(mu.d0)
        
        #dsa
       # for i, mu in enumerate (event.dsamuons):
        #    if mu.p4.pt()<5: continue
         #   if abs(mu.p4.eta())>2.4: continue
          #  if i not in mu_dsa:continue
           # self.Histos['%s/ptmudsa' % chan].Fill(mu.p4.pt())
            #self.Histos['%s/d0mudsa' % chan].Fill(mu.d0)
        
        
        dphi = abs(DeltaPhi(LJ0.p4,LJ1.p4))
        self.Histos['%s/dphiLJ'%chan].Fill(dphi)
        dr = DeltaR(LJ0.p4,LJ1.p4)
        self.Histos['%s/drLJ'%chan].Fill(dr)

        #for lj in [LJ0,LJ1]:
            #print lj
         #   self.Histos['%s/LJ0' % chan].Fill(lj.p4.pt())
            #for i in lj.pfcand_dsamuonIdx:
                #print i


        # RM: reco muon, TO: trigger object             
        #matched_Reco = []

        #Reco_Mu = [remu for i, remu in enumerate(event.ljsources)]# if abs(remu.pid)==13]                                                                                 
        #self.Histos['%s/RM_n' % chan].Fill(len(Reco_Mu))
        #dR_thr = 0.3
                    
        #if len(Reco_Mu)>1
         #   TriObj = [TO for TO in event.trigobjs]  # trigger objects in the event
            #self.Histos['%s/TO_n' % chan].Fill(len(TriObj))
            
          #  for TO in TriObj:
            #    self.Histos['%s/TO_bit' % chan].Fill(TO.bit)
           #     #print TO.bit
             #   self.Histos['%s/TO_pT' % chan].Fill(TO.p4.pt())

histCollection = [
    #{  'name': 'LJ0',      'binning' : (100, 0.0,300),                   'title': 'LJ0 p_{T}; p_{T} [GeV]; Number of entries'},
    #{  'name': 'LJ1',      'binning' : (100, 0.0,300),                   'title': 'LJ1 p_{T}; p_{T} [GeV]; Number of entries'},
    {  'name': 'dphiLJ',     'binning' : (50, -4.0,4.0),                 'title': '#Delta #phi between LJ; #Delta #phi; Number of entries'},
    {  'name': 'drLJ',     'binning' : (50, -5.0,5.0),                 'title': '#Delta R between LJ; #Delta R; Number of entries'},
    
    {  'name': 'ptmupf',     'binning' : (100, 0.0,500.0),                 'title': 'p_{T} of pf muons; p_{T} [GeV]; Number of entries'},
    {  'name': 'ptmupf2',     'binning' : (100, 0.0,500.0),                 'title': 'p_{T} of pf muons2; p_{T} [GeV]; Number of entries'},
    {  'name': 'd0mupf',     'binning' : (100, 0.0,20.0),                 'title': 'd_{0} of pf muons; d_{0} [cm]; Number of entries'},

    {  'name': 'ptmudsa',     'binning' : (100, 0.0,500.0),                 'title': 'p_{T} of dsa muons; p_{T} [GeV]; Number of entries'},
    {  'name': 'ptmudsa2',     'binning' : (100, 0.0,500.0),                 'title': 'p_{T} of dsa muons; p_{T} [GeV]; Number of entries'},
    {  'name': 'd0mudsa',     'binning' : (100, 0.0,50.0),                 'title': 'd_{0} of dsa muons; d_{0} [cm]; Number of entries'},

    {  'name': 'mass',     'binning' : (100, 0.0,500.0),                 'title': 'p_{T} of pf muons; p_{T} [GeV]; Number of entries'},



    #{  'name': 'geM_pT',      'binning' : (100, 0.0,500),                   'title': 'Gen muons p_{T}; p_{T} [GeV]; Number of entries'},
    #{  'name': 'RM_dR',
     #  'binning' : [[0,0.02, 0.04,0.06, 0.08, 0.1,0.15,0.2,.3,.4,]+list(np.arange(.08,.02,.01))],
      # 'title': '#Delta R of Reco muons; #Delta R; Number of entries'},

    #{  'name': 'RM_pT',     'binning' : (100, 0.0,500),                   'title': 'Reco muon p_{T} distribution; p_{T} [GeV]; Number of entries'},
    #{  'name': 'RM_n',     'binning' : (20, 0.0,20),                   'title': 'Number of Reco #mu ; #mu ; Number of entries'},
  #  {  'name': 'TO_n',     'binning' : (30, 0.0,30),                   'title': 'Number of trigger objects; #mu ; Number of entries'},
   # {  'name': 'TO_bit',     'binning' : (100, -50.0,5000),                   'title': 'Trigger object ID ; TO ID; Number of entries'},
   # {  'name': 'TO_pT',     'binning' : (50, 0.0,500),                   'title': 'TO p_{T} distribution;  p_{T} [GeV]; Number of entries'},

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


