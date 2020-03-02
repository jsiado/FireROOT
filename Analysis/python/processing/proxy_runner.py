#!/usr/bin/env python
from __future__ import print_function
import argparse
import math
import os, sys

from FireROOT.Analysis.Utils import *
from FireROOT.Analysis.DatasetMapLoader import (
    ProxyEventsBkgDatasetMapLoader,
    ProxyEventsSigDatasetMapLoader,
    ProxyEventsDataDatasetMapLoader
)

from rootpy.io import root_open
from rootpy.logger import log
log = log[__name__]


## parser
parser = argparse.ArgumentParser(description="proxy runner.")
parser.add_argument("--dataset", "-d",  type=str, nargs='*',default='all', help='dataset type')
parser.add_argument("--module", "-m", type=str, help='module path')
parser.add_argument("--outname", "-o", type=str, default=None, help='output ROOT file name')
parser.add_argument("--maxevents", "-n", type=int, default=-1, help='max number of events to run')
parser.add_argument("--create", "-c", type=str, default='recreate', choices=['recreate', 'update'], help='update output by')
args = parser.parse_args()

def args_sanity(args):
    ## dataset
    bkg, sig, data = False, False, False
    if isinstance(args.dataset, str) or 'all' in args.dataset:
        bkg, sig, data = True, True, True
    elif 'mc' in args.dataset:
        bkg, sig = True, True
    elif 'bkg' in args.dataset: bkg = True
    elif 'sig' in args.dataset: sig = True
    elif 'data' in args.dataset: data = True

    ## module
    moduleBase = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/processing/proxy')
    allmodules = [fn.split('.')[0] for fn in os.listdir(moduleBase) if not fn.startswith('_') and fn.endswith('.py')]
    if args.module not in allmodules:
        sys.exit('Available modules: {}'.format(str(allmodules)))

    return bkg, sig, data

runbkg, runsig, rundata = args_sanity(args)
imp = __import__('FireROOT.Analysis.processing.proxy.{}'.format(args.module), fromlist=['MyEvents', 'histCollection'])



