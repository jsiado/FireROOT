#!/usr/bin/env python
from rootpy.tree import Tree, TreeChain
from rootpy.io import root_open
import rootpy.ROOT as ROOT
from tqdm import tqdm
import os
import logging
logging.getLogger('rootpy.tree.chain').setLevel(logging.WARNING)
logging.getLogger('rootpy.interactive.rootwait').setLevel(logging.ERROR)


class LeptonJetMix(object):

    def nPFMu(self):
        return list(self.pfcand_type).count(3)

    def nDSA(self):
        return list(self.pfcand_type).count(8)

    def nPFElectron(self):
        return list(self.pfcand_type).count(2)

    def nPFPhoton(self):
        return list(self.pfcand_type).count(4)

    def nMuon(self):
        return self.nPFMu() + self.nDSA()

    def nDaughters(self):
        return len(list(self.pfcand_type))

    def type(self):
        if self.nMuon()==0: return 0
        elif self.nPFMu()>=2 and self.nDSA()==0: return 1
        elif self.nDSA()>0: return 2
        else: return -1

    def isMuonType(self):
        return self.nMuon()>=2

    def isPFMuType():
        return self.type()==1

    def isDSAType():
        return self.type()==2

    def isEgmType(self):
        return self.nMuon()==0

    def isElectronType(self):
        return self.isEgmType() and self.nPFElectron()>0

    def isPhotonType(self):
        return self.isEgmType() and self.nPFElectron()==0

    def qSum(self):
        return sum(list(self.pfcand_charge))

    def muonQSum(self):
        res = 0
        for ctype, q in zip(list(self.pfcand_type), list(self.pfcand_charge)):
            if ctype==3 or ctype==8: res+=q
        return res

    def isMuonNeutral(self):
        if self.isEgmType(): return True
        if self.isMuonType(): return self.muonQSum()==0

    def isMuonCharged(self):
        if self.isEgmType(): return True
        if self.isMuonType(): return self.muonQSum()!=0

    def dRcosmicDSA(self, event):
        return [event.dsamuons[i].deltaRCosmicDSA for i in self.pfcand_dsamuonIdx]

    def dRcosmicSeg(self, event):
        return [event.dsamuons[i].deltaRCosmicSeg for i in self.pfcand_dsamuonIdx]

    def muons(self, event):
        res = [event.muons[i] for i in self.pfcand_pfmuonIdx]
        res += [event.dsamuons[i] for i in self.pfcand_dsamuonIdx]
        return res

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

    def pfhadiso(self):
        return self.hadIsolationNoPU05

    def passSelection(self, event):
        if self.p4.pt()<30: return False
        if abs(self.p4.eta())>2.4: return False
        if self.minTwoTrackDist()>=20: return False
        if self.isMuonType() and max([abs(dz) for dz in self.pfcand_tkDz])>40: return False
        if not self.isMuonNeutral(): return False

        return True

    def passSelectionIncCosmic(self, event):
        '''turn off cosmic vetos'''
        if self.p4.pt()<30: return False
        if abs(self.p4.eta())>2.4: return False
        if not self.isMuonNeutral(): return False

        return True

    def passChargedSelection(self, event):
        if self.p4.pt()<30: return False
        if abs(self.p4.eta())>2.4: return False
        if self.minTwoTrackDist()>=20: return False
        if self.isMuonType() and max([abs(dz) for dz in self.pfcand_tkDz])>40: return False
        if not self.isMuonCharged(): return False

        return True


class ProxyMuonMix(object):

    def isPFMuon(self):
        return self.type==3

    def isDSA(self):
        return self.type==8

    def pfiso(self):
        return 1-self.pfIsolationNoPU05

    def muon(self, event):
        if self.isPFMuon():
            return event.muons[self.refIdx]
        if self.isDSA():
            return event.dsamuons[self.refIdx]

    def d0(self, event):
        return self.muon(event).d0

    def dz(self, event):
        return self.muon(event).dz

    def d0sig(self, event):
        return self.muon(event).d0Sig

    def passSelection(self):
        if self.p4.pt()<30: return False
        if abs(self.p4.eta())>2.4: return False
        return True


