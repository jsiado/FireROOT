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
		
                
		#for i, mu in enumerate(event.ljsources): solo por
		#	if 
		#
                #
                #
                
                # counting the events in the with two muons vs those with two muons passing one of the triggers 
		dsa = [p for p in event.dsamuons
		if p.p4.pt()>30 \
		and abs(p.p4.eta())<2.4]#\
		#and p.vtx.Rho()<700] #\
		#if abs(p.pid) == 13]

		if len(dsa) < 2 : return
		if len(dsa) == 2:
			dR01 = DeltaR(dsa[0].p4, dsa[1].p4)
			self.Histos['%s/dR01'%chan].Fill(dR01)
			self.Histos['%s/eNum'%chan].Fill(4)
			if dR01 > 0.4: return
			
			if dsa[0].p4.pt()>dsa[1].p4.pt():
				self.Histos['%s/ptvsdR'%chan].Fill(dR01,dsa[1].p4.pt())
				self.Histos['%s/leaMuEta'%chan].Fill(dsa[0].p4.eta())
				self.Histos['%s/subleaMuEta'%chan].Fill(dsa[1].p4.eta())
				subleapT = dsa[1].p4.pt()
				leapT = dsa[0].p4.pt()
				
			if dsa[1].p4.pt()>dsa[0].p4.pt():
				self.Histos['%s/ptvsdR'%chan].Fill(dR01,dsa[0].p4.pt())
				self.Histos['%s/leaMuEta'%chan].Fill(dsa[1].p4.eta())
				self.Histos['%s/subleaMuEta'%chan].Fill(dsa[0].p4.eta())
				subleapT = dsa[0].p4.pt()
				leapT = dsa[1].p4.pt()

			self.Histos['%s/allDimu_dR'%chan].Fill(dR01)
			self.Histos['%s/allDimu_lpT'%chan].Fill(leapT)
			self.Histos['%s/allDimu_slpT'%chan].Fill(subleapT)
			#self.Histos['%s/allDimu_slpT3b'%chan].Fill(subleapT)
			#self.Histos['%s/allDimu_slpT20b'%chan].Fill(subleapT)
			#if leapT > 200: self.Histos['%s/allDimu_hslpT'%chan].Fill(subleapT)
			
			if getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha") or getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha_NoL2Matched") or getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed") or getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched") or getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha_Eta2p4") or getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4"):
				self.Histos['%s/allDimu_ORdR'%chan].Fill(dR01)
				self.Histos['%s/allDimu_ORlpT'%chan].Fill(leapT)
				self.Histos['%s/allDimu_ORslpT'%chan].Fill(subleapT)
				self.Histos['%s/eNum'%chan].Fill(8)
				#self.Histos['%s/allDimu_ORslpT3b'%chan].Fill(subleapT)
				#self.Histos['%s/allDimu_ORslpT20b'%chan].Fill(subleapT)				
				#if leapT > 200: self.Histos['%s/allDimu_ORhslpT'%chan].Fill(subleapT)
				
histCollection = [
	{	'name': 'dR01',			'binning': (30, 0.0, 0.3),	       'title': '#Delta R between muons 0 and 1; #Delta R;# Events'   },
	{	'name': 'eNum',			'binning': (10, 0.0, 10.0),	       'title': 'Number of events; #mu collection;# Events'   },
        {	'name': 'allDimu_dR',		'binning': (30, 0.0, 1.0),	       'title': 'alldimu; #DeltaR; # Events'      },
	{	'name': 'allDimu_ORdR',		'binning': (30, 0.0, 1.0),             'title': 'alldimu_OR; #DeltaR; # Events'      },
	{	'name': 'allDimu_lpT',		'binning': (100, 0.0, 1000),           'title': 'All Sub-leading Muon p_T distribution;  p_T [GeV]; Entries'},
	{	'name': 'allDimu_ORlpT',	'binning': (100, 0.0, 1000),           'title': 'Pass Sub-leading Muon p_T distribution;  p_T [GeV]; Entries'},
	{	'name': 'ptvsdR',		'binning': (60, 0, 1.0, 100, 0, 1000), 'title': 'p_{t} vs #Delta R ; #Delta R ;p_{t}'},
	{	'name': 'leaMuEta',		'binning': (100, -3.5, 3.5),           'title': 'Leading Muon #eta distribution; #eta ;Entries'},
	{	'name': 'subleaMuEta',		'binning': (100, -3.5, 3.5),           'title': 'Sub-leading Muon #eta distribution;  #eta; Entries'},
	#{	'name': 'allDimu_pt',		'binning': (100, 0.0, 500),            'title': 'All Sub-leading Muon p_T distribution;  p_T [GeV]; Entries'},
	#{	'name': 'allDimu_ORpt',		'binning': (100, 0.0, 500),            'title': 'Pass Sub-leading Muon p_T distribution;  p_T [GeV]; Entries'},
	#{	'name': 'allDimu_slpT3b',	'binning': (7, 0.0, 500),              'title': 'Sub-leading Muon p_T distribution 3b;  p_T [GeV]; Entries'},
	#{	'name': 'allDimu_ORslpT3b',	'binning': (7, 0.0, 500),              'title': 'Pass Sub-leading Muon p_T distribution 3b;  p_T [GeV]; Entries'},
	#{	'name': 'allDimu_slpT20b',	'binning': (20, 0.0, 500),             'title': 'All Sub-leading Muon p_T distribution 20b;  p_T [GeV]; Entries'},
	#{	'name': 'allDimu_ORslpT20b',	'binning': (20, 0.0, 500),             'title': 'Pass Sub-leading Muon p_T distribution 20b;  p_T [GeV]; Entries'},
	#{	'name': 'allDimu_ORpt',		'binning': (100, 0.0, 500),            'title': 'Pass Sub-leading Muon p_T distribution;  p_T [GeV]; Entries'},
	#{	'name': 'allDimu_ORpt3b',	'binning': (7, 0.0, 500),              'title': 'Pass Sub-leading Muon p_T distribution 3b;  p_T [GeV]; Entries'},
        #{      'name': 'subleapTn3',           'binning': (3, 0.0, 200),              'title': 'Sub-leading Muon p_T distribution;  p_T [GeV]; Entries'},
	{	'name': 'allDimu_slpT',		'binning': (100, 0.0, 1000),           'title': 'leading Muon p_T distribution;  p_T [GeV]; Entries'},
	{	'name': 'allDimu_ORslpT'	'binning': (100, 0.0, 1000),           'title': 'Sub-leading Muon p_T distribution;  p_T [GeV]; Entries'},
	#{	'name': 'allDimu_hslpT',	'binning': (100, 0.0, 500),            'title': 'leading Muon p_T > 200 distribution;  p_T [GeV]; Entries'},
	#{	'name': 'allDimu_ORhslpT',	'binning': (100, 0.0, 500),            'title': 'Pass leading Muon p_T > 200 distribution;  p_T [GeV]; Entries'},
]

