#!/usr/bin/env python
from __future__ import print_function
import os, json
from collections import OrderedDict
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas

from FireROOT.Analysis.Utils import *

fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/isolationVariables.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/leptonjetIsoCutEfficiency')
if not os.path.isdir(outdir): os.makedirs(outdir)


set_style(MyStyle())
c = Canvas()

f = root_open(fn)
def routine(chan, hname, title):
    hs=[]
    effs = OrderedDict()
    chandir = getattr(f, 'ch'+chan)
    for it, sigtag in enumerate(sigTAGS):
        h = getattr(getattr(chandir.sig, sigtag), hname)
        h_total = h.integral(overflow=True)
        if h_total==0: continue

        h_ = h.clone()
        for i in range(1, h.nbins()+1):
            h_[i] = h.integral(xbin2=i,)/h_total
            h_[i].error = 0
            if i==15: effs[sigtag] = h.integral(xbin2=i,)/h_total
        h_.title = sigtag
        h_.color = sigCOLORS[it]
        h_.drawstyle = 'hist'
        h_.linewidth=2
        h_.legendstyle='L'
        hs.append(h_)
    mineff = min(effs.values())
    aveeff = sum(effs.values())/len(effs)
    effs['sig_ave'] = aveeff
    effs['sig_min'] = mineff

    for h in getattr(chandir.bkg, hname):
        h_total = h.integral(overflow=True)
        if h_total==0: continue
        h_ = h.empty_clone()
        for i in range(1, h.nbins()+1):
            h_[i] = h.integral(xbin2=i,)/h_total
            h_[i].error = 0
            if i==15: effs[h.title] = h.integral(xbin2=i,)/h_total
        h_.drawstyle = 'hist'
        h_.title=h.title
        h_.color = bkgCOLORS[h.title]
        h_.linestyle = 'dashed'
        h_.legendstyle='L'
        h_.linewidth=2
        hs.append(h_)


    print('>',chan)
    maxlen = max([len(k) for k in effs])
    for k in effs:
        fmt = '{:%d}:{:.2f}'%(maxlen+2)+'%'
        print(fmt.format(k, effs[k]*100))

    legend = Legend(hs, pad=c, margin=0.1, topmargin=0.02, entryheight=0.02, entrysep=0.01, textsize=12)
    axes, limits =draw(hs, ylimits=(0., 1.5), ytitle='(backward) cut efficiency',)
    legend.Draw()
    title = TitleAsLatex('[{}] {} cut efficiency'.format(chan.replace('mu', '#mu'), title))
    title.Draw()
    draw_labels('59.74 fb^{-1} (13 TeV)', cms_position='left', extra_text='work-in-progress')
    ROOT.gPad.SetGrid()

    c.SaveAs('{}/ch{}_{}.pdf'.format(outdir, chan, hname))
    c.Clear()

routine('2mu2e', 'egmljisopre', 'Egm-type lepton-jet isolation')
routine('4mu', 'maxljisopre', 'max lepton-jet isolation')
f.close()