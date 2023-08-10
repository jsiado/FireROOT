#!/usr/bin/env python
import math
from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *


class MyEvents(SignalEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']

        gmus = [p for p in event.gens \
            if abs(p.pid)==13 \
                and p.p4.pt()>10\
                and abs(p.p4.eta())<2.4\
                and p.vtx.Rho()<700]
        #if len(gmus)<2: return
        self.Histos['%s/ngen'%chan].Fill(len(gmus))




histCollection = [
    {
        'name': 'ngen',
        'binning': (6, -0.5, 5.5),
        'title': 'Number of gen muons per event;N muons;Events'
    },
    ]
