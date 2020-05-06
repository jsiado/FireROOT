#!/usr/bin/env python
from __future__ import print_function
import os, math
import ROOT
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas

from FireROOT.Analysis.samples.signalnumbers import genxsec
from FireROOT.Analysis.Utils import *

sigfn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/displacementVariables.root')
bkgfn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/proxy_4mu.root')
sigabcdfn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/myworkflow.root')

outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/optimized0')
if not os.path.isdir(outdir): os.makedirs(outdir)


def calculate_simpsig(s, b):
    return s/math.sqrt(b)

# def calculate_za(s, b):
#     """sigma_b = sqrt(b), just possion error"""
#     first = (s+b)*math.log(2*(s+b)/(s+2*b))
#     second = b*math.log(1+s/(2*b))
#     return math.sqrt(2*(first-second))

def calculate_za(s, b, sigma_b):
    first_term = (s+b)*math.log( ( (s+b)*(b+sigma_b**2) )/(b**2+(s+b)*sigma_b**2) )
    second_term = (b**2/sigma_b**2)*math.log( 1+(sigma_b**2*s)/(b*(b+sigma_b**2)) )
    try:
        return math.sqrt(2*(first_term-second_term))
    except:
        return 0


def extract_background(bkgh):
    nbinsX, nbinsY = bkgh.nbins(0), bkgh.nbins(1)
    xbound = bkgh.xaxis.FindBin(2.2)
    ybound = bkgh.yaxis.FindBin(0.15)

    NB = bkgh.integral(xbound, nbinsX, ybound, nbinsY)
    NA = bkgh.integral(1, xbound-1, ybound, nbinsY)
    NC = bkgh.integral(1, xbound-1, 1, ybound-1)
    ND = bkgh.integral(xbound, nbinsX, 1, ybound-1)
    sigma_d = ND*math.sqrt(1/NA + 1/NB + 1/NC)

    return ND, sigma_d

def extract_signal_d(sigh):
    nbinsX, nbinsY = sigh.nbins(0), sigh.nbins(1)
    xbound = sigh.xaxis.FindBin(2.2)
    ybound = sigh.yaxis.FindBin(0.15)

    ND = sigh.integral(xbound, nbinsX, 1, ybound-1)
    return ND

set_style(MyStyle())
canvas = Canvas()
ROOT.gPad.SetGrid()

sigf = root_open(sigfn)
bkgf = root_open(bkgfn)
sigabcdf = root_open(sigabcdfn)

bkgh = bkgf.ch4mu.data.muljd0.clone()
binnum = bkgh.xaxis.FindBin(100)
bkgh.scale(40.6/bkgh.integral(xbin1=binnum, overflow=True))
bkgh.drawstyle='hist'
bkgh.fillstyle='solid'
bkgh.legendstyle='F'
bkgh.linewidth=0
bkgh.fillcolor=sigCOLORS[-2]
bkgh.title='Background'
bkgh.SetBinContent(bkgh.nbins(), bkgh.GetBinContent(bkgh.nbins())+bkgh.overflow())
for i in range(1,binnum): bkgh.SetBinContent(i, 0)

sighs = []
for it, sigtag in enumerate(sigTAGS):
    h = getattr(sigf.ch4mu.sig, sigtag).mind0.clone()
    mboundstate = int(sigtag.split('_')[0].replace('mXX-', ''))
    h.scale( 30./genxsec[mboundstate] )
    h.SetBinContent(h.nbins(), h.GetBinContent(h.nbins())+h.overflow())
    for i in range(1,binnum): h.SetBinContent(i, 0)
    h.drawstyle='hist'
    h.color=sigCOLORS[it]
    h.linewidth=2
    h.title=sigtag+' (norm. 30fb)'
    h.legendstyle='L'
    sighs.append(h)

draw([bkgh]+sighs, ylimits=(1e-5,1e4), logy=True)
leg = Legend([bkgh]+sighs, pad=canvas,
            margin=0.25, leftmargin=0.45, topmargin=0.02,
            entrysep=0.01, entryheight=0.02, textsize=10)
leg.Draw()
title = TitleAsLatex('[4#mu] lepton-jet |d_{0}|')
title.Draw()


canvas.SaveAs('{}/ch4mu_muljd0.pdf'.format(outdir))
canvas.clear()

