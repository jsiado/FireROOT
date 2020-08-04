#!/usr/bin/env python
from __future__ import print_function
import os
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas

from FireROOT.Analysis.Utils import *

fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/modules/signalLifetime.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/overlaySignalLifetime')
if not os.path.isdir(outdir): os.makedirs(outdir)

set_style(MyStyle())
canvas = Canvas()
ROOT.gPad.SetGrid()
f = root_open(fn)

## overlay `dplxy` of private signal samples points
def routine(chan):
    chdir = getattr(f, 'ch'+chan).sig
    paramTags = [x.name for x in chdir.keys()]
    paramTags = [x for x in paramTags if x.endswith('lxy-300')]
    paramTags.sort()

    hs, legItems = [], []
    htitle=None
    for i, paramTag in enumerate(paramTags):
        h = getattr(chdir, paramTag).dplxy
        if htitle is None: htitle = h.title
        h.title = paramTag.rsplit('_', 1)[0]+' (N:{}, O:{})'.format(
            h.integral(), h.overflow()
        )
        h.color = sigCOLORS[i]
        h.legendstyle = 'LEP'
        h.markersize = 0.5
        h.scale( 10**i/h.integral() )
        hs.append(h)
        legItems.append(h)

    xmin_, xmax_, ymin_, ymax_ = get_limits(hs, logy=True)
    draw(hs, logy=True,)
    legend = Legend(legItems, pad=canvas, margin=0.25, leftmargin=0.3, topmargin=0.02,
        entryheight=0.02, entrysep=0.01, textsize=12, header='private signal samples <lxy>=300')
    legend.Draw()
    title = TitleAsLatex('[{}] '.format(chan.replace('mu', '#mu'))+htitle)
    title.Draw()
    draw_labels('59.74 fb^{-1} (13 TeV)', cms_position='left', extra_text='work-in-progress')

    canvas.SaveAs('{}/ch{}_dplxy.pdf'.format(outdir, chan))
    canvas.Clear()


routine('2mu2e')
routine('4mu')


f.close()