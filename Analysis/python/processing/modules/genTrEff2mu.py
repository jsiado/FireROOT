#!/usr/bin/env python
import math

from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *

class MyEvents(SignalEvents):
        def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e','4mu'], **kwargs):
		super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)

        def processEvent(self, event, aux):
                
                if aux['channel'] not in self.Channel: return
                chan = aux['channel']
                
                gmus = [p for p in event.gens \
                        if abs(p.pid)==13 \
                            and p.p4.pt()>30 \
                            and abs(p.p4.eta())<2.4\
                            and p.vtx.Rho()<700]
                self.Histos['%s/nmuons'%chan].Fill(len(gmus))
                #print len(gmus),'marica'
                if len(gmus) < 2 or len(gmus) > 2 : return
                dR = DeltaR(gmus[0].p4, gmus[1].p4)
                self.Histos['%s/dRgen'%chan].Fill(dR)
                if gmus[0].p4.pt()>gmus[1].p4.pt(): 
                        leapT = gmus[0].p4.pt()
                        leaEta = gmus[0].p4.eta()
                else: 
                        leapT = gmus[1].p4.pt()
                        leaEta = gmus[1].p4.eta()
                self.Histos['%s/lead_pT'%chan].Fill(leapT) 

#		if len(gmus) == 2:
#			dR01 = DeltaR(gmus[0].p4, gmus[1].p4)
#			self.Histos['%s/dR01'%chan].Fill(dR01)
#			#self.Histos['%s/eNum'%chan].Fill(2)
#			if gmus[0].p4.pt()>gmus[1].p4.pt():
#				self.Histos['%s/ptvsdR'%chan].Fill(dR01,gmus[1].p4.pt())
#				self.Histos['%s/leaMuEta'%chan].Fill(gmus[0].p4.eta())
#				self.Histos['%s/subleaMuEta'%chan].Fill(gmus[1].p4.eta())
#				subleapT = gmus[1].p4.pt()
#				leapT = gmus[0].p4.pt()
#				
#			if gmus[1].p4.pt()>gmus[0].p4.pt():
#				self.Histos['%s/ptvsdR'%chan].Fill(dR01,gmus[0].p4.pt())
#				self.Histos['%s/leaMuEta'%chan].Fill(gmus[1].p4.eta())
#				self.Histos['%s/subleaMuEta'%chan].Fill(gmus[0].p4.eta())
#				subleapT = gmus[0].p4.pt()
#				leapT = gmus[1].p4.pt()
#
#			self.Histos['%s/allDimu_dR'%chan].Fill(dR01)
#			self.Histos['%s/allDimu_lpT'%chan].Fill(leapT)
#			self.Histos['%s/allDimu_slpT'%chan].Fill(subleapT)
#			#self.Histos['%s/allDimu_slpT3b'%chan].Fill(subleapT)
#			#self.Histos['%s/allDimu_slpT20b'%chan].Fill(subleapT)
#			#if leapT > 200: self.Histos['%s/allDimu_hslpT'%chan].Fill(subleapT)'''

#if getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha"):
#				self.Histos['%s/allDimu_1'%chan].Fill(dR01)
#			if getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha_NoL2Matched"):
#				self.Histos['%s/allDimu_2'%chan].Fill(dR01)
 #       	if getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed"):
#				self.Histos['%s/allDimu_3'%chan].Fill(dR01)
#			if getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched"):
#				self.Histos['%s/allDimu_4'%chan].Fill(dR01)
#			if getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha_Eta2p4"):
#				self.Histos['%s/allDimu_5'%chan].Fill(dR01)
#			if getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4"):
#				self.Histos['%s/allDimu_6'%chan].Fill(dR01)'''
#				
#			if getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha") or getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha_NoL2Matched") or getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed") or getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched") or getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha_Eta2p4") or getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4"):
			#	self.Histos['%s/allDimu_ORdR'%chan].Fill(dR01)
			#	self.Histos['%s/allDimu_ORlpT'%chan].Fill(leapT)
			#	self.Histos['%s/allDimu_ORslpT'%chan].Fill(subleapT)
				#self.Histos['%s/eNum'%chan].Fill(6)
				#self.Histos['%s/allDimu_ORslpT3b'%chan].Fill(subleapT)
				#self.Histos['%s/allDimu_ORslpT20b'%chan].Fill(subleapT)				
				#if leapT > 200: self.Histos['%s/allDimu_ORhslpT'%chan].Fill(subleapT)'''
				
