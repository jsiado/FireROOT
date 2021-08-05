#!/usr/bin/env python
import math
from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *


class MyEvents(SignalEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)
    
    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']
        
        self.Histos['%s/oneTRG'%chan].Fill(250)
        
        #all double mu triggers 
        if getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha"): self.Histos['%s/oneTRG'%chan].Fill(10)
        if getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha_NoL2Matched"): self.Histos['%s/oneTRG'%chan].Fill(11)
        if getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed"): self.Histos['%s/oneTRG'%chan].Fill(12)
        if getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched"): self.Histos['%s/oneTRG'%chan].Fill(13)
        if getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha"): self.Histos['%s/oneTRG'%chan].Fill(14)
        if getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha_NoL2Matched"): self.Histos['%s/oneTRG'%chan].Fill(15)
        if getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha_CosmicSeed"): self.Histos['%s/oneTRG'%chan].Fill(16)
        if getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha_CosmicSeed_NoL2Matched"): self.Histos['%s/oneTRG'%chan].Fill(17)
        if getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha_Eta2p4"): self.Histos['%s/oneTRG'%chan].Fill(18)
        if getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4"): self.Histos['%s/oneTRG'%chan].Fill(19)
        if getattr(event.hlt, "DoubleL2Mu30NoVtx_2Cha_Eta2p4"): self.Histos['%s/oneTRG'%chan].Fill(20)
        #if getattr(event.hlt, "DoubleMu33NoFiltersNoVtxDisplaced"): self.Histos['%s/oneTRG'%chan].Fill(21)
        #if getattr(event.hlt, "DoubleMu40NoFiltersNoVtxDisplaced"): self.Histos['%s/oneTRG'%chan].Fill(22)
        #if getattr(event.hlt, "DoubleMu43NoFiltersNoVtx"): self.Histos['%s/oneTRG'%chan].Fill(23)
        #if getattr(event.hlt, "DoubleMu48NoFiltersNoVtx"): self.Histos['%s/oneTRG'%chan].Fill(24)
        
        # mu Egamma trigger
        #if getattr(event.hlt, "Mu38NoFiltersNoVtxDisplaced_Photon38_CaloIdL"): self.Histos['%s/oneTRG'%chan].Fill(40)
        #if getattr(event.hlt, "DiMu4_Ele9_CaloIdL_TrackIdL_DZ_Mass3p8"): self.Histos['%s/oneTRG'%chan].Fill(41)
        #if getattr(event.hlt, "DiMu9_Ele9_CaloIdL_TrackIdL_DZ"): self.Histos['%s/oneTRG'%chan].Fill(42)
        #if getattr(event.hlt, "DiMu9_Ele9_CaloIdL_TrackIdL"): self.Histos['%s/oneTRG'%chan].Fill(43)
        if getattr(event.hlt, "DoubleMu20_7_Mass0to30_L1_DM4EG"): self.Histos['%s/oneTRG'%chan].Fill(44)
        #if getattr(event.hlt, "DoubleMu20_7_Mass0to30_L1_DM4"):self.Histos['%s/oneTRG'%chan].Fill(45)
        #if getattr(event.hlt, "DoubleMu20_7_Mass0to30_Photon23"): self.Histos['%s/oneTRG'%chan].Fill(46)
        #if getattr(event.hlt, "Mu12_DoublePhoton20"): self.Histos['%s/oneTRG'%chan].Fill(47)
        '''if getattr(event.hlt, "Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"): self.Histos['%s/oneTRG'%chan].Fill(48)
        if getattr(event.hlt, "Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL"): self.Histos['%s/oneTRG'%chan].Fill(49)
        if getattr(event.hlt, "Mu17_Photon30_IsoCaloId"): self.Histos['%s/oneTRG'%chan].Fill(50)
        if getattr(event.hlt, "Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"): self.Histos['%s/oneTRG'%chan].Fill(51)
        if getattr(event.hlt, "Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL"): self.Histos['%s/oneTRG'%chan].Fill(52)
        if getattr(event.hlt, "Mu27_Ele37_CaloIdL_MW"): self.Histos['%s/oneTRG'%chan].Fill(53)
        if getattr(event.hlt, "Mu37_Ele27_CaloIdL_MW"): self.Histos['%s/oneTRG'%chan].Fill(54)'''
        if getattr(event.hlt, "Mu38NoFiltersNoVtxDisplaced_Photon38_CaloIdL"): self.Histos['%s/oneTRG'%chan].Fill(55)
        if getattr(event.hlt, "Mu43NoFiltersNoVtxDisplaced_Photon43_CaloIdL"): self.Histos['%s/oneTRG'%chan].Fill(56)
        if getattr(event.hlt, "Mu43NoFiltersNoVtx_Photon43_CaloIdL"): self.Histos['%s/oneTRG'%chan].Fill(57)
        if getattr(event.hlt, "Mu48NoFiltersNoVtx_Photon48_CaloIdL"): self.Histos['%s/oneTRG'%chan].Fill(58)
        '''if getattr(event.hlt, "Mu8_DiEle12_CaloIdL_TrackIdL_DZ"): self.Histos['%s/oneTRG'%chan].Fill(59)
        if getattr(event.hlt, "Mu8_DiEle12_CaloIdL_TrackIdL"): self.Histos['%s/oneTRG'%chan].Fill(60)
        if getattr(event.hlt, "Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT350_DZ"): self.Histos['%s/oneTRG'%chan].Fill(61)
        if getattr(event.hlt, "Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT350"): self.Histos['%s/oneTRG'%chan].Fill(62)'''
        
        #single Mu
        if getattr(event.hlt, "IsoMu24"):self.Histos['%s/oneTRG'%chan].Fill(70)
        if getattr(event.hlt, "Mu50"):self.Histos['%s/oneTRG'%chan].Fill(71)
        '''if getattr(event.hlt, "L1SingleMu18"):self.Histos['%s/oneTRG'%chan].Fill(72)
        if getattr(event.hlt, "L1SingleMu25"):self.Histos['%s/oneTRG'%chan].Fill(73)
        if getattr(event.hlt, "L2Mu10"):self.Histos['%s/oneTRG'%chan].Fill(74)
        if getattr(event.hlt, "L2Mu50"):self.Histos['%s/oneTRG'%chan].Fill(75)'''

        #Egamma
        #if getattr(event.hlt, "Photon100EBHE10"): self.Histos['%s/oneTRG'%chan].Fill(90)
        #if getattr(event.hlt, "Photon100EB_TightID_TightIso"): self.Histos['%s/oneTRG'%chan].Fill(91)
        #if getattr(event.hlt, "Photon100EEHE10"): self.Histos['%s/oneTRG'%chan].Fill(92)
        #if getattr(event.hlt, "Photon100EE_TightID_TightIso"): self.Histos['%s/oneTRG'%chan].Fill(93)
        if getattr(event.hlt, "Photon110EB_TightID_TightIso"): self.Histos['%s/oneTRG'%chan].Fill(94)
        if getattr(event.hlt, "Photon120EB_TightID_TightIso"): self.Histos['%s/oneTRG'%chan].Fill(95)
        '''if getattr(event.hlt, "Photon120_R9Id90_HE10_IsoM"): self.Histos['%s/oneTRG'%chan].Fill(96)
        if getattr(event.hlt, "Photon120"): self.Histos['%s/oneTRG'%chan].Fill(97)
        if getattr(event.hlt, "Photon150"): self.Histos['%s/oneTRG'%chan].Fill(98)
        if getattr(event.hlt, "Photon165_R9Id90_HE10_IsoM"): self.Histos['%s/oneTRG'%chan].Fill(99)
        if getattr(event.hlt, "Photon175"): self.Histos['%s/oneTRG'%chan].Fill(100)'''
        if getattr(event.hlt, "Photon200"): self.Histos['%s/oneTRG'%chan].Fill(101)
        '''if getattr(event.hlt, "Photon20_HoverELoose"): self.Histos['%s/oneTRG'%chan].Fill(102)
        if getattr(event.hlt, "Photon300_NoHE"): self.Histos['%s/oneTRG'%chan].Fill(103)
        if getattr(event.hlt, "Photon30_HoverELoose"): self.Histos['%s/oneTRG'%chan].Fill(104)
        if getattr(event.hlt, "Photon33"): self.Histos['%s/oneTRG'%chan].Fill(105)
        if getattr(event.hlt, "Photon50_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3_PFMET50"): self.Histos['%s/oneTRG'%chan].Fill(106)
        if getattr(event.hlt, "Photon50_R9Id90_HE10_IsoM"): self.Histos['%s/oneTRG'%chan].Fill(107)
        if getattr(event.hlt, "Photon50"): self.Histos['%s/oneTRG'%chan].Fill(108)
        if getattr(event.hlt, "Photon60_R9Id90_CaloIdL_IsoL_DisplacedIdL_PFHT350MinPFJet15"): self.Histos['%s/oneTRG'%chan].Fill(109)
        if getattr(event.hlt, "Photon60_R9Id90_CaloIdL_IsoL_DisplacedIdL"): self.Histos['%s/oneTRG'%chan].Fill(110)
        if getattr(event.hlt, "Photon60_R9Id90_CaloIdL_IsoL"): self.Histos['%s/oneTRG'%chan].Fill(111)
        if getattr(event.hlt, "Photon75_R9Id90_HE10_IsoM_EBOnly_CaloMJJ300_PFJetsMJJ400DEta3"): self.Histos['%s/oneTRG'%chan].Fill(112)
        if getattr(event.hlt, "Photon75_R9Id90_HE10_IsoM_EBOnly_CaloMJJ400_PFJetsMJJ600DEta3"): self.Histos['%s/oneTRG'%chan].Fill(113)
        if getattr(event.hlt, "Photon75_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3"): self.Histos['%s/oneTRG'%chan].Fill(114)
        if getattr(event.hlt, "Photon75_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ600DEta3"): self.Histos['%s/oneTRG'%chan].Fill(115)
        if getattr(event.hlt, "Photon75_R9Id90_HE10_IsoM"): self.Histos['%s/oneTRG'%chan].Fill(116)
        if getattr(event.hlt, "Photon75"): self.Histos['%s/oneTRG'%chan].Fill(117)
        if getattr(event.hlt, "Photon90_R9Id90_HE10_IsoM"): self.Histos['%s/oneTRG'%chan].Fill(118)
        if getattr(event.hlt, "Photon90" ): self.Histos['%s/oneTRG'%chan].Fill(119)'''
        
        # single electron
        if getattr(event.hlt, "Ele28_WPTight_Gsf"): self.Histos['%s/oneTRG'%chan].Fill(130)
        '''if getattr(event.hlt, "Ele115_CaloIdVT_GsfTrkIdT"): self.Histos['%s/oneTRG'%chan].Fill(131)
        if getattr(event.hlt, "Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30"): self.Histos['%s/oneTRG'%chan].Fill(132)
        if getattr(event.hlt, "Ele135_CaloIdVT_GsfTrkIdT"): self.Histos['%s/oneTRG'%chan].Fill(133)
        if getattr(event.hlt, "Ele145_CaloIdVT_GsfTrkIdT"): self.Histos['%s/oneTRG'%chan].Fill(134)
        #if getattr(event.hlt, "Ele15_IsoVVVL_PFHT450_CaloBTagCSV_4p5"): self.Histos['%s/oneTRG'%chan].Fill(135)
        #if getattr(event.hlt, "Ele15_IsoVVVL_PFHT450_PFMET50"): self.Histos['%s/oneTRG'%chan].Fill(136)
        if getattr(event.hlt, "Ele15_IsoVVVL_PFHT450"): self.Histos['%s/oneTRG'%chan].Fill(137)
        if getattr(event.hlt, "Ele15_IsoVVVL_PFHT600"): self.Histos['%s/oneTRG'%chan].Fill(138)
        if getattr(event.hlt, "Ele17_CaloIdM_TrackIdM_PFJet30"): self.Histos['%s/oneTRG'%chan].Fill(139)
        if getattr(event.hlt, "Ele200_CaloIdVT_GsfTrkIdT"): self.Histos['%s/oneTRG'%chan].Fill(140)
        if getattr(event.hlt, "Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30"): self.Histos['%s/oneTRG'%chan].Fill(141)
        if getattr(event.hlt, "Ele23_CaloIdM_TrackIdM_PFJet30"): self.Histos['%s/oneTRG'%chan].Fill(142)
        if getattr(event.hlt, "Ele250_CaloIdVT_GsfTrkIdT"): self.Histos['%s/oneTRG'%chan].Fill(143)
        if getattr(event.hlt, "Ele27_WPTight_Gsf"): self.Histos['%s/oneTRG'%chan].Fill(144)
        if getattr(event.hlt, "Ele28_eta2p1_WPTight_Gsf_HT150"): self.Histos['%s/oneTRG'%chan].Fill(145)
        if getattr(event.hlt, "Ele300_CaloIdVT_GsfTrkIdT"): self.Histos['%s/oneTRG'%chan].Fill(146)
        if getattr(event.hlt, "Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned"): self.Histos['%s/oneTRG'%chan].Fill(147)
        if getattr(event.hlt, "Ele32_WPTight_Gsf_L1DoubleEG"): self.Histos['%s/oneTRG'%chan].Fill(148)
        if getattr(event.hlt, "Ele32_WPTight_Gsf"): self.Histos['%s/oneTRG'%chan].Fill(149)
        if getattr(event.hlt, "Ele35_WPTight_Gsf_L1EGMT"): self.Histos['%s/oneTRG'%chan].Fill(150)
        if getattr(event.hlt, "Ele35_WPTight_Gsf"): self.Histos['%s/oneTRG'%chan].Fill(151)
        if getattr(event.hlt, "Ele38_WPTight_Gsf"): self.Histos['%s/oneTRG'%chan].Fill(152)
        if getattr(event.hlt, "Ele40_WPTight_Gsf"): self.Histos['%s/oneTRG'%chan].Fill(153)
        if getattr(event.hlt, "Ele50_CaloIdVT_GsfTrkIdT_PFJet165"): self.Histos['%s/oneTRG'%chan].Fill(154)
        if getattr(event.hlt, "Ele50_IsoVVVL_PFHT450"): self.Histos['%s/oneTRG'%chan].Fill(155)
        if getattr(event.hlt, "Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30"): self.Histos['%s/oneTRG'%chan].Fill(156)
        if getattr(event.hlt, "Ele8_CaloIdM_TrackIdM_PFJet30"): self.Histos['%s/oneTRG'%chan].Fill(157)'''
        
        # tri muon
        if getattr(event.hlt, "TrkMu16_DoubleTrkMu6NoFiltersNoVtx"): self.Histos['%s/oneTRG'%chan].Fill(170)
        
        DoubleMu = ["DoubleL2Mu23NoVtx_2Cha", "DoubleL2Mu23NoVtx_2Cha_NoL2Matched", "DoubleL2Mu23NoVtx_2Cha_CosmicSeed", "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched", "DoubleL2Mu25NoVtx_2Cha", "DoubleL2Mu25NoVtx_2Cha_NoL2Matched", "DoubleL2Mu25NoVtx_2Cha_CosmicSeed", "DoubleL2Mu25NoVtx_2Cha_CosmicSeed_NoL2Matched", "DoubleL2Mu25NoVtx_2Cha_Eta2p4", "DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4", "DoubleL2Mu30NoVtx_2Cha_Eta2p4", "DoubleMu33NoFiltersNoVtxDisplaced", "DoubleMu40NoFiltersNoVtxDisplaced", "DoubleMu43NoFiltersNoVtx", "DoubleMu48NoFiltersNoVtx"]

        # all double Mu
        if getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha") or getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha_NoL2Matched") or getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed") or getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched") or getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha") or getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha_NoL2Matched") or getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha_CosmicSeed") or getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha_CosmicSeed_NoL2Matched") or getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha_Eta2p4") or getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4") or getattr(event.hlt, "DoubleL2Mu30NoVtx_2Cha_Eta2p4") or getattr(event.hlt, "DoubleMu33NoFiltersNoVtxDisplaced") or getattr(event.hlt, "DoubleMu40NoFiltersNoVtxDisplaced") or getattr(event.hlt, "DoubleMu43NoFiltersNoVtx") or getattr(event.hlt, "DoubleMu48NoFiltersNoVtx"): self.Histos['%s/oneTRG'%chan].Fill(200)
        
        #all MuEGamma
        if getattr(event.hlt, "Mu38NoFiltersNoVtxDisplaced_Photon38_CaloIdL") or getattr(event.hlt, "DiMu4_Ele9_CaloIdL_TrackIdL_DZ_Mass3p8") or getattr(event.hlt, "DiMu9_Ele9_CaloIdL_TrackIdL_DZ") or getattr(event.hlt, "DiMu9_Ele9_CaloIdL_TrackIdL") or getattr(event.hlt, "DoubleMu20_7_Mass0to30_L1_DM4EG") or getattr(event.hlt, "DoubleMu20_7_Mass0to30_L1_DM4") or getattr(event.hlt, "DoubleMu20_7_Mass0to30_Photon23") or getattr(event.hlt, "Mu12_DoublePhoton20") or getattr(event.hlt, "Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ") or getattr(event.hlt, "Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL") or getattr(event.hlt, "Mu17_Photon30_IsoCaloId") or getattr(event.hlt, "Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ") or getattr(event.hlt, "Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL") or getattr(event.hlt, "Mu27_Ele37_CaloIdL_MW") or getattr(event.hlt, "Mu37_Ele27_CaloIdL_MW") or getattr(event.hlt, "Mu38NoFiltersNoVtxDisplaced_Photon38_CaloIdL") or getattr(event.hlt, "Mu43NoFiltersNoVtxDisplaced_Photon43_CaloIdL") or getattr(event.hlt, "Mu43NoFiltersNoVtx_Photon43_CaloIdL") or getattr(event.hlt, "Mu48NoFiltersNoVtx_Photon48_CaloIdL") or getattr(event.hlt, "Mu8_DiEle12_CaloIdL_TrackIdL_DZ") or getattr(event.hlt, "Mu8_DiEle12_CaloIdL_TrackIdL") or getattr(event.hlt, "Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT350_DZ") or getattr(event.hlt, "Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT350"): self.Histos['%s/oneTRG'%chan].Fill(210)
        
        #all single Mu
        if getattr(event.hlt, "IsoMu24") or getattr(event.hlt, "Mu50") or getattr(event.hlt, "L1SingleMu18") or getattr(event.hlt, "L1SingleMu25") or getattr(event.hlt, "L2Mu10") or getattr(event.hlt, "L2Mu50"): self.Histos['%s/oneTRG'%chan].Fill(220)

        #all Egamma
        if getattr(event.hlt, "Photon100EBHE10") or getattr(event.hlt, "Photon100EB_TightID_TightIso") or getattr(event.hlt, "Photon100EEHE10") or getattr(event.hlt, "Photon100EE_TightID_TightIso") or getattr(event.hlt, "Photon110EB_TightID_TightIso") or getattr(event.hlt, "Photon120EB_TightID_TightIso") or getattr(event.hlt, "Photon120_R9Id90_HE10_IsoM") or getattr(event.hlt, "Photon120") or getattr(event.hlt, "Photon150") or getattr(event.hlt, "Photon165_R9Id90_HE10_IsoM") or getattr(event.hlt, "Photon175") or getattr(event.hlt, "Photon200") or getattr(event.hlt, "Photon20_HoverELoose") or getattr(event.hlt, "Photon300_NoHE") or getattr(event.hlt, "Photon30_HoverELoose") or getattr(event.hlt, "Photon33") or getattr(event.hlt, "Photon50_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3_PFMET50") or getattr(event.hlt, "Photon50_R9Id90_HE10_IsoM") or getattr(event.hlt, "Photon50") or getattr(event.hlt, "Photon60_R9Id90_CaloIdL_IsoL_DisplacedIdL_PFHT350MinPFJet15") or getattr(event.hlt, "Photon60_R9Id90_CaloIdL_IsoL_DisplacedIdL") or getattr(event.hlt, "Photon60_R9Id90_CaloIdL_IsoL") or getattr(event.hlt, "Photon75_R9Id90_HE10_IsoM_EBOnly_CaloMJJ300_PFJetsMJJ400DEta3") or getattr(event.hlt, "Photon75_R9Id90_HE10_IsoM_EBOnly_CaloMJJ400_PFJetsMJJ600DEta3") or getattr(event.hlt, "Photon75_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3") or getattr(event.hlt, "Photon75_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ600DEta3") or getattr(event.hlt, "Photon75_R9Id90_HE10_IsoM") or getattr(event.hlt, "Photon75") or getattr(event.hlt, "Photon90_R9Id90_HE10_IsoM") or getattr(event.hlt, "Photon90" ): self.Histos['%s/oneTRG'%chan].Fill(230)

        #sinPho
        if getattr(event.hlt, "Photon110EB_TightID_TightIso") or getattr(event.hlt, "Photon120EB_TightID_TightIso") or getattr(event.hlt, "Photon200"): self.Histos['%s/oneTRG'%chan].Fill(235)
        
        #all Single Ele
        if getattr(event.hlt, "Ele28_WPTight_Gsf") or getattr(event.hlt, "Ele115_CaloIdVT_GsfTrkIdT") or getattr(event.hlt, "Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30") or getattr(event.hlt, "Ele135_CaloIdVT_GsfTrkIdT") or getattr(event.hlt, "Ele145_CaloIdVT_GsfTrkIdT") or getattr(event.hlt, "Ele15_IsoVVVL_PFHT450_CaloBTagCSV_4p5") or getattr(event.hlt, "Ele15_IsoVVVL_PFHT450_PFMET50") or getattr(event.hlt, "Ele15_IsoVVVL_PFHT450") or getattr(event.hlt, "Ele15_IsoVVVL_PFHT600") or getattr(event.hlt, "Ele17_CaloIdM_TrackIdM_PFJet30") or getattr(event.hlt, "Ele200_CaloIdVT_GsfTrkIdT") or getattr(event.hlt, "Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30") or getattr(event.hlt, "Ele23_CaloIdM_TrackIdM_PFJet30") or getattr(event.hlt, "Ele250_CaloIdVT_GsfTrkIdT") or getattr(event.hlt, "Ele27_WPTight_Gsf") or getattr(event.hlt, "Ele28_eta2p1_WPTight_Gsf_HT150") or getattr(event.hlt, "Ele300_CaloIdVT_GsfTrkIdT") or getattr(event.hlt, "Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned") or getattr(event.hlt, "Ele32_WPTight_Gsf_L1DoubleEG") or getattr(event.hlt, "Ele32_WPTight_Gsf") or getattr(event.hlt, "Ele35_WPTight_Gsf_L1EGMT") or getattr(event.hlt, "Ele35_WPTight_Gsf") or getattr(event.hlt, "Ele38_WPTight_Gsf") or getattr(event.hlt, "Ele40_WPTight_Gsf") or getattr(event.hlt, "Ele50_CaloIdVT_GsfTrkIdT_PFJet165") or getattr(event.hlt, "Ele50_IsoVVVL_PFHT450") or getattr(event.hlt, "Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30") or getattr(event.hlt, "Ele8_CaloIdM_TrackIdM_PFJet30"): self.Histos['%s/oneTRG'%chan].Fill(240)

        if not (getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha") or getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha_NoL2Matched") or getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed") or getattr(event.hlt, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched") or getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha") or getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha_NoL2Matched") or getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha_CosmicSeed") or getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha_CosmicSeed_NoL2Matched") or getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha_Eta2p4") or getattr(event.hlt, "DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4") or getattr(event.hlt, "DoubleL2Mu30NoVtx_2Cha_Eta2p4")):
            if getattr(event.hlt, "IsoMu24"): self.Histos['%s/oneTRG'%chan].Fill(260)
            if getattr(event.hlt, "Mu50"): self.Histos['%s/oneTRG'%chan].Fill(261)
            if getattr(event.hlt, "Mu38NoFiltersNoVtxDisplaced_Photon38_CaloIdL"): self.Histos['%s/oneTRG'%chan].Fill(262)
            if getattr(event.hlt, "DoubleMu20_7_Mass0to30_L1_DM4EG"): self.Histos['%s/oneTRG'%chan].Fill(263)
            if getattr(event.hlt, "Mu43NoFiltersNoVtxDisplaced_Photon43_CaloIdL"): self.Histos['%s/oneTRG'%chan].Fill(264)
            if getattr(event.hlt, "Mu43NoFiltersNoVtx_Photon43_CaloIdL"): self.Histos['%s/oneTRG'%chan].Fill(265)
            if getattr(event.hlt, "Mu48NoFiltersNoVtx_Photon48_CaloIdL"): self.Histos['%s/oneTRG'%chan].Fill(266)
            if getattr(event.hlt, "Photon110EB_TightID_TightIso"): self.Histos['%s/oneTRG'%chan].Fill(267)
            if getattr(event.hlt, "Photon120EB_TightID_TightIso"): self.Histos['%s/oneTRG'%chan].Fill(268)
            if getattr(event.hlt, "Photon200"): self.Histos['%s/oneTRG'%chan].Fill(269)
            if getattr(event.hlt, "Mu38NoFiltersNoVtxDisplaced_Photon38_CaloIdL") or getattr(event.hlt, "Photon110EB_TightID_TightIso"): self.Histos['%s/oneTRG'%chan].Fill(271)
            if getattr(event.hlt, "Mu38NoFiltersNoVtxDisplaced_Photon38_CaloIdL") or getattr(event.hlt, "Photon120EB_TightID_TightIso"): self.Histos['%s/oneTRG'%chan].Fill(272)
            if getattr(event.hlt, "Mu38NoFiltersNoVtxDisplaced_Photon38_CaloIdL") or getattr(event.hlt, "Photon200"): self.Histos['%s/oneTRG'%chan].Fill(273)


histCollection = [
    {'name': 'oneTRG',        'binning': (300, 0, 300.0),        'title': 'Number of events;Trigger path;counts'},
                 ]
