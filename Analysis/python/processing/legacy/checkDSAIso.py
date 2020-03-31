#!/usr/bin/env python
from __future__ import print_function
import math

from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *
from FireROOT.Analysis.DatasetMapLoader import DatasetMapLoader, SigDatasetMapLoader

from rootpy.logger import log
log = log[__name__]


sdml = SigDatasetMapLoader()
sigDS_2mu2e, sigSCALE_2mu2e = sdml.fetch('2mu2e')
sigDS_4mu, sigSCALE_4mu = sdml.fetch('4mu')


class MyEvents(Events):
    def __init__(self, files=None, type='MC'):
        super(MyEvents, self).__init__(files=files, type=type)

    def processEvent(self, event, aux):
        LJ0, LJ1 = aux['lj0'], aux['lj1']
        passCosmic = all(map(lambda lj: lj.passCosmicVeto(event), [LJ0, LJ1]))

        if not passCosmic: return
        for chan in ['2mu2e', '4mu']:
            if aux['channel'] == chan:
                for lj in [LJ0, LJ1]:
                    if '{}/dsaIso'.format(chan) in self.Histos:
                        for i in lj.pfcand_dsamuonIdx:
                            self.Histos['{}/dsaIso'.format(chan)].Fill(
                                event.dsamuons[i].PFIsoVal, aux['wgt']
                            )
                    if '{}/pfmuIso'.format(chan) in self.Histos:
                        for i in lj.pfcand_pfmuonIdx:
                            self.Histos['{}/pfmuIso'.format(chan)].Fill(
                                event.muons[i].isoValue, aux['wgt']
                            )

histCollection = [
    {
        'name': 'dsaIso',
        'binning': (30, 0, 0.3),
        'title': 'DSA Iso val;Iso;counts/0.01',
    },
    {
        'name': 'pfmuIso',
        'binning': (30, 0, 0.3),
        'title': 'PFMu Iso val;Iso;counts/0.01',
    },
]


# ________________________________________________________
sampleSig = ['mXX-500_mA-1p2_lxy-300']

### signal 4mu
SigHists4mu = {}
for ds in sampleSig:
    events_ = MyEvents(files=sigDS_4mu[ds], type='MC')
    events_.setScale(sigSCALE_4mu[ds])
    for hinfo in histCollection:
        events_.bookHisto('4mu/{}'.format(hinfo['name']), ROOT.Hist(*hinfo['binning'], name='{}__4mu__{}'.format(ds, hinfo['name']), title=hinfo['title'], drawstyle='hist', legendstyle='L'))
    events_.process()
    SigHists4mu[ds] = events_.histos


SigHists2mu2e = {}
for ds in sampleSig:
    events_ = MyEvents(files=sigDS_2mu2e[ds], type='MC')
    events_.setScale(sigSCALE_2mu2e[ds])
    for hinfo in histCollection:
        events_.bookHisto('2mu2e/{}'.format(hinfo['name']), ROOT.Hist(*hinfo['binning'], name='{}__2mu2e__{}'.format(ds, hinfo['name']), title=hinfo['title'], drawstyle='hist', legendstyle='L'))
    events_.process()
    SigHists2mu2e[ds] = events_.histos
log.info('signal MC done')


from rootpy.io import root_open
import os

outname = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/{}.root'.format(__file__.split('.')[0]))
log.info('saving to {}'.format(outname))



f = root_open(outname, 'recreate')
for hs in SigHists4mu.values():
    for h in hs.values():
        h.Write()
for hs in SigHists2mu2e.values():
    for h in hs.values():
        h.Write()


f.Close()

log.info('done.')