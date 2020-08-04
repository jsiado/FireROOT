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

        # displacement variable
        mind0s = []
        for lj in [LJ0, LJ1]:
            if not lj.isMuonType(): continue
            if not math.isnan(lj.pfcand_tkD0Min): mind0s.append(lj.pfcand_tkD0Min)
        if max(mind0s)*1e4<1000: return # max mind0<20um
        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1

        # if self.Dtag.startswith('DY'):
        #     for lj in [LJ0, LJ1]:
        #         if not lj.isMuonType(): continue
        #         print(['{:.3f}'.format(v.pt()) for v in lj.muons(event)])
        dphi = abs(DeltaPhi(LJ0.p4, LJ1.p4))
        maxpfiso = max([LJ0.pfiso(), LJ1.pfiso()])
        maxpfhadiso = max([LJ0.pfhadiso(), LJ1.pfhadiso()])

        # nbjets
        nbtight = 0
        for s, j in zip(event.hftagscores, event.ak4jets):
            if not (j.jetid and j.p4.pt()>30 and abs(j.p4.eta())<2.5): continue
            if (s.DeepCSV_b&(1<<2))==(1<<2): nbtight += 1
        self.Histos['{}/nbtight'.format(chan)].Fill(nbtight, aux['wgt'])
        if nbtight==0:
            self.Histos['{}/abcd0b'.format(chan)].Fill(dphi, maxpfiso, aux['wgt'])
            self.Histos['{}/dphi0b'.format(chan)].Fill(dphi, aux['wgt'])
        else:
            self.Histos['{}/abcdbs'.format(chan)].Fill(dphi, maxpfiso, aux['wgt'])
            self.Histos['{}/dphibs'.format(chan)].Fill(dphi, aux['wgt'])

        njet = sum([1 for j in event.ak4jets if j.jetid and j.p4.pt()>max([LJ0.p4.pt(), LJ1.p4.pt()]) and abs(j.p4.eta())<2.4])
        self.Histos['{}/njet'.format(chan)].Fill(njet, aux['wgt'])

        if njet>0: return
        self.Histos['{}/cutflow'.format(chan)].Fill(cutflowbin, aux['wgt']); cutflowbin+=1

    def postProcess(self):
        super(MyEvents, self).postProcess()

        for ch in self.Channel:
            xaxis = self.Histos['{}/cutflow'.format(ch)].axis(0)

            labels = [ch, 'ljcosmicveto_pass', 'd0_pass', 'njet_ge0',]

            for i, s in enumerate(labels, start=6):
                xaxis.SetBinLabel(i, s)
                # binNum., labAngel, labSize, labAlign, labColor, labFont, labText
                xaxis.ChangeLabel(i, 315, -1, 11, -1, -1, s)

        for k in self.Histos:
            if 'phi' not in k: continue
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
        'name': 'nbtight',
        'binning': (5, 0, 5),
        'title': 'Num. tight bjets;Num.bjets;Events'
    },
    {
        'name': 'njet',
        'binning': (5, 0, 5),
        'title': 'num. of AK4Jets;num.AK4jet;Events'
    },
    {
        'name': 'abcdbs',
        'binning': (30, 0, M_PI, 20, 0, 1),
        'title': 'Nbjet>0;|#Delta#phi|;maxIso',
    },
    {
        'name': 'abcd0b',
        'binning': (30, 0, M_PI, 20, 0, 1),
        'title': 'Nbjet=0;|#Delta#phi|;maxIso',
    },
    {
        'name': 'dphi0b',
        'binning': (30, 0, M_PI),
        'title': 'lepton-jet pair |#Delta#phi|(N_{bjet}=0);|#Delta#phi|;counts',
    },
    {
        'name': 'dphibs',
        'binning': (30, 0, M_PI),
        'title': 'lepton-jet pair |#Delta#phi|(N_{bjet}>0);|#Delta#phi|;counts',
    },
]