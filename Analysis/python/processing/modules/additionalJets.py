#!/usr/bin/env python
import math
from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *
#from FireROOT.Analysis.SignalEvents import *

nLJ3 = 0
right = 0
miss = 0
class MyEvents(Events):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)
    #nLJ3 = 0
    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']

        LJ0, LJ1,LJ2 = aux['lj0'], aux['lj1'], aux['lj2']
        passCosmic = all(map(lambda lj: lj.passCosmicVeto(event), [LJ0, LJ1, LJ2]))
        if not passCosmic: return
        passLjMass = all(map(lambda lj: lj.isEgmType() or lj.isMuonType() and lj.p4.M()<8, [LJ0, LJ1, LJ2]))
        if not passLjMass: return
        
        #cosalpha12 = computeCosAlpha(LJ0.p4, LJ1.p4)
        #cosalpha13 = computeCosAlpha(LJ0.p4, LJ2.p4)
        #cosalpha23 = computeCosAlpha(LJ1.p4, LJ2.p4)
        #if abs(cosalpha13>cosalpha12) or abs(cosalpha13>cosalpha12): print 'yes'
        #else: print 'no'
            
        #if abs(cosalpha23>cosalpha12) and abs(cosalpha23>cosalpha13):
            
    
        #print cosalpha12
        #if len(event.leptonjets)>2:
             #nLJ3= nLJ3 + 3
             #print '3LJ events'#, nLJ3
             #self.Histos['{}/jet3pt'.format(chan)].Fill(LJ2.p4.pt(), aux['wgt'])
             
        #print '1LJpt ',LJ0.p4.pt(),' 2LJpt ',LJ1.p4.pt(),' 3LJpt '#,LJ2.p4.pt()
        self.Histos['{}/jet1pt'.format(chan)].Fill(LJ0.p4.pt(), aux['wgt'])
        self.Histos['{}/jet2pt'.format(chan)].Fill(LJ1.p4.pt(), aux['wgt'])
        self.Histos['{}/jet3pt'.format(chan)].Fill(LJ2.p4.pt(), aux['wgt'])
        #print nLJ3
        
        #for p in aux['dp']:
            #ad = 3
            #zdlj = DeltaR(p.p4, lj.p4)

        Njet = 0
        NjetCleaned = 0
        for j in event.ak4jets:
            if not j.jetid: continue
            if j.p4.pt()<50: continue
            if abs(j.p4.eta())>2.4: continue

            Njet+=1

            mindist = min([DeltaR(j.p4, LJ0.p4), DeltaR(j.p4, LJ1.p4)])
            self.Histos['{}/ljdist'.format(chan)].Fill(mindist, aux['wgt'])
            if mindist<0.4: continue
            NjetCleaned+=1
            self.Histos['{}/jetpt'.format(chan)].Fill(j.p4.pt(), aux['wgt'])
            #self.Histos['{}/jet1pt'.format(chan)].Fill(j.p4.pt(), aux['wgt'])
            #self.Histos['{}/jet1pt'.format(chan)].Fill(j.p4.pt(), aux['wgt'])

        self.Histos['{}/njet'.format(chan)].Fill(Njet, aux['wgt'])
        self.Histos['{}/ncleanedjet'.format(chan)].Fill(NjetCleaned, aux['wgt'])

        invm = (LJ0.p4+LJ1.p4).M()
        self.Histos['{}/invm'.format(chan)].Fill(invm, aux['wgt'])




histCollection = [
    {
        'name': 'njet',
        'binning': (8, 0, 8),
        'title': 'Number of ak4jets;N;Events'
    },
    {
        'name': 'ncleanedjet',
        'binning': (8, 0, 8),
        'title': 'Number of cleaned ak4jets;N;Events'
    },
    {
        'name': 'ljdist',
        'binning': (50, 0, 5),
        'title': 'min dist btw ak4jet and lepton-jet;distance;Events'
    },
    {
        'name': 'jetpt',
        'binning': (50, 0, 500),
        'title': 'AK4Jet p_{T};pT [GeV];Events'
    },
    {
        'name': 'invm',
        'binning': (100, 0, 250),
        'title': 'inv mass;mass [GeV];Events'
    },
    {
        'name': 'jet1pt',
        'binning': (100, 0, 650),
        'title': '1lj Ak4Jet p_{t};pT [GeV];Events'
    },
    {
        'name': 'jet2pt',
        'binning': (100, 0, 550),
        'title': '2lj  Ak4Jet p_{t};pT [GeV];Events'
    },
    {
        'name': 'jet3pt',
        'binning': (100, 0, 450),
        'title': '3lj Ak4Jet p_{t};pT [GeV];Events'
    },
]
