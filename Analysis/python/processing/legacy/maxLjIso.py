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

        if not passCosmic: return

        isLargeIsoEvent = False
        LJs = [LJ0, LJ1]
        leadingIsoIdx = 0 if LJ0.pfiso()>LJ1.pfiso() else 1
        subleadIsoIdx = 1 - leadingIsoIdx
        for chan in ['2mu2e', '4mu']:
            if aux['channel'] == chan:
                if '{}/iso0'.format(chan) in self.Histos:
                    self.Histos['{}/iso0'.format(chan)].Fill(
                        LJs[leadingIsoIdx].pfiso(), aux['wgt']
                    )
                if LJs[leadingIsoIdx].type()==2: # DSA type
                    if '{}/iso0dsatype'.format(chan) in self.Histos:
                        self.Histos['{}/iso0dsatype'.format(chan)].Fill(
                            LJs[leadingIsoIdx].pfiso(), aux['wgt']
                        )
                    if LJs[leadingIsoIdx].nPFMu()==0 and '{}/iso0dsaonlytype'.format(chan) in self.Histos:
                        self.Histos['{}/iso0dsaonlytype'.format(chan)].Fill(
                            LJs[leadingIsoIdx].pfiso(), aux['wgt']
                        )
                else:
                    if '{}/iso0othertype'.format(chan) in self.Histos:
                        self.Histos['{}/iso0othertype'.format(chan)].Fill(
                            LJs[leadingIsoIdx].pfiso(), aux['wgt']
                        )

                if LJs[leadingIsoIdx].pfiso() > 0.2: # large band
                    if '{}/iso0largeIso0pt'.format(chan) in self.Histos:
                        self.Histos['{}/iso0largeIso0pt'.format(chan)].Fill(
                            LJs[leadingIsoIdx].p4.pt(), aux['wgt']
                        )
                    if '{}/iso0largeIso1pt'.format(chan) in self.Histos:
                        self.Histos['{}/iso0largeIso1pt'.format(chan)].Fill(
                            LJs[subleadIsoIdx].p4.pt(), aux['wgt']
                        )
                    if '{}/iso0largeIso0type'.format(chan) in self.Histos:
                        self.Histos['{}/iso0largeIso0type'.format(chan)].Fill(
                            LJs[leadingIsoIdx].type(), aux['wgt']
                        )
                    if '{}/iso0largeIso1type'.format(chan) in self.Histos:
                        self.Histos['{}/iso0largeIso1type'.format(chan)].Fill(
                            LJs[subleadIsoIdx].type(), aux['wgt']
                        )
                else: # small band
                    if '{}/iso0smallIso0pt'.format(chan) in self.Histos:
                        self.Histos['{}/iso0smallIso0pt'.format(chan)].Fill(
                            LJs[leadingIsoIdx].p4.pt(), aux['wgt']
                        )
                    if '{}/iso0smallIso1pt'.format(chan) in self.Histos:
                        self.Histos['{}/iso0smallIso1pt'.format(chan)].Fill(
                            LJs[subleadIsoIdx].p4.pt(), aux['wgt']
                        )

                for lj in LJs:
                    if lj.type()!=2: continue
                    if lj.pfiso()>0.2:

                        if not isLargeIsoEvent: isLargeIsoEvent = True
                        if '{}/dsaTypeLargeIsoEta'.format(chan) in self.Histos:
                            self.Histos['{}/dsaTypeLargeIsoEta'.format(chan)].Fill(
                                lj.p4.eta(), aux['wgt']
                            )
                        if '{}/dsaTypeLargeIsoPt'.format(chan) in self.Histos:
                            self.Histos['{}/dsaTypeLargeIsoPt'.format(chan)].Fill(
                                lj.p4.pt(), aux['wgt']
                            )
                    else:
                        if '{}/dsaTypeSmallIsoEta'.format(chan) in self.Histos:
                            self.Histos['{}/dsaTypeSmallIsoEta'.format(chan)].Fill(
                                lj.p4.eta(), aux['wgt']
                            )
                        if '{}/dsaTypeSmallIsoPt'.format(chan) in self.Histos:
                            self.Histos['{}/dsaTypeSmallIsoPt'.format(chan)].Fill(
                                lj.p4.pt(), aux['wgt']
                            )

                if isLargeIsoEvent:
                    print('{}:{}:{}'.format(event.run, event.lumi, event.event))


