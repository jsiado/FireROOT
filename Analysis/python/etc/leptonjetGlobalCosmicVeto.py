#!/usr/bin/env python
from __future__ import print_function
import os, ROOT
from rootpy.io import root_open

from FireROOT.Analysis.Utils import *

fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/modules/leptonjetTrackTrackDCA.root')
f=root_open(fn)

def routine(chan):
    chandir = getattr(f, 'ch'+chan)

    effs_ = []
    for it, sigtag in enumerate(sigTAGS):
        h = getattr(getattr(chandir.sig, sigtag), 'grandcosmicvetores')
        NTotal, NPass = h.GetBinContent(1), h.GetBinContent(2)
        print(sigtag, '  {:.2f}/{:.2f} {:.2f}%'.format(NPass, NTotal, float(NPass)*100./NTotal) )
        effs_.append( float(NPass)*100./NTotal )
    print( 'sig_ave', '  {:.2f}%'.format(sum(effs_)/len(effs_)) )
    print( 'sig_min', '  {:.2f}%'.format(min(effs_)) )

    h = getattr(chandir.data, 'grandcosmicvetores')
    NTotal, NPass = h.GetBinContent(1), h.GetBinContent(2)
    print('cosmic', '  {:.2f}/{:.2f} {:.2f}%'.format(NPass, NTotal, float(NPass)*100./NTotal) )


for chan in ['2mu2e', '4mu']:
    print('>> ', chan)
    routine(chan)

f.close()