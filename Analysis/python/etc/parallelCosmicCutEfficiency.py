#!/usr/bin/env python
from __future__ import print_function
import os, json, ROOT
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas

from FireROOT.Analysis.Utils import *

fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/parallelCosmicPairs.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/parallelCosmicCutEfficiency')
if not os.path.isdir(outdir): os.makedirs(outdir)


set_style(MyStyle())
c = Canvas()

f=root_open(fn)

def routine(chan):
    hs=[]
    chandir = getattr(f, 'ch'+chan)
    for t in chandir.sig.keys():
        sigtag = t.name
        h = getattr(getattr(chandir.sig, sigtag), 'npair') # Hist
        h_total = h.integral(overflow=True)

        h_ = h.clone()
        for i in range(1, h.nbins()+1):
            h_[i] = h.integral(1, xbin2=i)/h_total
            h_[i].error = 0
        h_.title = sigtag
        h_.drawstyle = 'PLC hist'
        h_.legendstyle='L'
        hs.append(h_)

    legend = Legend(hs, pad=c, margin=0.1, topmargin=0.02, entryheight=0.02, textsize=12)
    axes, limits =draw(hs, ylimits=(0.95, 1.05), ytitle='cut efficiency',)
    legend.Draw()
    title = TitleAsLatex('[{}] parallel cosmic pair cut efficiency'.format(chan.replace('mu', '#mu')))
    title.Draw()
    draw_labels('59.74 fb^{-1} (13 TeV)', cms_position='left', extra_text='work-in-progress')
    ROOT.gPad.SetGrid()

    c.SaveAs('{}/ch{}_npair.pdf'.format(outdir, chan))
    c.Clear()

for chan in ['2mu2e', '4mu']:
    routine(chan)
f.close()