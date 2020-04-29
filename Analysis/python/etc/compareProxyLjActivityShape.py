#!/usr/bin/env python
from __future__ import print_function
import os
import math
import ROOT
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas

from FireROOT.Analysis.Utils import *

proxyfn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/constructIso_4mu.root')
signalfn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/constructMuLjIso.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/compareProxyLjActivityShape')
if not os.path.isdir(outdir): os.makedirs(outdir)

color=[
    "#1696d2",
    "#ec008b",
    "#000000",
    "#d2d2d2",
    "#fdbf11",
    "#55b748",
    "#9e0142",
    "#f46d43",
    "#bf812d",
    "#66c2a5",
    "#5e4fa2",
    "#e6f598",
]


set_style(MyStyle())
canvas = Canvas()
ROOT.gPad.SetGrid()

pf = root_open(proxyfn)
sf = root_open(signalfn)

def collect(var):
    todraws, legitems = [], []
    sigtags = [k.name for k in sf.ch4mu.sig.keys()]
    for i, st in enumerate(sigtags):
        h_sig = getattr(getattr(sf.ch4mu.sig, st), var)
        h_sig.title=st+' (signal)'
        h_pxy = getattr(getattr(pf.ch4mu.sig, st), var)
        h_pxy.scale(h_sig.integral()/h_pxy.integral())
        h_pxy.linestyle='dashed'
        h_pxy.title = st+' (proxy)'

        todraw = [h_sig, h_pxy]
        for h in todraw:
            h.drawstyle='hist'
            h.linewidth=2
            h.color=color[i]
            h.legendstyle='L'
        todraws.extend(todraw)
        legitems.extend(todraw)

    return todraws, legitems


todraws, legitems = collect('ljiso')
draw(todraws, logy=True)
leg = Legend(legitems, pad=canvas, topmargin=0.02, margin=0.2, entryheight=0.015, entrysep=0.01, textsize=10,)
leg.Draw()
title = TitleAsLatex('[4#mu SR, VR] lepton-jet isolation shape comparison')
title.Draw()

canvas.SaveAs('{}/ch4mu_ljisoShape.pdf'.format(outdir))
canvas.clear()


todraws, legitems = collect('dphi')
draw(todraws, logy=True)
leg = Legend(legitems, pad=canvas, topmargin=0.02, leftmargin=0.05, rightmargin=0.5, margin=0.2, entryheight=0.015, entrysep=0.01, textsize=10,)
leg.Draw()
title = TitleAsLatex('[4#mu SR, VR] |#Delta#phi| shape comparison')
title.Draw()

canvas.SaveAs('{}/ch4mu_dphiShape.pdf'.format(outdir))
canvas.clear()


sf.close()
pf.close()





proxyfn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/constructIso_2mu2e.root')
signalfn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/constructEgmLjIso.root')

pf = root_open(proxyfn)
sf = root_open(signalfn)


def collect(var):
    todraws, legitems = [], []
    sigtags = [k.name for k in sf.ch2mu2e.sig.keys()]
    for i, st in enumerate(sigtags):
        h_sig = getattr(getattr(sf.ch2mu2e.sig, st), var)
        h_sig.title=st+' (signal)'
        h_pxy = getattr(getattr(pf.ch2mu2e.sig, st), var)
        h_pxy.scale(h_sig.integral()/h_pxy.integral())
        h_pxy.linestyle='dashed'
        h_pxy.title = st+' (proxy)'

        todraw = [h_sig, h_pxy]
        for h in todraw:
            h.drawstyle='hist'
            h.linewidth=2
            h.color=color[i]
            h.legendstyle='L'
        todraws.extend(todraw)
        legitems.extend(todraw)

    return todraws, legitems



todraws, legitems = collect('egmljiso')
draw(todraws, logy=True)
leg = Legend(legitems, pad=canvas, topmargin=0.02, margin=0.2, entryheight=0.015, entrysep=0.01, textsize=10,)
leg.Draw()
title = TitleAsLatex('[2#mu2e SR, VR] Egm-type lepton-jet isolation shape comparison')
title.Draw()

canvas.SaveAs('{}/ch2mu2e_egmljisoShape.pdf'.format(outdir))
canvas.clear()


todraws, legitems = collect('dphi')
draw(todraws, logy=True)
leg = Legend(legitems, pad=canvas, topmargin=0.02, leftmargin=0.05, rightmargin=0.5, margin=0.2, entryheight=0.015, entrysep=0.01, textsize=10,)
leg.Draw()
title = TitleAsLatex('[2#mu2e SR, VR] |#Delta#phi| shape comparison')
title.Draw()

canvas.SaveAs('{}/ch2mu2e_dphiShape.pdf'.format(outdir))
canvas.clear()


sf.close()
pf.close()
