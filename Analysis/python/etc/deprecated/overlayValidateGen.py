#!/usr/bin/env python
from __future__ import print_function
import os
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas

from FireROOT.Analysis.Utils import *

fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/centralSig/validategen.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/validategen')
if not os.path.isdir(outdir): os.makedirs(outdir)


set_style(MyStyle())

f = root_open(fn)

#################################################
# dark photon lxy
c = Canvas()
masstag = 'mXX-1000_mA-1p2'

mxx, ma = masstag.split('_')
mxx = mxx.split('-')[-1]
ma = ma.split('-')[1].replace('p', '.')

massdir = getattr(f.ch4mu, masstag)
lxytags = [x.name for x in massdir.keys()] # lxy-0p3_ctau-0p0025

hsd = {}
for tag in lxytags:
    lxy_, ctau_ = tag.split('_')
    lxy = lxy_.split('-')[1].replace('p', '.')
    ctau = ctau_.split('-')[1].replace('p', '.')
    h = getattr(massdir, tag).dplxy
    h.linewidth = 2
    h.drawstyle = 'PLC hist'
    h.scale(1./h.integral())
    h.legendstyle='L'
    h.title = 'lxy: {}cm c#tau: {}mm'.format(lxy, ctau)
    hsd[float(lxy)] = h
hs = [hsd[k] for k in sorted(hsd)]
leg = Legend(hs, pad=c, leftmargin=0.5, margin=0.1, entryheight=0.02, textsize=12)
draw(hs, pad=c, xlimits=(1e-1, 500), logy=True, logx=True)
leg.Draw()
t = LuminosityLabel('XX#rightarrow2A#rightarrow4#mu ({}, {}) GeV'.format(mxx, ma))
t.draw()
c.SaveAs(os.path.join(outdir, 'ch4mu_dplxy.pdf'.format(outdir)))

c.clear()

massdir = getattr(f.ch2mu2e, masstag)
lxytags = [x.name for x in massdir.keys()] # lxy-0p3_ctau-0p0025

hsd = {}
for tag in lxytags:
    lxy_, ctau_ = tag.split('_')
    lxy = lxy_.split('-')[1].replace('p', '.')
    ctau = ctau_.split('-')[1].replace('p', '.')
    h = getattr(massdir, tag).dplxy
    h.linewidth = 2
    h.drawstyle = 'PLC hist'
    h.scale(1./h.integral())
    h.legendstyle='L'
    h.title = 'lxy: {}cm c#tau: {}mm'.format(lxy, ctau)
    hsd[float(lxy)] = h
hs = [hsd[k] for k in sorted(hsd)]
leg = Legend(hs, pad=c, leftmargin=0.5, margin=0.1, entryheight=0.02, textsize=12)
draw(hs, pad=c, xlimits=(1e-1, 500), logy=True, logx=True)
leg.Draw()
t = LuminosityLabel('XX#rightarrow2A#rightarrow2#mu2e ({}, {}) GeV'.format(mxx, ma))
t.draw()
c.SaveAs(os.path.join(outdir, 'ch2mu2e_dplxy.pdf'.format(outdir)))


#################################################
# boundstate mass
c = Canvas()
ma, lxy = 'mA-1p2', 'lxy-150'

hsd = {}
masstags = [x.name for x in f.ch4mu.keys() if x.name.endswith(ma)]
for masstag in masstags:
    mxx, ma = masstag.split('_')
    mxx = mxx.split('-')[-1]
    massdir = getattr(f.ch4mu, masstag)
    lxytags = [x.name for x in massdir.keys() if x.name.startswith(lxy)]
    if not lxytags: continue
    h = getattr(massdir, lxytags[0]).psmass
    h.linewidth = 2
    h.drawstyle = 'PLC hist'
    h.scale(1./h.integral())
    h.legendstyle='L'
    h.title = 'm_{#chi#chi}: '+mxx+'GeV'
    hsd[int(mxx)] = h
hs = [hsd[k] for k in sorted(hsd)]
leg = Legend(hs, pad=c, leftmargin=0.6, margin=0.15, entryheight=0.02, textsize=12)
draw(hs, pad=c, logy=False,)
leg.Draw()
t = LuminosityLabel('XX#rightarrow2A#rightarrow4#mu')
t.draw()
c.SaveAs(os.path.join(outdir, 'ch4mu_psmass.pdf'.format(outdir)))


hsd = {}
masstags = [x.name for x in f.ch2mu2e.keys() if x.name.endswith(ma)]
for masstag in masstags:
    mxx, ma = masstag.split('_')
    mxx = mxx.split('-')[-1]
    massdir = getattr(f.ch2mu2e, masstag)
    lxytags = [x.name for x in massdir.keys() if x.name.startswith(lxy)]
    if not lxytags: continue
    h = getattr(massdir, lxytags[0]).psmass
    h.linewidth = 2
    h.drawstyle = 'PLC hist'
    h.scale(1./h.integral())
    h.legendstyle='L'
    h.title = 'm_{#chi#chi}: '+mxx+'GeV'
    hsd[int(mxx)] = h
hs = [hsd[k] for k in sorted(hsd)]
leg = Legend(hs, pad=c, leftmargin=0.6, margin=0.15, entryheight=0.02, textsize=12)
draw(hs, pad=c, logy=False,)
leg.Draw()
t = LuminosityLabel('XX#rightarrow2A#rightarrow2#mu2e')
t.draw()
c.SaveAs(os.path.join(outdir, 'ch2mu2e_psmass.pdf'.format(outdir)))


f.close()