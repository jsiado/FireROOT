#!/usr/bin/env python
from __future__ import print_function
import math
import ROOT

from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *
class MyEvents(Events):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)

    def processEvent(self, event, aux):
        if not self.Dtag.startswith('DYJets'): return
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']

        LJ0, LJ1 = aux['lj0'], aux['lj1']
        passCosmic = all(map(lambda lj: lj.passCosmicVeto(event), [LJ0, LJ1]))
        if not passCosmic: return

        passLjMass = all(map(lambda lj: lj.isEgmType() or lj.isMuonType() and lj.p4.M()<8, [LJ0, LJ1]))
        if not passLjMass: return

        _run, _lumi, _event = event.run, event.lumi, event.event
        tag = '{}:{}:{}'.format(_run, _lumi, _event)

        if tag not in [
            # 2mu2e
            # "1:57823:131488809",
            # "1:78664:178881086",
            # "1:19441:44208166",
            # "1:70304:159869961",
            # 4mu
            "1:82610:187854136",
            "1:71514:162622754",
            "1:18481:42025231",
            ]: return

        # if tag not in [
        #     "1:90061:204798108",
        #     "1:75879:172548337",
        #     "1:57823:131488809",
        #     "1:96800:220122374",
        #     "1:58349:132683492",
        #     "1:90350:205453932",
        #     "1:49206:111893014",
        #     "1:42661:97010313",
        #     "1:71334:162211873",
        #     "1:72428:164700367",
        #     "1:78664:178881086",
        #     "1:88539:201337467",
        #     "1:60986:138681185",
        #     "1:19441:44208166",
        #     "1:62505:142134674",
        #     "1:70304:159869961",
        #     "1:75509:171706907",
        #     "1:76489:173934403",
        #     "1:45909:104394887",
        #     "1:59905:136223608",
        #     "1:3682:8371771",
        # ]: return

        print((tag+' - '+chan).center(80, '#'))

        for ij, LJ in enumerate([LJ0, LJ1]):

            print('<LJ{}> type: {}| pT {:.2f}, eta {:.2f}, phi {:.2f}, energy {:.2f}'.format(
                ij, LJ.type(), LJ.p4.pt(), LJ.p4.eta(), LJ.p4.phi(), LJ.p4.energy()))
            for i, (t, pt, eta, phi, e) in enumerate(zip(
                LJ.pfcand_type,
                LJ.pfcand_pt,
                LJ.pfcand_eta,
                LJ.pfcand_phi,
                LJ.pfcand_energy,
            )):
                print('\t[{}] {}| {:.2f}, {:.2f}, {:.2f}, {:.2f}'.format(i, t, pt, eta, phi, e))
            if LJ.isEgmType():
                print('\tphotonIdx:', [i for i in LJ.pfcand_photonIdx])
                for idx in LJ.pfcand_photonIdx:
                    gamma = event.photons[idx]
                    print('\t({}) {:.2f}, {}'.format(idx,
                        gamma.p4.pt(),
                        gamma.hasPixelSeed,
                    ))
        print('LJ pair mass {:.2f}, |dPhi| {:.2f}'.format(
            (LJ0.p4+LJ1.p4).M(), abs(DeltaPhi(LJ0.p4, LJ1.p4))
        ))
        print('--')
        for i, g in enumerate(event.photons):
            print(i, g.p4.pt(), g.hasPixelSeed)



histCollection=[]