def globalCosmicShower(cosmicMuons, channel):
    from FireROOT.Analysis.Utils import computeCosAlpha

    cosmic_metric = {'4mu': 6, '2mu2e': 6}
    nppCOSMIC = 0
    for i, cosmic_i in enumerate(cosmicMuons):
        if cosmic_i.p4.pt()<5 or abs(cosmic_i.p4.eta())>1.2: continue
        for j, cosmic_j in enumerate(cosmicMuons):
            if j<=i: continue
            if cosmic_j.p4.pt()<5 or abs(cosmic_j.p4.eta())>1.2: continue
            cosalpha = computeCosAlpha(cosmic_i.p4, cosmic_j.p4)
            if abs(cosalpha)<0.99: continue
            nppCOSMIC+=1

    return nppCOSMIC, nppCOSMIC>cosmic_metric[channel]



class Events(object):
    def __init__(self, files=None, outname=None, type='MC', dtag='', maxevents=-1, channel=['4mu', '2mu2e'], ctau=None, chargedlj=False):

        if type.upper() not in ['MC', 'DATA']: raise ValueError("Argument `type` need to be MC/DATA")
        self.OutName = outname
        self.Type = type.upper()
        self.ChargedLJ = chargedlj
        self.MaxEvents = maxevents
        self.Channel = channel
        self.Dtag = dtag
        self.Ctau = ctau
        __signal_sample_param = dict([substr.split('-') for substr in self.Dtag.split('_')])
        self.SignalParam = {k.upper(): float(v.replace('p', '.')) for k, v in __signal_sample_param.items()}

        if not files: raise ValueError("Argument `files` need to be non-empty")
        if isinstance(files, str): files = [files,]
        self.Chain = TreeChain('ffNtuplizer/ffNtuple', files)

        ### register collections ###
        # self.Chain.define_collection('pvs', prefix='pv_', size='pv_n')
        self.Chain.define_collection('electrons', prefix='electron_', size='electron_n')
        self.Chain.define_collection('muons', prefix='muon_', size='muon_n')
        self.Chain.define_collection('dsamuons', prefix='dsamuon_', size='dsamuon_n')
        self.Chain.define_collection('photons', prefix='photon_', size='photon_n')
        self.Chain.define_collection('ak4jets', prefix='akjet_ak4PFJetsCHS_', size='akjet_ak4PFJetsCHS_n')
        self.Chain.define_collection('hftagscores', prefix='hftagscore_', size='hftagscore_n')
        self.Chain.define_collection('leptonjets', prefix='pfjet_', size='pfjet_n', mix=LeptonJetMix)
        self.Chain.define_collection('ljsources', prefix='ljsource_', size='ljsource_n')
        self.Chain.define_collection('cosmicmuons', prefix='cosmicmuon_', size='cosmicmuon_n')

        self.Chain.define_collection('trigobjs', prefix='trigobj_', size='trigobj_n')

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
        for chan in channel:
            self.Histos['{}/cutflow'.format(chan)] = ROOT.Hist(20,0,20,title='cutflow',drawstyle='hist')
        self.KeepCutFlow = False
        self.RawCutFlow = False

        self.LookupWeight = root_open(os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/data/PUWeights_2018.root')).Get('puWeights')
        self.LookupMuonSFLowpT = root_open(os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/data/mu_Loose_pt7.root')).Get('ratio_syst')
        self.LookupMuonSF = root_open(os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/data/RunABCD_SF_ID.root')).Get('NUM_LooseID_DEN_TrackerMuons_pt_abseta_syst')
        self.LookupElectronSF = root_open(os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/data/2018_ElectronLoose.root')).Get('EGamma_SF2D')
        self.LookupPhotonSF = root_open(os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/data/2018_PhotonsLoose.root')).Get('EGamma_SF2D')
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
            if self.MaxEvents>0 and i>self.MaxEvents: break

            ## event weight ##
            aux = {}
            aux['wgt'] = self.Scale
            if self.Type == 'MC':
                aux['wgt'] *= event.weight # gen weight
                aux['wgt'] *= self.LookupWeight.GetBinContent(self.LookupWeight.GetXaxis().FindBin(event.trueInteractionNum)) ## pileup correction

            for ch in self.Channel:
                if self.RawCutFlow: self.Histos['{}/cutflow'.format(ch)].Fill(0)
                else: self.Histos['{}/cutflow'.format(ch)].Fill(0, aux['wgt'])

            ## trigger ##
            if not any([getattr(event.hlt, t) for t in self.Triggers]): continue

            for ch in self.Channel:
                if self.RawCutFlow: self.Histos['{}/cutflow'.format(ch)].Fill(1)
                else: self.Histos['{}/cutflow'.format(ch)].Fill(1, aux['wgt'])

            ## 2 leptonjets in channel definition ##
            leptonjets = [lj for lj in event.leptonjets]
            if len(leptonjets)<2: continue
            leptonjets.sort(key=lambda lj: lj.p4.pt(), reverse=True)
            LJ0 = leptonjets[0]
            LJ1 = leptonjets[1]
            if self.ChargedLJ:
                if not LJ0.passChargedSelection(event): continue
                if not LJ1.passChargedSelection(event): continue
            else:
                if not LJ0.passSelection(event): continue
                if not LJ1.passSelection(event): continue

            if LJ0.isMuonType() and LJ1.isMuonType():  aux['channel'] = '4mu'
            elif LJ0.isMuonType() and LJ1.isEgmType(): aux['channel'] = '2mu2e'
            elif LJ0.isEgmType() and LJ1.isMuonType(): aux['channel'] = '2mu2e'
            else: continue

            aux['lj0'] = LJ0
            aux['lj1'] = LJ1

            if self.Type == 'MC':
                aux['sf_electron']     = 1.
                aux['sf_electron_up']  = 1.
                aux['sf_electron_low'] = 1.

                aux['sf_photon']     = 1.
                aux['sf_photon_up']  = 1.
                aux['sf_photon_low'] = 1.

                aux['sf_pfmuon']     = 1.
                aux['sf_pfmuon_up']  = 1.
                aux['sf_pfmuon_low'] = 1.

                for lj in [LJ0, LJ1]:
                    ## muon scale factor
                    for i in lj.pfcand_pfmuonIdx:
                        _pfmu_p4 = event.muons[i].p4
                        pt, eta = _pfmu_p4.pt(), _pfmu_p4.eta()
                        if pt>=20:
                            xbin = self.LookupMuonSF.xaxis.FindBin(pt)
                            xbin = min(max(xbin, 1), self.LookupMuonSF.nbins(0))
                            ybin = self.LookupMuonSF.yaxis.FindBin(abs(eta))
                            sf = self.LookupMuonSF.GetBinContent(xbin, ybin)
                            err_up = self.LookupMuonSF.GetBinErrorUp(xbin, ybin)
                            err_lo = self.LookupMuonSF.GetBinErrorLow(xbin, ybin)
                        else:
                            for i in range(self.LookupMuonSFLowpT.num_points):
                                x = self.LookupMuonSFLowpT.x(i)
                                xh = x + self.LookupMuonSFLowpT.xerrh(i)
                                xl = x - self.LookupMuonSFLowpT.xerrl(i)
                                if xl<=eta and eta<=xh:
                                    sf = self.LookupMuonSFLowpT.y(i)
                                    err_up = self.LookupMuonSFLowpT.yerrh(i)
                                    err_lo = self.LookupMuonSFLowpT.yerrl(i)
                                    break
                        aux['wgt'] *= sf

                        aux['sf_pfmuon']     *= sf
                        aux['sf_pfmuon_up']  *= sf+err_up
                        aux['sf_pfmuon_low'] *= sf-err_lo

                    ## NOTE DSA scale factor, nothing for now
                    for i in lj.pfcand_dsamuonIdx:
                        sf = 1.
                        aux['wgt'] *= sf

                    ## electron scale factor
                    for i in lj.pfcand_electronIdx:
                        _electron = event.electrons[i]
                        xbin = self.LookupElectronSF.xaxis.FindBin(_electron.scEta)
                        ybin = self.LookupElectronSF.xaxis.FindBin(_electron.p4.pt())
                        ybin = min(max(ybin, 1), self.LookupElectronSF.nbins(1))
                        sf = self.LookupElectronSF.GetBinContent(xbin, ybin)
                        aux['wgt'] *= sf

                        aux['sf_electron']    *= sf
                        aux['sf_electron_up'] *= sf+self.LookupElectronSF.GetBinErrorUp (xbin, ybin)
                        aux['sf_electron_low']*= sf-self.LookupElectronSF.GetBinErrorLow(xbin, ybin)

                    ## photon scale factor
                    for i in lj.pfcand_photonIdx:
                        _photon = event.photons[i]
                        xbin = self.LookupPhotonSF.xaxis.FindBin(_photon.scEta)
                        ybin = self.LookupPhotonSF.xaxis.FindBin(_photon.p4.pt())
                        ybin = min(max(ybin, 1), self.LookupPhotonSF.nbins(1))
                        sf = self.LookupPhotonSF.GetBinContent(xbin, ybin)
                        aux['wgt'] *= sf

                        aux['sf_photon']    *= sf
                        aux['sf_photon_up'] *= sf+self.LookupPhotonSF.GetBinErrorUp (xbin, ybin)
                        aux['sf_photon_low']*= sf-self.LookupPhotonSF.GetBinErrorLow(xbin, ybin)

                aux['wgt_electron_up']  = aux['wgt']/aux['sf_electron'] * aux['sf_electron_up']
                aux['wgt_electron_low'] = aux['wgt']/aux['sf_electron'] * aux['sf_electron_low']
                aux['wgt_photon_up']    = aux['wgt']/aux['sf_photon']   * aux['sf_photon_up']
                aux['wgt_photon_low']   = aux['wgt']/aux['sf_photon']   * aux['sf_photon_low']
                aux['wgt_pfmuon_up']    = aux['wgt']/aux['sf_pfmuon']   * aux['sf_pfmuon_up']
                aux['wgt_pfmuon_low']   = aux['wgt']/aux['sf_pfmuon']   * aux['sf_pfmuon_low']


                    # for t, pt, eta in zip(list(lj.pfcand_type), list(lj.pfcand_pt), list(lj.pfcand_eta)):
                    #     ## muon scale factor, DSA same as muon for now
                    #     if t==3 or t==8:
                    #         xbin = self.LookupMuonSF.xaxis.FindBin(pt)
                    #         xbin = min(max(xbin, 1), self.LookupMuonSF.nbins(0))
                    #         ybin = self.LookupMuonSF.yaxis.FindBin(abs(eta))
                    #         sf = self.LookupMuonSF.GetBinContent(xbin, ybin)
                    #         aux['wgt'] *= sf
                    #     ## electron scale factor, using eta instead of SC eta for now
                    #     if t==2:
                    #         xbin = self.LookupElectronSF.xaxis.FindBin(eta)
                    #         ybin = self.LookupElectronSF.xaxis.FindBin(pt)
                    #         ybin = min(max(ybin, 1), self.LookupElectronSF.nbins(1))
                    #         sf = self.LookupElectronSF.GetBinContent(xbin, ybin)
                    #         aux['wgt'] *= sf
                    #     ## photon scale factor, using eta instead of SC eta for now
                    #     if t==4:
                    #         xbin = self.LookupPhotonSF.xaxis.FindBin(eta)
                    #         ybin = self.LookupPhotonSF.xaxis.FindBin(pt)
                    #         ybin = min(max(ybin, 1), self.LookupPhotonSF.nbins(1))
                    #         sf = self.LookupPhotonSF.GetBinContent(xbin, ybin)
                    #         aux['wgt'] *= sf


            for ch in self.Channel:
                if self.RawCutFlow: self.Histos['{}/cutflow'.format(ch)].Fill(2)
                else: self.Histos['{}/cutflow'.format(ch)].Fill(2, aux['wgt'])

            ## event-level mask ##
            if not event.metfilters.PrimaryVertexFilter: continue
            for ch in self.Channel:
                if self.RawCutFlow: self.Histos['{}/cutflow'.format(ch)].Fill(3)
                else: self.Histos['{}/cutflow'.format(ch)].Fill(3, aux['wgt'])

            nppCOSMIC, cosmicShowerTagged = globalCosmicShower(event.cosmicmuons, aux['channel'])
            if cosmicShowerTagged: continue

            for ch in self.Channel:
                if self.RawCutFlow: self.Histos['{}/cutflow'.format(ch)].Fill(4)
                else: self.Histos['{}/cutflow'.format(ch)].Fill(4, aux['wgt'])


            self.processEvent(event, aux)


    def processEvent(self, event, aux):
        """To be override by daughter class"""
        pass

    def postProcess(self):
        if self.KeepCutFlow:
            labels = ['total', 'trigger_pass', 'leptonjet_ge2', 'pv_good', 'cosmicveto_pass']
            for ch in self.Channel:
                xaxis = self.Histos['{}/cutflow'.format(ch)].axis(0)
                for i, s in enumerate(labels, start=1):
                    xaxis.SetBinLabel(i, s)
                    # binNum., labAngel, labSize, labAlign, labColor, labFont, labText
                    xaxis.ChangeLabel(i, 315, -1, 11, -1, -1, s)
        else:
            for ch in self.Channel:
                self.Histos.pop('{}/cutflow'.format(ch))

    @property
    def histos(self):
        return self.Histos

    @property
    def channel(self):
        return self.Channel



class MuonTypeLJEvents(object):
    def __init__(self, files=None, type='MC', maxevents=-1):
        if type.upper() not in ['MC', 'DATA']: raise ValueError("Argument `type` need to be MC/DATA")
        self.Type = type
        self.MaxEvents = maxevents

        if not files: raise ValueError("Argument `files` need to be non-empty")
        if isinstance(files, str): files = [files,]
        self.Chain = TreeChain('ffNtuplizer/ffNtuple', files)

        ## register collections ###
        self.Chain.define_collection('pvs', prefix='pv_', size='pv_n')
        self.Chain.define_collection('muons', prefix='muon_', size='muon_n')
        self.Chain.define_collection('dsamuons', prefix='dsamuon_', size='dsamuon_n')
        self.Chain.define_collection('ak4jets', prefix='akjet_ak4PFJetsCHS_', size='akjet_ak4PFJetsCHS_n')
        self.Chain.define_collection('leptonjets', prefix='pfjet_', size='pfjet_n', mix=LeptonJetMix)

        self.Chain.define_collection('trigobjs', prefix='trigobj_', size='trigobj_n')

        self.Chain.define_object('hlt', prefix='HLT_')
        self.Chain.define_object('metfilters', prefix='metfilters_')
        self.Chain.define_object('cosmicveto', prefix='cosmicveto_')

        self.Histos = {}

        self.LookupWeight = root_open(os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/data/puWeights_10x_56ifb.root')).Get('puWeights')
        self.Scale = 1.

    def bookHisto(self, name, hist):
        self.Histos[name] = hist

    def setScale(self, scale):
        self.Scale = scale

    def process(self):

        for i, event in enumerate(self.Chain):

            if self.MaxEvents>0 and i>self.MaxEvents: break

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
            leptonjets.sort(key=lambda lj:lj.p4.pt(), reverse=True)
            leptonjets = leptonjets[:2]
            muontypeljs = [lj for lj in leptonjets if lj.isMuonType()]
            egmtypeljs = [lj for lj in leptonjets if lj.isEgmType()]
            # if not muontypeljs: continue

            aux['muontype'] = muontypeljs
            aux['egmtype'] = egmtypeljs
            aux['leptonjets'] = leptonjets

            looseMuonIdx, mediumMuonIdx = [], []
            for i, mu in enumerate(event.muons):
                if mu.p4.pt()<5: continue
                if abs(mu.p4.eta())>2.4: continue
                if (mu.selectors&(1<<0))!=(1<<0): continue # ID-loose
                if (mu.selectors&(1<<7))!=(1<<7): continue # Iso-loose
                looseMuonIdx.append(i)
                if (mu.selectors&(1<<1))!=(1<<1): continue # ID-medium
                mediumMuonIdx.append(i)

            if not mediumMuonIdx: continue
            muonpairs = []
            for m in mediumMuonIdx:
                for l in looseMuonIdx:
                    if m == l: continue
                    if (l, m) in muonpairs: continue
                    muonpairs.append( (m,l) )
            if not muonpairs: continue

            aux['muonpairs'] = muonpairs

            self.processEvent(event, aux)

    def processEvent(self, event, aux):
        """To be override by daughter class"""
        pass

    @property
    def histos(self):
        return self.Histos


class ProxyEvents(Events):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['4mu', '2mu2e'], **kwargs):
        super(ProxyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)
        self.Chain.define_collection('proxymuons', prefix='proxymuon_', size='proxymuon_n', mix=ProxyMuonMix)

    def process(self):

        for i, event in enumerate(self.Chain):
            if self.MaxEvents>0 and i>self.MaxEvents: break

            ## event weight ##
            aux = {}
            aux['wgt'] = self.Scale
            if self.Type == 'MC':
                aux['wgt'] *= event.weight # gen weight
                aux['wgt'] *= self.LookupWeight.GetBinContent(self.LookupWeight.GetXaxis().FindBin(event.trueInteractionNum)) ## pileup correction

            for ch in self.Channel: self.Histos['{}/cutflow'.format(ch)].Fill(0, aux['wgt'])

            ## trigger ##
            if not any([getattr(event.hlt, t) for t in self.Triggers]): continue

            for ch in self.Channel: self.Histos['{}/cutflow'.format(ch)].Fill(1, aux['wgt'])


            if not event.proxymuons: continue
            aux['proxy'] = sorted(event.proxymuons, key=lambda mu: mu.p4.pt(), reverse=True)[0]
            if not aux['proxy'].passSelection(): continue

            leptonjets = [lj for lj in event.leptonjets]
            if not leptonjets: continue
            if len([lj for lj in event.leptonjets if lj.isMuonType()])>1: continue

            leptonjets.sort(key=lambda lj: lj.p4.pt(), reverse=True)
            aux['lj'] = leptonjets[0]
            if not aux['lj'].passSelection(event): continue

            if aux['lj'].isMuonType(): aux['channel'] = '4mu'
            elif aux['lj'].isEgmType(): aux['channel'] = '2mu2e'
            else: continue

            if self.Type == 'MC':
                aux['sf_electron'] = 1.
                aux['sf_photon']   = 1.
                aux['sf_pfmuon']   = 1.

                _pfmuons_p4 = []
                for i in aux['lj'].pfcand_pfmuonIdx:
                    _pfmuons_p4.append( event.muons[i].p4 )
                if aux['proxy'].isPFMuon():
                    _pfmuons_p4.append(aux['proxy'].p4)

                for _pfmu_p4 in _pfmuons_p4:
                    pt, eta = _pfmu_p4.pt(), _pfmu_p4.eta()
                    if pt>=20:
                        xbin = self.LookupMuonSF.xaxis.FindBin(pt)
                        xbin = min(max(xbin, 1), self.LookupMuonSF.nbins(0))
                        ybin = self.LookupMuonSF.yaxis.FindBin(abs(eta))
                        sf = self.LookupMuonSF.GetBinContent(xbin, ybin)
                    else:
                        for i in range(self.LookupMuonSFLowpT.num_points):
                            x = self.LookupMuonSFLowpT.x(i)
                            xh = x + self.LookupMuonSFLowpT.xerrh(i)
                            xl = x - self.LookupMuonSFLowpT.xerrl(i)
                            if xl<=eta and eta<=xh:
                                sf = self.LookupMuonSFLowpT.y(i)
                                break
                    aux['wgt'] *= sf
                    aux['sf_pfmuon']     *= sf

                ## NOTE DSA scale factor, nothing for now.
                # remember to consider proxy muon also.
                for i in aux['lj'].pfcand_dsamuonIdx:
                    sf = 1.
                    aux['wgt'] *= sf

                ## electron scale factor
                for i in aux['lj'].pfcand_electronIdx:
                    _electron = event.electrons[i]
                    xbin = self.LookupElectronSF.xaxis.FindBin(_electron.scEta)
                    ybin = self.LookupElectronSF.xaxis.FindBin(_electron.p4.pt())
                    ybin = min(max(ybin, 1), self.LookupElectronSF.nbins(1))
                    sf = self.LookupElectronSF.GetBinContent(xbin, ybin)

                    aux['wgt'] *= sf
                    aux['sf_electron']    *= sf

                ## photon scale factor
                for i in lj.pfcand_photonIdx:
                    _photon = event.photons[i]
                    xbin = self.LookupPhotonSF.xaxis.FindBin(_photon.scEta)
                    ybin = self.LookupPhotonSF.xaxis.FindBin(_photon.p4.pt())
                    ybin = min(max(ybin, 1), self.LookupPhotonSF.nbins(1))
                    sf = self.LookupPhotonSF.GetBinContent(xbin, ybin)

                    aux['wgt'] *= sf
                    aux['sf_photon']    *= sf


            for ch in self.Channel: self.Histos['{}/cutflow'.format(ch)].Fill(2, aux['wgt'])

            ## event-level mask ##
            if not event.metfilters.PrimaryVertexFilter: continue

            ## event-level mask ##
            nppCOSMIC, cosmicShowerTagged = globalCosmicShower(event.cosmicmuons, aux['channel'])
            if cosmicShowerTagged: continue
            for ch in self.Channel: self.Histos['{}/cutflow'.format(ch)].Fill(3, aux['wgt'])

            if not event.cosmicveto.result: continue
            for ch in self.Channel: self.Histos['{}/cutflow'.format(ch)].Fill(4, aux['wgt'])


            self.processEvent(event, aux)

    def postProcess(self):
        if self.KeepCutFlow:
            labels = ['total', 'trigger_pass', 'leptonjetProxyMuon', 'pv_good', 'cosmicveto_pass']
            for ch in self.Channel:
                xaxis = self.Histos['{}/cutflow'.format(ch)].axis(0)
                for i, s in enumerate(labels, start=1):
                    xaxis.SetBinLabel(i, s)
                    # binNum., labAngel, labSize, labAlign, labColor, labFont, labText
                    xaxis.ChangeLabel(i, 315, -1, 11, -1, -1, s)
        else:
            for ch in self.Channel:
                self.Histos.pop('{}/cutflow'.format(ch))



class CosmicEvents(Events):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['4mu', '2mu2e'], **kwargs):
        super(CosmicEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)

    def process(self):

        for i, event in enumerate(self.Chain):
            if self.MaxEvents>0 and i>self.MaxEvents: break

            ## trigger ##
            if not any([getattr(event.hlt, t) for t in self.Triggers]): continue

            ## event-level mask ##
            # if not event.cosmicveto.result: continue
            if not event.metfilters.PrimaryVertexFilter: continue

            aux = {}
            ## event weight ##
            aux['wgt'] = self.Scale
            if self.Type == 'MC':
                aux['wgt'] *= event.weight # gen weight
                aux['wgt'] *= self.LookupWeight.GetBinContent(
                    self.LookupWeight.GetXaxis().FindBin(event.trueInteractionNum)) ## pileup correction


            leptonjets = [lj for lj in event.leptonjets]
            if len(leptonjets)<2: continue
            leptonjets.sort(key=lambda lj: lj.p4.pt(), reverse=True)
            LJ0 = leptonjets[0]
            LJ1 = leptonjets[1]
            if not LJ0.passSelectionIncCosmic(event): continue
            if not LJ1.passSelectionIncCosmic(event): continue

            if LJ0.isMuonType() and LJ1.isMuonType(): aux['channel'] = '4mu'
            elif LJ0.isMuonType() and LJ1.isEgmType(): aux['channel'] = '2mu2e'
            elif LJ0.isEgmType() and LJ1.isMuonType(): aux['channel'] = '2mu2e'
            else: continue

            nppCOSMIC, cosmicShowerTagged = globalCosmicShower(event.cosmicmuons, aux['channel'])

            aux['nparallel'] = nppCOSMIC
            aux['hasCosmicShower'] = cosmicShowerTagged


            aux['lj0'] = LJ0
            aux['lj1'] = LJ1


            self.processEvent(event, aux)


    def postProcess(self):
        if self.KeepCutFlow:
            labels = ['total', 'trigger_pass', 'leptonjetProxyMuon', 'pv_good', 'cosmicveto_pass']
            for ch in self.Channel:
                xaxis = self.Histos['{}/cutflow'.format(ch)].axis(0)
                for i, s in enumerate(labels, start=1):
                    xaxis.SetBinLabel(i, s)
                    # binNum., labAngel, labSize, labAlign, labColor, labFont, labText
                    xaxis.ChangeLabel(i, 315, -1, 11, -1, -1, s)
        else:
            for ch in self.Channel:
                self.Histos.pop('{}/cutflow'.format(ch))




class SignalEvents(Events):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['4mu', '2mu2e'], tqdm=False, **kwargs):
        super(SignalEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)
        self.Tqdm=tqdm
        self.Chain.define_collection('gens', prefix='gen_', size='gen_n')
        self.Chain.define_collection('trigobjs', prefix='trigobj_', size='trigobj_n')
        # self.Chain.define_object('pfmet', prefix='pfMet')

    def process(self):

        if self.Tqdm:
            if self.MaxEvents>0:
                pbar = tqdm(total=self.MaxEvents)
            else:
                pbar = tqdm(total=self.Chain.GetEntries())



        for i, event in enumerate(self.Chain):
            if self.MaxEvents>0 and i>self.MaxEvents: break

            aux = {}
            aux['wgt'] = self.Scale
            if self.Type == 'MC':
                aux['wgt'] *= event.weight # gen weight
                # aux['wgt'] *= self.LookupWeight.GetBinContent(self.LookupWeight.GetXaxis().FindBin(event.trueInteractionNum)) ## pileup correction

            aux['dp'] = [p for p in event.gens if p.pid==32]
            aux['channel'] = '4mu'
            if 11 in [abs(p.daupid) for p in aux['dp']]:
                aux['channel'] = '2mu2e'
            self.processEvent(event, aux)

            if self.Tqdm: pbar.update(1)



        if self.Tqdm:
            pbar.close()
