#!/usr/bin/env python
from __future__ import print_function
import os
from FireROOT.Analysis.Utils import *
from rootpy.plotting import Hist, Legend, Canvas
from rootpy.io import root_open

inname = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/ljIsodphi.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/plots/ljIsodphi')
if not os.path.isdir(outdir): os.makedirs(outdir)

from rootpy.plotting.style import set_style
set_style(MyStyle())

c = Canvas()

graphCollection = [
    {
        'name': 'isodphi',
        'title': 'lepton-jet min pfiso vs. pair #Delta#phi',
        'xlim': (0, ROOT.Math.Pi()),
        'ymax': {'2mu2e': 0.75, '4mu': 0.5},
    },
    {
        'name': 'invmdphi',
        'title': 'lepton-jet pair invM vs. pair #Delta#phi',
        'xlim': (0, ROOT.Math.Pi()),
    }
]

f = root_open(inname)

samples = 'mXX-150_mA-0p25_lxy-300|mXX-500_mA-1p2_lxy-300|mXX-800_mA-5_lxy-300'.split('|')
samples.append('data')

for g in graphCollection:
    for chan in ['4mu', '2mu2e']:

        if chan == '2mu2e':
            ymax = 0.75
        if chan =='4mu':
            ymax = 0.5
        channelLatex = chan.replace('mu', '#mu')
        ymax = g.get('ymax', None)
        if isinstance(ymax, dict):
            ymax = ymax[chan]

        for s in samples:
            histName = '{}__{}__{}'.format(s, chan, g['name'])
            h = getattr(f, histName).Clone()
            h.title = s
            h.drawstyle = 'ap'
            h.markersize = 0.4

            draw(h, pad=c)
            if ymax is not None: h.GetHistogram().SetMaximum(ymax)
            legend = Legend([h], pad=c, leftmargin=0.05, margin=0.1, entryheight=0.02, textsize=12)
            legend.Draw()
            title = TitleAsLatex("[{}] {}".format(channelLatex, g['title']))
            title.Draw()
            draw_labels('59.74 fb^{-1} (13 TeV)', cms_position='right', extra_text='work-in-progress')

            c.SaveAs('{}/{}.pdf'.format(outdir, histName))
            c.Clear()

f.Close()
