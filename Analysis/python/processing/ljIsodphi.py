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
        # for lj in [LJ0, LJ1]:
        #     if lj.isMuonType() and lj.minTkD0()<0.1: return

        for chan in ['2mu2e', '4mu']:
            if aux['channel'] == chan:
                if '{}/isodphi'.format(chan) in self.Histos:
                    self.Histos['{}/isodphi'.format(chan)]['x'].append( abs(DeltaPhi(LJ0.p4, LJ1.p4)) )
                    self.Histos['{}/isodphi'.format(chan)]['y'].append( max([LJ0.pfiso(), LJ1.pfiso()]) )
                if '{}/invmdphi'.format(chan) in self.Histos:
                    self.Histos['{}/invmdphi'.format(chan)]['x'].append( abs(DeltaPhi(LJ0.p4, LJ1.p4)) )
                    self.Histos['{}/invmdphi'.format(chan)]['y'].append( (LJ0.p4+LJ1.p4).M() )


graphCollection = [
    {
        'name': 'isodphi',
        'title': ';|#Delta#phi_{LJ}|;maxIso',
        'xlim': (0, ROOT.Math.Pi()),
        'ymax': {'2mu2e': 1, '4mu': 1},
    },
    # {
    #     'name': 'invmdphi',
    #     'title': ';|#Delta#phi_{LJ}|;M_{LJ0,LJ1}[GeV]',
    #     'xlim': (0, ROOT.Math.Pi()),
    # }
]


# ________________________________________________________
### data
DataHists = {}
_files = []
for ds in dataDS: _files.extend(dataDS[ds])
events_ = MyEvents(files=_files, type='DATA')
for chan in ['2mu2e', '4mu']:
    for g in graphCollection:
        events_.Histos['{}/{}'.format(chan, g['name'])] = {'x': [], 'y': []}
events_.process()
DataHists = events_.histos
log.info('data done')

# ________________________________________________________
sampleSig = 'mXX-150_mA-0p25_lxy-300|mXX-500_mA-1p2_lxy-300|mXX-800_mA-5_lxy-300'.split('|')
sampleSig.extend( 'mXX-100_mA-5_lxy-0p3|mXX-1000_mA-0p25_lxy-0p3'.split('|') )

### signal 4mu
SigHists4mu = {}
for ds in sampleSig:
    events_ = MyEvents(files=sigDS_4mu[ds], type='MC')
    for g in graphCollection:
        events_.Histos['4mu/{}'.format(g['name'])] = {'x': [], 'y': []}
    events_.process()
    SigHists4mu[ds] = events_.Histos

### signal 2mu2e
SigHists2mu2e = {}
for ds in sampleSig:
    events_ = MyEvents(files=sigDS_2mu2e[ds], type='MC')
    for g in graphCollection:
        events_.Histos['2mu2e/{}'.format(g['name'])] = {'x': [], 'y': []}
    events_.process()
    SigHists2mu2e[ds] = events_.Histos
log.info('signal done.')



from rootpy.plotting.style import set_style
set_style(MyStyle())

from rootpy.io import root_open
import os

outname = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/{}.root'.format(__file__.split('.')[0]))
log.info('saving to {}'.format(outname))

f = root_open(outname, 'recreate')
c = ROOT.Canvas()


for chan in ['2mu2e', '4mu']:
    if chan == '2mu2e':
        SigHists = SigHists2mu2e
        mc = 'red'
    if chan =='4mu':
        SigHists = SigHists4mu
        mc = 'blue'

    for g in graphCollection:
        z = zip(DataHists['{}/{}'.format(chan, g['name'])]['x'], DataHists['{}/{}'.format(chan, g['name'])]['y'])
        graph = ROOT.Graph(len(z), name='data__{}__{}'.format(chan, g['name']), title=g['title'], drawstyle='AP', markersize=0.2)
        for i, (x, y) in enumerate(z):
            graph.SetPoint(i, x, y)
        if 'ymax' in g:
            ymax = g['ymax']
            if isinstance(g['ymax'], dict):
                ymax = g['ymax'][chan]
            graph.GetHistogram().SetMaximum(ymax)
        if 'xlim' in g:
            graph.xaxis.SetLimits(*g['xlim'])
        graph.Write()


    for ds in SigHists:
        for g in graphCollection:
            z = zip(SigHists[ds]['{}/{}'.format(chan, g['name'])]['x'], SigHists[ds]['{}/{}'.format(chan, g['name'])]['y'])
            graph = ROOT.Graph(len(z), name='{}__{}__{}'.format(ds, chan, g['name']), title=g['title'], drawstyle='AP', markersize=0.2, markercolor=mc)
            for i, (x, y) in enumerate(z):
                graph.SetPoint(i, x, y)
            if 'ymax' in g:
                ymax = g['ymax']
                if isinstance(g['ymax'], dict):
                    ymax = g['ymax'][chan]
                graph.GetHistogram().SetMaximum(ymax)
            if 'xlim' in g:
                graph.xaxis.SetLimits(*g['xlim'])
            graph.Write()




f.Close()
log.info('done.')
