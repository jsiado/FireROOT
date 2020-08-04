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

fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/proxy_4mu.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/closureABCD')
if not os.path.isdir(outdir): os.makedirs(outdir)

set_style(MyStyle())
ROOT.gStyle.SetPadLeftMargin(0.11)
ROOT.gStyle.SetPadRightMargin(0.11)
ROOT.gStyle.SetPalette(ROOT.kBird)

COLORS = [sigCOLORS[4], sigCOLORS[1], sigCOLORS[2]] # the blue color is burried in the kBird 2D map

canvas = Canvas()
ROOT.gPad.SetGrid()

f = root_open(fn)


def create_ratioplot(h, xbound_bin=14, ybound_bin=4):
    nbins_per_slice=2
    # ybound_bin = 4
    ybound_val = h.yedges(ybound_bin+1)

    h_vert = Hist(h.GetNbinsX()/nbins_per_slice, h.xaxis.min, h.xaxis.max,
                  title=';|#Delta#phi|;High/low ratio',
                  drawstyle='e1', legendstyle='LEP')
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
    decorate_axis_pi(xax)



    nbins_per_slice=2
    # xbound_bin = 14
    xbound_val = h.xedges(xbound_bin+1)

    h_hori = Hist(h.GetNbinsY()/nbins_per_slice, h.yaxis.min, h.yaxis.max,
                  title=';Iso;High/low ratio',
                  drawstyle='e1', legendstyle='LEP')
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

h = f.ch4mu.data.dphiIso2Dinit
print('[4mu VR] dphiIsoinit - correlation factor: ', h.get_correlation_factor())
h.Draw('colz')
h.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
title = TitleAsLatex('[4#mu VR] '+h.title)
title.Draw()
canvas.SaveAs('{}/ch4mu_vr_dphiisopre.pdf'.format(outdir))
canvas.Clear()

h.Draw('colz')
h.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
title.Draw()
dphi_bounds = [0.7*math.pi, 0.8*math.pi, 0.9*math.pi]
vlines = []
for i, b in enumerate(dphi_bounds):
    vline = Line(b, h.yaxis.GetXmin(), b, h.yaxis.GetXmax())
    vline.color=COLORS[i]
    vline.linewidth=2
    vlines.append(vline)
for l in vlines: l.Draw()
canvas.SaveAs('{}/ch4mu_vr_dphiisopre_vline.pdf'.format(outdir))
canvas.Clear()

h.Draw('colz')
h.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
title.Draw()
iso_bounds = [0.2, 0.3, 0.4]
hlines = []
for i, b in enumerate(iso_bounds):
    hline = Line(h.xaxis.GetXmin(), b, h.xaxis.GetXmax(), b)
    hline.color=COLORS[i]
    hline.linewidth=2
    hlines.append(hline)
for l in hlines: l.Draw()
canvas.SaveAs('{}/ch4mu_vr_dphiisopre_hline.pdf'.format(outdir))
canvas.Clear()

ratios = {}
ratios[0.2] = create_ratioplot(h, ybound_bin=8) # h_vert, h_hori, ybound_val, xbound_val
ratios[0.3] = create_ratioplot(h, ybound_bin=12)
ratios[0.4] = create_ratioplot(h, ybound_bin=16)
todraw = [ratios[0.2][0], ratios[0.3][0], ratios[0.4][0]]
# fitfuncs = []
# for h_ in todraw:
#     h_.fit('pol1')
#     fitfunc = h_.GetFunction('pol1')
#     offset, slope = fitfunc.GetParameter(0), fitfunc.GetParameter(1)
#     fitfuncs.append(fitfunc)
for i, h_ in enumerate(todraw):
    h_.color=COLORS[i]
draw(todraw)
leg = Legend(3, pad=canvas, margin=0.25, leftmargin=0.45, topmargin=0.02, entrysep=0.01, entryheight=0.02, textsize=12)
leg.AddEntry(ratios[0.2][0], label='iso boundary=0.2')
leg.AddEntry(ratios[0.3][0], label='iso boundary=0.3')
leg.AddEntry(ratios[0.4][0], label='iso boundary=0.4')
leg.Draw()
title = TitleAsLatex('[4#mu VR] Ratio of maxiso <high> to maxiso <low>')
title.Draw()
canvas.SaveAs('{}/ch4mu_vr_ratio_maxiso.pdf'.format(outdir, ))
canvas.clear()

ratios = {}
ratios[0.7] = create_ratioplot(h, xbound_bin=14)
ratios[0.8] = create_ratioplot(h, xbound_bin=16)
ratios[0.9] = create_ratioplot(h, xbound_bin=18)
todraw = [ratios[0.7][1], ratios[0.8][1], ratios[0.9][1]]
for i, h_ in enumerate(todraw):
    h_.color=COLORS[i]
