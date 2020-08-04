#!/usr/bin/env python
from __future__ import print_function
import os
from collections import OrderedDict
from rootpy.io import root_open

from FireROOT.Analysis.Utils import *

fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/isolationStudy.root')

f = root_open(fn)

def routine(chan, varname):
    counts = OrderedDict()
    chandir = getattr(f, 'ch'+chan)
    for it, sigtag in enumerate(sigTAGS):
        h = getattr(getattr(chandir.sig, sigtag), varname) # Hist
        h_total = h.integral(overflow=True)
        counts[sigtag] = h_total

    print('>',chan, varname)
    maxlen = max([len(k) for k in counts])
    for k in counts:
        fmt = '{:%d}:{:.3f}'%(maxlen+2)
        print(fmt.format(k, counts[k]))

routine('2mu2e', 'egmljcorriso')
routine('2mu2e', 'egmljcorriso_d0')
routine('4mu', 'maxcorriso')
routine('4mu', 'maxcorriso_d0')

f.close()