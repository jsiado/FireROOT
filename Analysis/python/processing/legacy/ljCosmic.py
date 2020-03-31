#!/usr/bin/env python
from __future__ import print_function
import math

from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *
from FireROOT.Analysis.DatasetMapLoader import DatasetMapLoader, SigDatasetMapLoader

from rootpy.logger import log
log = log[__name__]

dml = DatasetMapLoader()
dataDS, dataMAP = dml.fetch('data')
bkgDS, bkgMAP, bkgSCALE = dml.fetch('bkg')

sdml = SigDatasetMapLoader()
sigDS_2mu2e, sigSCALE_2mu2e = sdml.fetch('2mu2e')
sigDS_4mu, sigSCALE_4mu = sdml.fetch('4mu')


class MyEvents(Events):
    def __init__(self, files=None, type='MC'):
        super(MyEvents, self).__init__(files=files, type=type)

    def processEvent(self, event, aux):
        LJ0, LJ1 = aux['lj0'], aux['lj1']

        for chan in ['2mu2e', '4mu']:
            if aux['channel'] != chan: continue
            for lj in [LJ0, LJ1]:
                if not lj.isMuonType(): continue
                drcosmicDSA = lj.dRcosmicDSA(event)
                drcosmicSeg = lj.dRcosmicSeg(event)
                if drcosmicDSA and 'drDSADSA-{}'.format(chan) in self.Histos:
                    self.Histos['drDSADSA-{}'.format(chan)].Fill(min(drcosmicDSA), aux['wgt'])
                if drcosmicSeg and 'drDSASeg-{}'.format(chan) in self.Histos:
                    self.Histos['drDSASeg-{}'.format(chan)].Fill(min(drcosmicSeg), aux['wgt'])


# ________________________________________________________
sampleSig = 'mXX-150_mA-0p25_lxy-300|mXX-500_mA-1p2_lxy-300|mXX-800_mA-5_lxy-300'.split('|')

### signal 4mu
SigHists4mu = {}
for ds in sampleSig:
    events_ = MyEvents(files=sigDS_4mu[ds], type='MC')
    events_.setScale(sigSCALE_4mu[ds])
    events_.bookHisto('drDSADSA-4mu', ROOT.Hist(50, 0, 1, name='DSADSA_4mu__'+ds, title=';#DeltaR_{cosmic};counts/50', drawstyle='hist', legendstyle='L'))
    events_.bookHisto('drDSASeg-4mu', ROOT.Hist(50, 0, 1, name='DSASeg_4mu__'+ds, title=';#DeltaR_{cosmic};counts/50', drawstyle='hist', legendstyle='L'))
    events_.process()
    SigHists4mu[ds] = events_.histos


SigHists2mu2e = {}
for ds in sampleSig:
    events_ = MyEvents(files=sigDS_2mu2e[ds], type='MC')
    events_.setScale(sigSCALE_2mu2e[ds])
    events_.bookHisto('drDSADSA-2mu2e', ROOT.Hist(50, 0, 1, name='DSADSA_2mu2e__'+ds, title=';#DeltaR_{cosmic};counts/50', drawstyle='hist', legendstyle='L'))
    events_.bookHisto('drDSASeg-2mu2e', ROOT.Hist(50, 0, 1, name='DSASeg_2mu2e__'+ds, title=';#DeltaR_{cosmic};counts/50', drawstyle='hist', legendstyle='L'))
    events_.process()
    SigHists2mu2e[ds] = events_.histos
log.info('signal MC done')


# ________________________________________________________
### data
DataHists = {}
_files = []
for ds in dataDS: _files.extend(dataDS[ds])
events_ = MyEvents(files=_files, type='DATA')
for chan in ['2mu2e', '4mu']:
    events_.bookHisto('drDSADSA-{}'.format(chan), ROOT.Hist(50, 0, 1, name='DSADSA_{}__data'.format(chan), title=';#DeltaR_{cosmic};counts/50', drawstyle='hist e1', legendstyle='LEP'))
    events_.bookHisto('drDSASeg-{}'.format(chan), ROOT.Hist(50, 0, 1, name='DSASeg_{}__data'.format(chan), title=';#DeltaR_{cosmic};counts/50', drawstyle='hist e1', legendstyle='LEP'))
events_.process()
DataHists = events_.histos
log.info('data done')


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
for h in DataHists.values():
    h.Write()
f.Close()

log.info('done.')