#!/usr/bin/env python
from __future__ import print_function
import os
import math
import ROOT
import pandas as pd
from collections import defaultdict
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas
from rootpy.plotting.shapes import Line

from FireROOT.Analysis.Utils import *

beforefn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/isolationVariables2.root')
afterfn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/isolationVariables2_afterIsoDrop.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/compareMuIsoDrop')
if not os.path.isdir(outdir): os.makedirs(outdir)

set_style(MyStyle())
canvas = Canvas()
ROOT.gPad.SetGrid()

beforef = root_open(beforefn)
afterf = root_open(afterfn)

def routine(chan, var):
    hs_b, hs_a = [], []
    htitle = None
    numbers = defaultdict(dict)

    # before
    chandir = getattr(beforef, 'ch'+chan)
    for it, sigtag in enumerate(sigTAGS):
        h = getattr(getattr(chandir.sig, sigtag), var) # Hist
        if htitle is None: htitle = h.title
        h.title=sigtag+' w/ mu iso'
        h.drawstyle = 'hist'
        h.color = sigCOLORS[it]
        h.linewidth=2
        h.legendstyle='L'
        hs_b.append(h)
        numbers[sigtag]['before'] = h.integral()

    # after
    chandir = getattr(afterf, 'ch'+chan)
    for it, sigtag in enumerate(sigTAGS):
        h = getattr(getattr(chandir.sig, sigtag), var) # Hist
        h.title='w/o mu iso'
        h.drawstyle = 'hist'
        h.color = sigCOLORS[it]
        h.linewidth=2
        h.linestyle='dashed'
        h.legendstyle='L'
        hs_a.append(h)
        numbers[sigtag]['after'] = h.integral()

    print('>', chan, var)
    df = pd.DataFrame(numbers).T
    df['incr %'] = (df['after']-df['before'])/df['before']*100
    print(df[['before', 'after', 'incr %']])
    draw(hs_b+hs_a, logy=True)

    legend = Legend(len(hs_b), pad=canvas, margin=0.25, leftmargin=0.3, topmargin=0.02, entrysep=0.01, entryheight=0.02, textsize=10)
    legend.SetNColumns(2)
    for _b, _a in zip(hs_b, hs_a):
        legend.AddEntry(_b)
        legend.AddEntry(_a)
    legend.Draw()

    title = TitleAsLatex('[{}] '.format(chan.replace('mu', '#mu'))+htitle)
    title.Draw()
    draw_labels('59.74 fb^{-1} (13 TeV)', cms_position='left', extra_text='work-in-progress')

    canvas.SaveAs('{}/ch{}_{}.pdf'.format(outdir, chan, var))
    canvas.Clear()



routine('2mu2e', 'egmisonopu')
routine('4mu', 'maxisonopu')

beforef.close()
afterf.close()