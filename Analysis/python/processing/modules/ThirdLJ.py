#!/usr/bin/env python
import math
from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *
#from FireROOT.Analysis.python.processing.module_runner import *

class MyEvents(SignalEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']
        
        #number of LJ in the events
        self.Histos['%s/nljet_1' % chan].Fill(1)# hist with # of LJ
        
        #event with 0, 1, 2 and 3 LJ
        #if len(event.leptonjets) == 0: 
            #print ('cero')
#            self.Histos['%s/oneLJ_pt'%chan].Fill((event.leptonjets[0].p4),aux['wgt'])

        '''if len(event.leptonjets) == 1: 
            #print ('uno')
            self.Histos['%s/oneLJ_pt'%chan].Fill((event.leptonjets[0].p4.pt()),aux['wgt'])
            self.Histos['%s/oneLJ_eta'%chan].Fill((event.leptonjets[0].p4.eta()),aux['wgt'])
            self.Histos['%s/oneLJ_phi'%chan].Fill((event.leptonjets[0].p4.phi()),aux['wgt'])

        #if len(event.leptonjets) == 2: print ('dos')
        
        if len(event.leptonjets) == 3:
            #print ('tres')
            dR12 = DeltaR(event.leptonjets[0].p4, event.leptonjets[1].p4)
            self.Histos['%s/dRLJ12_1'%chan].Fill(dR12,aux['wgt'])
            
            dR13 = DeltaR(event.leptonjets[0].p4, event.leptonjets[2].p4)
            self.Histos['%s/dRLJ13_1'%chan].Fill(dR13,aux['wgt'])

            dR23 = DeltaR(event.leptonjets[1].p4, event.leptonjets[2].p4)
            self.Histos['%s/dRLJ23_1'%chan].Fill(dR23,aux['wgt'])

            dphi12 = abs(DeltaPhi(event.leptonjets[0].p4, event.leptonjets[1].p4))
            self.Histos['%s/delphi12_1'%chan].Fill(dphi12,aux['wgt'])
            
            dphi13 = abs(DeltaPhi(event.leptonjets[0].p4, event.leptonjets[2].p4))
            self.Histos['%s/delphi13_1'%chan].Fill(dphi13,aux['wgt'])
            
            dphi23 = abs(DeltaPhi(event.leptonjets[1].p4, event.leptonjets[2].p4))
            self.Histos['%s/delphi23_1'%chan].Fill(dphi23,aux['wgt'])

            #if dphi12 < dphi13 or dphi12 < dphi23:
                #print ('noyno')
            #else:
                #print ('vaya')
            
            for p in aux['dp']:
                zdlj2 = DeltaR(p.p4, event.leptonjets[2].p4)
                self.Histos['%s/zdljdR_1'%chan].Fill(zdlj2,aux['wgt'])
                if zdlj2<0.4:
                    self.Histos['%s/matchLJ_1'%chan].Fill(-1,aux['wgt'])
                else:
                    self.Histos['%s/matchLJ_1'%chan].Fill(1,aux['wgt'])'''

histCollection = [
    {'name': 'nljet_1', 'binning':(50,0,10), 'title': 'number of lepton jets'},
#    {'name': 'zdljdR_1', 'binning':(50,-5,5), 'title': '#DeltaR zdlj3'},
 #%   {'name': 'matchLJ_1', 'binning':(50,-3,3), 'title': 'matching LJ3'},

  #  {'name': 'dRLJ12_1', 'binning':(50,-10,10), 'title': '#DeltaR LJ12'},
   # {'name': 'dRLJ13_1', 'binning':(50,-10,10), 'title': '#DeltaR LJ13'},
   # {'name': 'dRLJ23_1', 'binning':(50,-10,10), 'title': '#DeltaR LJ23'},
    
   # {'name': 'delphi12_1', 'binning':(50,-5.0,5.0), 'title': '#Delta #phi LJ12'},
   # {'name': 'delphi13_1', 'binning':(50,-5.0,5.0), 'title': '#Delta #phi LJ13'},
   # {'name': 'delphi23_1', 'binning':(50,-5.0,5.0), 'title': '#Delta #phi LJ23'},
   # {'name': 'zeroLJ_pt', 'binning':(50,0.0,300), 'title': 'Pt for zero LJ'},
    
   # {'name': 'oneLJ_pt', 'binning':(100,0.0,500), 'title': 'Pt for one LJ'},
   # {'name': 'oneLJ_eta', 'binning':(100,-2.5,2.5), 'title': 'eta for one LJ'},
   # {'name': 'oneLJ_phi', 'binning':(100,-3.5,3.5), 'title': 'phi for one LJ'},
    #{'name': 'oneLJ_pt', 'binning':(100,0.0,500), 'title': 'Pt for one LJ'},
]
