#!/usr/bin/env python
from __future__ import print_function
import os
import ROOT
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas

from FireROOT.Analysis.Utils import *

fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/additionalVariables.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/massXX')
if not os.path.isdir(outdir): os.makedirs(outdir)
# for d in ['ch2mu2e', 'ch4mu']:
#     _o = os.path.join(outdir, d)
#     if not os.path.isdir(_o):
#         os.makedirs(_o)
sty = MyStyle()
sty.SetOptStat(0)
sty.SetStatX(0.9)
sty.SetStatY(0.9)
sty.SetStatTextColor(ROOT.kRed)
sty.SetStatBorderSize(0)
set_style(sty)


def plot_4mu(masstag):
    mxx = masstag.split('_')[0].split('-')[1]
    ma = masstag.split('_')[1].split('-')[1].replace('p', '.')
    lxy = masstag.split('_')[2].split('-')[1].replace('p', '.')
    h = getattr(getattr(f.ch4mu.sig, masstag), 'invm_e{}'.format(mxx))
    h.color = 'blue'
    h.linewidth = 2
    h.drawstyle = 'hist'
    h.axis(0).SetTitle('lepton-jet pair invariant mass [GeV]')

    _fit = ROOT.TF1('_fit', 'gaus', float(mxx)/10*7, float(mxx)/10*13)
    _fit.SetLineColor(ROOT.kRed)
    _fit.SetLineWidth(2)
    h.Fit('_fit', 'QR')

    # print(_fit.GetChisquare(), _fit.GetNDF())
    # print(_fit.GetParameter(0), _fit.GetParameter(1), _fit.GetParameter(2))

    hs = [h,]

    xmin_, xmax_, ymin_, ymax_ = get_limits(hs)
    draw(hs, pad=c, ylimits=(0, ymax_))
    _fit.Draw('same')
    t = ROOT.TPaveText(0.25, 0.78, 0.5, 0.9, 'NB NDC')
    t.AddText('#chi#chi#rightarrow2A#rightarrow4#mu')
    t.AddText('m_{#chi#chi} = '+mxx+' GeV')
    t.AddText('m_{A} = '+ma+' GeV')
    t.AddText('lxy = '+lxy+' cm')
    t.SetTextColor(ROOT.kBlue)
    t.SetTextFont(42)
    t.SetTextSize(0.025)
    t.SetFillColor(0)
    t.Draw()
    c.SaveAs(os.path.join(outdir, 'ch4mu_{}.pdf'.format(masstag) ))

def plot_2mu2e(masstag):
    mxx = masstag.split('_')[0].split('-')[1]
    ma = masstag.split('_')[1].split('-')[1].replace('p', '.')
    lxy = masstag.split('_')[2].split('-')[1].replace('p', '.')
    h = getattr(getattr(f.ch2mu2e.sig, masstag), 'invm_e{}'.format(mxx))
    h.color = 'blue'
    h.linewidth = 2
    h.drawstyle = 'hist'
    h.axis(0).SetTitle('lepton-jet pair invariant mass [GeV]')

    _fit = ROOT.TF1('_fit', 'gaus', float(mxx)/10*7, float(mxx)/10*13)
    _fit.SetLineColor(ROOT.kRed)
    _fit.SetLineWidth(2)
    h.Fit('_fit', 'QR')

    # print(_fit.GetChisquare(), _fit.GetNDF())
    # print(_fit.GetParameter(0), _fit.GetParameter(1), _fit.GetParameter(2))

    hs = [h,]

    xmin_, xmax_, ymin_, ymax_ = get_limits(hs)
    draw(hs, pad=c, ylimits=(0, ymax_))
    _fit.Draw('same')
    t = ROOT.TPaveText(0.25, 0.78, 0.5, 0.9, 'NB NDC')
    t.AddText('#chi#chi#rightarrow2A#rightarrow2#mu2e')
    t.AddText('m_{#chi#chi} = '+mxx+' GeV')
    t.AddText('m_{A} = '+ma+' GeV')
    t.AddText('lxy = '+lxy+' cm')
    t.SetTextColor(ROOT.kBlue)
    t.SetTextFont(42)
    t.SetTextSize(0.025)
    t.SetFillColor(0)
    t.Draw()
    c.SaveAs(os.path.join(outdir, 'ch2mu2e_{}.pdf'.format(masstag) ))

f = root_open(fn)
c = Canvas()

# masstag = 'mXX-500_mA-1p2_lxy-300'
masstags = [k.name for k in f.ch4mu.sig.keys()]
for mt in masstags:
    plot_4mu(mt)
    c.clear()
masstags = [k.name for k in f.ch2mu2e.sig.keys()]
for mt in masstags:
    plot_2mu2e(mt)
    c.clear()
f.close()