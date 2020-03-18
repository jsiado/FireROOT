#!/usr/bin/env python
from __future__ import print_function
import os
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas

from FireROOT.Analysis.Utils import *


fn_proxy = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/bjets.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/')
if not os.path.isdir(outdir): os.makedirs(outdir)

f_proxy = root_open(fn_proxy)

h_sisoinv = f_proxy.ch4mu.data.dphi_sisoinv
h_siso = f_proxy.ch4mu.data.dphi_siso

set_style(MyStyle())
c = Canvas()

hs = [h_sisoinv, h_siso]
for h in hs:
    h.legendstyle = 'LEP'
    h.Scale(1./h.Integral())

h_sisoinv.title = 'proxy events, lepton-jet iso>0.15'
h_sisoinv.color = 'blue'
h_siso.title = 'proxy events, lepton-jet iso<0.15'
h_siso.color = 'red'

legend = Legend(hs, pad=c, leftmargin=0.1, margin=0.1, entryheight=0.02, textsize=12)

xmin_, xmax_, ymin_, ymax_ = get_limits(hs)
draw(hs, pad=c, ylimits=(0, ymax_), ytitle='norm. counts/#pi/20')
legend.Draw()
c.SaveAs('{}/dphi_proxy_byIso.pdf'.format(outdir))

f_proxy.close()
