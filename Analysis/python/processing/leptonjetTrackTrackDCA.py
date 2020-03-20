#!/usr/bin/env python

reminder='''\
you need to comment out
`if self.minTwoTrackDist()>=50: return False`
in `LeptonJetMix.passSelection(event)` method first
to make the output plot useful

IF YOU DO THIS, remember to un-comment out back when you are done.
'''

from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *

class MyEvents(Events):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu']):
        super(MyEvents, self).__init__(files=files,
                                       type=type, maxevents=maxevents, channel=channel)

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel:
            return
        chan = aux['channel']
        LJ0, LJ1 = aux['lj0'], aux['lj1']
        for lj in [LJ0, LJ1]:

            if lj.minTwoTrackDist()<0: continue ## meaning <2 tracks
            self.Histos['{}/tktkdca'.format(chan)].Fill(lj.minTwoTrackDist(), aux['wgt'])

print(reminder)

histCollection = [
    {
        'name': 'tktkdca',
        'binning': (50, 0, 100),
        'title': 'Lepton-jet min track-track DCA;D.C.A [cm];counts/2cm',
    },
]
