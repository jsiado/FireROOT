#!/usr/bin/python
import math

from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *

class MyEvents(Events):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu']):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel)

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']
        LJ0, LJ1 = aux['lj0'], aux['lj1']
        passCosmic = all(map(lambda lj: lj.passCosmicVeto(event), [LJ0, LJ1]))

        if not passCosmic: return

        dphi = abs(DeltaPhi(LJ0.p4, LJ1.p4))
        maxpfiso = max([LJ0.pfiso(), LJ1.pfiso()])
        njet = sum([1 for j in event.ak4jets if j.jetid and j.p4.pt()>max([LJ0.p4.pt(), LJ1.p4.pt()]) and abs(j.p4.eta())<2.4])
        ## displacement cut
        mind0sigs = []
        for lj in [LJ0, LJ1]:
            if lj.isMuonType() and not math.isnan(lj.pfcand_tkD0SigMin):
                mind0sigs.append(lj.pfcand_tkD0SigMin)

        nbtight = 0
        for s, j in zip(event.hftagscores, event.ak4jets):
            if not (j.jetid and j.p4.pt()>30 and abs(j.p4.eta())<2.5): continue
            if (s.DeepCSV_b&(1<<2))==(1<<2): nbtight += 1

        if chan=='2mu2e' and max(mind0sigs)>2: return
        if chan=='2mu2e' and max(mind0sigs)<0.5: return

        self.Histos['{}/nbtight'.format(chan)].Fill(nbtight, aux['wgt'])
        if nbtight==0: return

        self.Histos['{}/dphi'.format(chan)].Fill(dphi, aux['wgt'])
        self.Histos['{}/iso'.format(chan)].Fill(maxpfiso, aux['wgt'])
        self.Histos['{}/njet'.format(chan)].Fill(njet, aux['wgt'])

        if maxpfiso<0.15:
            self.Histos['{}/dphi_siso'.format(chan)].Fill(dphi, aux['wgt'])
        else:
            self.Histos['{}/dphi_sisoInv'.format(chan)].Fill(dphi, aux['wgt'])

histCollection = [
    {
        'name': 'nbtight',
        'binning': (5, 0, 5),
        'title': 'Num. tight bjets;Num.bjets;counts'
    },
    {
        'name': 'njet',
        'binning': (5, 0, 5),
        'title': 'num. of AK4Jets;num.AK4jet;counts/1'
    },
    {
        'name': 'iso',
        'binning': (50, 0, 1),
        'title': 'max lepton-jet isolation;isolation;counts/0.02'
    },
    {
        'name': 'dphi',
        'binning': (20, 0, M_PI),
        'title': '|#Delta#phi| between lepton-jet pair;|#Delta#phi|;counts/#pi/20'
    },
    {
        'name': 'dphi_siso',
        'binning': (20, 0, M_PI),
        'title': '|#Delta#phi| between lepton-jet pair;|#Delta#phi|;counts/#pi/20'
    },
    {
        'name': 'dphi_sisoInv',
        'binning': (20, 0, M_PI),
        'title': '|#Delta#phi| between lepton-jet pair;|#Delta#phi|;counts/#pi/20'
    },
]
