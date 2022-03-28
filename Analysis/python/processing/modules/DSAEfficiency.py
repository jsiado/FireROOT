#!/usr/bin/env python

from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *



class MyEvents(SignalEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']

        dp_toMu = [p for p in aux['dp'] if p.daupid==13]
        dp_toEl = [p for p in aux['dp'] if p.daupid==11]

        DR_THRESHOLD = 0.4 # maximum dR limit between (gen darkphoton, lepton-jets) matching

        # dp-> mu, mu
        for dp in dp_toMu:
            if dp.p4.pt()<30 or abs(dp.p4.eta())>2.4: continue

            lxy = (dp.dauvtx - dp.vtx).Rho()
            lz  = (dp.dauvtx - dp.vtx).Z()
            # if abs(lz)>800: continue
            self.Histos['%s/lxyDpToMu__total' % chan].Fill(lxy)
            self.Histos['%s/lepDrDpToMu__total' % chan].Fill(dp.daudr)

            mindr, matched = 999., None
            for lj in event.leptonjets:
                if not lj.isMuonType(): continue
                if not lj.passSelection(event): continue
                distance = DeltaR(dp.p4, lj.p4)
                if distance > DR_THRESHOLD: continue
                if distance<mindr:
                    mindr = distance
                    matched = lj

            if matched:
                self.Histos['%s/lxyDpToMu__match' % chan].Fill(lxy)
                self.Histos['%s/lepDrDpToMu__match' % chan].Fill(dp.daudr)
            else:
                # matching with PFAK4Jets
                for j in event.ak4jets:
                    if j.p4.pt()<30 or abs(j.p4.eta())>2.4: continue
                    distance = DeltaR(dp.p4, j.p4)
                    if distance > DR_THRESHOLD: continue
                    if distance<mindr:
                        mindr = distance
                        matched = j
                if matched is not None:
                    self.Histos['%s/lxyDpToMu__matchAk4' % chan].Fill(lxy)


        # dp-> el, el
        for dp in dp_toEl:
            if dp.p4.pt()<30 or abs(dp.p4.eta())>2.4: continue

            lxy = (dp.dauvtx - dp.vtx).Rho()
            lz  = (dp.dauvtx - dp.vtx).Z()
            # if abs(lz)>550: continue
            self.Histos['%s/lxyDpToEl__total' % chan].Fill(lxy)
            self.Histos['%s/lepDrDpToEl__total' % chan].Fill(dp.daudr)

            mindr, matched = 999., None
            for lj in event.leptonjets:
                if not lj.isEgmType(): continue
                if not lj.passSelection(event): continue
                distance = DeltaR(dp.p4, lj.p4)
                if distance > DR_THRESHOLD: continue
                if distance<mindr:
                    mindr = distance
                    matched = lj

            if matched is not None:
                self.Histos['%s/lxyDpToEl__match' % chan].Fill(lxy)
                self.Histos['%s/lepDrDpToEl__match' % chan].Fill(dp.daudr)
            else:
                # matching with PFElectrons
                _mindr, _matched = 999., None
                for e in event.electrons:
                    if e.p4.pt()<10 or abs(e.p4.eta())>2.4: continue
                    distance = DeltaR(dp.p4, e.p4)
                    if distance > DR_THRESHOLD: continue
                    else:
                        _mindr = distance
                        _matched = e
                if _matched:
                    self.Histos['%s/lxyDpToEl__matchEle' % chan].Fill(lxy)

                # matching with PFPhotons
                _mindr, _matched = 999., None
                for g in event.photons:
                    if g.p4.pt()<10 or abs(g.p4.eta())>2.4: continue
                    distance = DeltaR(dp.p4, g.p4)
                    if distance > DR_THRESHOLD: continue
                    else:
                        _mindr = distance
                        _matched = g
                if _matched:
                    self.Histos['%s/lxyDpToEl__matchPho' % chan].Fill(lxy)

                # matching with PFAK4Jets
                for j in event.ak4jets:
                    if j.p4.pt()<30 or abs(j.p4.eta())>2.4: continue
                    distance = DeltaR(dp.p4, j.p4)
                    if distance > DR_THRESHOLD: continue
                    if distance<mindr:
                        mindr = distance
                        matched = j
                if matched is not None:
                    self.Histos['%s/lxyDpToEl__matchAk4' % chan].Fill(lxy)

                    ## look deeper of those AK4PFJets
                    pt_resolution = (matched.p4.pt()-dp.p4.pt())/dp.p4.pt() # (reco-gen)/gen
                    rawpt_resolution = (matched.rawP4.pt()-dp.p4.pt())/dp.p4.pt() # (reco-gen)/gen
                    neu_had_fraction = matched.hadronEnergyFraction - matched.chaHadEnergyFraction
                    neu_em_fraction = matched.emEnergyFraction - matched.chaEmEnergyFraction
                    jetid = bool(matched.jetid)
                    ## First, lxy>140, purely AK4PFJets
                    if 270 > lxy > 140:
                        self.Histos['%s/pTResolution__matchAK4__outsideECAL' % chan].Fill(pt_resolution)
                        self.Histos['%s/rawPTResolution__matchAK4__outsideECAL' % chan].Fill(rawpt_resolution)
                        self.Histos['%s/neuHadFrac__matchAK4__outsideECAL' % chan].Fill(neu_had_fraction)
                        self.Histos['%s/jetid__matchAK4__outsideECAL' % chan].Fill(jetid)
                        self.Histos['%s/emfrac__matchAK4__outsideECAL' % chan].Fill(matched.emEnergyFraction)
                        self.Histos['%s/neuEmfrac__matchAK4__outsideECAL' % chan].Fill(neu_em_fraction)
                    elif lxy<140:
                        self.Histos['%s/pTResolution__matchAK4__insideECAL' % chan].Fill(pt_resolution)
                        self.Histos['%s/rawPTResolution__matchAK4__insideECAL' % chan].Fill(rawpt_resolution)
                        self.Histos['%s/neuHadFrac__matchAK4__insideECAL' % chan].Fill(neu_had_fraction)
                        self.Histos['%s/jetid__matchAK4__insideECAL' % chan].Fill(jetid)
                        self.Histos['%s/emfrac__matchAK4__insideECAL' % chan].Fill(matched.emEnergyFraction)
                        self.Histos['%s/neuEmfrac__matchAK4__insideECAL' % chan].Fill(neu_em_fraction)





histCollection = [
    {
        'name'   : 'lxyDpToMu__total',
        'binning': (100, 0, 500),
        'title'  : 'Z_{d} lxy;lxy [cm];counts/5cm',
    },
    {
        'name'   : 'lxyDpToMu__match',
        'binning': (100, 0, 500),
        'title'  : 'Z_{d} lxy;lxy [cm];counts/5cm',
    },
    {
        'name'   : 'lxyDpToMu__matchAk4',
        'binning': (100, 0, 500),
        'title'  : 'Z_{d} lxy;lxy [cm];counts/5cm',
    },
    {
        'name'   : 'lxyDpToEl__total',
        'binning': (100, 0, 250),
        'title'  : 'Z_{d} lxy;lxy [cm];counts/2.5cm',
    },
    {
        'name'   : 'lxyDpToEl__match',
        'binning': (100, 0, 250),
        'title'  : 'Z_{d} lxy;lxy [cm];counts/2.5cm',
    },
    {
        'name'   : 'lxyDpToEl__matchAk4',
        'binning': (100, 0, 250),
        'title'  : 'Z_{d} lxy;lxy [cm];counts/2.5cm',
    },
    ### PF AK4 JETS ###
    {
        'name'   : 'pTResolution__matchAK4__outsideECAL',
        'binning': (100, -1, 1),
        'title'  : 'p_{T} resolution of matched PFAK4Jets (270>lxy>140cm);(p_{T}^{reco}-p_{T}^{gen})/p_{T}^{gen};resolution',
    },
    {
        'name'   : 'rawPTResolution__matchAK4__outsideECAL',
        'binning': (100, -1, 1),
        'title'  : 'raw p_{T} resolution of matched PFAK4Jets (270>lxy>140cm);(p_{T}^{reco}-p_{T}^{gen})/p_{T}^{gen};resolution',
    },
    {
        'name'   : 'neuHadFrac__matchAK4__outsideECAL',
        'binning': (50, 0, 1),
        'title'  : 'Neutral hadronic energy fraction of matched PFAK4Jets (270>lxy>140cm);neutral hadronic energy fraction;counts',
    },
    {
        'name'   : 'emfrac__matchAK4__outsideECAL',
        'binning': (50, 0, 1),
        'title'  : 'EM energy fraction of matched PFAK4Jets (270>lxy>140cm);em energy fraction;counts',
    },
    {
        'name'   : 'neuEmfrac__matchAK4__outsideECAL',
        'binning': (50, 0, 1),
        'title'  : 'Neutral EM energy fraction of matched PFAK4Jets (270>lxy>140cm);neutral em energy fraction;counts',
    },
    {
        'name'   : 'jetid__matchAK4__outsideECAL',
        'binning': (2, 0, 2),
        'title'  : 'jet id of matched PFAK4Jets (270>lxy>140cm);pass jet id;counts',
    },

    {
        'name'   : 'pTResolution__matchAK4__insideECAL',
        'binning': (100, -1, 1),
        'title'  : 'p_{T} resolution of matched PFAK4Jets (lxy<140cm);(p_{T}^{reco}-p_{T}^{gen})/p_{T}^{gen};resolution',
    },
    {
        'name'   : 'rawPTResolution__matchAK4__insideECAL',
        'binning': (100, -1, 1),
        'title'  : 'raw p_{T} resolution of matched PFAK4Jets (lxy<140cm);(p_{T}^{reco}-p_{T}^{gen})/p_{T}^{gen};resolution',
    },
    {
        'name'   : 'neuHadFrac__matchAK4__insideECAL',
        'binning': (50, 0, 1),
        'title'  : 'Neutral hadronic energy fraction of matched PFAK4Jets (lxy<140cm);neutral hadronic energy fraction;counts',
    },
    {
        'name'   : 'emfrac__matchAK4__insideECAL',
        'binning': (50, 0, 1),
        'title'  : 'EM energy fraction of matched PFAK4Jets (lxy<140cm);em energy fraction;counts',
    },
    {
        'name'   : 'neuEmfrac__matchAK4__insideECAL',
        'binning': (50, 0, 1),
        'title'  : 'Neutral EM energy fraction of matched PFAK4Jets (lxy<140cm);neutral em energy fraction;counts',
    },
    {
        'name'   : 'jetid__matchAK4__insideECAL',
        'binning': (2, 0, 2),
        'title'  : 'jet id of matched PFAK4Jets (lxy<140cm);pass jet id;counts',
    },

    ## matching with PFElectrons
    {
        'name'   : 'lxyDpToEl__matchEle',
        'binning': (100, 0, 250),
        'title'  : 'Z_{d} lxy;lxy [cm];counts/2.5cm',
    },
    {
        'name'   : 'lxyDpToEl__matchPho',
        'binning': (100, 0, 250),
        'title'  : 'Z_{d} lxy;lxy [cm];counts/2.5cm',
    },


    ## opening angle
    {
        'name'   : 'lepDrDpToMu__total',
        'binning': (50, 0, 0.5),
        'title'  : 'Z_{d} #DeltaR(#mu^{+}#mu^{-});#DeltaR(#mu^{+}#mu^{-});counts/0.01',
    },
    {
        'name'   : 'lepDrDpToMu__match',
        'binning': (50, 0, 0.5),
        'title'  : 'Z_{d} #DeltaR(#mu^{+}#mu^{-});#DeltaR(#mu^{+}#mu^{-});counts/0.01',
    },
    {
        'name'   : 'lepDrDpToEl__total',
        'binning': (50, 0, 0.5),
        'title'  : 'Z_{d} #DeltaR(e^{+}e^{-});#DeltaR(e^{+}e^{-});counts/0.01',
    },
    {
        'name'   : 'lepDrDpToEl__match',
        'binning': (50, 0, 0.5),
        'title'  : 'Z_{d} #DeltaR(e^{+}e^{-});#DeltaR(e^{+}e^{-});counts/0.01',
    },
]
