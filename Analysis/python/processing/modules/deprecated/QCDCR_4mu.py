#!/usr/bin/env python
import math

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
        dphi = abs(DeltaPhi(LJ0.p4, LJ1.p4))
        njet = sum([1 for j in event.ak4jets if j.jetid and j.p4.pt()>50 and abs(j.p4.eta())<2.4])
        absetasum = abs(LJ0.p4.eta()+LJ1.p4.eta())
        maxiso = max([LJ0.pfiso(), LJ1.pfiso()])

        passLjMass = True
        for lj in [LJ0, LJ1]:
            if not lj.isMuonType(): continue
            ljmass = lj.p4.M()
            self.Histos['{}/ljmass'.format(chan)].Fill(ljmass, aux['wgt'])
            if ljmass>8: passLjMass=False
            if ljmass>2.9 and ljmass<3.3: passLjMass=False

        if not passLjMass: return

        self.Histos['{}/njet'.format(chan)].Fill(njet, aux['wgt'])
        self.Histos['{}/absetasum'.format(chan)].Fill(absetasum, aux['wgt'])
        self.Histos['{}/dphi'.format(chan)].Fill(dphi, aux['wgt'])
        self.Histos['{}/maxiso'.format(chan)].Fill(maxiso, aux['wgt'])

        if njet<1:
            self.Histos['{}/absetasum_njet_lt2'.format(chan)].Fill(absetasum, aux['wgt'])
            self.Histos['{}/maxiso_njet_l'.format(chan)].Fill(maxiso, aux['wgt'])
        else:
            self.Histos['{}/absetasum_njet_ge2'.format(chan)].Fill(absetasum, aux['wgt'])
            self.Histos['{}/maxiso_njet_g'.format(chan)].Fill(maxiso, aux['wgt'])


    def postProcess(self):
        super(MyEvents, self).postProcess()

        for k in self.Histos:
            if not k.split('/')[1].startswith('dphi'): continue
            xax = self.Histos[k].xaxis
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
        'name': 'njet',
        'binning': (5, 0, 5),
        'title': 'Number of ak4jets w/ p_{T}>50GeV;N_{jets};Events'
    },
    {
        'name': 'absetasum',
        'binning': (48, 0, 4.8),
        'title': 'lepton-jet |#eta_{0}+#eta_{1}|;|#eta_{0}+#eta_{1}|;counts',
    },
    {
        'name': 'dphi',
        'binning': (30, 0, M_PI),
        'title': 'lepton-jet pair |#Delta#phi|;|#Delta#phi|;counts',
    },
    {
        'name': 'ljmass',
        'binning': (100,0,10),
        'title': 'muon-type lepton-jet mass;mass [GeV];Events/0.01GeV',
    },
    {
        'name': 'absetasum_njet_lt2',
        'binning': (48, 0, 4.8),
        'title': 'lepton-jet |#eta_{0}+#eta_{1}| (N_{jet}<2);|#eta_{0}+#eta_{1}|;counts',
    },
    {
        'name': 'absetasum_njet_ge2',
        'binning': (48, 0, 4.8),
        'title': 'lepton-jet |#eta_{0}+#eta_{1}| (N_{jet}#geq2);|#eta_{0}+#eta_{1}|;counts',
    },
    {
        'name': 'maxiso',
        'binning': (50, 0, 0.25),
        'title': 'max lepton-jet iso;iso;counts',
    },
    {
        'name': 'maxiso_njet_l',
        'binning': (50, 0, 0.25),
        'title': 'max lepton-jet iso (N_{jet}<1);iso;counts',
    },
    {
        'name': 'maxiso_njet_g',
        'binning': (50, 0, 0.25),
        'title': 'max lepton-jet iso (N_{jet}#geq1);iso;counts',
    },
]