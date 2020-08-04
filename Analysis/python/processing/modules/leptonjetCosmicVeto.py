#!/usr/bin/env python

from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *
import numpy as np
import math

class MyEvents(CosmicEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files,
                                       type=type, maxevents=maxevents, channel=channel, **kwargs)

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        flag = False
        if aux['hasCosmicShower'] and self.Type=='DATA': flag=True
        if not aux['hasCosmicShower'] and self.Type!='DATA': flag=True
        if flag is False: return

        chan = aux['channel']
        LJ0, LJ1 = aux['lj0'], aux['lj1']
        for lj in [LJ0, LJ1]:
            if lj.isEgmType(): continue

            ### DR_cosmic ###
            drcosmicdsa = lj.dRcosmicDSA(event)
            drcosmicseg = lj.dRcosmicSeg(event)
            if drcosmicdsa:
                self.Histos['{}/drdsa'.format(chan)].Fill(min(drcosmicdsa), aux['wgt'])
                if min(drcosmicdsa)>0.05 and drcosmicseg:
                    self.Histos['{}/drseg'.format(chan)].Fill(min(drcosmicseg), aux['wgt'])

            ### muon timing ###
            for i in lj.pfcand_dsamuonIdx:
                dsa = event.dsamuons[i]
                self.Histos['%s/dsatime'%chan].Fill(dsa.dtCscTime, aux['wgt'])
            for i in lj.pfcand_pfmuonIdx:
                mu = event.muons[i]
                self.Histos['%s/pfmutime'%chan].Fill(mu.dtCscTime, aux['wgt'])

            ### track dz, muon timing interplay
            maxAbsDz = max([abs(dz) for dz in lj.pfcand_tkDz])
            maxAbsTime = max([abs(mu.dtCscTime) for mu in lj.muons(event)])
            self.Histos['%s/maxAbsDz'%chan].Fill(maxAbsDz, aux['wgt'])
            self.Histos['%s/maxAbsTime'%chan].Fill(maxAbsTime, aux['wgt'])
            if maxAbsDz<40:
                self.Histos['%s/maxAbsTimeCutDz'%chan].Fill(maxAbsTime, aux['wgt'])
                self.Histos['%s/phiCutDz'%chan].Fill(lj.p4.phi(), aux['wgt'])


            ### vertexing result###
            self.Histos['%s/goodVertex'%chan].Fill(int(math.isnan(lj.klmvtx_mass)), aux['wgt'])
            if not math.isnan(lj.klmvtx_mass):
                self.Histos['%s/cosThetaXy'%chan].Fill(lj.klmvtx_cosThetaXy, aux['wgt'])
                self.Histos['%s/impactDistXy'%chan].Fill(lj.klmvtx_impactDistXy, aux['wgt'])

            ### kinematic ###
            ## cosmic peaked at -pi/2 and pi/2, so top to bottom;
            ## siganls are very flat across -pi to pi
            self.Histos['%s/phi'%chan].Fill(lj.p4.phi(), aux['wgt'])

        ### both vertexing ###
        ## This is actually not good for signals, lots of them actually does not converge to a common vertex..
        self.Histos['%s/twoGoodVertex'%chan].Fill(int(math.isnan(LJ0.klmvtx_mass))+int(math.isnan(LJ1.klmvtx_mass)), aux['wgt'])

histCollection = [
    {
        'name': 'drdsa',
        'binning': [ list(np.arange(0,0.2,0.01))+[0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5] ],
        'title': r'#DeltaR_{cosmic}(DSA_{i}, DSA_{j});#DeltaR_{cosmic};counts',
    },
    {
        'name': 'drseg',
        'binning': [ list(np.arange(0,0.2,0.01))+[0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5] ],
        'title': r'#DeltaR_{cosmic}(DSA_{i}, segment) (#DeltaR_{cosmic}(DSA_{i}, DSA_{j})>0.05);#DeltaR_{cosmic};counts',
    },
    {
        'name': 'dsatime',
        'binning': (50, -50, 50),
        'title': 'DSA time;time [ns];counts/2'
    },
    {
        'name': 'pfmutime',
        'binning': (50, -50, 50),
        'title': 'PF muon time;time [ns];counts/2'
    },
    {
        'name': 'maxAbsTime',
        'binning': (25, 0, 50),
        'title': 'LJ max abs time;|time| [ns];counts/2'
    },
    {
        'name': 'maxAbsDz',
        'binning': [[0,2,4,6,8,10,15,20,30,40,60,100]],
        'title': 'muon-type lepton-jet max track |dz|;|dz| [cm];counts',
    },
    {
        'name': 'maxAbsTimeCutDz',
        'binning': (25, 0, 50),
        'title': 'LJ max abs time (max(dz)<40cm);|time| [ns];counts/2'
    },
    {
        'name': 'goodVertex',
        'binning': (2, 0, 2),
        'title': 'LJ has good vertex;isGoodVertex;counts'
    },
    {
        'name': 'phi',
        'binning': (40, -M_PI, M_PI),
        'title': 'LJ #phi;#phi;counts/#pi/20'
    },
    {
        'name': 'phiCutDz',
        'binning': (40, -M_PI, M_PI),
        'title': 'LJ #phi (max(dz)<40cm);#phi;counts/#pi/20'
    },
    {
        'name': 'cosThetaXy',
        'binning': (50, -1, 1),
        'title': 'LJ (vertexed) cos(#theta) 2D;cos(#theta);counts/50'
    },
    {
        'name': 'impactDistXy',
        'binning': (40, 0, 40),
        'title': 'LJ (vertexed) impact distance;distance [cm];counts'
    },
    {
        'name': 'twoGoodVertex',
        'binning': (3, 0, 3),
        'title': 'both LJs have good vertex;N(GoodVertex);Events'
    },

]
