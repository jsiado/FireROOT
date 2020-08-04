#!/usr/bin/env python
from __future__ import print_function
import os, math
import ROOT
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas
from rootpy.plotting.shapes import Line

from FireROOT.Analysis.samples.signalnumbers import genxsec
from FireROOT.Analysis.Utils import *


def calculate_za(s, b, sigma_b):
    first_term = (s+b)*math.log( ( (s+b)*(b+sigma_b**2) )/(b**2+(s+b)*sigma_b**2) )
    second_term = (b**2/sigma_b**2)*math.log( 1+(sigma_b**2*s)/(b*(b+sigma_b**2)) )
    try:
        return math.sqrt(2*(first_term-second_term))
    except:
        return 0


def create_za_map(sh, bh, optm_region=None):
    shc = sh.clone()
    bhc = bh.clone()
    zah = bhc.clone()
    zah.Reset()

    for i in range(1, bhc.GetNbinsX()):
        for j in range(1, bhc.GetNbinsY()):
            if optm_region and optm_region.GetBinContent(i,j)==0: continue

            bh_c = bhc.integral(1,i,1,j)
            bh_d = bhc.integral(i+1,bhc.GetNbinsX(),1,j)
            bh_a = bhc.integral(1,i,j+1,bhc.GetNbinsY())
            bh_b = bhc.integral(i+1,bhc.GetNbinsX(),j+1,bhc.GetNbinsY())

            bkg_ = bh_b*bh_c/bh_a
            sigma_b = bkg_*math.sqrt(1/bh_a + 1/bh_b + 1/bh_c)

            sig_ = shc.integral(i+1,shc.GetNbinsX(),1,j)
            za_ = calculate_za(sig_, bkg_, sigma_b)
            zah.SetBinContent(i,j,za_)

    zah.axis(2).SetTitle('Z_{A}')
    xax = zah.xaxis
    decorate_axis_pi(xax)

    return zah


def create_occupancy_map(h, thres=2, blindBD=False):
    hc = h.clone()
    hc.Reset()
    for i in range(1, h.GetNbinsX()):
        for j in range(1, h.GetNbinsY()):
            bh_c = h.integral(1,i,1,j)
            bh_d = h.integral(i+1,h.GetNbinsX(),1,j)
            bh_a = h.integral(1,i,j+1,h.GetNbinsY())
            bh_b = h.integral(i+1,h.GetNbinsX(),j+1,h.GetNbinsY())

            if blindBD:
                if bh_a<thres or bh_c<thres or i>14:
                    hc.SetBinContent(i,j,0)
                else: hc.SetBinContent(i,j,thres)
            else:
                if bh_a<thres or bh_b<thres or bh_c<thres:
                    hc.SetBinContent(i,j,0)
                else: hc.SetBinContent(i,j,thres)

    xax = hc.xaxis
    decorate_axis_pi(xax)

    return hc


def combine_occupancy_map(bkgh_occu, datah_occu, thres=3):
    hc = bkgh_occu.clone()
    hc.Reset()
    for i in range(1, hc.GetNbinsX()):
        for j in range(1, hc.GetNbinsY()):
            # In unblinded region, opimization region=overlap(bkgh_occu, datah_occu)
            if i<=14:
                if bkgh_occu.GetBinContent(i,j)>=thres and datah_occu.GetBinContent(i,j)>=thres:
                    hc.SetBinContent(i,j, thres)
                else: hc.SetBinContent(i,j, 0)
            # In blinded region, opimization region=bkgh_occu
            else:
                if bkgh_occu.GetBinContent(i,j)>=thres:
                    hc.SetBinContent(i,j, thres)
                else: hc.SetBinContent(i,j, 0)

    xax = hc.xaxis
    decorate_axis_pi(xax)

    return hc


def mark_maximum_bin(h):
    maxbin = h.GetMaximumBin()
    maxval = h.GetMaximum()
    i, j, k = ROOT.Long(), ROOT.Long(), ROOT.Long()
    h.GetBinXYZ(maxbin, i,j,k)
    xedge = h.xedges(i+1)
    yedge = h.yedges(j+1)
    # print(i,j, maxval)
    marker_x = (xedge+h.xedges(i))/2.
    marker_y = (yedge+h.yedges(j))/2.
    g = ROOT.TGraph(1)
    g.SetPoint(0, marker_x, marker_y)
    g.SetMarkerStyle(28)
    g.SetMarkerSize(1.4)
    return g, xedge, yedge, maxval


