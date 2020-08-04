#!/usr/bin/env python
from __future__ import print_function
import os
import math
import ROOT
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas
from rootpy.plotting.shapes import Line

from FireROOT.Analysis.Utils import *

fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/isolationStudy.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/overlayIsoByIsolation')
if not os.path.isdir(outdir): os.makedirs(outdir)

set_style(MyStyle())
canvas = Canvas()
ROOT.gPad.SetGrid()

f = root_open(fn)

def routine(parampoint, color):

    # 2mu2e - egmiso
    hs = []

    h = getattr(getattr(f.ch2mu2e.sig, parampoint), 'egmljisonopu')
    h.title = 'pv-based pu correction'
    h.linestyle='dashed'
    hs.append(h)
    h = getattr(getattr(f.ch2mu2e.sig, parampoint), 'egmljcorriso')
    h.title = '#rho-based pu correction'
    h.linestyle='solid'
    hs.append(h)
    h = getattr(getattr(f.ch2mu2e.sig, parampoint), 'egmljiso')
    h.title = 'no pu correction'
    h.linestyle='longdashdotdotdot'
    hs.append(h)

    for h in hs:
        h.color = color
        h.drawstyle='hist'
        h.linewidth=2
        h.legendstyle='L'

    legItems = [h for h in hs]
    draw(hs, logy=True)

    legend = Legend(legItems, pad=canvas, header=parampoint, margin=0.25, leftmargin=0.5, topmargin=0.02, entrysep=0.01, entryheight=0.02, textsize=10)
    legend.Draw()
    title = TitleAsLatex('[2#mu2e] egm-type lepton-jet isolation comparison')
    title.Draw()
    draw_labels('59.74 fb^{-1} (13 TeV)', cms_position='left', extra_text='work-in-progress')

    canvas.SaveAs('{}/ch2mu2e_egmljiso__{}.pdf'.format(outdir, parampoint))
    canvas.Clear()


    # 4mu - maxiso
    hs = []

    h = getattr(getattr(f.ch4mu.sig, parampoint), 'maxisonopu')
    h.title = 'pv-based pu correction'
    h.linestyle='dashed'
    hs.append(h)
    h = getattr(getattr(f.ch4mu.sig, parampoint), 'maxcorriso')
    h.title = '#rho-based pu correction'
    h.linestyle='solid'
    hs.append(h)
    h = getattr(getattr(f.ch4mu.sig, parampoint), 'maxiso')
    h.title = 'no pu correction'
    h.linestyle='longdashdotdotdot'
    hs.append(h)

    for h in hs:
        h.color = color
        h.drawstyle='hist'
        h.linewidth=2
        h.legendstyle='L'

    legItems = [h for h in hs]
    draw(hs, logy=True)

    legend = Legend(legItems, pad=canvas, header=parampoint, margin=0.25, leftmargin=0.5, topmargin=0.02, entrysep=0.01, entryheight=0.02, textsize=10)
    legend.Draw()
    title = TitleAsLatex('[4#mu] max lepton-jet isolation comparison')
    title.Draw()
    draw_labels('59.74 fb^{-1} (13 TeV)', cms_position='left', extra_text='work-in-progress')

    canvas.SaveAs('{}/ch4mu_maxljiso__{}.pdf'.format(outdir, parampoint))
    canvas.Clear()


for it, sigtag in enumerate(sigTAGS):
    routine(sigtag, sigCOLORS[it])