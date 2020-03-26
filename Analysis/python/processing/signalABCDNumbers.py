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


pointsToScan = [1, 0.1, 0.05, 0.01]
requireChargedLj = False
## print out global variables
print("Points to scan:", pointsToScan)
print("Charged Lepton-jets only:", requireChargedLj)

class MyEvents(Events):
    def __init__(self, files=None, type='MC', **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, **kwargs)

    def processEvent(self, event, aux):
        LJ0, LJ1 = aux['lj0'], aux['lj1']
        passCosmic = all(map(lambda lj: lj.passCosmicVeto(event), [LJ0, LJ1]))

        if not passCosmic: return

        metric_ = []
        for lj in [LJ0, LJ1]:
            if lj.isMuonType():
                metric_.append( lj.minTkD0() )
        metric = max(metric_)*10 # mm

        for chan in ['2mu2e', '4mu']:
            if aux['channel'] == chan:
                if '{}/ABCD'.format(chan) in self.Histos:
                    self.Histos['{}/ABCD'.format(chan)].Fill( abs(DeltaPhi(LJ0.p4, LJ1.p4)),
                                                              1-max([LJ0.pfiso(), LJ1.pfiso()]), aux['wgt'])
                if '{}/ABCD0w'.format(chan) in self.Histos:
                    self.Histos['{}/ABCD0w'.format(chan)].Fill( abs(DeltaPhi(LJ0.p4, LJ1.p4)),
                                                              1-max([LJ0.pfiso(), LJ1.pfiso()]) )
                for metricval in pointsToScan:
                    name_ = '{}/ABCD/{}'.format(chan, str(metricval).replace('.', 'p'))
                    if name_ in self.Histos and metric>metricval:
                        self.Histos[name_].Fill( abs(DeltaPhi(LJ0.p4, LJ1.p4)),
                                                1-max([LJ0.pfiso(), LJ1.pfiso()]), aux['wgt'])


# ________________________________________________________
sampleSig = 'mXX-150_mA-0p25_lxy-300|mXX-500_mA-1p2_lxy-300|mXX-800_mA-5_lxy-300'.split('|')
sampleSig.extend( 'mXX-100_mA-5_lxy-0p3|mXX-1000_mA-0p25_lxy-0p3'.split('|') )

from collections import OrderedDict
### signal 4mu
SigHists4mu = OrderedDict()
for ds in sampleSig:
    events_ = MyEvents(files=sigDS_4mu[ds], type='MC', chargedlj=requireChargedLj)
    events_.setScale(sigSCALE_4mu[ds])
    events_.Histos['4mu/ABCD'] = ROOT.Hist2D([0, M_PI/2, M_PI], [0, 0.85, 1], name=ds+'__4mu')
    for v in pointsToScan:
        name_ = '4mu/ABCD/{}'.format(str(v).replace('.', 'p'))
        events_.Histos[name_] = ROOT.Hist2D([0, M_PI/2, M_PI], [0, 0.85, 1], name='{}__4mu__{}'.format(ds, str(v).replace('.', 'p')))
    events_.process()
    SigHists4mu[ds] = events_.Histos

### signal 2mu2e
SigHists2mu2e = OrderedDict()
for ds in sampleSig:
    events_ = MyEvents(files=sigDS_2mu2e[ds], type='MC', chargedlj=requireChargedLj)
    events_.setScale(sigSCALE_2mu2e[ds])
    events_.Histos['2mu2e/ABCD'] = ROOT.Hist2D([0, M_PI/2, M_PI], [0, 0.9, 1], name=ds+'__2mu2e')
    for v in pointsToScan:
        name_ = '2mu2e/ABCD/{}'.format(str(v).replace('.', 'p'))
        events_.Histos[name_] = ROOT.Hist2D([0, M_PI/2, M_PI], [0, 0.9, 1], name='{}__2mu2e__{}'.format(ds, str(v).replace('.', 'p')))
    events_.process()
    SigHists2mu2e[ds] = events_.Histos

log.info('signal done.')



def maxIsoBoundary(ch):
    """different boundary value for different channel"""
    if ch == '2mu2e': return 0.9
    if ch == '4mu': return 0.85




### backgrounds
BkgHists = {}
for ds, files in bkgDS.items():
    events_ = MyEvents(files=files, type='MC', chargedlj=requireChargedLj)
    events_.setScale(bkgSCALE[ds])
    for chan in ['2mu2e', '4mu']:
        events_.Histos['{}/ABCD'.format(chan)] = ROOT.Hist2D([0, M_PI/2, M_PI], [0, maxIsoBoundary(chan), 1])
        events_.Histos['{}/ABCD0w'.format(chan)] = ROOT.Hist2D([0, M_PI/2, M_PI], [0, maxIsoBoundary(chan), 1])
        for v in pointsToScan:
            name_ = '{}/ABCD/{}'.format(chan, str(v).replace('.', 'p'))
            events_.Histos[name_] = ROOT.Hist2D([0, M_PI/2, M_PI], [0, maxIsoBoundary(chan), 1])
    events_.process()
    BkgHists[ds] = events_.histos
