#!/usr/bin/env python
import math

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

        dphi = abs(DeltaPhi(LJ0.p4, LJ1.p4))
        invm = (LJ0.p4+LJ1.p4).M()
        maxpfiso = max([LJ0.pfiso(), LJ1.pfiso()])
        njet = sum([1 for j in event.ak4jets if j.jetid and j.p4.pt()>50 and abs(j.p4.eta())<2.4])

        ## before displacement
        self.Histos['{}/invm_inc100'.format(chan)].Fill(invm, aux['wgt'])
        self.Histos['{}/invm_inc150'.format(chan)].Fill(invm, aux['wgt'])
        self.Histos['{}/invm_inc200'.format(chan)].Fill(invm, aux['wgt'])
        self.Histos['{}/invm_inc500'.format(chan)].Fill(invm, aux['wgt'])
        self.Histos['{}/invm_inc800'.format(chan)].Fill(invm, aux['wgt'])
        self.Histos['{}/invm_inc1000'.format(chan)].Fill(invm, aux['wgt'])
        self.Histos['{}/dphi_inc'.format(chan)].Fill(dphi, aux['wgt'])

        self.Histos['{}/etasum'.format(chan)].Fill(abs(LJ0.p4.eta()+LJ1.p4.eta()), aux['wgt'])
        self.Histos['{}/etadiff'.format(chan)].Fill(abs(LJ0.p4.eta()-LJ1.p4.eta()), aux['wgt'])
        self.Histos['{}/maxabseta'.format(chan)].Fill(max([abs(LJ0.p4.eta()),abs(LJ1.p4.eta())]), aux['wgt'])

        N_endcapMuLJ = 0
        N_endcapEgmLJ = 0
        N_endcapLJ = 0
        for lj in [LJ0, LJ1]:
            if lj.isEgmType() and abs(lj.p4.eta())>1.4:
                N_endcapEgmLJ+=1
                N_endcapLJ+=1
            if lj.isMuonType() and abs(lj.p4.eta())>0.9:
                N_endcapMuLJ+=1
                N_endcapLJ+=1

        self.Histos['{}/endcapmulj'.format(chan)].Fill(N_endcapMuLJ, aux['wgt'])
        self.Histos['{}/endcapegmlj'.format(chan)].Fill(N_endcapEgmLJ, aux['wgt'])
        self.Histos['{}/endcaplj'.format(chan)].Fill(N_endcapLJ, aux['wgt'])


        ## displacement cut
        # mind0sigs = []
        # for lj in [LJ0, LJ1]:
        #     if lj.isMuonType() and not math.isnan(lj.pfcand_tkD0SigMin):
        #         mind0sigs.append(lj.pfcand_tkD0SigMin)

        # metric_d0sig = {'2mu2e': 2, '4mu': 0.5}
        # metric_pfiso = {'2mu2e': 0.15, '4mu': 0.15}

        # if max(mind0sigs)<metric_d0sig[chan]: return

        # if chan=='2mu2e' and njet>0: return

        # mf = event.metfilters
        # ## before ABCD
        # self.Histos['{}/invm_b100'.format(chan)].Fill(invm, aux['wgt'])
        # self.Histos['{}/invm_b150'.format(chan)].Fill(invm, aux['wgt'])
        # self.Histos['{}/invm_b200'.format(chan)].Fill(invm, aux['wgt'])
        # self.Histos['{}/invm_b500'.format(chan)].Fill(invm, aux['wgt'])
        # self.Histos['{}/invm_b800'.format(chan)].Fill(invm, aux['wgt'])
        # self.Histos['{}/invm_b1000'.format(chan)].Fill(invm, aux['wgt'])
        # self.Histos['{}/bmf_b'.format(chan)].Fill(int(mf.BadMuonFilter), aux['wgt'])


        # if maxpfiso>metric_pfiso[chan] or dphi<math.pi/2: return
        # ## signal region
        # self.Histos['{}/invm_e100'.format(chan)].Fill(invm, aux['wgt'])
        # self.Histos['{}/invm_e150'.format(chan)].Fill(invm, aux['wgt'])
        # self.Histos['{}/invm_e200'.format(chan)].Fill(invm, aux['wgt'])
        # self.Histos['{}/invm_e500'.format(chan)].Fill(invm, aux['wgt'])
        # self.Histos['{}/invm_e800'.format(chan)].Fill(invm, aux['wgt'])
        # self.Histos['{}/invm_e1000'.format(chan)].Fill(invm, aux['wgt'])
        # self.Histos['{}/bmf_e'.format(chan)].Fill(int(mf.BadMuonFilter), aux['wgt'])

    def postProcess(self):
        super(MyEvents, self).postProcess()

        for k in self.Histos:
            if 'phi' not in k: continue
            xax = self.Histos[k].axis(0)
            decorate_axis_pi(xax)

histCollection = [
    {
        'name': 'invm_inc100',
        'binning': (100, 0, 200),
        'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/2GeV'
    },
    {
        'name': 'invm_inc150',
        'binning': (100, 0, 300),
        'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/3GeV'
    },
    {
        'name': 'invm_inc200',
        'binning': (100, 0, 400),
        'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/4GeV'
    },
    {
        'name': 'invm_inc500',
        'binning': (100, 0, 1000),
        'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/10GeV'
    },
    {
        'name': 'invm_inc800',
        'binning': (100, 0, 1600),
        'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/16GeV'
    },
    {
        'name': 'invm_inc1000',
        'binning': (100, 0, 2000),
        'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/20GeV'
    },
    {
        'name': 'dphi_inc',
        'binning': (30, 0, M_PI),
        'title': 'lepton-jet pair |#Delta#phi|;|#Delta#phi|;counts',
    },
    {
        'name': 'endcapmulj',
        'binning': (3, 0, 3),
        'title': '# endcap muon-type lepton-jets |#eta|>0.9;N;counts',
    },
    {
        'name': 'endcapegmlj',
        'binning': (2, 0, 2),
        'title': '# endcap egm-type lepton-jets |#eta|>1.479;N;counts',
    },
    {
        'name': 'endcaplj',
        'binning': (3, 0, 3),
        'title': '# endcap lepton-jets;N;counts',
    },
    {
        'name': 'etasum',
        'binning': (48, 0, 4.8),
        'title': 'lepton-jet pair |#eta_{0}+#eta_{1}|;|#eta_{0}+#eta_{1}|;counts',
    },
    {
        'name': 'etadiff',
        'binning': (48, 0, 4.8),
        'title': 'lepton-jet pair |#eta_{0}-#eta_{1}|;|#eta_{0}-#eta_{1}|;counts',
    },
    {
        'name': 'maxabseta',
        'binning': (24, 0, 2.4),
        'title': 'max lepton-jet |#eta|;|#eta|;counts',
    },
]