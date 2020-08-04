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
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/constructIsolationProfile')
if not os.path.isdir(outdir): os.makedirs(outdir)

set_style(MyStyle())
canvas = Canvas()
ROOT.gPad.SetGrid()

pxyf = root_open(proxyfn)
sigf = root_open(signalfn)

ljisos, proxyisos = [], []
for k in pxyf.ch4mu.sig.keys():
    ljiso = getattr(pxyf.ch4mu.sig, k.name).ljisoenergy
    proxyiso = getattr(pxyf.ch4mu.sig, k.name).proxyisoenergy
    ljisos.append(ljiso)
    proxyisos.append(proxyiso)

pljiso = ljisos.pop()
for p in ljisos: pljiso.Add(p)
pproxyiso = proxyisos.pop()
for p in proxyisos: pproxyiso.Add(p)

pljiso.color='#1696d2'
pproxyiso.color='#ec008b'

sljisos = []
for k in sigf.ch4mu.sig.keys():
    ljiso = getattr(sigf.ch4mu.sig, k.name).ljisoenergy
    sljisos.append(ljiso)
psljiso = sljisos.pop()
for p in sljisos: psljiso.Add(p)

psljiso.color="#fdbf11"

ljisotot = pljiso.Clone()
ljisotot.Add(psljiso)
ljisotot.color="#000000"

for p in [pljiso, pproxyiso, psljiso, ljisotot]:
    p.markersize=0.5
    p.legendstyle='LEP'

draw([pljiso, pproxyiso, psljiso, ljisotot],)# ylimits=(3e-3,1), logy=True)
leg = Legend(4, pad=canvas, topmargin=0.02, margin=0.2, entryheight=0.015, entrysep=0.01, textsize=10)
leg.AddEntry(pproxyiso, label='proxy muon iso')
leg.AddEntry(pljiso, label='lepton-jet iso (proxy events)')
leg.AddEntry(psljiso, label='lepton-jet iso (signal events)')
leg.AddEntry(ljisotot, label='lepton-jet iso (signal+proxy events)')
leg.Draw()
canvas.SaveAs('{}/ch4mu_isolationprofiles.pdf'.format(outdir))
canvas.clear()

proxymusf = pljiso.Clone()
proxymusf.Divide(pproxyiso)
draw([proxymusf], ylimits=(0,2))
leg = Legend([proxymusf], pad=canvas, topmargin=0.02, margin=0.2, entryheight=0.015, entrysep=0.01, textsize=10)
leg.Draw()
canvas.SaveAs('{}/ch4mu_proxymuisosf.pdf'.format(outdir))
canvas.clear()


sigf.close()
pxyf.close()