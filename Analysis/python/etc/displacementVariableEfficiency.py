#!/usr/bin/env python
from __future__ import print_function
import os, json
from collections import defaultdict
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas

from FireROOT.Analysis.Utils import *

fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/displacementVariables.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/displacementVariableEfficiency')
if not os.path.isdir(outdir): os.makedirs(outdir)


set_style(MyStyle())
c = Canvas()

f = root_open(fn)
table_data = defaultdict(dict)
# chan = '2mu2e'
def routine(varname, chan):
    htitle = None
    hs = []
    chandir = getattr(f, 'ch'+chan)
    for t in chandir.sig.keys():
        sigtag = t.name
        h = getattr(getattr(chandir.sig, sigtag), varname) # Hist
        h_total = h.integral(overflow=True)
        if not htitle: htitle = h.title

        h_ = h.clone()
        for i in range(1, h.nbins()+1):
            h_[i] = h.integral(xbin1=i, overflow=True)/h_total
            h_[i].error = 0
        h_.title = sigtag
        h_.drawstyle = 'PLC hist'
        h_.legendstyle='L'
        hs.append(h_)

    # chandir.bkg.mind0 # HistStack, hs
    # total = sum([h.integral(overflow=True) for h in hs])
    # total = hs.Integral(start=1, end=h.nbins()+1)
    binIdbyDy = None
    binLowEdgebyDy = None
    for h in getattr(chandir.bkg, varname):
        h_total = h.integral(overflow=True)
        if h_total == 0: continue

        h_ = h.empty_clone()
        for i in range(1, h.nbins()+1):
            h_[i] = h.integral(xbin1=i, overflow=True)/h_total
            h_[i].error = 0
            if h.title.startswith('DYJets') and h_[i].value<0.2 and binIdbyDy is None:
                binIdbyDy = i
                binLowEdgebyDy = h_[i].x.low
        h_.drawstyle = 'hist'
        h_.title=h.title
        h_.color = bkgCOLORS[h.title]
        h_.linestyle = 'dashed'
        h_.legendstyle='L'
        h_.linewidth=2
        hs.append(h_)

    ## print signal efficiency
    if binIdbyDy and chan=='2mu2e':
        # print('$'*20, varname, chan, binLowEdgebyDy)
        colname = varname+' @{}'.format(binLowEdgebyDy)
        for h in hs:
            # print('{:30} {:.2f}%'.format(h.title, h[binIdbyDy].value*100))
            table_data[h.title][colname] = '{:.2f}%'.format(h[binIdbyDy].value*100)

    xmin_, xmax_, ymin_, ymax_ = get_limits(hs, logx=True)
    legend = Legend(hs, pad=c, margin=0.1, topmargin=0.02, entryheight=0.02, textsize=12)
    axes, limits =draw(hs, ylimits=(0, 1.8), ytitle='cut efficiency', logx=True, logx_crop_value=0.1)
    axes[0].SetMoreLogLabels()
    ROOT.gPad.RedrawAxis()
    legend.Draw()
    title = TitleAsLatex('[{}] {}'.format(chan.replace('mu', '#mu'), htitle))
    title.Draw()
    draw_labels('59.74 fb^{-1} (13 TeV)', cms_position='left', extra_text='work-in-progress')

    c.SaveAs('{}/ch{}_{}.pdf'.format(outdir, chan, varname))
    c.Clear()


for chan in ['2mu2e', ]: #'4mu'
    for varname in [ 'mind0sig', 'maxd0sig', 'aved0sig', 'mind0', 'maxd0', 'aved0',]:
        routine(varname, chan)

# with open('dispvar_efficiency.json', 'w') as f:
#     f.write(json.dumps(table_data, indent=4))
f.close()