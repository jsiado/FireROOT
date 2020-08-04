#!/usr/bin/env python
import math
import numpy as np

from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *


class MyEvents(Events):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)
        self.KeepCutFlow=True
        self.RawCutFlow=True

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']
        cutflowbin = 5

        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin); cutflowbin+=1

        LJ0, LJ1 = aux['lj0'], aux['lj1']
        passCosmic = all(map(lambda lj: lj.passCosmicVeto(event), [LJ0, LJ1]))

        if not passCosmic: return
        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin); cutflowbin+=1

        dphi = abs(DeltaPhi(LJ0.p4, LJ1.p4))
        if self.Type=='DATA' and dphi>2.2: return

        mind0s = []
        for lj in [LJ0, LJ1]:
            if lj.isMuonType() and not math.isnan(lj.pfcand_tkD0Min):
                mind0s.append(lj.pfcand_tkD0Min*1e4)

        for v in mind0s:
            self.Histos['{}/mind0'.format(chan)].Fill(v, aux['wgt'])
        self.Histos['{}/maxmind0'.format(chan)].Fill(max(mind0s), aux['wgt'])

        maxpfiso = max([LJ0.pfiso(), LJ1.pfiso()])
        egmljiso = None
        for lj in [LJ0, LJ1]:
            if lj.isEgmType(): egmljiso = lj.pfiso()
        if max(mind0s)<100: return

        # all events with |d0|>0.1mm
        self.Histos['{}/dphiIso2Dinc'.format(chan)].Fill(dphi, maxpfiso, aux['wgt'])
        if egmljiso is not None:
            self.Histos['{}/dphiEgmIso2Dinc'.format(chan)].Fill(dphi, egmljiso, aux['wgt'])


        ## displacement cut
        metric_d0 = {'2mu2e': 1500, '4mu': 1000}
        if max(mind0s)<metric_d0[chan]: return
        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin); cutflowbin+=1

        self.Histos['{}/rawevents'.format(chan)].Fill(0)


        self.Histos['{}/dphi'.format(chan)].Fill(dphi, aux['wgt'])
        self.Histos['{}/maxiso'.format(chan)].Fill(maxpfiso, aux['wgt'])
        for lj in [LJ0, LJ1]:
            self.Histos['{}/ljiso'.format(chan)].Fill(lj.pfiso(), aux['wgt'])
            if lj.isMuonType():
                self.Histos['{}/muljiso'.format(chan)].Fill(lj.pfiso(), aux['wgt'])
                self.Histos['%s/muljphi'%chan].Fill(lj.p4.phi(), aux['wgt'])

            if lj.isEgmType():
                egmljiso = lj.pfiso()
                self.Histos['{}/egmljiso'.format(chan)].Fill(lj.pfiso(), aux['wgt'])


        self.Histos['{}/dphiIso2D'.format(chan)].Fill(dphi, maxpfiso, aux['wgt'])
        if egmljiso is not None:
            self.Histos['{}/dphiEgmIso2D'.format(chan)].Fill(dphi, egmljiso, aux['wgt'])


    def postProcess(self):
        super(MyEvents, self).postProcess()

        for ch in self.Channel:
            xaxis = self.Histos['{}/cutflow'.format(ch)].axis(0)
            labels = [ch, 'ljcosmicveto_pass', 'mind0_pass',]

            for i, s in enumerate(labels, start=6):
                xaxis.SetBinLabel(i, s)
                # binNum., labAngel, labSize, labAlign, labColor, labFont, labText
                xaxis.ChangeLabel(i, 315, -1, 11, -1, -1, s)

        for k in self.Histos:
            if 'phi' not in k: continue
            xax = self.Histos[k].axis(0)
            decorate_axis_pi(xax)
            if '2D' in k:
                self.Histos[k].yaxis.SetNdivisions(-210)


histCollection = [
    {
        'name': 'mind0',
        # 'binning': [[0,2,4,6,8,10,20,50,]+list(np.arange(100,2501,100))],
        'binning': (40, 0, 2000),
        'title': 'muon-type lepton-jet minimum |d_{0}|;|d_{0}| [#mum];Events',
    },
    {
        'name': 'maxmind0',
        # 'binning': [[0,2,4,6,8,10,20,50,]+list(np.arange(100,2501,100))],
        'binning': (40, 0, 2000),
        'title': 'maximum of muon-type lepton-jets min |d_{0}|s;|d_{0}| [#mum];Events',
    },
    {
        'name': 'dphi',
        'binning': (20, 0, M_PI),
        'title': '|#Delta#phi| of lepton-jet pair;|#Delta#phi|;counts/#pi/20'
    },
    {
        'name': 'maxiso',
        'binning': (20, 0, 0.5),
        'title': 'max lepton-jet isolation;isolation;Events'
    },
    {
        'name': 'ljiso',
        'binning': (20, 0, 0.5),
        'title': 'lepton-jet isolation;isolation;Events'
    },
    {
        'name': 'muljiso',
        'binning': (20, 0, 0.5),
        'title': 'muon-type lepton-jet isolation;isolation;Events'
    },
    {
        'name': 'egmljiso',
        'binning': (20, 0, 0.5),
        'title': 'EGM-type lepton-jet isolation;isolation;Events'
    },
    {
        'name': 'dphiIso2Dinc',
        'binning': (20, 0, M_PI, 20, 0, 0.5),
        'title': '|#Delta#phi| vs maxiso;|#Delta#phi|;maxIso',
    },
    {
        'name': 'dphiEgmIso2Dinc',
        'binning': (20, 0, M_PI, 20, 0, 0.5),
        'title': '|#Delta#phi| vs egm-type lepton-jet Iso;|#Delta#phi|; Egm-type LJ Iso',
    },
    {
        'name': 'dphiIso2D',
        'binning': (20, 0, M_PI, 20, 0, 0.5),
        'title': '|#Delta#phi| vs maxiso;|#Delta#phi|;maxIso',
    },
    {
        'name': 'dphiEgmIso2D',
        'binning': (20, 0, M_PI, 20, 0, 0.5),
        'title': '|#Delta#phi| vs egm-type lepton-jet Iso;|#Delta#phi|; Egm-type LJ Iso',
    },
    {
        'name': 'rawevents',
        'binning': (1,0,1),
        'title': 'Raw events count;;Events',
    },
    {
        'name': 'muljphi',
        'binning': (40, -M_PI, M_PI),
        'title': 'muon-type LJ #phi;#phi;counts/#pi/20'
    },
]