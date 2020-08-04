#!/usr/bin/env python
from __future__ import print_function
import os
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas

from FireROOT.Analysis.Utils import *


fn_proxy = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/bjets.root')
fn_signal = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/ljpairDphi.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/')
if not os.path.isdir(outdir): os.makedirs(outdir)

f_proxy = root_open(fn_proxy)
f_signal = root_open(fn_signal)

h_proxy = f_proxy.ch4mu.data.dphi_sisoinv
h_signal = f_signal.ch4mu.data.dphi_sisoInv

set_style(MyStyle())
c = Canvas()

hs = [h_proxy, h_signal]
for h in hs:
    h.legendstyle = 'LEP'
    h.Scale(1./h.Integral())

h_proxy.title = 'proxy events, lepton-jet iso>0.15'
h_proxy.color = 'blue'
h_signal.title = 'signal events, max lepton-jet iso>0.15'
h_signal.color = 'red'

legend = Legend(hs, pad=c, leftmargin=0.1, margin=0.1, entryheight=0.02, textsize=12)

xmin_, xmax_, ymin_, ymax_ = get_limits(hs)
draw(hs, pad=c, ylimits=(0, ymax_), ytitle='norm. counts/#pi/20')
legend.Draw()
c.SaveAs('{}/dphi_proxySignal_largeIso.pdf'.format(outdir))

f_proxy.close()
f_signal.close()
