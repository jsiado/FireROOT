#!/usr/bin/env python
from __future__ import print_function
import os
from FireROOT.Analysis.Utils import *
from rootpy.plotting import Hist, Legend, Canvas
from rootpy.io import root_open

inname = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/ljSumtkpt.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/plots/ljSumtkpt')
if not os.path.isdir(outdir): os.makedirs(outdir)

from rootpy.plotting.style import set_style
set_style(MyStyle())



c = Canvas()

f = root_open(inname)

samples = 'mXX-150_mA-0p25_lxy-300|mXX-500_mA-1p2_lxy-300|mXX-800_mA-5_lxy-300'.split('|')
samples.append('data')

for histType in ['maxTkPtSum', 'minPfIso05', 'ljpairmass']:
    for chan in ['2mu2e', '4mu']:
        hs = []
        legend = Legend(len(samples), pad=c, margin=0.1, entryheight=0.02, textsize=12)

        for i, s in enumerate(samples):
            histName = '{}__{}__{}'.format(s, chan, histType)
            h = getattr(f, histName).Clone()
            h.xaxis.SetRange(1, h.nbins()+1)
            h.title = s
            h.Scale(1./h.Integral())
            h.drawstyle = 'hist pmc plc'
            h.legendstyle = 'L'
            if s =='data':
                h.fillstyle = '\\'
                h.color = 'salmon'
                h.drawstyle = 'hist'
                h.legendstyle = 'F'
            hs.append(h)
            legend.AddEntry(h)

        xmin, xmax, ymin, ymax = get_limits(hs)
        draw(hs, pad=c, ytitle='norm. '+hs[0].yaxis.title, xlimits=(xmin, hs[0].xaxis.GetBinUpEdge(hs[0].nbins()+1)), ylimits=(0, ymax))
        legend.Draw()
        title = TitleAsLatex('[{}] {}'.format(chan.replace('mu', '#mu'), histType))
        title.Draw()
        draw_labels('59.74 fb^{-1} (13 TeV)', cms_position='left', extra_text='work-in-progress')

        c.SaveAs('{}/{}_{}.pdf'.format(outdir, histType, chan))
        c.Clear()

f.Close()