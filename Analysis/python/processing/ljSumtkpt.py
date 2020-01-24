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
        passCosmic = all(map(lambda lj: lj.passCosmicVeto(event), [LJ0, LJ1]))
        passIso = all(map(lambda lj: not (lj.pfiso()>=0.12), [LJ0, LJ1]))

        if not passCosmic: return

        for chan in ['2mu2e', '4mu']:
            if aux['channel'] == chan:
                if '{}/maxTkPtSum'.format(chan) in self.Histos:
                    self.Histos['{}/maxTkPtSum'.format(chan)].Fill(
                        max([LJ0.tkPtSum08, LJ1.tkPtSum08]),
                        aux['wgt']
                    )
                if '{}/minPfIso05'.format(chan) in self.Histos:
                    self.Histos['{}/minPfIso05'.format(chan)].Fill(
                        min([LJ0.pfiso(), LJ1.pfiso()]),
                        aux['wgt']
                    )
                if '{}/ljpairmass'.format(chan) in self.Histos:
                    self.Histos['{}/ljpairmass'.format(chan)].Fill(
                        (LJ0.p4+LJ1.p4).M(),
                        aux['wgt']
                    )

histCollection = [
    # {
    #     'name': 'maxTkPtSum',
    #     'binning': (50, 0, 20),
    #     'title': 'maxTkSum;max#sum p_{T} [GeV];counts/0.4GeV',
    # },
    {
        'name': 'minPfIso05',
        'binning': (50, 0, 0.5),
        'title': 'minIso;minIso_{LJ};counts/0.01',
    },
    # {
    #     'name': 'ljpairmass',
    #     'binning': (50, 0, 200),
    #     'title': 'lepton-jet pair mass;M_{LJ0,LJ1}[GeV];counts/4GeV'
    # }
]

### backgrounds
BkgHists = {}
for ds, files in bkgDS.items():
    events_ = MyEvents(files=files, type='MC')
    events_.setScale(bkgSCALE[ds])
    for chan in ['2mu2e', '4mu']:
        for hinfo in histCollection:
            events_.bookHisto('{}/{}'.format(chan, hinfo['name']), ROOT.Hist(*hinfo['binning'], title=hinfo['title'], drawstyle='hist', fillstyle='solid', linewidth=0, legendstyle='F'))
    events_.process()
    BkgHists[ds] = events_.histos
log.info('background MC done')

# ________________________________________________________
sampleSig = 'mXX-150_mA-0p25_lxy-300|mXX-500_mA-1p2_lxy-300|mXX-800_mA-5_lxy-300'.split('|')
sampleSig.extend( 'mXX-100_mA-5_lxy-0p3|mXX-1000_mA-0p25_lxy-0p3'.split('|') )

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

# ________________________________________________________
### data
DataHists = {}
_files = []
for ds in dataDS: _files.extend(dataDS[ds])
events_ = MyEvents(files=_files, type='DATA')
for chan in ['2mu2e', '4mu']:
    for hinfo in histCollection:
        events_.bookHisto('{}/{}'.format(chan, hinfo['name']), ROOT.Hist(*hinfo['binning'], name='data__{}__{}'.format(chan, hinfo['name']), title=hinfo['title'], drawstyle='hist e1', legendstyle='LEP'))
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

for chan in ['2mu2e', '4mu']:
    for hinfo in histCollection:
        histName = '{}/{}'.format(chan, hinfo['name'])
        CatHists = mergeHistsFromMapping(extractHistByName(BkgHists, histName), bkgMAP, bkgCOLORS)
        hstack = ROOT.HistStack(list(CatHists.values()), name='bkgs__{}__{}'.format(chan, hinfo['name']), title=hinfo['title'], drawstyle='HIST')
        hstack.Write()

f.Close()

log.info('done.')