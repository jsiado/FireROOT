#!/usr/bin/env python
from __future__ import print_function
import os
from collections import OrderedDict
from rootpy.io import root_open
import pandas as pd

from FireROOT.Analysis.Utils import *

fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/myworkflow.root')
f = root_open(fn)

rawevents = OrderedDict()

for sigtag in sigTAGS:
    entries = {}
    h=getattr(f.ch4mu.sig, sigtag).rawevents
    entries['4mu']=h.GetBinContent(1)
    h=getattr(f.ch2mu2e.sig, sigtag).rawevents
    entries['2mu2e']=h.GetBinContent(1)
    rawevents[sigtag] = entries

df = pd.DataFrame(rawevents)

print(df.T)

cutflowlabels = None
cutflownumbers = OrderedDict()
for sigtag in sigTAGS:
    entries = OrderedDict()
    h=getattr(f.ch4mu.sig, sigtag).cutflow
    _cutflowlabels = []
    for i in range(1,9):
        _cutflowlabels.append(h.xaxis.GetBinLabel(i))
        entries[h.xaxis.GetBinLabel(i)] = h.GetBinContent(i)
    if cutflowlabels is None: cutflowlabels = _cutflowlabels
    cutflownumbers[sigtag]=entries
df = pd.DataFrame(cutflownumbers)
print('--- 4mu')
print(df.T[cutflowlabels])

cutflowlabels = None
cutflownumbers = OrderedDict()
for sigtag in sigTAGS:
    entries = OrderedDict()
    h=getattr(f.ch2mu2e.sig, sigtag).cutflow
    _cutflowlabels = []
    for i in range(1,9):
        _cutflowlabels.append(h.xaxis.GetBinLabel(i))
        entries[h.xaxis.GetBinLabel(i)] = h.GetBinContent(i)
    if cutflowlabels is None: cutflowlabels = _cutflowlabels
    cutflownumbers[sigtag]=entries
df = pd.DataFrame(cutflownumbers)
print('--- 2mu2e')
print(df.T[_cutflowlabels])

f.close()