histCollection = [
    {
        'name': 'iso0',
        'binning': (50, 0, 1),
        'title': 'max pfIso;Iso;counts/0.02',
    },
    {
        'name': 'iso0dsatype',
        'binning': (50, 0, 1),
        'title': 'max pfIso(dsa type);Iso;counts/0.02',
    },
    {
        'name': 'iso0dsaonlytype',
        'binning': (50, 0, 1),
        'title': 'max pfIso(dsa-only type);Iso;counts/0.02',
    },
    {
        'name': 'iso0othertype',
        'binning': (50, 0, 1),
        'title': 'max pfIso(other type);Iso;counts/0.02',
    },
    {
        'name': 'iso0largeIso0pt',
        'binning': (50, 0, 500),
        'title': 'pT of leading Iso(>0.2);pT[GeV];counts/10GeV',
    },
    {
        'name': 'iso0largeIso1pt',
        'binning': (50, 0, 500),
        'title': 'pT of subleading Iso(>0.2);pT[GeV];counts/10GeV',
    },
    {
        'name': 'iso0smallIso0pt',
        'binning': (50, 0, 500),
        'title': 'pT of leading Iso(<0.2);pT[GeV];counts/10GeV',
    },
    {
        'name': 'iso0smallIso1pt',
        'binning': (50, 0, 500),
        'title': 'pT of subleading Iso(<0.2);pT[GeV];counts/10GeV',
    },
    {
        'name': 'iso0largeIso0type',
        'binning': (4, -1, 3),
        'title': 'type of leading Iso(>0.2);type;counts',
    },
    {
        'name': 'iso0largeIso1type',
        'binning': (4, -1, 3),
        'title': 'type of subleading Iso(>0.2);type;counts',
    },
    {
        'name': 'dsaTypeLargeIsoEta',
        'binning': (24, -2.4, 2.4),
        'title': '#eta of dsa-type lj (Iso>0.2);#eta;counts/0.2'
    },
    {
        'name': 'dsaTypeSmallIsoEta',
        'binning': (24, -2.4, 2.4),
        'title': '#eta of dsa-type lj (Iso<=0.2);#eta;counts/0.2'
    },
    {
        'name': 'dsaTypeLargeIsoPt',
        'binning': (50, 0, 500),
        'title': 'pT of dsa-type lj (Iso>0.2);pT [GeV];counts/0.2',
    },
    {
        'name': 'dsaTypeSmallIsoPt',
        'binning': (50, 0, 500),
        'title': 'pT of dsa-type lj (Iso<=0.2);pT [GeV];counts/0.2',
    },
]

# ________________________________________________________
sampleSig = ['mXX-500_mA-1p2_lxy-300']

# _files = """\
# root://cmseos.fnal.gov///store/group/lpcmetx/SIDM/ffNtupleV2/2018/CRAB_PrivateMC/SIDM_BsTo2DpTo4Mu_MBs-500_MDp-1p2_ctau-18/200128_171026/ffNtuple_0.root
# root://cmseos.fnal.gov///store/group/lpcmetx/SIDM/ffNtupleV2/2018/CRAB_PrivateMC/SIDM_BsTo2DpTo4Mu_MBs-500_MDp-1p2_ctau-18/200128_171026/ffNtuple_1.root
# root://cmseos.fnal.gov///store/group/lpcmetx/SIDM/ffNtupleV2/2018/CRAB_PrivateMC/SIDM_BsTo2DpTo4Mu_MBs-500_MDp-1p2_ctau-18/200128_171026/ffNtuple_2.root
# root://cmseos.fnal.gov///store/group/lpcmetx/SIDM/ffNtupleV2/2018/CRAB_PrivateMC/SIDM_BsTo2DpTo4Mu_MBs-500_MDp-1p2_ctau-18/200128_171026/ffNtuple_3.root
# root://cmseos.fnal.gov///store/group/lpcmetx/SIDM/ffNtupleV2/2018/CRAB_PrivateMC/SIDM_BsTo2DpTo4Mu_MBs-500_MDp-1p2_ctau-18/200128_171026/ffNtuple_4.root""".split()

### signal 4mu
SigHists4mu = {}
for ds in sampleSig:
    # events_ = MyEvents(files=_files, type='MC')
    events_ = MyEvents(files=sigDS_4mu[ds], type='MC')
    events_.setScale(sigSCALE_4mu[ds])
    for hinfo in histCollection:
        events_.bookHisto('4mu/{}'.format(hinfo['name']), ROOT.Hist(*hinfo['binning'], name='{}__4mu__{}'.format(ds, hinfo['name']), title=hinfo['title'], drawstyle='hist', legendstyle='L'))
    events_.process()
    SigHists4mu[ds] = events_.histos
log.info('signal 4mu done')


SigHists2mu2e = {}
for ds in sampleSig:
    events_ = MyEvents(files=sigDS_2mu2e[ds], type='MC')
    events_.setScale(sigSCALE_2mu2e[ds])
    for hinfo in histCollection:
        events_.bookHisto('2mu2e/{}'.format(hinfo['name']), ROOT.Hist(*hinfo['binning'], name='{}__2mu2e__{}'.format(ds, hinfo['name']), title=hinfo['title'], drawstyle='hist', legendstyle='L'))
    events_.process()
    SigHists2mu2e[ds] = events_.histos
log.info('signal 2mu2e done')


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