histCollection = [
        {	'name'    : 'dRgen',
                'binning' : (15, 0.0, 0.3),
                'title'   : '#Delta R of gen muons; #Delta R;# Events'
        },
	{	'name': 'nmuons',
                'binning': (10, 0.0, 10.0),
                'title': 'Number of muons; #mu collection;# Events'
        },
        {       'name': 'lead_pT',
                'binning': (100, 0.0, 710.0),
                'title': 'p_T distribution; p_T [GeV];# Events'
        },
	#{    'name': 'findR',        'binning': (30, 0.0, 0.15),      'title': '#Delta R between muons 0 and 1; #Delta R;# Events'   },
	#{    'name': 'iso24',        'binning': (30, 0.0, 0.3),       'title': 'IsoMu24_2mu ;#Delta R; # Events'                      },
	#{    'name': 'Dimu_1',       'binning': (30, 0.0, 0.3),       'title': 'DoubleL2Mu23NoVtx_2Cha_2mu ;#DeltaR ;# Events'      },
	#{    'name': 'Dimu_2',       'binning': (30, 0.0, 0.3),       'title': 'DoubleL2Mu23NoVtx_2Cha_2mu ;#DeltaR ;# Events'      },
	#{    'name': 'Dimu_3',       'binning': (30, 0.0, 0.3),       'title': 'DoubleL2Mu25NoVtx_2Cha; #DeltaR ;# of Events'      },
	#{    'name': 'Dimu_4',       'binning': (30, 0.0, 0.3),       'title': 'DoubleL2Mu25NoVtx_2Cha; #DeltaR ;# of Events'      },
	#{	'name': 'allDimu_dR',		'binning': (30, 0.0, 0.3),				'title': 'alldimu; #DeltaR; # Events'      },
	#{#	'name': 'allDimu_ORdR',		'binning': (30, 0.0, 0.3),             'title': 'alldimu_OR; #DeltaR; # Events'      },
	
	#{	'name': 'allDimu_lpT',		'binning': (100, 0.0, 500),           'title': 'All Sub-leading Muon p_T distribution;  p_T [GeV]; Entries'},
	#{	'name': 'allDimu_ORlpT',		'binning': (100, 0.0, 500),           'title': 'Pass Sub-leading Muon p_T distribution;  p_T [GeV]; Entries'},
	
	#{    'name': 'allDimu_1',    'binning': (30, 0.0, 0.3),             'title': 'alldimu; #DeltaR; # Events'      },
	#{    'name': 'allDimu_2',    'binning': (30, 0.0, 0.3),             'title': 'alldimu; #DeltaR; # Events'      },
	#{    'name': 'allDimu_3',    'binning': (30, 0.0, 0.3),             'title': 'alldimu; #DeltaR; # Events'      },
	#{    'name': 'allDimu_4',    'binning': (30, 0.0, 0.3),             'title': 'alldimu; #DeltaR; # Events'      },
	#{    'name': 'allDimu_5',    'binning': (30, 0.0, 0.3),             'title': 'alldimu; #DeltaR; # Events'      },
	#{    'name': 'allDimu_6',    'binning': (30, 0.0, 0.3),             'title': 'alldimu; #DeltaR; # Events'      },
	#{    'name': 'allDimu_OR',   'binning': (30, 0.0, 0.3),             'title': 'alldimu_OR; #DeltaR; # Events'      },
	
	#{	'name': 'ptvsdR',			'binning': (60, 0, 0.2, 100, 0, 700),  'title': 'p_{t} vs #Delta R ; #Delta R ;p_{t}'},
	
	#{	'name': 'leaMuEta',			'binning': (100, -3.0, 3.0),           'title': 'Leading Muon #eta distribution; #eta ;Entries'},
	#{	'name': 'subleaMuEta',		'binning': (100, -3.0, 3.0),           'title': 'Sub-leading Muon #eta distribution;  #eta; Entries'},
	
	#{	'name': 'allDimu_pt',		'binning': (100, 0.0, 500),           'title': 'All Sub-leading Muon p_T distribution;  p_T [GeV]; Entries'},
	#{	'name': 'allDimu_ORpt',		'binning': (100, 0.0, 500),           'title': 'Pass Sub-leading Muon p_T distribution;  p_T [GeV]; Entries'},
	
	#{	'name': 'allDimu_slpT3b',		'binning': (7, 0.0, 500),           'title': 'Sub-leading Muon p_T distribution 3b;  p_T [GeV]; Entries'},
	#{	'name': 'allDimu_ORslpT3b',	'binning': (7, 0.0, 500),           'title': 'Pass Sub-leading Muon p_T distribution 3b;  p_T [GeV]; Entries'},
	
	#{	'name': 'allDimu_slpT20b',	'binning': (20, 0.0, 500),           'title': 'All Sub-leading Muon p_T distribution 20b;  p_T [GeV]; Entries'},
	#{	'name': 'allDimu_ORslpT20b',	'binning': (20, 0.0, 500),           'title': 'Pass Sub-leading Muon p_T distribution 20b;  p_T [GeV]; Entries'},
	
	#{	'name': 'allDimu_ORpt',		'binning': (100, 0.0, 500),           'title': 'Pass Sub-leading Muon p_T distribution;  p_T [GeV]; Entries'},
	#{	'name': 'allDimu_ORpt3b',	'binning': (7, 0.0, 500),           'title': 'Pass Sub-leading Muon p_T distribution 3b;  p_T [GeV]; Entries'},
	
	#{    'name': 'subleapTn3',   'binning': (3, 0.0, 200),           'title': 'Sub-leading Muon p_T distribution;  p_T [GeV]; Entries'},
	
	#{	'name': 'allDimu_slpT',			'binning': (100, 0.0, 500),           'title': 'leading Muon p_T distribution;  p_T [GeV]; Entries'},
	#{	'name': 'allDimu_ORslpT',			'binning': (100, 0.0, 500),           'title': 'Sub-leading Muon p_T distribution;  p_T [GeV]; Entries'},
	
	#{	'name': 'allDimu_hslpT',		'binning': (100, 0.0, 500),           'title': 'leading Muon p_T > 200 distribution;  p_T [GeV]; Entries'},
	#{	'name': 'allDimu_ORhslpT',		'binning': (100, 0.0, 500),           'title': 'Pass leading Muon p_T > 200 distribution;  p_T [GeV]; Entries'},
]

