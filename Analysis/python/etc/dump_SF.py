#!/usr/bin/env python
from __future__ import print_function
import os
import ROOT
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas

from FireROOT.Analysis.Utils import *

BASEDIR = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/data')
electronSF_f = os.path.join(BASEDIR, '2018_ElectronLoose.root')
photonSF_f   = os.path.join(BASEDIR, '2018_PhotonsLoose.root')
pfmuonSF1_f  = os.path.join(BASEDIR, 'RunABCD_SF_ID.root')
pfmuonSF0_f  = os.path.join(BASEDIR, 'mu_Loose_pt7.root')

outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/dump_SF')
if not os.path.isdir(outdir): os.makedirs(outdir)

set_style(MyStyle())
ROOT.gStyle.SetPaintTextFormat('.3f')
canvas = Canvas()

##################################################
electronSF_h = root_open(electronSF_f).EGamma_SF2D
ROOT.gPad.SetLogy()
electronSF_h.yaxis.SetMoreLogLabels()
electronSF_h.yaxis.SetNoExponent()
electronSF_h.yaxis.SetLabelSize(0.03)
electronSF_h.yaxis.SetTitleSize(0.03)
electronSF_h.yaxis.SetTitleOffset(2)
electronSF_h.xaxis.SetLabelSize(0.03)
electronSF_h.xaxis.SetTitleSize(0.03)
electronSF_h.xaxis.SetTitleOffset(1.5)

electronSF_h.drawstyle = 'col text'
electronSF_h.Draw()

YearLabel = LuminosityLabel('2018')
YearLabel.draw()
title = TitleAsLatex('Electron Scale Factor')
title.Draw()

canvas.SaveAs('%s/electronSF.pdf'%outdir)
canvas.clear()

#-------------------------------------------------
electronSyst_h = electronSF_h.clone()
electronSyst_h.Reset()
for i in range(1, electronSF_h.nbins(0)+1):
    for j in range(1, electronSF_h.nbins(1)+1):
        # print(electronSF_h.GetBinError(i,j), electronSF_h.GetBinErrorUp(i,j), electronSF_h.GetBinErrorLow(i,j))
        electronSyst_h.SetBinContent(i, j, electronSF_h.GetBinError(i,j))

electronSyst_h.zaxis.SetRangeUser(0, 0.07)
electronSyst_h.Draw()

YearLabel = LuminosityLabel('2018')
YearLabel.draw()
title = TitleAsLatex('Electron SF systematic error')
title.Draw()

canvas.SaveAs('%s/electronSFsyst.pdf'%outdir)
canvas.clear()

##################################################

##################################################
photonSF_h = root_open(photonSF_f).EGamma_SF2D
ROOT.gPad.SetLogy()
photonSF_h.yaxis.SetMoreLogLabels()
photonSF_h.yaxis.SetNoExponent()
photonSF_h.yaxis.SetLabelSize(0.03)
photonSF_h.yaxis.SetTitleSize(0.03)
photonSF_h.yaxis.SetTitleOffset(2)
photonSF_h.xaxis.SetLabelSize(0.03)
photonSF_h.xaxis.SetTitleSize(0.03)
photonSF_h.xaxis.SetTitleOffset(1.5)

photonSF_h.drawstyle = 'col text'
photonSF_h.Draw()

YearLabel = LuminosityLabel('2018')
YearLabel.draw()
title = TitleAsLatex('Photon Scale Factor')
title.Draw()

canvas.SaveAs('%s/photonSF.pdf'%outdir)
canvas.clear()

#-------------------------------------------------
photonSyst_h = photonSF_h.clone()
photonSyst_h.Reset()
for i in range(1, photonSF_h.nbins(0)+1):
    for j in range(1, photonSF_h.nbins(1)+1):
        photonSyst_h.SetBinContent(i, j, photonSF_h.GetBinError(i,j))