draw(todraw)
leg = Legend(3, pad=canvas, margin=0.25, leftmargin=0.45, topmargin=0.02, entrysep=0.01, entryheight=0.02, textsize=12)
leg.AddEntry(ratios[0.7][1], label='|#Delta#phi| boundary=0.7#pi')
leg.AddEntry(ratios[0.8][1], label='|#Delta#phi| boundary=0.8#pi')
leg.AddEntry(ratios[0.9][1], label='|#Delta#phi| boundary=0.9#pi')
leg.Draw()
title = TitleAsLatex('[4#mu VR] Ratio of |#Delta#phi| <high> to |#Delta#phi| <low>')
title.Draw()
canvas.SaveAs('{}/ch4mu_vr_ratio_absdphi.pdf'.format(outdir, ))
canvas.clear()

f.close()


###########################


fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/proxy_2mu2e.root')
f = root_open(fn)

h = f.ch2mu2e.data.dphiIso2Dinit
print('[2mu2e VR] dphiIsoinit - correlation factor: ', h.get_correlation_factor())
h.Draw('colz')
h.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
title = TitleAsLatex('[2#mu2e VR] '+h.title)
title.Draw()
canvas.SaveAs('{}/ch2mu2e_vr_dphiisopre.pdf'.format(outdir))
canvas.Clear()

h.Draw('colz')
h.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
title.Draw()
dphi_bounds = [0.7*math.pi, 0.8*math.pi, 0.9*math.pi]
vlines = []
for i, b in enumerate(dphi_bounds):
    vline = Line(b, h.yaxis.GetXmin(), b, h.yaxis.GetXmax())
    vline.color=COLORS[i]
    vline.linewidth=2
    vlines.append(vline)
for l in vlines: l.Draw()
canvas.SaveAs('{}/ch2mu2e_vr_dphiisopre_vline.pdf'.format(outdir))
canvas.Clear()

h.Draw('colz')
h.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
title.Draw()
iso_bounds = [0.05, 0.1, 0.15]
hlines = []
for i, b in enumerate(iso_bounds):
    hline = Line(h.xaxis.GetXmin(), b, h.xaxis.GetXmax(), b)
    hline.color=COLORS[i]
    hline.linewidth=2
    hlines.append(hline)
for l in hlines: l.Draw()
canvas.SaveAs('{}/ch2mu2e_vr_dphiisopre_hline.pdf'.format(outdir))
canvas.Clear()


ratios = {}
ratios[0.05] = create_ratioplot(h, ybound_bin=2) # h_vert, h_hori, ybound_val, xbound_val
ratios[0.1 ] = create_ratioplot(h, ybound_bin=4)
ratios[0.15] = create_ratioplot(h, ybound_bin=6)
todraw = [ratios[0.05][0], ratios[0.10][0], ratios[0.15][0]]
for i, h_ in enumerate(todraw):
    h_.color=COLORS[i]
draw(todraw)
leg = Legend(3, pad=canvas, margin=0.25, leftmargin=0.45, topmargin=0.02, entrysep=0.01, entryheight=0.02, textsize=12)
leg.AddEntry(ratios[0.05][0], label='iso boundary=0.05')
leg.AddEntry(ratios[0.1 ][0], label='iso boundary=0.10')
leg.AddEntry(ratios[0.15][0], label='iso boundary=0.15')
leg.Draw()
title = TitleAsLatex('[2#mu2e VR] Ratio of iso <high> to iso <low>')
title.Draw()
canvas.SaveAs('{}/ch2mu2e_vr_ratio_iso.pdf'.format(outdir, ))
canvas.clear()

ratios = {}
# ratios[0.6] = create_ratioplot(h, xbound_bin=12) # h_vert, h_hori, ybound_val, xbound_val
ratios[0.7] = create_ratioplot(h, xbound_bin=14)
ratios[0.8] = create_ratioplot(h, xbound_bin=16)
ratios[0.9] = create_ratioplot(h, xbound_bin=18)
todraw = [ratios[0.7][1], ratios[0.8][1], ratios[0.9][1]]
for i, h_ in enumerate(todraw):
    h_.color=COLORS[i]
draw(todraw)
leg = Legend(3, pad=canvas, margin=0.25, leftmargin=0.45, topmargin=0.02, entrysep=0.01, entryheight=0.02, textsize=12)
leg.AddEntry(ratios[0.7][1], label='|#Delta#phi| boundary=0.7#pi')
leg.AddEntry(ratios[0.8][1], label='|#Delta#phi| boundary=0.8#pi')
leg.AddEntry(ratios[0.9][1], label='|#Delta#phi| boundary=0.9#pi')
leg.Draw()
title = TitleAsLatex('[2#mu2e VR] Ratio of |#Delta#phi| <high> to |#Delta#phi| <low>')
title.Draw()
canvas.SaveAs('{}/ch2mu2e_vr_ratio_absdphi.pdf'.format(outdir, ))
canvas.clear()

f.close()
