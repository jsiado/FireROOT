#!/usr/bin/env python
from __future__ import print_function
import os, json, math
import ROOT
from collections import defaultdict
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas

from FireROOT.Analysis.Utils import *

fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/modules/displacementVariables.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/displacementSignificance')
if not os.path.isdir(outdir): os.makedirs(outdir)



set_style(MyStyle())
c = Canvas()

f = root_open(fn)

def routine(varname, chan):
    htitle = None
    hs = []
    chandir = getattr(f, 'ch'+chan)

    bkghs = getattr(chandir.bkg, varname).GetHists()
    bkgh = bkghs.pop()
    for h in bkghs: bkgh.Add(h)
    for it, sigtag in enumerate(sigTAGS):
        h = getattr(getattr(chandir.sig, sigtag), varname) # Hist
        if not htitle: htitle = h.title

        h_ = h.empty_clone()
        for i in range(1, h.nbins()+1):
            sigN = h.integral(xbin1=i, overflow=True)
            bkgN = bkgh.integral(xbin1=i, overflow=True)
            if bkgN == 0: h[i] = h[i-1]
            else: h_[i] = sigN/math.sqrt(bkgN)
            ## tried s/sqrt(b), s/sqrt(s+b), 2(sqrt(s+b)-sqrt(b))
            ## shape slightly different, trend similar, conclusion remain the same
            # h_[i] = 2*(math.sqrt(sigN+bkgN)-math.sqrt(bkgN))
            h_[i].error = 0
        h_.title = sigtag
        h_.color = sigCOLORS[it]
        h_.drawstyle = 'hist'#'PLC hist'
        h_.linewidth = 2
        h_.legendstyle='L'
        h_.xaxis.SetTitle(h.xaxis.GetTitle())
        h_.yaxis.SetTitle('(forward) s/#sqrt{b}')
        hs.append(h_)

    legend = Legend(hs, pad=c, margin=0.25, topmargin=0.02, entrysep=0.01, entryheight=0.02, textsize=11)
    axes, limits =draw(hs, logy=True,logx=False, ylimits=(1e-5,1e3))
    ROOT.gPad.SetGrid()
    legend.Draw()
    title = TitleAsLatex('[{}] {}'.format(chan.replace('mu', '#mu'), htitle))
    title.Draw()
    draw_labels('59.74 fb^{-1} (13 TeV)', cms_position='left', extra_text='work-in-progress')

    c.SaveAs('{}/ch{}_{}.pdf'.format(outdir, chan, varname))
    c.Clear()


for chan in ['2mu2e', '4mu']: #
    for varname in [ 'mind0sig', 'maxd0sig', 'aved0sig', 'mind0', 'maxd0', 'aved0',]:
        routine(varname, chan)

f.close()