#!/usr/bin/env python
import math

from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *

class MyEvents(Events):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e','4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']
        
        LJ0, LJ1 = aux['lj0'], aux['lj1']
        passCosmic = all(map(lambda lj: lj.passCosmicVeto(event), [LJ0, LJ1]))
        
        if not passCosmic: return
        
        dauther = []
        for lj in [LJ0, LJ1]:
            if lj.isMuonType():
                for i, mu in enumerate(event.muons):
                    print len(event.muons)
                
            #if lj.isEgmType():
             #

        '''            matched_reco_muons = []
        #first loop over the trigger objects and find which reco muon it is closest to
        for TO in (double muon trigger objects):
        #this is the minimum delta R between this trigger object and all reco muons
        min_dR = 1000
        RM_index = -1
        for index, RM in enumerate(all reco muons):
        if DeltaR(TO.p4, RM.p4) < min_dR:
        min_dR = DeltaR(TO.p4, RM.p4)
        RM_index = index
        if min_DR < 0.2: #(or some other tight threshold; this might have to be optimized)
        matched_reco_muons.append( RM_index) 
        #this might give us weird behavior if the same reco muon matches to two trigger objects; might be worth adding an explicit 
        #now loop over the reco muons again and fill the numerator and denominator histograms for the efficiency
        for index, RM in enumerate(all reco muons):
        apply pt, eta, ID cuts here
        # now min_dR is the minimum deltaR between this reco muon and all *other* reco muons
        min_dR = 1000
        for i2, RM2 in enumerate(all reco muons):
        if i2 == i1: continue
        if DeltaR(RM.p4, RM2.p4) < min_dR: min_dR = DeltaR(RM.p4, RM2.p4)
    
        denominator_hist.Fill(min_dR)
        #Check to see whether this reco muon matched to a TO; if so, fill the numerator histogram
        if (index in matched_reco_muons): numerator_hist.Fill(min_dR)'''

                            
histCollection = [
    {   'name': 'dR01',        'binning': (1000, 0.0, 0.05),      'title': '#Delta R between muons 0 and 1; #Delta R;counts'     },
    {   'name': 'iso24_4mu',   'binning': (20, 0.0, 0.05),        'title': 'IsoMu24_4mu  ;#DeltaR ;counts'                       },
    {   'name': 'Dimu_2mu',    'binning': (20, 0.0, 5.0),         'title': 'DoubleL2Mu23NoVtx_2Cha__2mu ;#DeltaR ;counts'        },
    {   'name': 'Dimu_4mu',    'binning': (20, 0.0, 0.05),        'title': 'DoubleL2Mu23NoVtx_2Cha_4mu ;#DeltaR ;counts'         },
]
