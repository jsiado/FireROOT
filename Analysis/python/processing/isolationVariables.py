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

        # displacement variable
        mind0s = []
        lxy = []
        muljmass = []
        for lj in [LJ0, LJ1]:
            if not lj.isMuonType(): continue
            if not math.isnan(lj.pfcand_tkD0Min): mind0s.append(abs(lj.pfcand_tkD0Min)*1e4)
            muljmass.append(lj.p4.M())
            if not math.isnan(lj.klmvtx_lxy):
                if lj.klmvtx_lxy>0: lxy.append(lj.klmvtx_lxy)
        # if max(mind0s)*1e4<10: return # max mind0<10um
        hasJpsi = False
        if any(map(lambda x: x>2.9 and x<3.3, muljmass)): hasJpsi = True

        if not lxy: return
        if max(mind0s)<20: return
        self.Histos['{}/ljlxy'.format(chan)].Fill(max(lxy), aux['wgt'])

        njet = sum([1 for j in event.ak4jets if j.jetid and j.p4.pt()>50 and abs(j.p4.eta())<2.4])
        # if njet>0: return

        nbtight = 0
        for s, j in zip(event.hftagscores, event.ak4jets):
            if not (j.jetid and j.p4.pt()>30 and abs(j.p4.eta())<2.5): continue
            if (s.DeepCSV_b&(1<<2))==(1<<2): nbtight += 1

        ## isolation variables
        hadronic_activities = []
        scaledd0s = []
        for lj in [LJ0, LJ1]:
            if not math.isnan(lj.pfIsolationNoPU05):
                self.Histos['{}/pfisoNoPU'.format(chan)].Fill(lj.pfIsolationNoPU05, aux['wgt'])
                activity = lj.p4.energy()*lj.pfIsolationNoPU05/(1-lj.pfIsolationNoPU05)
                self.Histos['{}/pfactivity'.format(chan)].Fill(activity, aux['wgt'])
            if not math.isnan(lj.hadIsolationNoPU05):
                self.Histos['{}/hadisoNoPU'.format(chan)].Fill(lj.hadIsolationNoPU05, aux['wgt'])
                activity = lj.p4.energy()*lj.hadIsolationNoPU05/(1-lj.hadIsolationNoPU05)
                hadronic_activities.append( activity )
                self.Histos['{}/hadactivity'.format(chan)].Fill(activity, aux['wgt'])
                if njet==0:
                    self.Histos['{}/hadactivity_njet_l'.format(chan)].Fill(activity, aux['wgt'])
                if nbtight==0:
                    self.Histos['{}/hadactivity_nbtight_l'.format(chan)].Fill(activity, aux['wgt'])
            if lj.isMuonType():
                ljmass = lj.p4.M()
                if ljmass==0: ljmass=8
                scaledD0 = math.log10(abs(lj.pfcand_tkD0Min * 1e4 * lj.p4.pt() /ljmass))
                scaledd0s.append(scaledD0)

        self.Histos['{}/ljlxy_hadact'.format(chan)].Fill(max(lxy), max(hadronic_activities), aux['wgt'])

        invm = (LJ0.p4+LJ1.p4).M()
        massratio = LJ0.p4.energy()*LJ1.p4.energy()/invm**2
        self.Histos['{}/massratio'.format(chan)].Fill(massratio, aux['wgt'])
        self.Histos['{}/d0_massratio'.format(chan)].Fill(max(mind0s), massratio, aux['wgt'])
        if max(mind0s)>100 and nbtight==0 and not hasJpsi:
            self.Histos['{}/maxhadact_massratio'.format(chan)].Fill(max(hadronic_activities), massratio, aux['wgt'])
            self.Histos['{}/scaledd0_massratio'.format(chan)].Fill(max(scaledd0s), massratio, aux['wgt'])


        self.Histos['{}/maxhadact'.format(chan)].Fill(max(hadronic_activities), aux['wgt'])
        self.Histos['{}/maxhadact_scaledd0'.format(chan)].Fill(max(hadronic_activities), max(scaledd0s), aux['wgt'])
        if njet==0:
            self.Histos['{}/maxhadact_njet_l'.format(chan)].Fill(max(hadronic_activities), aux['wgt'])
            self.Histos['{}/maxhadact_scaledd0_njet_l'.format(chan)].Fill(max(hadronic_activities), max(scaledd0s), aux['wgt'])
        if nbtight==0:
            self.Histos['{}/maxhadact_nbtight_l'.format(chan)].Fill(max(hadronic_activities), aux['wgt'])
            self.Histos['{}/maxhadact_scaledd0_nbtight_l'.format(chan)].Fill(max(hadronic_activities), max(scaledd0s), aux['wgt'])



