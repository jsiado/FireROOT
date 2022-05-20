#!/usr/bin/env python
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
        
        #isolation
        isonopu = []
        iso = []

        for lj in [LJ0, LJ1]:
            # if not math.isnan(lj.pfIsolationNoPU05):
            isonopu.append(lj.pfIsolationNoPU05)
            # if not math.isnan(lj.pfIsolation05):
            iso.append(lj.pfIsolation05)
            if lj.isEgmType():
                self.Histos['{}/egmisonopu'.format(chan)].Fill(lj.pfIsolationNoPU05, aux['wgt'])
                self.Histos['{}/egmiso'.format(chan)].Fill(lj.pfIsolation05, aux['wgt'])

        self.Histos['{}/maxisonopu'.format(chan)].Fill(max(isonopu), aux['wgt'])
        self.Histos['{}/maxiso'.format(chan)].Fill(max(iso), aux['wgt'])
        
        #leptonjetDSARange.py
        for lj in [LJ0, LJ1]:
            if not lj.isMuonType(): continue
            for i in lj.pfcand_dsamuonIdx:
                dsa = event.dsamuons[i]
                self.Histos['{}/dsapt'.format(chan)].Fill(dsa.p4.pt(), aux['wgt'])
                self.Histos['{}/dsaeta'.format(chan)].Fill(dsa.p4.eta(), aux['wgt'])
                self.Histos['{}/dsaphi'.format(chan)].Fill(dsa.p4.phi(), aux['wgt'])
                self.Histos['{}/dsad0'.format(chan)].Fill(abs(dsa.d0), aux['wgt'])
                self.Histos['{}/dsadz'.format(chan)].Fill(abs(dsa.dz), aux['wgt'])
                self.Histos['{}/normchi2'.format(chan)].Fill(dsa.normChi2, aux['wgt'])
        
        #pt of dsa
        #for i, dsa in enumerate(event.dsamuons):
         #   if dsa.p4.pt()<5 or abs(dsa.p4.eta())>2.4: continue
          #  self.Histos['%s/DsaPt'%chan].Fill(dsa.p4.pt(), aux['wgt'])
            #if dsa.p4.pt()<50:
             #   self.Histos['%s/DsaPtzoom2'%chan].Fill(dsa.p4.pt(), aux['wgt'])
        
        #dark photons
        #for p in aux['dp']:
         #   rho = (p.dauvtx-p.vtx).Rho()
          #  self.Histos['{}/dplxy'.format(chan)].Fill(rho,aux['wgt'])
            
        #lepton jets
        #self.Histos['%s/nljet'%chan].Fill(len(event.leptonjets),aux['wgt'])
        #if len(event.leptonjets) == 2:
         #   dRLJ = DeltaR(event.leptonjets[0].p4, event.leptonjets[1].p4)
          #  dphiLJ = abs(DeltaPhi(event.leptonjets[0].p4, event.leptonjets[1].p4))
           # self.Histos['%s/dRLJ'%chan].Fill(dRLJ,aux['wgt'])
            #self.Histos['%s/delPhiLJ'%chan].Fill(dphiLJ,aux['wgt'])
        
histCollection = [
    {
        'name': 'maxisonopu',
        'binning': (50, 0, 0.5),
        'title': 'max lepton-jet isolation (no PU);isolation;counts',
    },
    {
        'name': 'maxiso',
        'binning': (50, 0, 0.5),
        'title': 'max lepton-jet isolation (w/ PU);isolation;counts',
    },
    {
        'name': 'egmisonopu',
        'binning': (50, 0, 0.5),
        'title': 'egm-type lepton-jet isolation (no PU);isolation;counts',
    },
    {
        'name': 'egmiso',
        'binning': (50, 0, 0.5),
        'title': 'egm-type lepton-jet isolation (w/ PU);isolation;counts',
    },
    {
        'name': 'dsapt',
        'binning': [[0,5,10,20,50,]+list(np.arange(100,501,50))],
        'title': 'DSA p_{T};p_{T} [GeV];counts',
    },
    {
        'name': 'dsaeta',
        'binning': (24, -2.4, 2.4),
        'title': 'DSA #eta;#eta;counts',
    },
    {
        'name': 'dsaphi',
        'binning': (24, -math.pi, math.pi),
        'title': 'DSA #phi;#phi;counts',
    },
    {
        'name': 'dsad0',
        'binning': (50, 0, 150),
        'title': 'DSA |d_{0}|;|d_{0}| [cm];counts',
    },
    {
        'name': 'dsadz',
        'binning': (50, 0, 50),
        'title': 'DSA |d_{z}|;|d_{z}| [cm];counts',
    },
    {
        'name': 'normchi2',
        'binning': (50, 0, 20),
        'title': 'DSA #chi^{2}/ndof;#chi^{2}/ndof;counts',
    },
    #{'name': 'nMu',            'binning': (100, 0.0, 5.0),    'title': 'Number of muons ;N ;counts'},
    #{'name': 'nEle',            'binning': (100, 0.0, 5.0),    'title': 'Number of electrons ;N ;counts'},
    #{'name': 'nLepton',            'binning': (100, 0.0, 8.0),    'title': 'Number of leptons ;N ;counts'},
    #{'name': 'DsaPt',            'binning': (100, 0.0, 500.0),    'title': 'DSA #mu p_{T}  ;p_{T} ;counts'},
    #{'name': 'DsaPtzoom2',       'binning': (100, 0.0, 80.0),    'title': 'DSA #mu p_{T} zoom ;p_{T} ;counts'},
    #{'name': 'nljet',            'binning': (100, 0.0, 3.0),    'title': 'Number of Lepton jets ;N ;counts'},
    #{'name': 'dRLJ',            'binning': (100, 0.0, 5.5),    'title': '#Delta R between lepton jets ;#Delta R ;counts'},
    #{'name': 'delPhiLJ',         'binning': (100, 0.0, 3.5),    'title': '#Delta #phi between lepton jets ;#Delta #phi ;counts'},
    #{'name': 'dplxy',        'binning': (100, 0, 500),        'title': 'darkphoton lxy;Lxy [cm];counts/1cm'},
    #{'name': 'MuPt',        'binning': (100, 0, 500.0),        'title': 'all Muons;p_{T} [GeV]; counts'    },
]