photonSyst_h.zaxis.SetRangeUser(0, 0.07)
photonSyst_h.Draw()

YearLabel = LuminosityLabel('2018')
YearLabel.draw()
title = TitleAsLatex('Photon SF systematic error')
title.Draw()

canvas.SaveAs('%s/photonSFsyst.pdf'%outdir)
canvas.clear()

##################################################

##################################################
pfmuonSF1_h = root_open(pfmuonSF1_f).NUM_LooseID_DEN_TrackerMuons_pt_abseta_syst
ROOT.gPad.SetLogy(0)
ROOT.gPad.SetLogx()
pfmuonSF1_h.xaxis.SetMoreLogLabels()
pfmuonSF1_h.drawstyle='col text'
pfmuonSF1_h.Draw()

YearLabel = LuminosityLabel('2018')
YearLabel.draw()
title = TitleAsLatex('PF muon Scale Factor')
title.Draw()

canvas.SaveAs('%s/pfmuon1SF.pdf'%outdir)
canvas.clear()

#-------------------------------------------------
pfmuonSyst1_h = pfmuonSF1_h.clone()
pfmuonSyst1_h.Reset()

for i in range(1, pfmuonSF1_h.nbins(0)+1):
    for j in range(1, pfmuonSF1_h.nbins(1)+1):
        pfmuonSyst1_h.SetBinContent(i, j, pfmuonSF1_h.GetBinError(i,j))

# pfmuonSyst1_h.zaxis.SetRangeUser(0, 0.07)
pfmuonSyst1_h.Draw()

YearLabel = LuminosityLabel('2018')
YearLabel.draw()
title = TitleAsLatex('PF muon SF systematic error')
title.Draw()

canvas.SaveAs('%s/pfmuon1SFsyst.pdf'%outdir)
canvas.clear()
##################################################

##################################################
pfmuonSF0_g = root_open(pfmuonSF0_f).ratio_syst
ROOT.gPad.SetLogx(0)
pfmuonSF0_g.xaxis.title='#eta'
pfmuonSF0_g.Draw('ap')

pts = {}
for i in range(pfmuonSF0_g.num_points):
    x = pfmuonSF0_g.x(i)
    xl, xh = x-pfmuonSF0_g.xerrl(i), x+pfmuonSF0_g.xerrh(i)
    yl, yh = 1.009, 1.012
    p = ROOT.TPaveText(xl, yl, xh, yh, 'NB')
    p.AddText('%.3f' % pfmuonSF0_g.y(i))
    p.AddText('#pm{:.3f}'.format( (pfmuonSF0_g.yerrh(i)+pfmuonSF0_g.yerrl(i))/2) )
    pts[i] = p

# draw a description tpavetext
width = pts[0].GetX2() - pts[0].GetX1()
xl, xh = pfmuonSF0_g.xaxis.GetXmin(), -2.15
yl, yh = 1.009, 1.012
p = ROOT.TPaveText(xl, yl, xh, yh, 'NB')
p.AddText("scale factor:")
p.AddText("syst. unc.:")
# p.SetTextAlign(32)
# p.SetTextFont(42)
# p.SetFillColor(0)
# p.Draw()
pts[-1] = p
for i, p in pts.items():
    # if i<0: continue
    p.SetTextAlign(22)
    p.SetTextFont(42)
    p.SetTextSize(0.02)
    # p.SetTextColor(convert_color(sigCOLORS[1], 'root'))
    p.SetFillColor(0)
    p.SetFillStyle(0)
    p.SetBorderSize(0)
    p.Draw()
pts[-1].SetTextAlign(32)
pts[-1].SetTextFont(62)

YearLabel = LuminosityLabel('2018')
YearLabel.draw()
title = TitleAsLatex('PF muon (p_{T}<20GeV) Scale Factor')
title.Draw()

canvas.SaveAs('%s/pfmuon0SF.pdf'%outdir)
canvas.clear()
##################################################