histCollection = [
    {
        'name': 'pfisoNoPU',
        'binning': (100, 0, 1),
        'title': 'lepton-jet pfIsoNoPU05;pfIsoNoPU;counts/0.01',
    },
    {
        'name': 'pfactivity',
        'binning': (100, 0, 100),
        'title': 'lepton-jet isolation PFcand activity;activity [GeV];Events/1GeV',
    },
    {
        'name': 'hadisoNoPU',
        'binning': (100, 0, 1),
        'title': 'lepton-jet hadIsoNoPU05;hadIsoNoPU;counts/0.01',
    },
    {
        'name': 'hadactivity',
        'binning': (100, 0, 100),
        'title': 'lepton-jet isolation hadronic PFcand activity;hadronic activity [GeV];Events/1GeV',
    },
    {
        'name': 'hadactivity_njet_l',
        'binning': (100, 0, 100),
        'title': 'lepton-jet isolation hadronic PFcand activity (N_{jet}=0);hadronic activity [GeV];Events/1GeV',
    },
    {
        'name': 'hadactivity_nbtight_l',
        'binning': (100, 0, 100),
        'title': 'lepton-jet isolation hadronic PFcand activity (N_{bjet}=0);hadronic activity [GeV];Events/1GeV',
    },
    {
        'name': 'maxhadact',
        'binning': (100, 0, 100),
        'title': 'max lepton-jet isolation hadronic activity;hadronic activity [GeV];Events/1GeV',
    },
    {
        'name': 'maxhadact_njet_l',
        'binning': (100, 0, 100),
        'title': 'max lepton-jet isolation hadronic activity (N_{jet}=0);hadronic activity [GeV];Events/1GeV',
    },
    {
        'name': 'maxhadact_nbtight_l',
        'binning': (100, 0, 100),
        'title': 'max lepton-jet isolation hadronic activity (N_{bjet}=0);hadronic activity [GeV];Events/1GeV',
    },
    {
        'name': 'maxhadact_scaledd0',
        'binning': (40, 0, 100, 40, 0, 8),
        'title': 'scaledd0 vs. max lepton-jet isolation hadronic activity;hadronic activity [GeV];scaled d0',
    },
    {
        'name': 'maxhadact_scaledd0_njet_l',
        'binning': (40, 0, 100, 40, 0, 8),
        'title': 'scaledd0 vs. max lepton-jet isolation hadronic activity (N_{jet}=0);hadronic activity [GeV];scaled d0',
    },
    {
        'name': 'maxhadact_scaledd0_nbtight_l',
        'binning': (40, 0, 100, 40, 0, 8),
        'title': 'scaledd0 vs. max lepton-jet isolation hadronic activity (N_{jet}=0);hadronic activity [GeV];scaled d0',
    },
    {
        'name': 'massratio',
        'binning': (100, 0.2, 1.2),
        'title': 'mass ratio variable;#frac{E_{0}E_{1}}{MM};Events',
    },
    {
        'name': 'maxhadact_massratio',
        'binning': (40, 0, 100, 50, 0.2, 1.2),
        'title': 'massratio vs. max lepton-jet isolation hadronic activity;hadronic activity [GeV];#frac{E_{0}E_{1}}{MM}',
    },
    {
        'name': 'scaledd0_massratio',
        'binning': (40, 0, 8, 50, 0.2, 1.2),
        'title': 'massratio vs. scaled d0;scaled d0;#frac{E_{0}E_{1}}{MM}',
    },
    {
        'name': 'd0_massratio',
        'binning': (100, 0, 1000, 50, 0.2, 1.2),
        'title': 'massratio vs. d0;d0[#mum];#frac{E_{0}E_{1}}{MM}',
    },
    {
        'name': 'ljlxy',
        'binning': (100, 0, 200),
        'title': 'muon-type lepton-jet lxy;lxy [cm];counts',
    },
    {
        'name': 'ljlxy_hadact',
        'binning': (100, 0, 200, 40,0,100),
        'title': 'max had activity vs. muon-type lepton-jet lxy;lxy [cm];hadronic activity [GeV]',
    },

]