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

def formatABCD(h, isdata=False):
    a = '{:.3E}'.format(h.GetBinContent(2,2))
    b = '{:.3E}'.format(h.GetBinContent(2,1))
    c = '{:.3E}'.format(h.GetBinContent(1,2))
    d = '{:.3E}'.format(h.GetBinContent(1,1))

    """
    c | a
    -----
    d | b
    """

    res = 'C:{} | A:{}'.format(c, a)
    res += '\n'+len(res)*'-'+'\n'
    res += 'D:{} | B:{}'.format(d, b)
    res += '\n'

    if isdata:
        res = '\n'.join([
            'C:{} | A:{}'.format(c, 'BLINDED'),
            '-'*25,
            'D:{} | B:{}'.format(d, b),
        ])

    return res



class MyEvents(Events):
    def __init__(self, files=None, type='MC'):
        super(MyEvents, self).__init__(files=files, type=type)

    def processEvent(self, event, aux):
        LJ0, LJ1 = aux['lj0'], aux['lj1']
        passCosmic = all(map(lambda lj: lj.passCosmicVeto(event), [LJ0, LJ1]))

        if not passCosmic: return
        for lj in [LJ0, LJ1]:
            if lj.isMuonType() and lj.minTkD0()<0.1: return

        for chan in ['2mu2e', '4mu']:
            if aux['channel'] == chan:
                if '{}/ABCD'.format(chan) in self.Histos:
                    self.Histos['{}/ABCD'.format(chan)].Fill( abs(DeltaPhi(LJ0.p4, LJ1.p4)),
                                                              1-min([LJ0.pfiso(), LJ1.pfiso()]), aux['wgt'])
                if '{}/ABCD0w'.format(chan) in self.Histos:
                    self.Histos['{}/ABCD0w'.format(chan)].Fill( abs(DeltaPhi(LJ0.p4, LJ1.p4)),
                                                              1-min([LJ0.pfiso(), LJ1.pfiso()]) )

# ________________________________________________________
sampleSig = 'mXX-150_mA-0p25_lxy-300|mXX-500_mA-1p2_lxy-300|mXX-800_mA-5_lxy-300'.split('|')
sampleSig.extend( 'mXX-100_mA-5_lxy-0p3|mXX-1000_mA-0p25_lxy-0p3'.split('|') )

from collections import OrderedDict
### signal 4mu
SigHists4mu = OrderedDict()
for ds in sampleSig:
    events_ = MyEvents(files=sigDS_4mu[ds], type='MC')
    events_.setScale(sigSCALE_4mu[ds])
    events_.Histos['4mu/ABCD'] = ROOT.Hist2D([0, M_PI/2, M_PI], [0, 0.9, 1])
    events_.process()
    SigHists4mu[ds] = events_.Histos

### signal 2mu2e
SigHists2mu2e = OrderedDict()
for ds in sampleSig:
    events_ = MyEvents(files=sigDS_2mu2e[ds], type='MC')
    events_.setScale(sigSCALE_2mu2e[ds])
    events_.Histos['2mu2e/ABCD'] = ROOT.Hist2D([0, M_PI/2, M_PI], [0, 0.9, 1])
    events_.process()
    SigHists2mu2e[ds] = events_.Histos

log.info('signal done.')

### backgrounds
BkgHists = {}
for ds, files in bkgDS.items():
    events_ = MyEvents(files=files, type='MC')
    events_.setScale(bkgSCALE[ds])
    for chan in ['2mu2e', '4mu']:
        events_.Histos['{}/ABCD'.format(chan)] = ROOT.Hist2D([0, M_PI/2, M_PI], [0, 0.9, 1])
        events_.Histos['{}/ABCD0w'.format(chan)] = ROOT.Hist2D([0, M_PI/2, M_PI], [0, 0.9, 1])
    events_.process()
    BkgHists[ds] = events_.histos
log.info('background MC done')


### data
DataHists = {}
_files = []
for ds in dataDS: _files.extend(dataDS[ds])
events_ = MyEvents(files=_files, type='DATA')
for chan in ['2mu2e', '4mu']:
    events_.Histos['{}/ABCD'.format(chan)] = ROOT.Hist2D([0, M_PI/2, M_PI], [0, 0.9, 1])
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

print('#'*50)
print('4mu'.center(50, ' '))
print('#'*50)
for ds in SigHists4mu:
    print(ds)
    print(formatABCD(SigHists4mu[ds]['4mu/ABCD']))
print('_'*50)
CatHists = mergeHistsFromMapping(extractHistByName(BkgHists, '4mu/ABCD'), bkgMAP, bkgCOLORS)
hstack = ROOT.HistStack(list(CatHists.values()), name='bkg__4mu', drawstyle='pfc')
hstacksum = sumHistStack(hstack)
print('Background')
print(formatABCD(hstacksum))
hstack.Write()
CatHists = mergeHistsFromMapping(extractHistByName(BkgHists, '4mu/ABCD0w'), bkgMAP, bkgCOLORS)
hstack = ROOT.HistStack(list(CatHists.values()), name='bkg__4mu0w', drawstyle='pfc')
hstack.Write()

print('_'*50)
print('Data')
print(formatABCD(DataHists['4mu/ABCD'], isdata=True))

print('\n\n')

print('#'*50)
print('2mu2e'.center(50, ' '))
print('#'*50)
for ds in SigHists2mu2e:
    print(ds)
    print(formatABCD(SigHists2mu2e[ds]['2mu2e/ABCD']))
print('_'*50)
CatHists = mergeHistsFromMapping(extractHistByName(BkgHists, '2mu2e/ABCD'), bkgMAP, bkgCOLORS)
hstack = ROOT.HistStack(list(CatHists.values()), name='bkg__2mu2e', drawstyle='pfc')
hstacksum = sumHistStack(hstack)
print('Background')
print(formatABCD(hstacksum))
hstack.Write()
CatHists = mergeHistsFromMapping(extractHistByName(BkgHists, '2mu2e/ABCD0w'), bkgMAP, bkgCOLORS)
hstack = ROOT.HistStack(list(CatHists.values()), name='bkg__2mu2e0w', drawstyle='pfc')
hstack.Write()

print('_'*50)
print('Data')
print(formatABCD(DataHists['2mu2e/ABCD'], isdata=True))

f.Close()
log.info('done.')