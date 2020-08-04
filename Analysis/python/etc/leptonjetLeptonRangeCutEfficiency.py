#!/usr/bin/env python
from __future__ import print_function
import os
from collections import OrderedDict
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas

from FireROOT.Analysis.Utils import *

fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/leptonjetLeptonRange.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/leptonjetLeptonRangeCutEfficiency')
if not os.path.isdir(outdir): os.makedirs(outdir)


set_style(MyStyle())
c = Canvas()
ROOT.gPad.SetGrid()

def routine(chan, varname, cutbin):
    hs=[]
    effs = OrderedDict()
    chandir = getattr(f, 'ch'+chan)
    for it, sigtag in enumerate(sigTAGS):
        h = getattr(getattr(chandir.sig, sigtag), varname) # Hist
        h_total = h.integral(overflow=True)
        if h_total==0: continue

        h_ = h.clone()
        for i in range(1, h.nbins()+1):
            h_[i] = h.integral(xbin1=i, overflow=True)/h_total
            h_[i].error = 0
            if i==cutbin: effs[sigtag] = h.integral(xbin1=i, overflow=True)/h_total
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

    print('>',chan)
    maxlen = max([len(k) for k in effs])
    for k in effs:
        fmt = '{:%d}:{:.2f}'%(maxlen+2)+'%'
        print(fmt.format(k, effs[k]*100))

    legend = Legend(hs, pad=c, margin=0.1, topmargin=0.02, entryheight=0.02, entrysep=0.01, textsize=12)
    axes, limits =draw(hs, ylimits=(0., 1.), ytitle='(forward) cut efficiency',)
    legend.Draw()
    title = TitleAsLatex('[{}] lepton-jet {} cut efficiency'.format(chan.replace('mu', '#mu'), varname))
    title.Draw()
    draw_labels('59.74 fb^{-1} (13 TeV)', cms_position='left', extra_text='work-in-progress')
    ROOT.gPad.SetGrid()

    c.SaveAs('{}/ch{}_{}.pdf'.format(outdir, chan, varname))
    c.Clear()

f = root_open(fn)

# routine('4mu', 'muonPt', 4)
# routine('2mu2e', 'muonPt', 4)
# routine('2mu2e', 'electronPt', 3)
# routine('2mu2e', 'photonPt', 4)

routine('2mu2e', 'vetoLowPtElectron', 2)
routine('2mu2e', 'vetoLowPtPhoton', 2)
routine('2mu2e', 'vetoLowPtEgm', 2)

# routine('2mu2e', 'vetoLowPtMuon', 2)
# routine('4mu', 'vetoLowPtMuon', 2)

f.close()