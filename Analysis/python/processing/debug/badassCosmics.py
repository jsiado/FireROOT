#!/usr/bin/env python
from __future__ import print_function
import math
import ROOT

from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *
class MyEvents(CosmicEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        flag = False
        if aux['hasCosmicShower'] and self.Type=='DATA': flag=True
        if not aux['hasCosmicShower'] and self.Type!='DATA': flag=True
        if flag is False: return

        chan = aux['channel']
        LJ0, LJ1 = aux['lj0'], aux['lj1']

        _run, _lumi, _event = event.run, event.lumi, event.event
        tag = '{} {} {}'.format(_run, _lumi, _event)

        if tag not in [
            '319579 326 434769445',
        ]: return

        print((tag+' - '+chan).center(80, '#'))

        for ij, LJ in enumerate([LJ0, LJ1]):

            print('<LJ{}> type: {}| pT {:.2f}, eta {:.2f}, phi {:.2f}, energy {:.2f}'.format(
                ij, LJ.type(), LJ.p4.pt(), LJ.p4.eta(), LJ.p4.phi(), LJ.p4.energy()))
            if LJ.isMuonType():
                print('\t\tmind0 {:.2f}, tktkdca {:.2f} passCosmicVeto {}'.format(LJ.pfcand_tkD0Min*1e4, LJ.minTwoTrackDist(), LJ.passCosmicVeto(event)))
            for i, (t, pt, eta, phi, e) in enumerate(zip(
                LJ.pfcand_type,
                LJ.pfcand_pt,
                LJ.pfcand_eta,
                LJ.pfcand_phi,
                LJ.pfcand_energy,
            )):
                print('\t[{}] {}| {:.2f}, {:.2f}, {:.2f}, {:.2f}'.format(i, t, pt, eta, phi, e))

        print('LJ pair mass {:.2f}, |dPhi| {:.2f}'.format(
            (LJ0.p4+LJ1.p4).M(), abs(DeltaPhi(LJ0.p4, LJ1.p4))
        ))
        print('--')

histCollection=[]