#!/usr/bin/env python
import argparse, os, sys, fnmatch

from tqdm import tqdm
from FireROOT.Analysis.Utils import *
from FireROOT.Analysis.DatasetMapLoader import (
    DatasetMapLoader,
    SigDatasetMapLoader,
    CentralSignalMapLoader,
)

from rootpy.io import root_open
from rootpy.logger import log
log = log[__name__]


## parser
parser = argparse.ArgumentParser(description="module runner.")
parser.add_argument("--dataset", "-d",  type=str, nargs='*', default='mc', help='dataset type')
parser.add_argument("--sigparam", "-p",  type=str, nargs='*',default=None, help='signal parameters')
parser.add_argument("--module", "-m", type=str, help='module path')
parser.add_argument("--outname", "-o", type=str, default=None, help='output ROOT file name')
parser.add_argument("--maxevents", "-n", type=int, default=-1, help='max number of events to run')
parser.add_argument("--channel", "-ch", nargs='*', default=['2mu2e', '4mu'], choices=['2mu2e', '4mu'], help='channels to run')
parser.add_argument("--create", "-c", type=str, default='recreate', choices=['recreate', 'update'], help='update output by')
parser.add_argument("--mbase", "-b", type=str, default='slimTrees', choices=['slimTrees'], help='module base name')
parser.add_argument("--private", action='store_true', help='run private signal sample')
args = parser.parse_args()

def args_sanity(args):
    ## dataset
    bkg, sig, data = False, False, False
    if isinstance(args.dataset, str) or 'all' in args.dataset:
        bkg, sig, data = True, True, True
    else:
        if 'mc' in args.dataset: bkg, sig = True, True
        if 'bkg' in args.dataset: bkg = True
        if 'sig' in args.dataset: sig = True
        if 'data' in args.dataset: data = True

    ## module
    moduleBase = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/processing/{}'.format(args.mbase))
    assert(os.path.isdir(moduleBase))

    return bkg, sig, data

runbkg, runsig, rundata = args_sanity(args)
_modulebase = 'FireROOT.Analysis.processing.{}'.format(args.mbase)
imp = __import__('{}.{}'.format(_modulebase, args.module), fromlist=['MyEvents',])

if __name__ == '__main__':


    outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/{}/'.format(args.mbase))
    if not os.path.isdir(outdir): os.makedirs(outdir)

    if args.outname: outname = os.path.join(outdir, '{}__TREE.root'.format(args.outname))
    else:            outname = os.path.join(outdir, '{}__TREE.root'.format(args.module))
    if args.create == 'update' and not os.path.isfile(outname):
        sys.exit('UPDATE was used not file not recreated yet.')

    #################
    ### SIGNAL MC ###
    #################
    if runsig:

        ### set dataset loader
        if args.private: sdml = SigDatasetMapLoader()
        else:            sdml = CentralSignalMapLoader()

        ### set sample name
        # sampleSig = 'mXX-150_mA-0p25_lxy-300|mXX-500_mA-1p2_lxy-300|mXX-800_mA-5_lxy-300'.split('|')
        # sampleSig.extend( 'mXX-100_mA-5_lxy-0p3|mXX-1000_mA-0p25_lxy-0p3'.split('|') )
        sampleSig = []
        if args.sigparam:
            for s in args.sigparam:
                if '*' in s or '?' in s:
                    sampleSig.extend( fnmatch.filter(sdml.get_datasets('4mu').keys(), s) )
                else: sampleSig.append(s)
            sampleSig = list(set(sampleSig))

        print 'Signal samples to process:'
        print ', '.join(sampleSig)




        if '4mu' in args.channel:
            sigDS_4mu_inc, sigSCALE_4mu_inc = sdml.fetch('4mu')

            outnames = []
            for s in sampleSig:
                files, scale = sigDS_4mu_inc[s], sigSCALE_4mu_inc[s]
                _outname = outname[:-5]+'__'+s+outname[-5:]
                events_ = imp.MyEvents(files=files, type='MC', dtag=s, outname=_outname,
                                    maxevents=args.maxevents, channel=['4mu'], tqdm=True)
                events_.setScale(scale)
                events_.process()
                events_.postProcess()
                outnames.append(_outname)

        if '2mu2e' in args.channel:
            sigDS_2mu2e_inc, sigSCALE_2mu2e_inc = sdml.fetch('2mu2e')

            outnames = []
            for s in sampleSig:
                files, scale = sigDS_2mu2e_inc[s], sigSCALE_2mu2e_inc[s]
                _outname = outname[:-5]+'__'+s+outname[-5:]
                events_ = imp.MyEvents(files=files, type='MC', dtag=s, outname=_outname,
                                    maxevents=args.maxevents, channel=['2mu2e'], tqdm=True)
                events_.setScale(scale)
                events_.process()
                events_.postProcess()
                outnames.append(_outname)

        # merge them
        if len(outnames)>1:
            cmd = 'hadd -f {} {}'.format(outname, ' '.join(outnames))
            os.system(cmd)
            # remove after success merge
            for n in outnames: os.remove(n)


    else:
        raise NotImplementedError()

