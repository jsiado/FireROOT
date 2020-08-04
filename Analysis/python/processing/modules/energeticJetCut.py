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

        ## displacement cut
        mind0sigs = []
        mind0s = []
        for lj in [LJ0, LJ1]:
            if not lj.isMuonType(): continue
            if not math.isnan(lj.pfcand_tkD0SigMin): mind0sigs.append(lj.pfcand_tkD0SigMin)
            if not math.isnan(lj.pfcand_tkD0Min): mind0s.append(lj.pfcand_tkD0Min*1e4)

        if max(mind0s)<1000: return

        dphi = abs(DeltaPhi(LJ0.p4, LJ1.p4))

        njet = sum([1 for j in event.ak4jets if j.jetid and j.p4.pt()>50 and abs(j.p4.eta())<2.4])
        self.Histos['{}/njet'.format(chan)].Fill(njet, aux['wgt'])
        if njet==0:
            self.Histos['{}/dphi_njet_l'.format(chan)].Fill(dphi, aux['wgt'])
        else:
            self.Histos['{}/dphi_njet_g'.format(chan)].Fill(dphi, aux['wgt'])


        ## invert energetic jet cut
        njet = sum([1 for j in event.ak4jets if j.jetid and j.p4.pt()>max([LJ0.p4.pt(), LJ1.p4.pt()]) and abs(j.p4.eta())<2.4])
        jet_ljcleaned = []
        maxpt, mindist = 0., 999.
        for j in event.ak4jets:
            if not j.jetid: continue
            if abs(j.p4.eta())>2.4: continue
            if j.p4.pt()>maxpt:
                maxpt = j.p4.pt()
                mindist = min([DeltaR(j.p4, LJ0.p4), DeltaR(j.p4, LJ1.p4)])
            if min([DeltaR(j.p4, LJ0.p4), DeltaR(j.p4, LJ1.p4)])<0.4: continue
            if j.p4.pt()>max([LJ0.p4.pt(), LJ1.p4.pt()]): jet_ljcleaned.append( 1 )
            else: jet_ljcleaned.append( 0 )
        # if not jet_ljcleaned: return
        njet_ljcleaned = sum(jet_ljcleaned)

        if njet==0:
            self.Histos['{}/mindist'.format(chan)].Fill(mindist, aux['wgt'])

        maxpfiso = max([LJ0.pfiso(), LJ1.pfiso()])
        maxpfhadiso = max([LJ0.pfhadiso(), LJ1.pfhadiso()])

        if njet==0:
            self.Histos['{}/abcd0j'.format(chan)].Fill(dphi, maxpfiso, aux['wgt'])
        # elif mindist>0.4:
        else:
            self.Histos['{}/abcdjs'.format(chan)].Fill(dphi, maxpfiso, aux['wgt'])
            if mindist>0.4:
                self.Histos['{}/abcdjsiso'.format(chan)].Fill(dphi, maxpfiso, aux['wgt'])

    def postProcess(self):
        super(MyEvents, self).postProcess()

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
        'name': 'abcdjs',
        'binning': (30, 0, M_PI, 20, 0, 1),
        'title': 'Njet>0;|#Delta#phi|;maxIso',
    },
    {
        'name': 'abcdjsiso',
        'binning': (30, 0, M_PI, 20, 0, 1),
        'title': 'Njet>0;|#Delta#phi|;maxIso',
    },
    {
        'name': 'abcd0j',
        'binning': (30, 0, M_PI, 20, 0, 1),
        'title': 'Njet=0;|#Delta#phi|;maxIso',
    },
    {
        'name': 'mindist',
        'binning': (60,0,6),
        'title': 'min#DeltaR(leading AK4jet, lepton-jet);#DeltaR;Events/0.1',
    },
    {
        'name': 'njet',
        'binning': (5, 0, 5),
        'title': 'Number of ak4jets w/ p_{T}>50GeV;N_{jets};Events'
    },
    {
        'name': 'dphi_njet_l',
        'binning': (30, 0, M_PI),
        'title': 'lepton-jet pair |#Delta#phi|(N_{jet}=0);|#Delta#phi|;counts',
    },
    {
        'name': 'dphi_njet_g',
        'binning': (30, 0, M_PI),
        'title': 'lepton-jet pair |#Delta#phi|(N_{jet}>0);|#Delta#phi|;counts',
    },
]