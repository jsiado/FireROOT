#!/usr/bin/env python
import math
import numpy as np
from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *


class MyEvents(Events):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['4mu',], **kwargs):
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

        njet = sum([1 for j in event.ak4jets if j.jetid and j.p4.pt()>50 and abs(j.p4.eta())<2.4])
        if njet>1: return
        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1

        passLjMass = all(map(lambda lj: lj.isEgmType() or lj.isMuonType() and lj.p4.M()<8, [LJ0, LJ1]))
        if not passLjMass: return
        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1

        self.Histos['{}/ljetasum'.format(chan)].Fill(abs(LJ0.p4.eta())+abs(LJ1.p4.eta()), aux['wgt'])
        self.Histos['{}/ljetaabssum'.format(chan)].Fill(abs(LJ0.p4.eta()+LJ1.p4.eta()), aux['wgt'])
        self.Histos['{}/maxljiso'.format(chan)].Fill(max([LJ0.pfiso(), LJ1.pfiso()]), aux['wgt'])
        self.Histos['{}/tkmind0'.format(chan)].Fill(max([abs(lj.pfcand_tkD0Min*1e4) for lj in [LJ0, LJ1] if lj.isMuonType() ]), aux['wgt'])
        for lj in [LJ0, LJ1]:
            if not lj.isMuonType(): continue
            ljmass = lj.p4.M()
            if ljmass==0: ljmass=0.25
            scaledD0 = math.log10(abs(lj.pfcand_tkD0Min * 1e4 * lj.p4.pt() /ljmass))
            self.Histos['{}/scaledd0'.format(chan)].Fill(scaledD0, aux['wgt'])

        dphi = abs(DeltaPhi(LJ0.p4, LJ1.p4))
        self.Histos['{}/dphi_e'.format(chan)].Fill(dphi, aux['wgt'])
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
            labels = [ch, 'ljcosmicveto_pass', 'njet_lt2', 'muljmass_lt8',
                    'dphi_gt2p1']

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
        'name': 'scaledd0',
        'binning': (40,0,8),
        'title': 'muon-type lepton-jet scaled d0;scaled |d0|;Events',
    },
]