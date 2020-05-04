#!/usr/bin/env python
from __future__ import print_function
import os
import math
import ROOT
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas

from FireROOT.Analysis.Utils import *

proxyfn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/proxy_4mu.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/compareProxyLjD0Shape')
if not os.path.isdir(outdir): os.makedirs(outdir)

set_style(MyStyle())
canvas = Canvas()
ROOT.gPad.SetGrid()

pf = root_open(proxyfn)


d0inc = pf.ch4mu.data.muljd0inc
d0wbj = pf.ch4mu.data.muljd0
d0inc.color = sigCOLORS[0]
d0wbj.color = sigCOLORS[1]
d0inc.legendstyle='LEP'
d0wbj.legendstyle='LEP'

binnum = d0inc.axis(0).FindBin(100)
d0wbj_c = d0wbj.clone()
d0wbj_c.scale(d0inc.integral(xbin1=binnum, overflow=True) / d0wbj.integral(xbin1=binnum, overflow=True))
d0wbj_c.linestyle='dashed'
d0wbj_c.linewidth=2
d0wbj_c.drawstyle='hist'
d0wbj_c.legendstyle='L'

draw([d0inc, d0wbj, d0wbj_c], ylimits=(1e-1, 1e5), logy=True)
leg = Legend(3, pad=canvas, topmargin=0.05, margin=0.2, entryheight=0.02, entrysep=0.01, textsize=12,)
leg.AddEntry(d0inc, label='inclusive')
leg.AddEntry(d0wbj, label='N_{bjet}#geq1')
leg.AddEntry(d0wbj_c, label='N_{bjet}#geq1 (scaled)')

leg.Draw()

title = TitleAsLatex('[4#mu VR] muon-type lepton-jet min |d_{0}| shape comparison')
title.Draw()

canvas.SaveAs('{}/ch4mu_muljd0Shape.pdf'.format(outdir))
canvas.clear()

pf.close()