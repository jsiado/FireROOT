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

        if njet>1: return

        nbtight = 0
        for s, j in zip(event.hftagscores, event.ak4jets):
            if not (j.jetid and j.p4.pt()>30 and abs(j.p4.eta())<2.5): continue
            if (s.DeepCSV_b&(1<<2))==(1<<2): nbtight += 1
        if nbtight>0: return


        for lj in [LJ0, LJ1]:
            if not lj.isMuonType(): continue
            self.Histos['{}/ljmass'.format(chan)].Fill(lj.p4.M(), aux['wgt'])

        passLjMass = all(map(lambda lj: lj.isEgmType() or lj.isMuonType() and lj.p4.M()<8, [LJ0, LJ1]))
        if passLjMass:
            # wsi: print badass DYJets events
            # if self.Dtag.startswith('DYJets'):
            #     print('{:4} {}:{}:{}'.format(chan, event.run, event.lumi, event.event))
            return


        self.Histos['{}/invm_inc'.format(chan)].Fill(invm, aux['wgt'])
        self.Histos['{}/dphi_inc'.format(chan)].Fill(dphi, aux['wgt'])

        scaledD0s = []
        for lj in [LJ0, LJ1]:
            if not lj.isMuonType(): continue
            ljmass = lj.p4.M()
            if ljmass==0: ljmass=0.25
            scaledD0 = math.log10(abs(lj.pfcand_tkD0Min * 1e4 * lj.p4.pt() /ljmass))
            scaledD0s.append(scaledD0)

        absetasum = abs(LJ0.p4.eta()+LJ1.p4.eta())
        if max(scaledD0s)<1.5:
            self.Histos['{}/absetasum_tf'.format(chan)].Fill(absetasum, aux['wgt'])
        elif max(scaledD0s)<2.5:
            self.Histos['{}/absetasum_vr'.format(chan)].Fill(absetasum, aux['wgt'])
        else:
            self.Histos['{}/absetasum_cr'.format(chan)].Fill(absetasum, aux['wgt'])

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
        'name': 'dphi_inc',
        'binning': (30, 0, M_PI),
        'title': 'lepton-jet pair |#Delta#phi|;|#Delta#phi|;counts',
    },
    {
        'name': 'invm_inc',
        'binning': (100, 0, 1600),
        'title': 'invariant mass of lepton-jet pair;invM [GeV];counts/16GeV'
    },
    {
        'name': 'ljmass',
        'binning': (100,0,25),
        'title': 'muon-type lepton-jet mass;mass [GeV];Events/0.25GeV',
    },
    {
        'name': 'absetasum_tf',
        'binning': (48, 0, 4.8),
        'title': 'lepton-jet |#eta_{0}+#eta_{1}| (TF);|#eta_{0}+#eta_{1}|;counts',
    },
    {
        'name': 'absetasum_vr',
        'binning': (48, 0, 4.8),
        'title': 'lepton-jet |#eta_{0}+#eta_{1}| (VR);|#eta_{0}+#eta_{1}|;counts',
    },
    {
        'name': 'absetasum_cr',
        'binning': (48, 0, 4.8),
        'title': 'lepton-jet |#eta_{0}+#eta_{1}| (CR);|#eta_{0}+#eta_{1}|;counts',
    },
]