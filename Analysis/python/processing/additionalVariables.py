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
        if any(map(lambda lj: lj.isElectronType() and lj.nPFElectron()%2!=0, [LJ0, LJ1])): return

        passCosmic = all(map(lambda lj: lj.passCosmicVeto(event), [LJ0, LJ1]))
        if not passCosmic: return
        passLjMass = all(map(lambda lj: lj.isEgmType() or lj.isMuonType() and lj.p4.M()<8, [LJ0, LJ1]))
        if not passLjMass: return

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
        for lj in [LJ0, LJ1]:
            if not lj.isEgmType(): continue
            if lj.nPFElectron()%2==0:
                self.Histos["{}/eleven_inc".format(chan)].Fill(0, aux['wgt'])
            else:
                self.Histos["{}/eleven_inc".format(chan)].Fill(1, aux['wgt'])
        self.Histos['{}/etasum'.format(chan)].Fill(abs(LJ0.p4.eta()+LJ1.p4.eta()), aux['wgt'])
        if njet<2:
            self.Histos['{}/etasum_lowjet'.format(chan)].Fill(abs(LJ0.p4.eta()+LJ1.p4.eta()), aux['wgt'])

        if not (chan=='2mu2e' and invm<120):
            self.Histos['{}/dphi_highm'.format(chan)].Fill(dphi, aux['wgt'])
            self.Histos['{}/etasum_highm'.format(chan)].Fill(abs(LJ0.p4.eta()+LJ1.p4.eta()), aux['wgt'])
            if njet<2:
                self.Histos['{}/etasum_highm_lowjet'.format(chan)].Fill(abs(LJ0.p4.eta()+LJ1.p4.eta()), aux['wgt'])

            endcap_mulj = 0
            for lj in [LJ0, LJ1]:
                if lj.isMuonType() and abs(lj.p4.eta())>0.9:
                    endcap_mulj += 1
                elif lj.isEgmType():
                    if lj.nPFElectron()%2==0:
                        self.Histos["{}/eleven_highm".format(chan)].Fill(0, aux['wgt'])
                    else:
                        self.Histos["{}/eleven_highm".format(chan)].Fill(1, aux['wgt'])
            self.Histos['{}/endcapmulj'.format(chan)].Fill(endcap_mulj, aux['wgt'])


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

        for ch in self.Channel:
            xax = self.Histos['{}/dphi_inc'.format(ch)].axis(0)
            xax.SetNdivisions(-310)
            xax.ChangeLabel(2,-1,-1,-1,-1,-1,"#frac{#pi}{10}")
            xax.ChangeLabel(3,-1,-1,-1,-1,-1,"#frac{#pi}{5}")
            xax.ChangeLabel(4,-1,-1,-1,-1,-1,"#frac{3#pi}{10}")
            xax.ChangeLabel(5,-1,-1,-1,-1,-1,"#frac{2#pi}{5}")
            xax.ChangeLabel(6,-1,-1,-1,-1,-1,"#frac{#pi}{2}")
            xax.ChangeLabel(7,-1,-1,-1,-1,-1,"#frac{3#pi}{5}")
            xax.ChangeLabel(8,-1,-1,-1,-1,-1,"#frac{7#pi}{10}")
            xax.ChangeLabel(9,-1,-1,-1,-1,-1,"#frac{4#pi}{5}")
            xax.ChangeLabel(10,-1,-1,-1,-1,-1,"#frac{9#pi}{10}")
            xax.ChangeLabel(11,-1,-1,-1,-1,-1,"#pi")

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
    # {
    #     'name': 'invm_b100',
    #     'binning': (100, 0, 200),
    #     'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/2GeV'
    # },
    # {
    #     'name': 'invm_b150',
    #     'binning': (100, 0, 300),
    #     'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/3GeV'
    # },
    # {
    #     'name': 'invm_b200',
    #     'binning': (100, 0, 400),
    #     'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/4GeV'
    # },
    # {
    #     'name': 'invm_b500',
    #     'binning': (100, 0, 1000),
    #     'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/10GeV'
    # },
    # {
    #     'name': 'invm_b800',
    #     'binning': (100, 0, 1600),
    #     'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/16GeV'
    # },
    # {
    #     'name': 'invm_b1000',
    #     'binning': (100, 0, 2000),
    #     'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/20GeV'
    # },
    # {
    #     'name': 'invm_e100',
    #     'binning': (100, 0, 200),
    #     'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/2GeV'
    # },
    # {
    #     'name': 'invm_e150',
    #     'binning': (100, 0, 300),
    #     'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/3GeV'
    # },
    # {
    #     'name': 'invm_e200',
    #     'binning': (100, 0, 400),
    #     'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/4GeV'
    # },
    # {
    #     'name': 'invm_e500',
    #     'binning': (100, 0, 1000),
    #     'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/10GeV'
    # },
    # {
    #     'name': 'invm_e800',
    #     'binning': (100, 0, 1600),
    #     'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/16GeV'
    # },
    # {
    #     'name': 'invm_e1000',
    #     'binning': (100, 0, 2000),
    #     'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/20GeV'
    # },
    # {
    #     'name': 'bmf_b',
    #     'binning': (2, 0, 2),
    #     'title': 'BadMuonFilter;result;counts',
    # },
    # {
    #     'name': 'bmf_e',
    #     'binning': (2, 0, 2),
    #     'title': 'BadMuonFilter;result;counts',
    # },
    {
        'name': 'dphi_inc',
        'binning': (30, 0, M_PI),
        'title': 'lepton-jet pair |#Delta#phi|;|#Delta#phi|;counts',
    },
    {
        'name': 'dphi_highm',
        'binning': (30, 0, M_PI),
        'title': 'lepton-jet pair |#Delta#phi| (M>120);|#Delta#phi|;counts',
    },
    {
        'name': 'endcapmulj',
        'binning': (3, 0, 3),
        'title': '# muon-type lepton-jets |#eta|>0.9;N_{lepton-jets};counts',
    },
    {
        'name': 'eleven_inc',
        'binning': (2, 0, 2),
        'title': 'EGM-type lepton-jet nElectron%2=0;#el%2;counts',
    },
    {
        'name': 'eleven_highm',
        'binning': (2, 0, 2),
        'title': 'EGM-type lepton-jet nElectron%2=0 (M>120);#el%2;counts',
    },
    {
        'name': 'etasum',
        'binning': (48, 0, 4.8),
        'title': 'lepton-jet pair |#eta_{0}+#eta_{1}|;|#eta_{0}+#eta_{1}|;counts',
    },
    {
        'name': 'etasum_lowjet',
        'binning': (48, 0, 4.8),
        'title': 'lepton-jet pair |#eta_{0}+#eta_{1}| (Njet<2);|#eta_{0}+#eta_{1}|;counts',
    },
    {
        'name': 'etasum_highm',
        'binning': (48, 0, 4.8),
        'title': 'lepton-jet pair |#eta_{0}+#eta_{1}| (M>120);|#eta_{0}+#eta_{1}|;counts',
    },
    {
        'name': 'etasum_highm_lowjet',
        'binning': (48, 0, 4.8),
        'title': 'lepton-jet pair |#eta_{0}+#eta_{1}| (M>120,Njet<2);|#eta_{0}+#eta_{1}|;counts',
    },
]