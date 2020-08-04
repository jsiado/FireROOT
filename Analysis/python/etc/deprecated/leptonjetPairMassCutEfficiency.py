#!/usr/bin/env python
from __future__ import print_function
import os, json
from collections import OrderedDict
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas

from FireROOT.Analysis.Utils import *

fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/additionalVariables.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/leptonjetPairMassCutEfficiency')
if not os.path.isdir(outdir): os.makedirs(outdir)

set_style(MyStyle())
c = Canvas()

f = root_open(fn)
def routine(chan, direction):
    hs=[]
    effs = OrderedDict()
    chandir = getattr(f, 'ch'+chan)
    for t in chandir.sig.keys():
        sigtag = t.name
        h = getattr(getattr(chandir.sig, sigtag), 'invm_inc500') # Hist
        h_total = h.integral(overflow=True)

        h_ = h.clone()
        for i in range(1, h.nbins()+1):
            if direction=='forward':
                h_sub = h.integral(xbin1=i, overflow=True)
            elif direction=='backward':
                h_sub = h.integral(1, xbin2=i)
            h_[i] = h_sub/h_total
            h_[i].error = 0
            if i==12 and direction=='backward': effs[sigtag] = h_sub/h_total
            if i==13 and direction=='forward': effs[sigtag] = h_sub/h_total
        h_.title = sigtag
        h_.drawstyle = 'PLC hist'
        h_.legendstyle='L'
        hs.append(h_)
    mineff = min(effs.values())
    aveeff = sum(effs.values())/len(effs)
    effs['sig_ave'] = aveeff
    effs['sig_min'] = mineff

    for h in getattr(chandir.bkg, 'invm_inc500'):
        h_total = h.integral(overflow=True)
        if h_total==0: continue
        h_ = h.empty_clone()
        for i in range(1, h.nbins()+1):
            if direction=='forward':
                h_sub = h.integral(xbin1=i, overflow=True)
            elif direction=='backward':
                h_sub = h.integral(1, xbin2=i)
            h_[i] = h_sub/h_total
            h_[i].error = 0
            if i==12 and direction=='backward': effs[h.title] = h_sub/h_total
            if i==13 and direction=='forward': effs[h.title] = h_sub/h_total
        h_.drawstyle = 'hist'
        h_.title=h.title
        h_.color = bkgCOLORS[h.title]
        h_.linestyle = 'dashed'
        h_.legendstyle='L'
        h_.linewidth=2
        hs.append(h_)

    print('>',chan, direction)
    maxlen = max([len(k) for k in effs])
    for k in effs:
        fmt = '{:%d}:{:.2f}'%(maxlen+2)+'%'
        print(fmt.format(k, effs[k]*100))

    legend = Legend(hs, pad=c, margin=0.1, topmargin=0.02, entryheight=0.02, textsize=12)
    axes, limits =draw(hs, ylimits=(0,1.5), logy=False, ytitle='({}) cut efficiency'.format(direction),)
    legend.Draw()
    title = TitleAsLatex('[{}] lepton-jet pair invM cut efficiency'.format(chan.replace('mu', '#mu')))
    title.Draw()
    draw_labels('59.74 fb^{-1} (13 TeV)', cms_position='left', extra_text='work-in-progress')
    ROOT.gPad.SetGrid()

    c.SaveAs('{}/ch{}_invm_{}.pdf'.format(outdir, chan, direction))
    c.Clear()

for direction in ['forward', 'backward']:
    for chan in ['2mu2e', '4mu']:
        routine(chan, direction)
f.close()