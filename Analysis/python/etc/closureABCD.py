#!/usr/bin/env python
from __future__ import print_function
import os
import math
import ROOT
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas

from FireROOT.Analysis.Utils import *

fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/proxy_4mu.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/closureABCD')
if not os.path.isdir(outdir): os.makedirs(outdir)

set_style(MyStyle())
# ROOT.gStyle.SetPadTopMargin(0.1)
# ROOT.gStyle.SetPadBottomMargin(0.09)
ROOT.gStyle.SetPadLeftMargin(0.11)
ROOT.gStyle.SetPadRightMargin(0.11)
ROOT.gStyle.SetPalette(ROOT.kBird)
ROOT.gStyle.SetPaintTextFormat('.2f')
canvas = Canvas()
ROOT.gPad.SetGrid()

f = root_open(fn)


def create_closure_map(h, thres=1):
    ## closure map
    hc = h.clone()
    hc.Reset()
    ave_closure = 0.
    ave_closure_sqrd = 0.
    nbins = 0

    for i in range(1, h.GetNbinsX()):
        for j in range(1, h.GetNbinsY()):
            c = h.integral(1,i,1,j)
            d = h.integral(i+1,h.GetNbinsX(),1,j)
            a = h.integral(1,i,j+1,h.GetNbinsY())
            b = h.integral(i+1,h.GetNbinsX(),j+1,h.GetNbinsY())
            # if a==0 or b==0 or c==0 or d==0:
            if a<thres or b<thres or c<thres:
                hc.SetBinContent(i,j,0)
                continue

            d_pred_val = b*c/float(a)
            d_pred_err = d_pred_val*math.sqrt(1/float(a)+1/float(b)+1/float(c))
            if d!=0: d_diff = abs(d-d_pred_val)/d
            else: d_diff = abs(d-d_pred_val)/d_pred_val
            # d_diff = d-d_pred_val
            # if d_pred_err < 0.5*d_pred_val:
                # hc.SetBinContent(i,j,(d-d_pred_val)/d)
            if d_diff==0: d_diff = 1e-6 # to diff from no filled bin
            hc.SetBinContent(i,j,d_diff)
            ave_closure += d_diff
            ave_closure_sqrd += d_diff**2
            nbins += 1
            # else:
            #     hc.SetBinContent(i,j,0)

    xax = hc.xaxis
    decorate_axis_pi(xax)

    ave_closure /= nbins
    ave_closure_sqrd /= nbins

    return hc, ave_closure, ave_closure_sqrd


def create_closeness_map(h, thres=3):
    hc = h.clone()
    hc.Reset()

    for i in range(1, h.GetNbinsX()):
        for j in range(1, h.GetNbinsY()):
            c = h.integral(1,i,1,j)
            d = h.integral(i+1,h.GetNbinsX(),1,j)
            a = h.integral(1,i,j+1,h.GetNbinsY())
            b = h.integral(i+1,h.GetNbinsX(),j+1,h.GetNbinsY())
            # if a==0 or b==0 or c==0 or d==0:
            if a<thres or b<thres or c<thres:
                # outside optimization region
                hc.SetBinContent(i,j,-1)
                continue

            d_pred_val = b*c/float(a)
            d_pred_err = d_pred_val*math.sqrt(1/float(a)+1/float(b)+1/float(c))

            close = True
            if d-math.sqrt(d)>d_pred_val+d_pred_err or d+math.sqrt(d)<d_pred_val-d_pred_err: close =False
            # print('({}, {}) - {}'.format(i,j,close))
            hc.SetBinContent(i,j,int(close))

    xax = hc.xaxis
    decorate_axis_pi(xax)

    return hc


### initial closeness
h = f.ch4mu.data.dphiIso2Dinit

hc = create_closeness_map(h)
hc.Draw('colz')
hc.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
title = TitleAsLatex('[4#mu VR] '+h.title+' closeness map')
title.Draw()
canvas.SaveAs('{}/ch4mu_vr_dphiisoInit_closeness_noscale.pdf'.format(outdir))
canvas.Clear()

