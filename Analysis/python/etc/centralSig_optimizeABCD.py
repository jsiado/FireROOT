#!/usr/bin/env python
from __future__ import print_function
import os
from collections import OrderedDict
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas
from rootpy.plotting.shapes import Line

from FireROOT.Analysis.samples.signalnumbers import genxsec
from FireROOT.Analysis.Utils import *
from FireROOT.Analysis.etc.optimizeABCD import (
    calculate_za,
    create_za_map,
    create_occupancy_map,
    combine_occupancy_map,
    mark_maximum_bin
)

sigfn  = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/centralSig/leptonIDSyst.root')
datafn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/modules/myworkflow.root')
OUTBASE = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/centralSig/optimizeABCD')
if not os.path.isdir(OUTBASE): os.makedirs(OUTBASE)

NORM_FACTOR_4MU   = 84.2
NORM_FACTOR_2MU2E = 57.3


def routine(chandir, bkgh, optm_region, outdir):
    canvas = Canvas()
    ROOT.gPad.SetGrid()

    for massKey in chandir.keys():
        mboundstate = int(massKey.name.split('_')[0].replace('mXX-', ''))
        NORM_FACTOR_SIGNAL = 30./genxsec[mboundstate] # norm to 30/fb

        massDir = getattr(chandir, massKey.name)
        _outdir = os.path.join(outdir, massKey.name)
        if not os.path.isdir(_outdir): os.makedirs(_outdir)

        boundary_edges = {}
        for lifetimeKey in massDir.keys():
            lifetimeDir = getattr(massDir, lifetimeKey.name)
            sigh = lifetimeDir.dphiIso2D_nominal
            sigh.scale( NORM_FACTOR_SIGNAL )

            ###### ZA map ######
            zah = create_za_map(sigh, bkgh, optm_region=optm_region)
            zah.Draw('colz')
            zah.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
            mkh, xedge, yedge, maxval = mark_maximum_bin(zah)
            boundary_edges[lifetimeKey.name] = (xedge, yedge, maxval) # bookkeeping for overlap plot
            label = '(|#Delta#phi|, iso): {:.2f}, {:.2f} '.format(xedge, yedge)+'Z_{A}: '+'{:.3f}'.format(maxval)
            mkh.Draw('p same')
            if outdir.endswith('ch4mu'):
                title = TitleAsLatex('[4#mu {}] '.format(massKey.name)+'proxy significance Z_{A}')
            if outdir.endswith('ch2mu2e'):
                title = TitleAsLatex('[2#mu2e {}] '.format(massKey.name)+'proxy significance Z_{A}')
            title.Draw()
            leg = Legend(1, margin=0.25, leftmargin=0.05, rightmargin=0.5, topmargin=0.05,
                    entrysep=0.01, entryheight=0.02, textsize=15, header=lifetimeKey.name)
            leg.AddEntry(mkh, label=label)
            leg.Draw()
            canvas.SaveAs('{}/ZA__{}.png'.format(_outdir, lifetimeKey.name))
            canvas.SaveAs('{}/ZA__{}.pdf'.format(_outdir, lifetimeKey.name))
            canvas.Clear()


            ###### signal distribution ######
            sigc = sigh.clone()
            sigc.Draw('colz')
            if sigc.integral():
                sigc.GetListOfFunctions().FindObject("palette").SetX2NDC(0.92)
            if outdir.endswith('ch4mu'):
                title = TitleAsLatex('[4#mu SR {}] '.format(massKey.name)+'|#Delta#phi| vs. maxIso')
            if outdir.endswith('ch2mu2e'):
                title = TitleAsLatex('[2#mu2e SR {}] '.format(massKey.name)+'|#Delta#phi| vs. Iso')
                sigc.yaxis.title='egm lepton-jet iso'
            title.Draw()
            decorate_axis_pi(sigc.xaxis)
            hline = Line(sigc.xaxis.GetXmin(), yedge, sigc.xaxis.GetXmax(), yedge)
            vline = Line(xedge, sigc.yaxis.GetXmin(), xedge, sigc.yaxis.GetXmax())
            for l in [hline, vline]:
                l.linewidth=2
                l.color='red'
                l.Draw()
            canvas.SaveAs('{}/IsoDphi_{}.png'.format(_outdir, lifetimeKey.name))
            canvas.SaveAs('{}/IsoDphi_{}.pdf'.format(_outdir, lifetimeKey.name))
            canvas.Clear()


        ###### optimal boundaries ######

        boundsh = sigh.clone()
        boundsh.Reset()
        boundsh.Draw('col')
        decorate_axis_pi(boundsh.xaxis)
        leg = Legend(len(boundary_edges), margin=0.25, leftmargin=0.05, rightmargin=0.5, topmargin=0.05,
                    entrysep=0.01, entryheight=0.02, textsize=12)

        get_lxy = lambda t : float(t.split('_')[0].split('-')[-1].replace('p', '.'))

        for i, k in enumerate(sorted(boundary_edges, key=get_lxy)):
            bx, by, za = boundary_edges[k]
            hline = Line(boundsh.xaxis.GetXmin(), by, boundsh.xaxis.GetXmax(), by)
            vline = Line(bx, boundsh.yaxis.GetXmin(), bx, boundsh.yaxis.GetXmax())

            label = '{:20}'.format(k)
            label+='({:.2f}, {:.2f})'.format(bx, by)
            label+=' Z_{A}: %.3f'%za
            leg.AddEntry(hline, label=label, style='L')

            for l in (hline, vline):
                l.linewidth=2
                l.color=sigCOLORS[i]
                if i%2==0: l.linestyle='dashed'
                l.Draw()

        leg.Draw()
        if outdir.endswith('ch4mu'):
            title = TitleAsLatex('[4#mu {}] '.format(massKey.name)+'optimial boundaries')
        if outdir.endswith('ch2mu2e'):
            title = TitleAsLatex('[2#mu2e SR {}] '.format(massKey.name)+'optimal boundaries')
        title.Draw()

        canvas.SaveAs('{}/boundaries.png'.format(_outdir))
        canvas.SaveAs('{}/boundaries.pdf'.format(_outdir))
        canvas.Clear()