log.info('background MC done')


### data
DataHists = {}
_files = []
for ds in dataDS: _files.extend(dataDS[ds])
events_ = MyEvents(files=_files, type='DATA', chargedlj=requireChargedLj)
for chan in ['2mu2e', '4mu']:
    events_.Histos['{}/ABCD'.format(chan)] = ROOT.Hist2D([0, M_PI/2, M_PI], [0, maxIsoBoundary(chan), 1], name='data__{}'.format(chan))
    for v in pointsToScan:
        name_ = '{}/ABCD/{}'.format(chan, str(v).replace('.', 'p'))
        events_.Histos[name_] = ROOT.Hist2D([0, M_PI/2, M_PI], [0, maxIsoBoundary(chan), 1], name='data__{}__{}'.format(chan, str(v).replace('.', 'p')))

events_.process()
DataHists = events_.histos
log.info('data done')


from rootpy.plotting.style import set_style
set_style(MyStyle())

from rootpy.io import root_open
import os

outname = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/{}.root'.format(__file__.split('.')[0]))
log.info('saving to {}'.format(outname))

f = root_open(outname, 'recreate')


for ds, hs in SigHists4mu.items():
    hs['4mu/ABCD'].Write()
    for v in pointsToScan:
        name_ = '4mu/ABCD/{}'.format(str(v).replace('.', 'p'))
        hs[name_].Write()

CatHists = mergeHistsFromMapping(extractHistByName(BkgHists, '4mu/ABCD'), bkgMAP, bkgCOLORS)
hstack = ROOT.HistStack(list(CatHists.values()), name='bkg__4mu', drawstyle='pfc')
hstacksum = sumHistStack(hstack)
hstack.Write()
for v in pointsToScan:
    vstr = str(v).replace('.', 'p')
    CatHists = mergeHistsFromMapping(extractHistByName(BkgHists, '4mu/ABCD/'+vstr), bkgMAP, bkgCOLORS)
    hstack = ROOT.HistStack(list(CatHists.values()), name='bkg__4mu__'+vstr, drawstyle='pfc')
    hstacksum = sumHistStack(hstack)
    hstack.Write()
CatHists = mergeHistsFromMapping(extractHistByName(BkgHists, '4mu/ABCD0w'), bkgMAP, bkgCOLORS)
hstack = ROOT.HistStack(list(CatHists.values()), name='bkg__4mu0w', drawstyle='pfc')
hstack.Write()

DataHists['4mu/ABCD'].Write()
for v in pointsToScan:
    vstr = str(v).replace('.', 'p')
    DataHists['4mu/ABCD/'+vstr].Write()

for ds, hs in SigHists2mu2e.items():
    hs['2mu2e/ABCD'].Write()
    for v in pointsToScan:
        name_ = '2mu2e/ABCD/{}'.format(str(v).replace('.', 'p'))
        hs[name_].Write()

CatHists = mergeHistsFromMapping(extractHistByName(BkgHists, '2mu2e/ABCD'), bkgMAP, bkgCOLORS)
hstack = ROOT.HistStack(list(CatHists.values()), name='bkg__2mu2e', drawstyle='pfc')
hstacksum = sumHistStack(hstack)
hstack.Write()
for v in pointsToScan:
    vstr = str(v).replace('.', 'p')
    CatHists = mergeHistsFromMapping(extractHistByName(BkgHists, '2mu2e/ABCD/'+vstr), bkgMAP, bkgCOLORS)
    hstack = ROOT.HistStack(list(CatHists.values()), name='bkg__2mu2e__'+vstr, drawstyle='pfc')
    hstacksum = sumHistStack(hstack)
    hstack.Write()
CatHists = mergeHistsFromMapping(extractHistByName(BkgHists, '2mu2e/ABCD0w'), bkgMAP, bkgCOLORS)
hstack = ROOT.HistStack(list(CatHists.values()), name='bkg__2mu2e0w', drawstyle='pfc')
hstack.Write()

DataHists['2mu2e/ABCD'].Write()
for v in pointsToScan:
    vstr = str(v).replace('.', 'p')
    DataHists['2mu2e/ABCD/'+vstr].Write()

f.Close()
log.info('done.')