hc, ave_closure, ave_closure_sqrd = create_closure_map(h)
hc.Draw('colz text')
hc.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
hc.zaxis.SetRangeUser(0,1)
title = TitleAsLatex('[4#mu VR] '+h.title+' closure map')
title.Draw()
canvas.SaveAs('{}/ch4mu_vr_dphiisoInit_closuremap_noscale.pdf'.format(outdir))
canvas.Clear()

#################################
h = f.ch4mu.data.dphiIso2D

hc = create_closeness_map(h)
hc.Draw('colz')
hc.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
title = TitleAsLatex('[4#mu VR] '+h.title+' closeness map')
title.Draw()
canvas.SaveAs('{}/ch4mu_vr_dphiiso_closeness_noscale.pdf'.format(outdir))
canvas.Clear()


h.scale(84.2/h.integral())

h.Draw('colz')
h.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
title = TitleAsLatex('[4#mu VR] '+h.title)
title.Draw()
canvas.SaveAs('{}/ch4mu_vr_dphiiso.pdf'.format(outdir))
canvas.Clear()


hc, ave_closure, ave_closure_sqrd = create_closure_map(h)
print('Average closure: {:.3f}'.format(ave_closure))
print('Spread: {:.3f}'.format(math.sqrt(abs(ave_closure_sqrd-ave_closure**2))))

hc.Draw('colz text')
hc.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
hc.zaxis.SetRangeUser(0,1)
title = TitleAsLatex('[4#mu VR] '+h.title+' closure map')
title.Draw()
canvas.SaveAs('{}/ch4mu_vr_dphiiso_closuremap.pdf'.format(outdir))
canvas.Clear()


hc = create_closeness_map(h)
hc.Draw('colz')
hc.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
title = TitleAsLatex('[4#mu VR] '+h.title+' closeness map')
title.Draw()

canvas.SaveAs('{}/ch4mu_vr_dphiiso_closeness.pdf'.format(outdir))
canvas.Clear()


f.close()


###########################


fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/proxy_2mu2e.root')
f = root_open(fn)

### init closeness
h = f.ch2mu2e.data.dphiIso2Dinit

hc = create_closeness_map(h)
hc.Draw('colz')
hc.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
title = TitleAsLatex('[2#mu2e VR] '+h.title+' closeness map')
title.Draw()
canvas.SaveAs('{}/ch2mu2e_vr_dphiisoInit_closeness_noscale.pdf'.format(outdir))
canvas.Clear()

hc, ave_closure, ave_closure_sqrd = create_closure_map(h)
hc.Draw('colz text')
hc.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
hc.zaxis.SetRangeUser(0,1)
title = TitleAsLatex('[2#mu2e VR] '+h.title+' closure map')
title.Draw()
canvas.SaveAs('{}/ch2mu2e_vr_dphiisoInit_closuremap_noscale.pdf'.format(outdir))
canvas.Clear()

#############################

h = f.ch2mu2e.data.dphiIso2D

hc = create_closeness_map(h)
hc.Draw('colz')
hc.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
title = TitleAsLatex('[2#mu2e VR] '+h.title+' closeness map')
title.Draw()
canvas.SaveAs('{}/ch2mu2e_vr_dphiiso_closeness_noscale.pdf'.format(outdir))
canvas.Clear()

h.scale(57.3/h.integral())

h.Draw('colz')
h.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
title = TitleAsLatex('[2#mu2e VR] '+h.title)
title.Draw()
canvas.SaveAs('{}/ch2mu2e_vr_dphiiso.pdf'.format(outdir))
canvas.Clear()

hc, ave_closure, ave_closure_sqrd = create_closure_map(h)
print('Average closure: {:.3f}'.format(ave_closure))
print('Spread: {:.3f}'.format(math.sqrt(abs(ave_closure_sqrd-ave_closure**2))))

hc.Draw('colz text')
hc.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
hc.zaxis.SetRangeUser(0,1)
title = TitleAsLatex('[2#mu2e VR] '+h.title+' closure map')
title.Draw()
canvas.SaveAs('{}/ch2mu2e_vr_dphiiso_closuremap.pdf'.format(outdir))
canvas.Clear()

