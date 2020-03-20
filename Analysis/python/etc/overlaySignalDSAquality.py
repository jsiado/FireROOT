#!/usr/bin/env python
from __future__ import print_function
import os
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas

from FireROOT.Analysis.Utils import *

fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/signalDSAquality.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/')
if not os.path.isdir(outdir): os.makedirs(outdir)


def routine(hs, c):
    c.clear()
    for h in hs:
        h.drawstyle='hist'
        h.scale(1./h.integral())
        h.linewidth=2
        h.legendstyle='L'

    legend = Legend(hs, pad=c, leftmargin=0.5, margin=0.1, entryheight=0.02, textsize=12)
    xmin_, xmax_, ymin_, ymax_ = get_limits(hs)
    draw(hs, pad=c, ylimits=(0, ymax_),)
    legend.Draw()
    t = LuminosityLabel('XX#rightarrow2A#rightarrow4#mu (500GeV, 1.2GeV, 300cm)')
    t.draw()


f = root_open(fn)
hdir = getattr(f.ch4mu.sig, 'mXX-500_mA-1p2_lxy-300')

set_style(MyStyle())
c = Canvas()

# 1. stations
h0, h1 = hdir.nstas, hdir.nstasInv
h0.title='N(DT+CSC) stations #geq 2'
h0.color='blue'

h1.title='N(DT+CSC) stations < 2'
h1.color='red'

routine([h0, h1], c)
c.SaveAs(os.path.join(outdir, 'signalDSAquality_nsta.pdf'.format(outdir)))

# 2. hits
h0, h1 = hdir.nhits, hdir.nhitsInv
h0.title='N(DT+CSC) hits #geq 12'
h0.color='blue'

h1.title='N(DT+CSC) hits < 12'
h1.color='red'

routine([h0, h1], c)
c.SaveAs(os.path.join(outdir, 'signalDSAquality_nhit.pdf'.format(outdir)))

# 3. pterror
h0, h1 = hdir.pterr, hdir.pterrInv
h0.title='#sigma_{p_{T}}/p_{T} < 1'
h0.color='blue'

h1.title='#sigma_{p_{T}}/p_{T} #geq 1'
h1.color='red'

routine([h0, h1], c)
c.SaveAs(os.path.join(outdir, 'signalDSAquality_pterr.pdf'.format(outdir)))

# 4. normalized chi2
h0, h1 = hdir.normchi2, hdir.normchi2Inv
h0.title='#chi^{2}/ndof < 4'
h0.color='blue'

h1.title='#chi^{2}/ndof #geq 4'
h1.color='red'

routine([h0, h1], c)
c.SaveAs(os.path.join(outdir, 'signalDSAquality_normchi2.pdf'.format(outdir)))

# 5. dthits
h0, h1 = hdir.dthits, hdir.dthitsInv
h0.title='N(CSC) hits=0, N(DT) hits > 18'
h0.color='blue'

h1.title='N(CSC) hits=0, N(DT) hits #leq 18'
h1.color='red'

routine([h0, h1], c)
c.SaveAs(os.path.join(outdir, 'signalDSAquality_dthit.pdf'.format(outdir)))

f.close()