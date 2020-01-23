#!/usr/bin/env python
from rootpy.tree import Tree, TreeChain
from rootpy.io import root_open
import rootpy.ROOT as ROOT

import os
import logging
logging.getLogger('rootpy.tree.chain').setLevel(logging.WARNING)
logging.getLogger('rootpy.interactive.rootwait').setLevel(logging.ERROR)


DeltaPhi = ROOT.Math.VectorUtil.DeltaPhi
DeltaR = ROOT.Math.VectorUtil.DeltaR


class LeptonJetMix(object):

    def nPFMu(self):
        return list(self.pfcand_type).count(3)

    def nDSA(self):
        return list(self.pfcand_type).count(8)

    def nMuon(self):
        return self.nPFMu() + self.nDSA()

    def type(self):
        if self.nMuon()==0: return 0
        elif self.nPFMu()>=2 and self.nDSA()==0: return 1
        elif self.nDSA()>0: return 2
        else: return -1

    def isMuonType(self):
        return self.nMuon()>=2

    def isEgmType(self):
        return self.nMuon()==0

    def qSum(self):
        return sum(list(self.pfcand_charge))

    def isNeutral(self):
        if self.isEgmType(): return True
        if self.isMuonType(): return self.qSum()==0

    def dRcosmicDSA(self, event):
        return [event.dsamuons[i].deltaRCosmicDSA for i in self.pfcand_dsamuonIdx]

    def dRcosmicSeg(self, event):
        return [event.dsamuons[i].deltaRCosmicSeg for i in self.pfcand_dsamuonIdx]

    def passCosmicVeto(self, event, thres=0.05):
        if self.isEgmType(): return True

        drcosmicDSA = self.dRcosmicDSA(event)
        drcosmicSeg = self.dRcosmicSeg(event)

        if drcosmicDSA:
            drcosmicDSAmin = min(drcosmicDSA)
            if drcosmicDSAmin<=thres: return False
            elif drcosmicSeg: return min(drcosmicSeg)>thres
            else: return True
        elif drcosmicSeg:
            return min(drcosmicSeg)>thres
        else:
            return True

    def maxTrackNormChi2(self):
        tkNormChi2 = list(self.pfcand_tkNormChi2)
        if tkNormChi2:
            return max(tkNormChi2)
        else:
            return -1

    def minTrackNormChi2(self):
        tkNormChi2 = list(self.pfcand_tkNormChi2)
        if tkNormChi2:
            return min(tkNormChi2)
        else:
            return -1

    def minTwoTrackDist(self):
        import math
        return -1 if math.isnan(self.pfcands_minTwoTkDist) else self.pfcands_minTwoTkDist

    def minTkD0(self):
        import math
        return -1 if math.isnan(self.pfcand_tkD0Min) else self.pfcand_tkD0Min

    def pfiso(self):
        return self.pfIsolationNoPU05

    def passSelection(self, event):
        if self.p4.pt()<30: return False
        if self.minTwoTrackDist()>=50: return False
        if not self.isNeutral(): return False
        # if not self.passCosmicVeto(event): return False
        # if self.pfiso()>=0.12: return False
        # if self.maxTrackNormChi2()>=2: return False
        # if self.isMuonType() and self.minTkD0()>0 and self.minTkD0()<=0.1: return False

        return True



class Events(object):
    def __init__(self, files=None, type='MC'):

        if type.upper() not in ['MC', 'DATA']: raise ValueError("Argument `type` need to be MC/DATA")
        self.Type = type

        if not files: raise ValueError("Argument `files` need to be non-empty")
        if isinstance(files, str): files = [files,]
        self.Chain = TreeChain('ffNtuplizer/ffNtuple', files)

        ### register collections ###
        # self.Chain.define_collection('pvs', prefix='pv_', size='pv_n')
        # self.Chain.define_collection('electrons', prefix='electron_', size='electron_n')
        # self.Chain.define_collection('muons', prefix='muon_', size='muon_n')
        self.Chain.define_collection('dsamuons', prefix='dsamuon_', size='dsamuon_n')
        # self.Chain.define_collection('photons', prefix='photon_', size='photon_n')
        # self.Chain.define_collection('cosmiconelegs', prefix='cosmiconeleg_', size='cosmiconeleg_n')
        # self.Chain.define_collection('ak4jets', prefix='akjet_ak4PFJetsCHS', size='akjet_ak4PFJetsCHS_n')
        # self.Chain.define_collection('hftagscores', prefix='hftagscore_', size='hftagscore_n')
        self.Chain.define_collection('leptonjets', prefix='pfjet_', size='pfjet_n', mix=LeptonJetMix)
        # self.Chain.define_collection('ljsources', prefix='ljsource_', size='ljsource_n')

        self.Chain.define_object('hlt', prefix='HLT_')
        self.Chain.define_object('metfilters', prefix='metfilters_')
        self.Chain.define_object('cosmicveto', prefix='cosmicveto_')

        self.Triggers = [
            "DoubleL2Mu23NoVtx_2Cha",
            "DoubleL2Mu23NoVtx_2Cha_NoL2Matched",
            "DoubleL2Mu23NoVtx_2Cha_CosmicSeed",
            "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched",
            "DoubleL2Mu25NoVtx_2Cha_Eta2p4",
            "DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4",
        ]

        self.Histos = {}

        self.LookupWeight = root_open(os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/data/puWeights_10x_56ifb.root')).Get('puWeights')
        self.Scale = 1.

    def setTriggers(self, triggers):
        self.Triggers = triggers
    def addTrigger(self, trigger):
        self.Triggers.append(trigger)

    def bookHisto(self, name, hist):
        self.Histos[name] = hist

    def setScale(self, scale):
        self.Scale = scale

    def process(self):

        for i, event in enumerate(self.Chain):

            ## trigger ##
            if not any([getattr(event.hlt, t) for t in self.Triggers]): continue

            ## event-level mask ##
            if not event.cosmicveto.result: continue
            if not event.metfilters.PrimaryVertexFilter: continue

            aux = {}
            ## event weight ##
            aux['wgt'] = self.Scale
            if self.Type == 'MC':
                aux['wgt'] *= event.weight # gen weight
                aux['wgt'] *= self.LookupWeight.GetBinContent(self.LookupWeight.GetXaxis().FindBin(event.trueInteractionNum)) ## pileup correction


            leptonjets = [lj for lj in event.leptonjets if lj.passSelection(event)]
            if len(leptonjets)<2: continue
            sorted(leptonjets, key=lambda lj: lj.p4.pt(), reverse=True)
            LJ0 = leptonjets[0]
            LJ1 = leptonjets[1]

            if LJ0.isMuonType() and LJ1.isMuonType(): aux['channel'] = '4mu'
            elif LJ0.isMuonType() and LJ1.isEgmType(): aux['channel'] = '2mu2e'
            elif LJ0.isEgmType() and LJ1.isMuonType(): aux['channel'] = '2mu2e'
            else: continue


            aux['lj0'] = LJ0
            aux['lj1'] = LJ1


            self.processEvent(event, aux)


    def processEvent(self, event, aux):
        """To be override by daughter class"""
        pass

    @property
    def histos(self):
        return self.Histos





