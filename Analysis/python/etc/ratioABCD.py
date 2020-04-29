#!/usr/bin/env python
from __future__ import print_function
import os
import math
import ROOT
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas

from FireROOT.Analysis.Utils import *

fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/bjets.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/closureABCD')
if not os.path.isdir(outdir): os.makedirs(outdir)

set_style(MyStyle())
canvas = Canvas()

f = root_open(fn)

h = f.ch4mu.data.dphiIso2D

def create_ratioplot(h):
    nbins_per_slice=3
    ybound_bin = 16
    ybound_val = h.yedges(ybound_bin+1)

    h_vert = ROOT.TH1F('h_vert', ';|#Delta#phi|;High/low ratio', h.GetNbinsX()/nbins_per_slice, h.xaxis.min, h.xaxis.max)
    for i in range(1, h.GetNbinsX()+1, nbins_per_slice):
        lo = h.integral(i, i+nbins_per_slice-1, 1, ybound_bin)
        hi = h.integral(i, i+nbins_per_slice-1, ybound_bin+1, h.GetNbinsY())
        ratio, ratio_err = -1, 0.
        if lo>0 and hi>0:
            ratio = hi/lo
            ratio_err = ratio * math.sqrt(1/lo+1/hi)
            h_vert.Fill(h.xedges(i), ratio)
            h_vert.SetBinError(int(i/nbins_per_slice)+1, ratio_err)

    xax = h_vert.xaxis
    xax.SetNdivisions(-310)
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



    nbins_per_slice=3
    xbound_bin = 22
    xbound_val = h.xedges(xbound_bin+1)

    h_hori = ROOT.TH1F('h_hori', ';maxIso;High/low ratio', h.GetNbinsY()/nbins_per_slice, h.yaxis.min, h.yaxis.max)
    for i in range(1, h.GetNbinsY()+1, nbins_per_slice):
        lo = h.integral(1, xbound_bin, i, i+nbins_per_slice-1)
        hi = h.integral(xbound_bin+1, h.GetNbinsX(), i, i+nbins_per_slice-1)
        ratio, ratio_err = -1, 0.
        if lo>0 and hi>0:
            ratio = hi/lo
            ratio_err = ratio * math.sqrt(1/lo+1/hi)
            h_hori.Fill(h.yedges(i), ratio)
            h_hori.SetBinError(int(i/nbins_per_slice)+1, ratio_err)

    return h_vert, h_hori, ybound_val, xbound_val

h_vert, h_hori, ybound_val, xbound_val = create_ratioplot(h)
ROOT.gPad.SetGrid()
draw(h_vert)
title = TitleAsLatex('[4#mu VR] Ratio of maxiso#geq{} to maxiso<{}'.format(ybound_val,ybound_val))
title.Draw()
canvas.SaveAs('{}/ch4mu_vr_ratio_maxiso.pdf'.format(outdir, ))
canvas.clear()

draw(h_hori)
title = TitleAsLatex('[4#mu VR] Ratio of |#Delta#phi|#geq{:.2f} to |#Delta#phi|<{:.2f}'.format(xbound_val,xbound_val))
title.Draw()
canvas.SaveAs('{}/ch4mu_vr_ratio_absdphi.pdf'.format(outdir, ))
canvas.clear()

f.close()


###########################


fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/val2mu2e.root')
fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/proxy_2mu2e.root')
f = root_open(fn)

h = f.ch2mu2e.data.dphiIso2D

h_vert, h_hori, ybound_val, xbound_val = create_ratioplot(h)
ROOT.gPad.SetGrid()
draw(h_vert)
title = TitleAsLatex('[2#mu2e VR] Ratio of maxiso#geq{} to maxiso<{}'.format(ybound_val,ybound_val))
title.Draw()
canvas.SaveAs('{}/ch2mu2e_vr_ratio_maxiso.pdf'.format(outdir, ))
canvas.clear()

draw(h_hori)
title = TitleAsLatex('[2#mu2e VR] Ratio of |#Delta#phi|#geq{:.2f} to |#Delta#phi|<{:.2f}'.format(xbound_val,xbound_val))
title.Draw()
canvas.SaveAs('{}/ch2mu2e_vr_ratio_absdphi.pdf'.format(outdir, ))
canvas.clear()

f.close()
