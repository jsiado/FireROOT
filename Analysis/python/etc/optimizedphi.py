#!/usr/bin/env python
from __future__ import print_function
import os, math
import ROOT
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas

from FireROOT.Analysis.samples.signalnumbers import genxsec
from FireROOT.Analysis.Utils import *

sigfn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/ljpairDphi.root')
bkgfn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/proxy_4mu.root')

outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/optimizedphi')
if not os.path.isdir(outdir): os.makedirs(outdir)

def decorate_xaxis_pi(xax):
    # xax.SetNdivisions(-310)
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
    return xax

def calculate_simpsig(s, b):
    return s/math.sqrt(b)

def calculate_za(s, b):
    """sigma_b = sqrt(b), just possion error"""
    first = (s+b)*math.log(2*(s+b)/(s+2*b))
    second = b*math.log(1+s/(2*b))
    return math.sqrt(2*(first-second))


set_style(MyStyle())
canvas = Canvas()
ROOT.gPad.SetGrid()

sigf = root_open(sigfn)
bkgf = root_open(bkgfn)


bkgh = bkgf.ch4mu.data.dphi_100.clone()
bkgh.scale(40.6/bkgh.integral())
bkgh.drawstyle='hist'
bkgh.fillstyle='solid'
bkgh.legendstyle='F'
bkgh.linewidth=0
bkgh.fillcolor=sigCOLORS[-2]
bkgh.title='Background'

sighs = []
for it, sigtag in enumerate(sigTAGS):
    h = getattr(sigf.ch4mu.sig, sigtag).dphi.clone()
    mboundstate = int(sigtag.split('_')[0].replace('mXX-', ''))
    h.scale( 30./genxsec[mboundstate] )
    h.drawstyle='hist'
    h.color=sigCOLORS[it]
    h.linewidth=2
    h.title=sigtag+' (norm. 30fb)'
    h.legendstyle='L'
    sighs.append(h)

axes, limits = draw([bkgh]+sighs, ylimits=(1e-5,1e4), logy=True)
decorate_xaxis_pi(axes[0])
leg = Legend([bkgh]+sighs, pad=canvas,
            margin=0.25, leftmargin=0.45, topmargin=0.02,
            entrysep=0.01, entryheight=0.02, textsize=10)
leg.Draw()
title = TitleAsLatex('[4#mu] lepton-jet |#Delta#phi|')
title.Draw()


canvas.SaveAs('{}/ch4mu_dphi.pdf'.format(outdir))
canvas.clear()


signalsigs = []
for h in sighs:
    h_ = h.clone()
    for i in range(1, h.nbins()+1):
        b = math.sqrt(bkgh.integral(xbin1=i, overflow=True))
        s = h.integral(xbin1=i, overflow=True)
        h_[i] = calculate_za(s, b)
        h_[i].error = 0
    h_.scale(1/h_.integral())
    signalsigs.append(h_)

ROOT.gPad.SetLogy(0)
axes, limits = draw(signalsigs[:], ylimits=(0.025, 0.04), logy=False, ytitle='Z_{A} A.U.')
decorate_xaxis_pi(axes[0])
leg = Legend(signalsigs, pad=canvas,
            margin=0.25, leftmargin=0.45, topmargin=0.02,
            entrysep=0.01, entryheight=0.02, textsize=10)
leg.Draw()
title.Draw()

canvas.SaveAs('{}/ch4mu_dphisignificance.pdf'.format(outdir))
canvas.clear()


bkgf.close()

#########################################
bkgfn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/proxy_2mu2e.root')
bkgf = root_open(bkgfn)


bkgh = bkgf.ch2mu2e.data.dphi.clone()
bkgh.scale(37.9/bkgh.integral())
bkgh.drawstyle='hist'
bkgh.fillstyle='solid'
bkgh.legendstyle='F'
bkgh.linewidth=0
bkgh.fillcolor=sigCOLORS[-2]
bkgh.title='Background'

sighs = []
for it, sigtag in enumerate(sigTAGS):
    h = getattr(sigf.ch2mu2e.sig, sigtag).dphi.clone()
    mboundstate = int(sigtag.split('_')[0].replace('mXX-', ''))
    h.scale( 30./genxsec[mboundstate] )
    h.drawstyle='hist'
    h.color=sigCOLORS[it]
    h.linewidth=2
    h.title=sigtag+' (norm. 30fb)'
    h.legendstyle='L'
    sighs.append(h)

axes, limits = draw([bkgh]+sighs, ylimits=(1e-5,1e4), logy=True)
decorate_xaxis_pi(axes[0])
leg = Legend([bkgh]+sighs, pad=canvas,
            margin=0.25, leftmargin=0.45, topmargin=0.02,
            entrysep=0.01, entryheight=0.02, textsize=10)
leg.Draw()
title = TitleAsLatex('[2#mu2e] lepton-jet |#Delta#phi|')
title.Draw()


canvas.SaveAs('{}/ch2mu2e_dphi.pdf'.format(outdir))
canvas.clear()


signalsigs = []
for h in sighs:
    h_ = h.clone()
    for i in range(1, h.nbins()+1):
        b = math.sqrt(bkgh.integral(xbin1=i, overflow=True))
        s = h.integral(xbin1=i, overflow=True)
        h_[i] = calculate_simpsig(s, b)
        h_[i].error = 0
    h_.scale(1/h_.integral())
    signalsigs.append(h_)

ROOT.gPad.SetLogy(0)
axes, limits = draw(signalsigs[:], ylimits=(0.025, 0.06), logy=False, ytitle='s/#sqrt{b} A.U.')
decorate_xaxis_pi(axes[0])
leg = Legend(signalsigs, pad=canvas,
            margin=0.25, leftmargin=0.45, topmargin=0.02,
            entrysep=0.01, entryheight=0.02, textsize=10)
leg.Draw()
title.Draw()

canvas.SaveAs('{}/ch2mu2e_dphisignificance.pdf'.format(outdir))
canvas.clear()




bkgf.close()
sigf.close()