if __name__ == '__main__':

    outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/')
    if not os.path.isdir(outdir): os.makedirs(outdir)
    if args.outname:
        outname = os.path.join(outdir, '{}.root'.format(args.outname))
    else:
        outname = os.path.join(outdir, '{}.root'.format(args.module))
    if args.create == 'update' and not os.path.isfile(outname):
        sys.exit('UPDATE was used not file not recreated yet.')

    if runbkg:
        PROXYDIR = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/samples/merged/proxy')
        bdml = ProxyEventsBkgDatasetMapLoader(proxydir=PROXYDIR)
        bkgDS, bkgMAP, bkgSCALE = bdml.fetch()

        BkgHists = {}
        for ds, files in bkgDS.items():
            events_ = imp.MyEvents(files=files, type='MC', maxevents=args.maxevents)
            events_.setScale(bkgSCALE[ds])
            for chan in events_.channel:
                for hinfo in imp.histCollection:
                    events_.bookHisto('{}/{}'.format(chan, hinfo['name']),
                            ROOT.Hist(*hinfo['binning'], title=hinfo['title'],
                                drawstyle='hist', fillstyle='solid', linewidth=0, legendstyle='F')
                            )
            events_.process()
            BkgHists[ds] = events_.histos
        log.info('background MC done')

    if runsig:
        sdml = ProxyEventsSigDatasetMapLoader()
        sigDS_2mu2e, sigSCALE_2mu2e = sdml.fetch('2mu2e')
        sigDS_4mu, sigSCALE_4mu = sdml.fetch('4mu')


        sampleSig = 'mXX-150_mA-0p25_lxy-300|mXX-500_mA-1p2_lxy-300|mXX-800_mA-5_lxy-300'.split('|')
        sampleSig.extend( 'mXX-100_mA-5_lxy-0p3|mXX-1000_mA-0p25_lxy-0p3'.split('|') )
        
        ### signal 4mu
        SigHists4mu = {}
        for ds in sampleSig:
            events_ = imp.MyEvents(files=sigDS_4mu[ds], type='MC', maxevents=args.maxevents, channel=['4mu',])
            events_.setScale(sigSCALE_4mu[ds])
            for hinfo in imp.histCollection:
                events_.bookHisto('4mu/{}'.format(hinfo['name']),
                        ROOT.Hist(*hinfo['binning'], name='{}__4mu__{}'.format(ds, hinfo['name']),
                            title=hinfo['title'], drawstyle='hist', legendstyle='L')
                        )
            events_.process()
            SigHists4mu[ds] = events_.histos
        
        ### signal 2mu2e
        SigHists2mu2e = {}
        for ds in sampleSig:
            events_ = imp.MyEvents(files=sigDS_2mu2e[ds], type='MC', maxevents=args.maxevents, channel=['2mu2e',])
            events_.setScale(sigSCALE_2mu2e[ds])
            for hinfo in imp.histCollection:
                events_.bookHisto('2mu2e/{}'.format(hinfo['name']),
                        ROOT.Hist(*hinfo['binning'], name='{}__2mu2e__{}'.format(ds, hinfo['name']),
                            title=hinfo['title'], drawstyle='hist', legendstyle='L')
                        )
            events_.process()
            SigHists2mu2e[ds] = events_.histos
        log.info('signal MC done')

    if rundata:
        PROXYDIR = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/samples/merged/proxy')
        ddml = ProxyEventsDataDatasetMapLoader(proxydir=PROXYDIR)
        dataDS, dataMAP = ddml.fetch()

        DataHists = {}
        _files = []
        for ds in dataDS:
            if isinstance(dataDS[ds], str): _files.append(dataDS[ds])
            else: _files.extend(dataDS[ds])
        events_ = imp.MyEvents(files=_files, type='DATA', maxevents=args.maxevents, channel=['2mu2e', '4mu'])
        for chan in events_.channel:
            for hinfo in imp.histCollection:
                events_.bookHisto('{}/{}'.format(chan, hinfo['name']),
                        ROOT.Hist(*hinfo['binning'], name='data__{}__{}'.format(chan, hinfo['name']),
                            title=hinfo['title'], drawstyle='hist e1', legendstyle='LEP')
                        )
        events_.process()
        DataHists = events_.histos
        log.info('data done')


    
    log.info('saving to {}'.format(outname))
    
    f = root_open(outname, args.create)
    if runsig:
        try:
            f.mkdir('ch4mu/sig', recurse=True)
            f.mkdir('ch2mu2e/sig', recurse=True)
        except:
            pass
        f.ch4mu.sig.cd()
        for hs in SigHists4mu.values():
            for h in hs.values():
                h.name = h.name.replace('4mu__', '')
                if args.create=='update': h.Write('', ROOT.TObject.kOverwrite)
                else: h.Write()
        f.ch2mu2e.sig.cd()
        for hs in SigHists2mu2e.values():
            for h in hs.values():
                h.name = h.name.replace('2mu2e__', '')
                if args.create=='update': h.Write('', ROOT.TObject.kOverwrite)
                else: h.Write()

    if rundata:
        try:
            f.mkdir('ch4mu/data', recurse=True)
            f.mkdir('ch2mu2e/data', recurse=True)
        except:
            pass
        for h in DataHists.values():
            _, chan, name = h.name.split('__')
            getattr(f, 'ch{}'.format(chan)).data.cd()
            h.name = name
            if args.create=='update': h.Write('', ROOT.TObject.kOverwrite)
            else: h.Write()
    
    if runbkg:
        try:
            f.mkdir('ch4mu/bkg', recurse=True)
            f.mkdir('ch2mu2e/bkg', recurse=True)
        except:
            pass
        for chan in ['2mu2e', '4mu']:
            getattr(f, 'ch{}'.format(chan)).bkg.cd()
            for hinfo in imp.histCollection:
                histName = '{}/{}'.format(chan, hinfo['name'])
                CatHists = mergeHistsFromMapping(extractHistByName(BkgHists, histName), bkgMAP, bkgCOLORS)
                hstack = ROOT.HistStack(list(CatHists.values()), name='{}'.format(hinfo['name']), title=hinfo['title'], drawstyle='HIST')
                if args.create=='update': hstack.Write('', ROOT.TObject.kOverwrite)
                else: hstack.Write()
    f.Close()
