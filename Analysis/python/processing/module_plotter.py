#!/usr/bin/env python
from __future__ import print_function
import argparse
import os, sys
from functools import reduce
import ROOT
from FireROOT.Analysis.Utils import *
from FireROOT.Analysis.samples.signalnumbers import genxsec
from rootpy.plotting import Hist, Legend, Canvas, HistStack
from rootpy.io import root_open

## parser
parser = argparse.ArgumentParser(description="module plotter.")
parser.add_argument("--inname", "-i", type=str, default=None, help='input ROOT file name')
parser.add_argument("--normsig", "-r", type=float, default=-1, help='Normalize signal distributions to a fix value')
parser.add_argument("--normsigxsec", "-x", type=float, default=30, help='Normalize signal distributions to a fix xsec [fb]')
parser.add_argument("--dataset", "-d", type=str, default='mc', choices=['data', 'mc'], help='dataset to plot')
parser.add_argument("--subdir", "-s", type=str, default=None, choices=['proxy',], help='subdir modules, DEFAULT None')
parser.add_argument("--logx", action='store_true')
parser.add_argument("--overflow", type=bool, default=True)

args = parser.parse_args()
if args.normsig>0 and args.normsigxsec>0:
    sys.exit('You cannot normalize signal to a fixed value and a fixed xsec at the same time.')

inputdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/')
if args.subdir: inputdir = os.path.join(inputdir, args.subdir)
assert(os.path.isdir(inputdir))
allfiles = [f for f in os.listdir(inputdir) if f.endswith('.root')]
if args.inname+'.root' not in allfiles:
    sys.exit('Available ROOT files: {}'.format(str(allfiles)))

def get_unique_histnames(fname):
    res = []
    f = root_open(fname)
    for dirpath, dirnames, filenames in f.walk():
        if not filenames: continue
        if dirpath.endswith('data') or dirpath.endswith('bkg'):
            dirobj = reduce(lambda a,b: getattr(a, b), [f]+dirpath.split('/'))
            for fn in filenames:
                h_ = getattr(dirobj, fn)
                if isinstance(h_, HistStack): h_ = h_[0]
                if h_.GetDimension()>1: continue
                res.append(fn)
        if 'sig' in dirpath and not dirnames:
            dirobj = reduce(lambda a,b: getattr(a, b), [f]+dirpath.split('/'))
            for fn in filenames:
                if getattr(dirobj, fn).GetDimension()>1: continue
                res.append(fn)
    f.close()
    return list(set(res))

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



if __name__ ==  '__main__':

    infile = os.path.join(inputdir, args.inname+'.root')
    outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/plots/')
    if args.subdir: outdir = os.path.join(outdir, args.subdir)
    outdir = os.path.join(outdir, args.inname)
    if not os.path.isdir(outdir): os.makedirs(outdir)

    from rootpy.plotting.style import set_style
    set_style(MyStyle())

    hist_toplot = get_unique_histnames(infile)

    c = Canvas()
    f = root_open(infile)
    for hname in hist_toplot:
        for chan in ['4mu', '2mu2e']:
            if not hasattr(f, 'ch'+chan): continue
            channelDir = getattr(f, 'ch'+chan)

            hs, legItems = [], []
            htitle = None
            drawOverflow, xmax = False, None

            if args.dataset=='mc':
                ## bkg
                if hasattr(channelDir, 'bkg') and hasattr(channelDir.bkg, hname):
                    hstack = getattr(channelDir.bkg, hname)
                    if not htitle: htitle = hstack.title

                    for h in hstack:
                        h.fillstyle='solid'
                        h.linewidth=0
                        h.legendstyle='F'
                        h.fillcolor = bkgCOLORS[h.title]
                        if args.overflow:
                            h.SetBinContent(h.nbins(), h.GetBinContent(h.nbins())+h.overflow())

                    hs.append(hstack)


                    if hstack.Integral():
                        stackError = ErrorBandFromHistStack(hstack)
                        hs.append(stackError)
                        for h in hstack:
                            if h.integral(overflow=True)==0: continue
                            legItems.append(h)
                        legItems.append(stackError)

            if args.dataset=='data':
                ## data
                if hasattr(channelDir, 'data') and hasattr(channelDir.data, hname):
                    h = getattr(channelDir.data, hname)
                    if not htitle: htitle = h.title
                    h.title = 'data'
                    h.SetBinContent(h.nbins(), h.GetBinContent(h.nbins())+h.overflow())
                    h.legendstyle = 'LEP'
                    hs.append(h)
                    legItems.append(h)

            ## sig
            if hasattr(channelDir, 'sig'):
                sampleSig = 'mXX-150_mA-0p25_lxy-300|mXX-500_mA-1p2_lxy-300|mXX-800_mA-5_lxy-300'.split('|')
                sampleSig.extend( 'mXX-100_mA-5_lxy-0p3|mXX-1000_mA-0p25_lxy-0p3'.split('|') )
                # for ds in channelDir.sig.keys():
                for i, ds in enumerate(sampleSig):
                    if not hasattr(channelDir.sig, ds): continue
                    dsdir = getattr(channelDir.sig, ds)
                    h=None
                    for k in dsdir.keys():
                        if k.name!=hname: continue
                        h = getattr(dsdir, k.name).Clone()
                    if h is None: continue
                    if h.integral(overflow=True)==0: continue

                    if not htitle: htitle = h.title
                    h.title = ds
                    if args.normsig>0:
                        h.title += ' (norm.)'
                        if h.integral(overflow=True)>0:
                            h.scale( 1.*args.normsig/h.integral(overflow=True) )
                    if args.normsigxsec>0:
                        h.title += ' (norm. {:g}fb)'.format(args.normsigxsec)
                        mboundstate = int(ds.split('_')[0].replace('mXX-',''))
                        if h.integral(overflow=True)>0:
                            h.scale( args.normsigxsec/genxsec[mboundstate] )
                    if args.overflow:
                        h.SetBinContent(h.nbins(), h.GetBinContent(h.nbins())+h.overflow())

                    h.drawstyle = 'hist'
                    h.color = sigCOLORS[i]
                    h.legendstyle = 'L'
                    h.linewidth = 2
                    hs.append(h)
                    legItems.append(h)

            legend = Legend(legItems, pad=c, margin=0.25, leftmargin=0.45, topmargin=0.02, entrysep=0.01, entryheight=0.02, textsize=10)

            xmin_, xmax_, ymin_, ymax_ = get_limits(hs, logx=args.logx)
            if drawOverflow and xmax is not None: xmax_ = xmax

            xdiv_ = -310 if 'phi' in htitle else None
            if args.dataset=='mc':
                axes, limits = draw(hs, pad=c, logy=True, logx=args.logx, xdivisions=xdiv_)
            elif args.dataset=='data':
                axes, limits = draw(hs, pad=c, logy=False, ylimits=(0, ymax_), logx=args.logx, xdivisions=xdiv_)
            if 'phi' in htitle: decorate_xaxis_pi(axes[0])
            if args.logx: axes[0].SetMoreLogLabels()
            ROOT.gPad.SetGrid()
            ROOT.gPad.Update()
            legend.Draw()
            title = TitleAsLatex('[{}] {}'.format(chan.replace('mu', '#mu'), htitle.split(';')[0]))
            title.Draw()
            draw_labels('59.74 fb^{-1} (13 TeV)', cms_position='left', extra_text='work-in-progress')

            c.SaveAs('{}/{}__{}_{}.pdf'.format(outdir, args.dataset, chan, hname))
            c.Clear()

    f.close()
