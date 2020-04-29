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
        cutflowbin = 5

        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1

        LJ0, LJ1 = aux['lj0'], aux['lj1']
        passCosmic = all(map(lambda lj: lj.passCosmicVeto(event), [LJ0, LJ1]))

        if not passCosmic: return
        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1

        dphi = abs(DeltaPhi(LJ0.p4, LJ1.p4))
        maxpfiso = max([LJ0.pfiso(), LJ1.pfiso()])
        njet = sum([1 for j in event.ak4jets if j.jetid and j.p4.pt()>max([LJ0.p4.pt(), LJ1.p4.pt()]) and abs(j.p4.eta())<2.4])
        ## displacement cut
        mind0sigs = []
        for lj in [LJ0, LJ1]:
            if lj.isMuonType() and not math.isnan(lj.pfcand_tkD0SigMin):
                mind0sigs.append(lj.pfcand_tkD0SigMin)

        metric_d0sig = {'2mu2e': 2, '4mu': 0.5}
        metric_pfiso = {'2mu2e': 0.15, '4mu': 0.15}

        self.Histos['{}/d0sig'.format(chan)].Fill(max(mind0sigs), aux['wgt'])
        if max(mind0sigs)<metric_d0sig[chan]: return
        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1

        self.Histos['{}/njet'.format(chan)].Fill(njet, aux['wgt'])

        if njet==0:
            self.Histos['{}/dphi_0jet'.format(chan)].Fill(dphi, aux['wgt'])
        else:
            self.Histos['{}/dphi_0jetInv'.format(chan)].Fill(dphi, aux['wgt'])

        if chan=='2mu2e':
            if njet>0: return
            else: self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1

        self.Histos['{}/dphiIso2D'.format(chan)].Fill(dphi, maxpfiso, aux['wgt'])

        self.Histos['{}/dphi'.format(chan)].Fill(dphi, aux['wgt'])
        self.Histos['{}/iso'.format(chan)].Fill(maxpfiso, aux['wgt'])
        invm = (LJ0.p4+LJ1.p4).M()
        self.Histos['{}/invm'.format(chan)].Fill(invm, aux['wgt'])

        if maxpfiso<metric_pfiso[chan]:
            self.Histos['{}/dphi_siso'.format(chan)].Fill(dphi, aux['wgt'])

            self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1
            if dphi>math.pi/2:
                self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1

        else:
            self.Histos['{}/dphi_sisoInv'.format(chan)].Fill(dphi, aux['wgt'])

    def postProcess(self):
        super(MyEvents, self).postProcess()

        for ch in self.Channel:
            xaxis = self.Histos['{}/cutflow'.format(ch)].axis(0)

            labels = [ch, 'ljcosmicveto_pass', 'd0sig_pass']
            if ch=='2mu2e': labels.append('njet_eq0')
            labels.extend(['maxljiso_pass', 'ljpairdphi_pass'])

            for i, s in enumerate(labels, start=6):
                xaxis.SetBinLabel(i, s)
                # binNum., labAngel, labSize, labAlign, labColor, labFont, labText
                xaxis.ChangeLabel(i, 315, -1, 11, -1, -1, s)

        for k in self.Histos:
            if 'phi' not in k: continue
            xax = self.Histos[k].axis(0)
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
        'name': 'dphi',
        'binning': (30, 0, M_PI),
        'title': '|#Delta#phi| of lepton-jet pair;|#Delta#phi|;counts/#pi/30'
    },
    {
        'name': 'iso',
        'binning': (50, 0, 1),
        'title': 'max lepton-jet isolation;isolation;Events'
    },
    {
        'name': 'njet',
        'binning': (5, 0, 5),
        'title': 'num. of AK4Jets;num.AK4jet;counts/1'
    },
    {
        'name': 'd0sig',
        'binning': [[0, 0.25, 0.5, 1.0, 1.5, 2.0, 3, 4, 6, 8, 10]],
        'title': 'max lepton-jet min d0 significance;d0/#sigma_{d0};Events'
    },
    {
        'name': 'dphi_0jet',
        'binning': (30, 0, M_PI),
        'title': '|#Delta#phi| of lepton-jet pair;|#Delta#phi|;counts/#pi/30'
    },
    {
        'name': 'dphi_0jetInv',
        'binning': (30, 0, M_PI),
        'title': '|#Delta#phi| of lepton-jet pair;|#Delta#phi|;counts/#pi/30'
    },
    {
        'name': 'dphi_siso',
        'binning': (30, 0, M_PI),
        'title': '|#Delta#phi| of lepton-jet pair;|#Delta#phi|;counts/#pi/30'
    },
    {
        'name': 'dphi_sisoInv',
        'binning': (30, 0, M_PI),
        'title': '|#Delta#phi| of lepton-jet pair;|#Delta#phi|;counts/#pi/30'
    },
    {
        'name': 'dphiIso2D',
        'binning': (30, 0, M_PI, 30, 0, 0.3),
        'title': '|#Delta#phi| vs maxiso;|#Delta#phi|;maxIso',
    },
    {
        'name': 'invm',
        'binning': (100, 0, 250),
        'title': 'inv mass;mass [GeV];Events'
    },
]