if __name__ == '__main__':

    set_style(MyStyle())
    ROOT.gStyle.SetPadLeftMargin(0.11)
    ROOT.gStyle.SetPadRightMargin(0.11)


    sigf  = root_open(sigfn)
    dataf = root_open(datafn)

    # ----------------------------------------
    bkgfn  = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/proxy_4mu.root')
    bkgf  = root_open(bkgfn)

    ######## Optimization region from VR ########
    bkgh = bkgf.ch4mu.data.dphiIso2D
    bkgh.scale( NORM_FACTOR_4MU/bkgh.integral() )
    bkgh_occu = create_occupancy_map(bkgh, thres=3)
    ######## Optimization region from SR ########
    datah = dataf.ch4mu.data.dphiIso2D
    datah_occu = create_occupancy_map(datah, thres=3, blindBD=True)
    ######## Optimization region combined ########
    comb_occu = combine_occupancy_map(bkgh_occu, datah_occu)

    outdir = os.path.join(OUTBASE, 'ch4mu')
    routine(chandir=sigf.ch4mu, bkgh=bkgh, optm_region=comb_occu, outdir=outdir)

    bkgf.close()

    # ----------------------------------------


    bkgfn  = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/proxy_2mu2e.root')
    bkgf  = root_open(bkgfn)

    ######## Optimization region from VR ########
    bkgh = bkgf.ch2mu2e.data.dphiIso2D
    bkgh.scale( NORM_FACTOR_2MU2E/bkgh.integral() )
    bkgh_occu = create_occupancy_map(bkgh, thres=3)
    ######## Optimization region from SR ########
    datah = dataf.ch2mu2e.data.dphiEgmIso2D
    datah_occu = create_occupancy_map(datah, thres=3, blindBD=True)
    ######## Optimization region combined ########
    comb_occu = combine_occupancy_map(bkgh_occu, datah_occu)

    outdir = os.path.join(OUTBASE, 'ch2mu2e')
    routine(chandir=sigf.ch2mu2e, bkgh=bkgh, optm_region=comb_occu, outdir=outdir)

    bkgf.close()

    # ----------------------------------------


    sigf.close()
    dataf.close()