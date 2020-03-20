#!/usr/bin/env python
from __future__ import print_function
import argparse
import os
from FireROOT.Analysis.Utils import *
from rootpy.plotting import Hist, Legend, Canvas
from rootpy.io import root_open

## parser
parser = argparse.ArgumentParser(description="module plotter.")
parser.add_argument("--inname", "-i", type=str, default=None, help='input ROOT file name')
parser.add_argument("--normsig", "-r", type=float, default=-1, help='Normalize signal distributions')
parser.add_argument("--dataset", "-d", type=str, default='mc', choices=['data', 'mc'], help='dataset to plot')
parser.add_argument("--subdir", "-s", type=str, default=None, choices=['proxy',], help='subdir modules, DEFAULT None')

args = parser.parse_args()

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
        if dirpath.endswith('data') or dirpath.endswith('bkg'): res.extend(filenames)
        if dirpath.endswith('sig'):
            for fn in filenames:
                res.append(fn.split('__')[-1])
    f.close()
    return list(set(res))


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
                        if h.overflow()!=0:
                            drawOverflow=True
                            h.xaxis.SetRange(1, h.nbins()+1)
                            if not xmax: xmax = h.xaxis.GetBinUpEdge(h.nbins()+1)
                            else: xmax = max(xmax, h.xaxis.GetBinUpEdge(h.nbins()+1))
                    stackError = ErrorBandFromHistStack(hstack)

                    hs.append(hstack)
                    hs.append(stackError)

                    for h in hstack: legItems.append(h)
                    legItems.append(stackError)

            if args.dataset=='data':
                ## data
                if hasattr(channelDir, 'data') and hasattr(channelDir.data, hname):
                    h = getattr(channelDir.data, hname)
                    if not htitle: htitle = h.title
                    if h.overflow()!=0:
                        drawOverflow=True
                        h.xaxis.SetRange(1, h.nbins()+1)
                        if not xmax: xmax = h.xaxis.GetBinUpEdge(h.nbins()+1)
                        else: xmax = max(xmax, h.xaxis.GetBinUpEdge(h.nbins()+1))
                    h.title = 'data'
                    h.SetBinContent(h.nbins(), h.GetBinContent(h.nbins())+h.overflow())
                    h.legendstyle = 'LEP'
                    hs.append(h)
                    legItems.append(h)

            ## sig
            if hasattr(channelDir, 'sig'):
                for ds in channelDir.sig.keys():
                    dsdir = getattr(channelDir.sig, ds.name)
                    h=None
                    for k in dsdir.keys():
                        if k.name!=hname: continue
                        h = getattr(dsdir, k.name).Clone()
                    if h is None: continue

                    if not htitle: htitle = h.title
                    if h.overflow()!=0:
                        drawOverflow=True
                        h.xaxis.SetRange(1, h.nbins()+1)
                        if not xmax: xmax = h.xaxis.GetBinUpEdge(h.nbins()+1)
                        else: xmax = max(xmax, h.xaxis.GetBinUpEdge(h.nbins()+1))
                    h.title = ds.name
                    if args.normsig>0:
                        h.title += ' (norm.)'
                        h.Scale(1.*args.normsig/h.Integral())
                    h.drawstyle = 'hist pmc plc'
                    h.legendstyle = 'L'
                    h.linewidth = 2
                    hs.append(h)
                    legItems.append(h)


            legend = Legend(legItems, pad=c, margin=0.1, entryheight=0.02, textsize=12)

            xmin_, xmax_, ymin_, ymax_ = get_limits(hs)
            if drawOverflow and xmax is not None: xmax_ = xmax
            if args.dataset=='mc': draw(hs, pad=c, xlimits=(xmin_, xmax_), logy=True)
            elif args.dataset=='data': draw(hs, pad=c, xlimits=(xmin_, xmax_), logy=False, ylimits=(0, ymax_), )
            legend.Draw()
            title = TitleAsLatex('[{}] {}'.format(chan.replace('mu', '#mu'), htitle.split(';')[0]))
            title.Draw()
            draw_labels('59.74 fb^{-1} (13 TeV)', cms_position='left', extra_text='work-in-progress')

            c.SaveAs('{}/{}__{}_{}.pdf'.format(outdir, args.dataset, chan, hname))
            c.Clear()

    f.close()
