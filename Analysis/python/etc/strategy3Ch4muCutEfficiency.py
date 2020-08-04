#!/usr/bin/env python
from __future__ import print_function
import os, json
from collections import OrderedDict
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas

from FireROOT.Analysis.Utils import *

fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/strategy3_ch4mu.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/strategy3Ch4muCutEfficiency')
if not os.path.isdir(outdir): os.makedirs(outdir)

set_style(MyStyle())
c = Canvas()

f = root_open(fn)
def routine(chan, var, direction, binidx, titlecontent):
    hs=[]
    effs = OrderedDict()
    chandir = getattr(f, 'ch'+chan)
    for t in chandir.sig.keys():
        sigtag = t.name
        h = getattr(getattr(chandir.sig, sigtag), var) # Hist
        h_total = h.integral(overflow=True)

        h_ = h.clone()
        for i in range(1, h.nbins()+1):
            if direction=='forward':
                h_sub = h.integral(xbin1=i, overflow=True)
            elif direction=='backward':
                h_sub = h.integral(1, xbin2=i)
            h_[i] = h_sub/h_total
            h_[i].error = 0
            if i==binidx: effs[sigtag] = h_sub/h_total
        h_.title = sigtag
        h_.drawstyle = 'PLC hist'
        h_.legendstyle='L'
        hs.append(h_)
    mineff = min(effs.values())
    aveeff = sum(effs.values())/len(effs)
    effs['sig_ave'] = aveeff
    effs['sig_min'] = mineff

    for h in getattr(chandir.bkg, var):
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
            if i==binidx: effs[h.title] = h_sub/h_total
        h_.drawstyle = 'hist'
        h_.title=h.title
        h_.color = bkgCOLORS[h.title]
        h_.linestyle = 'dashed'
        h_.legendstyle='L'
        h_.linewidth=2
        hs.append(h_)

    if 'dphi' in var:
        for h in hs:
            xax = h.xaxis
            xax.SetNdivisions(-310)
            xax.ChangeLabel(2,-1,-1,-1,-1,-1,"#frac{#pi}{10}")
            xax.ChangeLabel(3,-1,-1,-1,-1,-1,"#frac{#pi}{5}")
            xax.ChangeLabel(4,-1,-1,-1,-1,-1,"#frac{3#pi}{10}")
            xax.ChangeLabel(5,-1,-1,-1,-1,-1,"#frac{2#pi}{5}")
            xax.ChangeLabel(6,-1,-1,-1,-1,-1,"#frac{#pi}{2}")
            xax.ChangeLabel(7,-1,-1,-1,-1,-1,"#frac{3#pi}{5}")
            xax.ChangeLabel(8,-1,-1,-1,-1,-1,"#frac{7#pi}{10}")
            xax.ChangeLabel(9,-1,-1,-1,-1,-1,"#frac{4#pi}{5}")
            xax.ChangeLabel(10,-1,-1,-1,-1,-1,"#frac{9#pi}{10}")
            xax.ChangeLabel(11,-1,-1,-1,-1,-1,"#pi")

    print('>',chan, var, direction)
    maxlen = max([len(k) for k in effs])
    for k in effs:
        fmt = '{:%d}:{:.2f}'%(maxlen+2)+'%'
        print(fmt.format(k, effs[k]*100))

    legend = Legend(hs, pad=c, margin=0.1, topmargin=0.02, entryheight=0.02, textsize=12)
    axes, limits =draw(hs, ylimits=(0,1.5), logy=False, ytitle='({}) cut efficiency'.format(direction),)
    legend.Draw()
    title = TitleAsLatex('[{}]'.format(chan.replace('mu', '#mu'))+' {} cut efficiency'.format(titlecontent))
    title.Draw()
    draw_labels('59.74 fb^{-1} (13 TeV)', cms_position='left', extra_text='work-in-progress')
    ROOT.gPad.SetGrid()

    c.SaveAs('{}/ch{}_{}.pdf'.format(outdir, chan, var))
    c.Clear()

# routine('4mu', 'dphi_e', 'forward', 24, 'lepton-jet pair |#Delta#phi|')
# routine('4mu', 'ljetaabssum', 'backward', 29, 'lepton-jet |#eta_{0}+#eta_{1}|')
# routine('4mu', 'maxljiso', 'backward', 36, 'max lepton-jet isolation')

routine('4mu', 'scaledd0', 'forward', 16, 'muon-type lepton-jet scaled d0')

f.close()