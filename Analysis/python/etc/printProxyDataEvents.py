#!/usr/bin/env python
from __future__ import print_function
import os
from collections import OrderedDict
from rootpy.io import root_open
import pandas as pd

from FireROOT.Analysis.Utils import *

fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/proxy_4mu.root')
f = root_open(fn)

entries = OrderedDict()
h=f.ch4mu.data.cutflow
for i in range(1,10):
    entries[h.xaxis.GetBinLabel(i)] = h.GetBinContent(i)
df = pd.Series(entries)
print('--- 4mu')
print(df)
f.close()