if __name__ == '__main__':

    sigfn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/modules/myworkflow.root')
    bkgfn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/proxy_4mu.root')

    outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/optimizeABCD')
    if not os.path.isdir(outdir): os.makedirs(outdir)

    set_style(MyStyle())
    ROOT.gStyle.SetPadLeftMargin(0.11)
    ROOT.gStyle.SetPadRightMargin(0.11)
    ROOT.gStyle.SetPalette(ROOT.kBird)

    canvas = Canvas()
    ROOT.gPad.SetGrid()

    sigf = root_open(sigfn)
    bkgf = root_open(bkgfn)



    ######## Optimization region from VR ########
    bkgh = bkgf.ch4mu.data.dphiIso2D
    bkgh.scale(84.2/bkgh.integral())
    bkgh.Draw('colz')
    bkgh.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
    canvas.SaveAs('{}/ch4mu_bkg.pdf'.format(outdir))
    canvas.Clear()

    bkgh_occu = create_occupancy_map(bkgh, thres=3)
    bkgh_occu.Draw('colz')
    bkgh_occu.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
    title = TitleAsLatex('[4#mu VR] optimization region')
    title.Draw()
    canvas.SaveAs('{}/ch4mu_bkg_occupancy.pdf'.format(outdir))
    canvas.Clear()
    #############################################


    ######## Optimization region from SR ########
    datah = sigf.ch4mu.data.dphiIso2D

    datah_occu = create_occupancy_map(datah, thres=3, blindBD=True)
    datah_occu.Draw('colz')
    datah_occu.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
    title = TitleAsLatex('[4#mu SR] optimization region (from region AC)')
    title.Draw()
    blind_region = ROOT.TBox(datah_occu.xedges(14+1), datah_occu.yedges(1),
                            datah_occu.xedges(datah_occu.nbins(0)+1),
                            datah_occu.yedges(datah_occu.nbins(1)+1))
    blind_region.SetFillStyle(3345)
    blind_region.SetFillColor(ROOT.kGray+2)
    blind_region.Draw('same')
    canvas.SaveAs('{}/ch4mu_sig_occupancy.pdf'.format(outdir))
    canvas.Clear()
    #############################################


    ######## Optimization region combined ########
    comb_occu = combine_occupancy_map(bkgh_occu, datah_occu)
    comb_occu.Draw('colz')
    comb_occu.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)

    title = TitleAsLatex('[4#mu] combined optimization region')
    title.Draw()
    canvas.SaveAs('{}/ch4mu_comb_occupancy.pdf'.format(outdir))
    canvas.Clear()
    #############################################


    for sigtag in sigTAGS:
        sigh = getattr(sigf.ch4mu.sig, sigtag).dphiIso2D
        mboundstate = int(sigtag.split('_')[0].replace('mXX-', ''))
        sigh.scale( 30./genxsec[mboundstate] )

        zah = create_za_map(sigh, bkgh, optm_region=comb_occu)
        zah.Draw('colz')
        zah.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
        mkh, xedge, yedge, maxval = mark_maximum_bin(zah)
        label = '(|#Delta#phi|, iso): {:.2f}, {:.2f} '.format(xedge, yedge)+'Z_{A}: '+'{:.3f}'.format(maxval)
        mkh.Draw('p same')
        title = TitleAsLatex('[4#mu {}] '.format(sigtag)+'proxy significance Z_{A}')
        title.Draw()
        leg = Legend(1, margin=0.25, leftmargin=0.05, rightmargin=0.5, topmargin=0.05,
                entrysep=0.01, entryheight=0.02, textsize=15)
        leg.AddEntry(mkh, label=label)
        leg.Draw()
        canvas.SaveAs('{}/ch4mu_{}.pdf'.format(outdir, sigtag))
        canvas.Clear()

        sigc = sigh.clone()
        sigc.Draw('colz')
        sigc.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
        title = TitleAsLatex('[4#mu SR {}] '.format(sigtag)+'|#Delta#phi| vs. maxIso')
        title.Draw()
        decorate_axis_pi(sigc.xaxis)
        hline = Line(sigc.xaxis.GetXmin(), yedge, sigc.xaxis.GetXmax(), yedge)
        vline = Line(xedge, sigc.yaxis.GetXmin(), xedge, sigc.yaxis.GetXmax())
        for l in [hline, vline]:
            l.linewidth=2
            l.color='red'
            l.Draw()
        canvas.SaveAs('{}/ch4mu_isodphi_{}.pdf'.format(outdir, sigtag))
        canvas.Clear()


    bkgf.close()

    #########################################
    bkgfn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/proxy_2mu2e.root')
    bkgf = root_open(bkgfn)

    bkgh = bkgf.ch2mu2e.data.dphiIso2D
    bkgh.scale(57.3/bkgh.integral())
    bkgh.Draw('colz')
    bkgh.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
    canvas.SaveAs('{}/ch2mu2e_bkg.pdf'.format(outdir))
    canvas.Clear()

    bkgh_occu = create_occupancy_map(bkgh, thres=3)
    bkgh_occu.Draw('colz')
    bkgh_occu.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
    title = TitleAsLatex('[2#mu2e VR] optimization region')
    title.Draw()
    canvas.SaveAs('{}/ch2mu2e_bkg_occupancy.pdf'.format(outdir))
    canvas.Clear()


    ######## Optimization region from SR ########
    datah = sigf.ch2mu2e.data.dphiEgmIso2D

    datah_occu = create_occupancy_map(datah, thres=3, blindBD=True)
    datah_occu.Draw('colz')
    datah_occu.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
    title = TitleAsLatex('[2#mu2e SR] optimization region (from region AC)')
    title.Draw()
    blind_region = ROOT.TBox(datah_occu.xedges(14+1), datah_occu.yedges(1),
                            datah_occu.xedges(datah_occu.nbins(0)+1),
                            datah_occu.yedges(datah_occu.nbins(1)+1))
    blind_region.SetFillStyle(3345)
    blind_region.SetFillColor(ROOT.kGray+2)
    blind_region.Draw('same')
    canvas.SaveAs('{}/ch2mu2e_sig_occupancy.pdf'.format(outdir))
    canvas.Clear()
    #############################################

    ######## Optimization region combined ########
    comb_occu = combine_occupancy_map(bkgh_occu, datah_occu)
    comb_occu.Draw('colz')
    comb_occu.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)

    title = TitleAsLatex('[2#mu2e] combined optimization region')
    title.Draw()
    canvas.SaveAs('{}/ch2mu2e_comb_occupancy.pdf'.format(outdir))
    canvas.Clear()
    #############################################


    for sigtag in sigTAGS:
        sigh = getattr(sigf.ch2mu2e.sig, sigtag).dphiEgmIso2D
        mboundstate = int(sigtag.split('_')[0].replace('mXX-', ''))
        sigh.scale( 30./genxsec[mboundstate] )

        zah = create_za_map(sigh, bkgh, optm_region=comb_occu)
        zah.Draw('colz')
        zah.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
        mkh, xedge, yedge, maxval = mark_maximum_bin(zah)
        label = '(|#Delta#phi|, iso): {:.2f}, {:.2f} '.format(xedge, yedge)+'Z_{A}: '+'{:.3f}'.format(maxval)
        mkh.Draw('p same')
        title = TitleAsLatex('[2#mu2e {}] '.format(sigtag)+'proxy significance Z_{A}')
        title.Draw()
        leg = Legend(1, margin=0.25, leftmargin=0.05, rightmargin=0.5, topmargin=0.05,
                entrysep=0.01, entryheight=0.02, textsize=15)
        leg.AddEntry(mkh, label=label)
        leg.Draw()
        canvas.SaveAs('{}/ch2mu2e_{}.pdf'.format(outdir, sigtag))
        canvas.Clear()

        sigc = sigh.clone()
        sigc.Draw('colz')
        if sigc.integral()!=0:
            sigc.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
        title = TitleAsLatex('[2#mu2e SR {}] '.format(sigtag)+'|#Delta#phi| vs. Iso')
        title.Draw()
        decorate_axis_pi(sigc.xaxis)
        hline = Line(sigc.xaxis.GetXmin(), yedge, sigc.xaxis.GetXmax(), yedge)
        vline = Line(xedge, sigc.yaxis.GetXmin(), xedge, sigc.yaxis.GetXmax())
        for l in [hline, vline]:
            l.linewidth=2
            l.color='red'
            l.Draw()
        canvas.SaveAs('{}/ch2mu2e_isodphi_{}.pdf'.format(outdir, sigtag))
        canvas.Clear()


    bkgf.close()
    sigf.close()