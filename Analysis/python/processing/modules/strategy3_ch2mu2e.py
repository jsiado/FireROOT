#!/usr/bin/env python
import math
import numpy as np
from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *


class MyEvents(Events):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e',], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']
        cutflowbin = 5
        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1

        LJ0, LJ1 = aux['lj0'], aux['lj1']
        passCosmic = all(map(lambda lj: lj.passCosmicVeto(event), [LJ0, LJ1]))
        if not passCosmic: return
        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1

        invm = (LJ0.p4+LJ1.p4).M()

        njet = sum([1 for j in event.ak4jets if j.jetid and j.p4.pt()>50 and abs(j.p4.eta())<2.4])
        if njet>0: return
        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1

        passLjMass = True
        for lj in [LJ0, LJ1]:
            if not lj.isMuonType(): continue
            ljmass = lj.p4.M()
            if ljmass>8: passLjMass=False
            if ljmass>2.9 and ljmass<3.3: passLjMass=False
        if not passLjMass: return
        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1

        nbtight = 0
        for s, j in zip(event.hftagscores, event.ak4jets):
            if not (j.jetid and j.p4.pt()>30 and abs(j.p4.eta())<2.5): continue
            if (s.DeepCSV_b&(1<<2))==(1<<2): nbtight += 1
        if nbtight>0: return
        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1

        self.Histos['{}/ljetasum'.format(chan)].Fill(abs(LJ0.p4.eta())+abs(LJ1.p4.eta()), aux['wgt'])
        self.Histos['{}/ljetaabssum'.format(chan)].Fill(abs(LJ0.p4.eta()+LJ1.p4.eta()), aux['wgt'])
        self.Histos['{}/maxljiso'.format(chan)].Fill(max([LJ0.pfiso(), LJ1.pfiso()]), aux['wgt'])
        tkmind0 = max([abs(lj.pfcand_tkD0Min*1e4) for lj in [LJ0, LJ1] if lj.isMuonType() ])
        self.Histos['{}/tkmind0'.format(chan)].Fill(tkmind0, aux['wgt'])

        scaledD0s = []
        for lj in [LJ0, LJ1]:
            if not lj.isMuonType(): continue
            ljmass = lj.p4.M()
            if ljmass==0: ljmass=0.25
            scaledD0 = math.log10(abs(lj.pfcand_tkD0Min * 1e4 * lj.p4.pt() /ljmass))
            scaledD0s.append(scaledD0)
            self.Histos['{}/scaledd0'.format(chan)].Fill(scaledD0, aux['wgt'])

        maxiso = max([LJ0.pfiso(), LJ1.pfiso()])

        if maxiso<0.25 and maxiso>0.16:
            self.Histos['{}/scaled0_tf'.format(chan)].Fill(max(scaledD0s), aux['wgt'])
            self.Histos['{}/tkmind0_tf'.format(chan)].Fill(tkmind0, aux['wgt'])
        elif maxiso<0.16 and maxiso>0.12:
            self.Histos['{}/scaled0_vr'.format(chan)].Fill(max(scaledD0s), aux['wgt'])
            self.Histos['{}/tkmind0_vr'.format(chan)].Fill(tkmind0, aux['wgt'])
        elif maxiso<0.12:
            self.Histos['{}/scaled0_cr'.format(chan)].Fill(max(scaledD0s), aux['wgt'])
            self.Histos['{}/tkmind0_cr'.format(chan)].Fill(tkmind0, aux['wgt'])

        dphi = abs(DeltaPhi(LJ0.p4, LJ1.p4))
        self.Histos['{}/dphi_e'.format(chan)].Fill(dphi, aux['wgt'])
        self.Histos['{}/invm_e'.format(chan)].Fill(invm, aux['wgt'])
        if tkmind0>25:
            self.Histos['{}/dphi_edisp'.format(chan)].Fill(dphi, aux['wgt'])

        if dphi<2.1: return
        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1

    def postProcess(self):
        super(MyEvents, self).postProcess()

        for ch in self.Channel:
            xax = self.Histos['{}/dphi_e'.format(ch)].axis(0)
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

            xaxis = self.Histos['{}/cutflow'.format(ch)].axis(0)
            labels = [ch, 'ljcosmicveto_pass', 'njet_eq0',
                    'muljmass_lt8', 'nbtight_eq0', 'dphi_gt2p1']

            for i, s in enumerate(labels, start=6):
                xaxis.SetBinLabel(i, s)
                # binNum., labAngel, labSize, labAlign, labColor, labFont, labText
                xaxis.ChangeLabel(i, 315, -1, 11, -1, -1, s)


histCollection = [
    {
        'name': 'dphi_e',
        'binning': (30, 0, M_PI),
        'title': 'lepton-jet pair |#Delta#phi|;|#Delta#phi|;counts',
    },
    {
        'name': 'dphi_edisp',
        'binning': (30, 0, M_PI),
        'title': 'lepton-jet pair |#Delta#phi|;|#Delta#phi|;counts',
    },
    {
        'name': 'invm_e',
        'binning': (100, 0, 1600),
        'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/16GeV'
    },
    {
        'name': 'ljetasum',
        'binning': (48, 0, 4.8),
        'title': 'lepton-jet |#eta_{0}|+|#eta_{1}|;|#eta_{0}|+|#eta_{1}|;counts',
    },
    {
        'name': 'ljetaabssum',
        'binning': (48, 0, 4.8),
        'title': 'lepton-jet |#eta_{0}+#eta_{1}|;|#eta_{0}+#eta_{1}|;counts',
    },
    {
        'name': 'maxljiso',
        'binning': (50, 0, 0.25),
        'title': 'max lepton-jet iso;iso;counts',
    },
    {
        'name': 'tkmind0',
        'binning': [list(np.arange(0,50,5))+list(np.arange(50,150,10))+list(np.arange(150,500,50))],
        'title': 'muon-type lepton-jet min track d0;|d0| [#mum];Events',
    },
    {
        'name': 'tkmind0_tf',
        'binning': [list(np.arange(0,50,5))+list(np.arange(50,150,10))+list(np.arange(150,500,50))],
        'title': 'muon-type lepton-jet min track d0 (TF);|d0| [#mum];Events',
    },
    {
        'name': 'tkmind0_vr',
        'binning': [list(np.arange(0,50,5))+list(np.arange(50,150,10))+list(np.arange(150,500,50))],
        'title': 'muon-type lepton-jet min track d0 (VR);|d0| [#mum];Events',
    },
    {
        'name': 'tkmind0_cr',
        'binning': [list(np.arange(0,50,5))+list(np.arange(50,150,10))+list(np.arange(150,500,50))],
        'title': 'muon-type lepton-jet min track d0 (CR);|d0| [#mum];Events',
    },
    {
        'name': 'scaledd0',
        'binning': (40,0,8),
        'title': 'muon-type lepton-jet scaled d0;scaled |d0|;Events',
    },
    {
        'name': 'scaled0_tf',
        'binning': (40,0,8),
        'title': 'muon-type lepton-jet scaled d0 (TF);scaled |d0|;Events',
    },
    {
        'name': 'scaled0_vr',
        'binning': (40,0,8),
        'title': 'muon-type lepton-jet scaled d0 (VR);scaled |d0|;Events',
    },
    {
        'name': 'scaled0_cr',
        'binning': (40,0,8),
        'title': 'muon-type lepton-jet scaled d0 (CR);scaled |d0|;Events',
    },
]