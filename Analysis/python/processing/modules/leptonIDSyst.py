#!/usr/bin/env python
import math

from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *

##
# lepton ID systematics evaluation
##

class MyEvents(Events):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)


    def processEvent(self, event, aux):
        if self.Type != 'MC': return
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']

        LJ0, LJ1 = aux['lj0'], aux['lj1']
        passCosmic = all(map(lambda lj: lj.passCosmicVeto(event), [LJ0, LJ1]))
        if not passCosmic: return

        mind0s = []
        for lj in [LJ0, LJ1]:
            if lj.isMuonType() and not math.isnan(lj.pfcand_tkD0Min):
                mind0s.append(lj.pfcand_tkD0Min*1e4)

        ## displacement cut
        metric_d0 = {'2mu2e': 1500, '4mu': 1000}
        if max(mind0s)<metric_d0[chan]: return

        dphi = abs(DeltaPhi(LJ0.p4, LJ1.p4))
        maxpfiso = max([LJ0.pfiso(), LJ1.pfiso()])
        egmljiso = None
        for lj in [LJ0, LJ1]:
            if lj.isEgmType(): egmljiso = lj.pfiso()

        if chan=='2mu2e':
            self.Histos['{}/dphiIso2D_nominal'     .format(chan)].Fill(dphi, egmljiso, aux['wgt'])
            # self.Histos['{}/dphiIso2D_electron'    .format(chan)].Fill(dphi, egmljiso, aux['wgt_electron'])
            self.Histos['{}/dphiIso2D_electron_up' .format(chan)].Fill(dphi, egmljiso, aux['wgt_electron_up'])
            self.Histos['{}/dphiIso2D_electron_low'.format(chan)].Fill(dphi, egmljiso, aux['wgt_electron_low'])
            # self.Histos['{}/dphiIso2D_photon'      .format(chan)].Fill(dphi, egmljiso, aux['wgt_photon'])
            self.Histos['{}/dphiIso2D_photon_up'   .format(chan)].Fill(dphi, egmljiso, aux['wgt_photon_up'])
            self.Histos['{}/dphiIso2D_photon_low'  .format(chan)].Fill(dphi, egmljiso, aux['wgt_photon_low'])
            # self.Histos['{}/dphiIso2D_pfmuon'      .format(chan)].Fill(dphi, egmljiso, aux['wgt_pfmuon'])
            self.Histos['{}/dphiIso2D_pfmuon_up'   .format(chan)].Fill(dphi, egmljiso, aux['wgt_pfmuon_up'])
            self.Histos['{}/dphiIso2D_pfmuon_low'  .format(chan)].Fill(dphi, egmljiso, aux['wgt_pfmuon_low'])

            # self.Histos['{}/sfelectron_up' .format(chan)].Fill(aux['sf_electron_up']-aux['sf_electron'])
            # self.Histos['{}/sfelectron_low'.format(chan)].Fill(aux['sf_electron']-aux['sf_electron_low'])

            # self.Histos['{}/sfphoton_up' .format(chan)].Fill(aux['sf_photon_up']-aux['sf_photon'])
            # self.Histos['{}/sfphoton_low'.format(chan)].Fill(aux['sf_photon']-aux['sf_photon_low'])

        if chan=='4mu':
            self.Histos['{}/dphiIso2D_nominal'     .format(chan)].Fill(dphi, maxpfiso, aux['wgt'])
            # self.Histos['{}/dphiIso2D_pfmuon'      .format(chan)].Fill(dphi, maxpfiso, aux['sf_pfmuon'])
            self.Histos['{}/dphiIso2D_pfmuon_up'   .format(chan)].Fill(dphi, maxpfiso, aux['wgt_pfmuon_up'])
            self.Histos['{}/dphiIso2D_pfmuon_low'  .format(chan)].Fill(dphi, maxpfiso, aux['wgt_pfmuon_low'])


    def postProcess(self):
        super(MyEvents, self).postProcess()

        for k in self.Histos:
            if 'phi' not in k: continue
            xax = self.Histos[k].axis(0)
            decorate_axis_pi(xax)
            if '2D' in k:
                self.Histos[k].yaxis.SetNdivisions(-210)


histCollection = [
    {
        'name': 'dphiIso2D_nominal',
        'binning': (20, 0, M_PI, 20, 0, 0.5),
        'title': '|#Delta#phi| vs iso;|#Delta#phi|;iso',
    },
    # {
    #     'name': 'dphiIso2D_electron',
    #     'binning': (30, 0, M_PI, 50, 0, 0.5),
    #     'title': '|#Delta#phi| vs iso;|#Delta#phi|;iso',
    # },
    {
        'name': 'dphiIso2D_electron_up',
        'binning': (20, 0, M_PI, 20, 0, 0.5),
        'title': '|#Delta#phi| vs iso;|#Delta#phi|;iso',
    },
    {
        'name': 'dphiIso2D_electron_low',
        'binning': (20, 0, M_PI, 20, 0, 0.5),
        'title': '|#Delta#phi| vs iso;|#Delta#phi|;iso',
    },
    # {
    #     'name': 'dphiIso2D_photon',
    #     'binning': (30, 0, M_PI, 50, 0, 0.5),
    #     'title': '|#Delta#phi| vs iso;|#Delta#phi|;iso',
    # },
    {
        'name': 'dphiIso2D_photon_up',
        'binning': (20, 0, M_PI, 20, 0, 0.5),
        'title': '|#Delta#phi| vs iso;|#Delta#phi|;iso',
    },
    {
        'name': 'dphiIso2D_photon_low',
        'binning': (20, 0, M_PI, 20, 0, 0.5),
        'title': '|#Delta#phi| vs iso;|#Delta#phi|;iso',
    },
    # {
    #     'name': 'dphiIso2D_pfmuon',
    #     'binning': (30, 0, M_PI, 50, 0, 0.5),
    #     'title': '|#Delta#phi| vs iso;|#Delta#phi|;iso',
    # },
    {
        'name': 'dphiIso2D_pfmuon_up',
        'binning': (20, 0, M_PI, 20, 0, 0.5),
        'title': '|#Delta#phi| vs iso;|#Delta#phi|;iso',
    },
    {
        'name': 'dphiIso2D_pfmuon_low',
        'binning': (20, 0, M_PI, 20, 0, 0.5),
        'title': '|#Delta#phi| vs iso;|#Delta#phi|;iso',
    },
    # {
    #     'name': 'sfelectron_up',
    #     'binning': (30, 0, 0.15),
    #     'title': 'electron ID SF syst. up;syst. up;counts',
    # },
    # {
    #     'name': 'sfelectron_low',
    #     'binning': (30, 0, 0.15),
    #     'title': 'electron ID SF syst. low;syst. low;counts',
    # },
    # {
    #     'name': 'sfphoton_up',
    #     'binning': (30, 0, 0.15),
    #     'title': 'photon ID SF syst. up;syst. up;counts',
    # },
    # {
    #     'name': 'sfphoton_low',
    #     'binning': (30, 0, 0.15),
    #     'title': 'photon ID SF syst. low;syst. low;counts',
    # },
]