signalsigs = []
for h in sighs:
    h_ = h.clone()
    for i in range(binnum, h.nbins()+1):
        bkg_tot = bkgh.integral(xbin1=i, overflow=True)
        bkg_abcd = bkgf.ch4mu.data.dphiIso2D.clone()
        bkg_abcd.scale( bkg_tot/bkg_abcd.integral() )
        b, sigma_b = extract_background(bkg_abcd)

        sig_tot = h.integral(xbin1=i, overflow=True)
        sigtag = h.title.split(' ')[0]
        sig_abcd = getattr(sigabcdf.ch4mu.sig, sigtag).dphiIso2Dinc.clone()
        sig_abcd.scale( sig_tot/sig_abcd.integral() )
        s = extract_signal_d(sig_abcd)

        h_[i] = calculate_za(s, b, sigma_b)
        h_[i].error = 0
    h_.scale(1/h_.integral())
    signalsigs.append(h_)

ROOT.gPad.SetLogy(0)
draw(signalsigs[:], ylimits=(0.025,0.06), ytitle='Z_{A} A.U.')
leg = Legend(signalsigs, pad=canvas,
            margin=0.25, leftmargin=0.45, topmargin=0.02,
            entrysep=0.01, entryheight=0.02, textsize=10)
leg.Draw()
title.Draw()

canvas.SaveAs('{}/ch4mu_muljd0significance.pdf'.format(outdir))
canvas.clear()


#########################################

bkgh = bkgf.ch4mu.data.muljd0.clone()
binnum = bkgh.xaxis.FindBin(100)
bkgh.scale(287.5/bkgh.integral(xbin1=binnum, overflow=True))
bkgh.drawstyle='hist'
bkgh.fillstyle='solid'
bkgh.legendstyle='F'
bkgh.linewidth=0
bkgh.fillcolor=sigCOLORS[-2]
bkgh.title='Background'
bkgh.SetBinContent(bkgh.nbins(), bkgh.GetBinContent(bkgh.nbins())+bkgh.overflow())
for i in range(1,binnum): bkgh.SetBinContent(i, 0)


sighs = []
for it, sigtag in enumerate(sigTAGS):
    h = getattr(sigf.ch2mu2e.sig, sigtag).mind0.clone()
    mboundstate = int(sigtag.split('_')[0].replace('mXX-', ''))
    h.scale( 30./genxsec[mboundstate] )
    h.SetBinContent(h.nbins(), h.GetBinContent(h.nbins())+h.overflow())
    for i in range(1,binnum): h.SetBinContent(i, 0)
    h.drawstyle='hist'
    h.color=sigCOLORS[it]
    h.linewidth=2
    h.title=sigtag+' (norm. 30fb)'
    h.legendstyle='L'
    sighs.append(h)

draw([bkgh]+sighs, ylimits=(1e-5,1e4), logy=True)
leg = Legend([bkgh]+sighs, pad=canvas,
            margin=0.25, leftmargin=0.45, topmargin=0.02,
            entrysep=0.01, entryheight=0.02, textsize=10)
leg.Draw()
title = TitleAsLatex('[2#mu2e] lepton-jet |d_{0}|')
title.Draw()


canvas.SaveAs('{}/ch2mu2e_muljd0.pdf'.format(outdir))
canvas.clear()

# background abcd histogram
ch2mu2efn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/proxy_2mu2e.root')
ch2mu2ef = root_open(ch2mu2efn)

signalsigs = []
for h in sighs:
    h_ = h.clone()
    for i in range(binnum, h.nbins()+1):
        bkg_tot = bkgh.integral(xbin1=i, overflow=True)
        bkg_abcd = ch2mu2ef.ch2mu2e.data.dphiIso2D.clone()
        bkg_abcd.scale( bkg_tot/bkg_abcd.integral() )
        b, sigma_b = extract_background(bkg_abcd)

        sig_tot = h.integral(xbin1=i, overflow=True)
        sigtag = h.title.split(' ')[0]
        sig_abcd = getattr(sigabcdf.ch2mu2e.sig, sigtag).dphiEgmIso2Dinc.clone()
        sig_abcd.scale( sig_tot/sig_abcd.integral() )
        s = extract_signal_d(sig_abcd)

        h_[i] = calculate_za(s, b, sigma_b)
        h_[i].error = 0
    h_.scale(1/h_.integral())
    signalsigs.append(h_)


ROOT.gPad.SetLogy(0)
draw(signalsigs[:], ylimits=(0.01,0.07), pad=canvas, ytitle='Z_{A} A.U.')
leg = Legend(signalsigs, pad=canvas,
            margin=0.25, leftmargin=0.45, topmargin=0.02,
            entrysep=0.01, entryheight=0.02, textsize=10)
leg.Draw()
title.Draw()

canvas.SaveAs('{}/ch2mu2e_muljd0significance.pdf'.format(outdir))
canvas.clear()

ch2mu2ef.close()

sigabcdf.close()
sigf.close()
bkgf.close()