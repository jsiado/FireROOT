#!/usr/bin/env python
from __future__ import print_function
import os
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas

from FireROOT.Analysis.Utils import *


fn_proxy = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/proxy_4mu.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/overlayProxyDphi')
if not os.path.isdir(outdir): os.makedirs(outdir)

f = root_open(fn_proxy)

set_style(MyStyle())
canvas = Canvas()
ROOT.gPad.SetGrid()

hs, legitems = [], []
for i, d0 in enumerate([100,200,300,400,500]):
    h = getattr(f.ch4mu.data, 'dphi_{}'.format(d0))
    h.color = sigCOLORS[i]
    h.legendstyle='LEP'
    h.title='lepton-jet |d_{0}|>'+'{}#mum'.format(d0)
    hs.append(h)
    legitems.append(h)

draw(hs, ylimits=(1e-1, 1e4), logy=True)
leg = Legend(legitems, pad=canvas, leftmargin=0.1, margin=0.1, entryheight=0.02, textsize=12)
leg.Draw()

title = TitleAsLatex('[4#mu VR] |#Delta#phi|(lepton-jet, proxy muon) shape comparison')
title.Draw()

canvas.SaveAs('{}/ch4mu_dphi.pdf'.format(outdir))
canvas.clear()


ph = f.ch4mu.data.dphi
ph.color = sigCOLORS[0]
ph.legendstyle='LEP'
ph.title='proxy'

sfn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/ljpairDphi.root')
sf = root_open(sfn)
sh = sf.ch4mu.data.dphi
sh.color = sigCOLORS[1]
sh.legendstyle='LEP'
sh.title='SR'

phc = ph.clone()
phc.scale(sh.integral(xbin2=21)/phc.integral(xbin2=21)*2.2)
phc.drawstyle='hist'
phc.linestyle='dashed'


draw([ph,sh, phc], ylimits=(1e-1, 1e4), logy=True)
leg = Legend([ph, sh, phc], pad=canvas, leftmargin=0.1, margin=0.1, entryheight=0.02, textsize=12)
leg.Draw()

title = TitleAsLatex('[4#mu VR] |#Delta#phi|(lepton-jet, proxy muon) shape comparison')
title.Draw()

canvas.SaveAs('{}/ch4mu_dphicomp.pdf'.format(outdir))
canvas.clear()
sf.close()

f.close()


#################################################

fn_proxy = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/proxy_2mu2e.root')
f = root_open(fn_proxy)

hs, legitems = [], []
for i, d0 in enumerate([100,200,300,400,500]):
    h = getattr(f.ch2mu2e.data, 'dphi_{}'.format(d0))
    h.color = sigCOLORS[i]
    h.legendstyle='LEP'
    h.title='proxy muon |d_{0}|>'+'{}#mum'.format(d0)
    hs.append(h)
    legitems.append(h)

draw(hs, logy=True)
leg = Legend(legitems, pad=canvas, leftmargin=0.1, margin=0.1, entryheight=0.02, textsize=12)
leg.Draw()

title = TitleAsLatex('[2#mu2e VR] |#Delta#phi|(lepton-jet, proxy muon) shape comparison')
title.Draw()

canvas.SaveAs('{}/ch2mu2e_dphi.pdf'.format(outdir))
canvas.clear()
f.close()