hc = create_closeness_map(h)
hc.Draw('colz')
hc.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
title = TitleAsLatex('[2#mu2e VR] '+h.title+' closeness map')
title.Draw()

canvas.SaveAs('{}/ch2mu2e_vr_dphiiso_closeness.pdf'.format(outdir))
canvas.Clear()

f.close()


fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/modules/myworkflow.root')
f = root_open(fn)

fout = root_open('out.root', 'recreate')
h = f.ch4mu.data.dphiIso2D
print('4mu: correlation factor ', h.get_correlation_factor())

# for i in range(14+1, h.nbins(0)+1):
#     for j in range(1, h.nbins(1)+1):
#         h.SetBinContent(i,j,0)
h.Draw('colz')
h.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
title = TitleAsLatex('[4#mu SR] '+h.title)
title.Draw()
blind_region = ROOT.TBox(h.xedges(14+1), h.yaxis.GetXmin(),
                         h.xaxis.GetXmax(), h.yaxis.GetXmax())
blind_region.SetFillStyle(3345)
blind_region.SetFillColor(ROOT.kGray+2)
blind_region.Draw('same')
canvas.SaveAs('{}/ch4mu_sr_dphiiso.pdf'.format(outdir))
canvas.Clear()


hc, ave_closure, ave_closure_sqrd = create_closure_map(h)
print('Average closure: {:.3f}'.format(ave_closure))
print('Spread: {:.3f}'.format(math.sqrt(abs(ave_closure_sqrd-ave_closure**2))))
hc.Draw('colz text')
hc.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
hc.SetName('ch4mu')
hc.write()
hc.zaxis.SetRangeUser(0,2)
title = TitleAsLatex('[4#mu SR] '+h.title+' closure map')
title.Draw()
canvas.SaveAs('{}/ch4mu_sr_dphiiso_closuremap.pdf'.format(outdir))
canvas.Clear()


hc = create_closeness_map(h)
hc.Draw('colz')
hc.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
title = TitleAsLatex('[4#mu SR] '+h.title+' closeness map')
title.Draw()
canvas.SaveAs('{}/ch4mu_sr_dphiiso_closeness.pdf'.format(outdir))
canvas.clear()


h= f.ch2mu2e.data.dphiEgmIso2D
print('2mu2e: correlation factor ', h.get_correlation_factor())

# for i in range(14+1, h.nbins(0)+1):
#     for j in range(1, h.nbins(1)+1):
#         h.SetBinContent(i,j,0)
h.Draw('colz')
h.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
title = TitleAsLatex('[2#mu2e SR] '+h.title)
title.Draw()
blind_region = ROOT.TBox(h.xedges(14+1), h.yaxis.GetXmin(),
                         h.xaxis.GetXmax(), h.yaxis.GetXmax())
blind_region.SetFillStyle(3345)
blind_region.SetFillColor(ROOT.kGray+2)
blind_region.Draw('same')
canvas.SaveAs('{}/ch2mu2e_sr_dphiiso.pdf'.format(outdir))
canvas.Clear()


hc, ave_closure, ave_closure_sqrd = create_closure_map(h)
print('Average closure: {:.3f}'.format(ave_closure))
print('Spread: {:.3f}'.format(math.sqrt(abs(ave_closure_sqrd-ave_closure**2))))
hc.Draw('colz text')
hc.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
hc.zaxis.SetRangeUser(0,1)
hc.SetName('ch2mu2e')
hc.write()
title = TitleAsLatex('[2#mu2e SR] '+h.title+' closure map')
title.Draw()
canvas.SaveAs('{}/ch2mu2e_sr_dphiiso_closuremap.pdf'.format(outdir))
canvas.Clear()

hc = create_closeness_map(h)
hc.Draw('colz')
hc.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
title = TitleAsLatex('[2#mu2e SR] '+h.title+' closeness map')
title.Draw()
canvas.SaveAs('{}/ch2mu2e_sr_dphiiso_closeness.pdf'.format(outdir))
canvas.clear()

fout.close()

f.close()