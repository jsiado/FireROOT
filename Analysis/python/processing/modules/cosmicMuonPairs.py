#!/usr/bin/env python
from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *

class MyEvents(CosmicEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files,
                                       type=type, maxevents=maxevents, channel=channel, **kwargs)
        self.Chain.define_collection('cosmicmuons', prefix='cosmicmuon_', size='cosmicmuon_n')

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        flag = False
        if aux['hasCosmicShower'] and self.Type=='DATA': flag=True
        if not aux['hasCosmicShower'] and self.Type!='DATA': flag=True
        if flag is False: return

        chan = aux['channel']
        LJ0, LJ1 = aux['lj0'], aux['lj1']

        nparallel = 0
        nparallel2 = 0
        for i, cosmic_i in enumerate(event.cosmicmuons):
            mom_i = ROOT.TVector3(cosmic_i.p4.px(), cosmic_i.p4.py(), cosmic_i.p4.pz())
            for j, cosmic_j in enumerate(event.cosmicmuons):
                if j<=i: continue
                mom_j = ROOT.TVector3(cosmic_j.p4.px(), cosmic_j.p4.py(), cosmic_j.p4.pz())
                cosalpha = mom_i.Dot(mom_j)
                cosalpha /= mom_i.Mag()*mom_j.Mag()
                if abs(cosalpha)<=0.99: continue
                nparallel+=1

                if cosmic_i.p4.pt()>2 and cosmic_j.p4.pt()>2: nparallel2+=1
        self.Histos['{}/parallelpairs'.format(chan)].Fill(nparallel, aux['wgt'])
        self.Histos['{}/parallelpairs2'.format(chan)].Fill(nparallel2, aux['wgt'])

        if nparallel2<8:
            print chan, event.run, event.lumi, event.event

histCollection = [
    {
        'name': 'parallelpairs',
        'binning': (15,0,15),
        'title': 'parallel cosmicMuon pairs;N;counts',
    },
    {
        'name': 'parallelpairs2',
        'binning': (15,0,15),
        'title': 'parallel cosmicMuon (p_{T}>2GeV) pairs;N;counts',
    },

]
