#!/usr/bin/env python
from __future__ import print_function
import os, json
import numpy as np
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas

from FireROOT.Analysis.Utils import *

fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/bjets.root')
proxyisodatafile = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/processing/proxyisoval.json')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/findProxyMuonIsoRate')
if not os.path.isdir(outdir): os.makedirs(outdir)

set_style(MyStyle())
canvas = Canvas()
ROOT.gPad.SetGrid()

f = root_open(fn)

muljiso = f.ch4mu.data.muljiso
proxyisoarr = np.array(json.load(open(proxyisodatafile)))

# for i in np.arange(1.4,1.6,0.001):
#     testh = Hist(50,0,1)
#     testh.fill_array(proxyisoarr*i)
#     val = muljiso.KolmogorovTest(testh, 'N')

#     print(i, val)

muljiso.Scale(1/muljiso.integral())
muljiso.legendstyle = 'LEP'

scaledproxyiso = muljiso.empty_clone()
scaledproxyiso.fill_array(proxyisoarr*1.53)
scaledproxyiso.Scale(1/scaledproxyiso.integral())
scaledproxyiso.color = 'red'
scaledproxyiso.title = 'proxy muon iso (#times0.765)'
scaledproxyiso.legendstyle = 'LEP'

hs = [muljiso, scaledproxyiso, ]
draw(hs)

leg = Legend(2, pad=canvas, textsize=12)
leg.AddEntry(muljiso, label='muon-type lepton-jet iso')
leg.AddEntry(scaledproxyiso, label='proxy muon iso (#times0.765)')
leg.Draw()
canvas.SaveAs('{}/scaledproxy_ljiso.pdf'.format(outdir))
f.close()