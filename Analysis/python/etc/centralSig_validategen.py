#!/usr/bin/env python
from __future__ import print_function
import os
from collections import OrderedDict
from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Hist, Legend, Canvas

from FireROOT.Analysis.Utils import *

fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/centralSig/validategen.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/centralSig/validategen')
if not os.path.isdir(outdir): os.makedirs(outdir)


set_style(MyStyle())
canvas = Canvas()
ROOT.gPad.SetGrid()


get_first  = lambda t: float(t.split('_')[0].split('-')[-1].replace('p', '.'))
get_second = lambda t: float(t.split('_')[1].split('-')[-1].replace('p', '.'))

def plot_pt(chan, obj):
    assert(chan in ['2mu2e', '4mu'])
    assert(obj in ['mu', 'el'])

    chandir = getattr(f, 'ch'+chan)
    masskeys_ = [k.name for k in chandir.keys()]
    # mzd=5
    masskeys = [k for k in masskeys_ if k.endswith('mA-5')]
    masskeys.sort(key=get_first)
    hs = []
    for i, masskey in enumerate(masskeys):
        massdir = getattr(chandir, masskey)
        lifetimekeys_ = [k.name for k in massdir.keys()]
        # lxy=3
        lifetimekeys = [ k for k in lifetimekeys_ if k.startswith('lxy-3') ]
        if not lifetimekeys: continue

        lifetimedir = getattr(massdir, lifetimekeys[0])
        h = getattr(lifetimedir, '%s0pt'%obj)

        h.scale(1./h.integral())
        h.title = 'm_{#chi#chi} = %d GeV' % int(get_first(masskey))
        h.color = sigCOLORS[i]
        h.legendstyle = 'LEP'
        h.markersize = 0.5

        hs.append( h )

    legItems = [h for h in hs]
    draw(hs, logy=True, ytitle='Normalized counts/1GeV')
    legheader = 'm_{Z_{d}} = 5 GeV, lxy = 3 cm'
    leg = Legend(legItems, pad=canvas, margin=0.25, topmargin=0.02, entryheight=0.02, entrysep=0.01, textsize=12, header=legheader)
    leg.Draw()

    if obj == 'mu':   htitle = 'leading #mu p_{T}'
    elif obj == 'el': htitle = 'leading electron p_{T}'
    title = TitleAsLatex('[{}] '.format(chan.replace('mu', '#mu'))+htitle)
    title.Draw()
    draw_labels('59.74 fb^{-1} (13 TeV)', cms_position='left', extra_text='Simulation Preliminary')

    canvas.SaveAs('{}/ch{}_{}0pt.pdf'.format(outdir, chan, obj))
    canvas.clear()


def plot_dr(chan, obj):
    assert(chan in ['2mu2e', '4mu'])
    assert(obj in ['muon', 'electron'])

    chandir = getattr(f, 'ch'+chan)
    masskeys_ = [k.name for k in chandir.keys()]
    # mzd=5
    masskeys = [k for k in masskeys_ if k.endswith('mA-5')]
    masskeys.sort(key=get_first)
    hs = []
    for i, masskey in enumerate(masskeys):
        massdir = getattr(chandir, masskey)
        lifetimekeys_ = [k.name for k in massdir.keys()]
        # lxy=3
        lifetimekeys = [ k for k in lifetimekeys_ if k.startswith('lxy-3') ]
        if not lifetimekeys: continue

        lifetimedir = getattr(massdir, lifetimekeys[0])
        h = getattr(lifetimedir, '%spairdr'%obj)

        h.scale(1./h.integral())
        h.title = 'm_{#chi#chi} = %d GeV' % int(get_first(masskey))
        h.color = sigCOLORS[i]
        h.legendstyle = 'LEP'
        h.markersize = 0.5
        h.drawstyle='hist e'

        hs.append( h )

    legItems = [h for h in hs]
    draw(hs, logy=True, ytitle='Normalized counts')
    legheader = 'm_{Z_{d}} = 5 GeV, lxy = 3 cm'
    leg = Legend(legItems, pad=canvas, margin=0.25, topmargin=0.02, entryheight=0.02, entrysep=0.01, textsize=12, header=legheader)
    leg.Draw()

    htitle = '#DeltaR between %s pair' % obj
    title = TitleAsLatex('[{}] '.format(chan.replace('mu', '#mu'))+htitle)
    title.Draw()
    draw_labels('59.74 fb^{-1} (13 TeV)', cms_position='left', extra_text='Simulation Preliminary')

    canvas.SaveAs('{}/ch{}_{}pairdr.pdf'.format(outdir, chan, obj))
    canvas.clear()


def plot_lxy(chan):
    assert(chan in ['2mu2e', '4mu'])
    masstag = 'mXX-150_mA-0p25'

    chandir = getattr(f, 'ch'+chan)
    massdir = getattr(chandir, masstag)
    lifetimekeys = [k.name for k in massdir.keys()]
    lifetimekeys.sort(key=get_first)
    hs = []
    for i, lifetimekey in enumerate(lifetimekeys):
        h = getattr(massdir, lifetimekey).dplxy

        h.scale(1./h.integral())
        h.title = 'lxy: {:g} cm'.format(get_first(lifetimekey))
        h.color = sigCOLORS[i]
        h.legendstyle = 'LEP'
        h.markersize = 0.5

        hs.append(h)

    legItems = [h for h in hs]
    draw(hs, logy=True, ytitle='Normalized counts/1cm')
    legheader = 'm_{#chi#chi} = 150 GeV, m_{Z_{d}} = 0.25 GeV'
    leg = Legend(legItems, pad=canvas, margin=0.25, topmargin=0.02, entryheight=0.02, entrysep=0.01, textsize=12, header=legheader)
    leg.Draw()

    htitle = 'Dark photon lxy'
    title = TitleAsLatex('[{}] '.format(chan.replace('mu', '#mu'))+htitle)
    title.Draw()
    draw_labels('59.74 fb^{-1} (13 TeV)', cms_position='left', extra_text='Simulation Preliminary')

    canvas.SaveAs('{}/ch{}_dplxy.pdf'.format(outdir, chan))
    canvas.clear()


def plot_dphi(chan):
    assert(chan in ['2mu2e', '4mu'])

    chandir = getattr(f, 'ch'+chan)
    masskeys_ = [k.name for k in chandir.keys()]
    # mzd=1.2
    masskeys = [k for k in masskeys_ if k.endswith('mA-1p2')]
    masskeys.sort(key=get_first)
    hs = []
    htitle = None
    for i, masskey in enumerate(masskeys):
        massdir = getattr(chandir, masskey)
        lifetimekeys_ = [k.name for k in massdir.keys()]
        # lxy=30
        lifetimekeys = [ k for k in lifetimekeys_ if k.startswith('lxy-30') ]
        if not lifetimekeys: continue

        lifetimedir = getattr(massdir, lifetimekeys[0])
        h = getattr(lifetimedir, 'dpdphi')

        h.scale(1./h.integral())
        if htitle is None: htitle = h.title
        h.title = 'm_{#chi#chi} = %d GeV' % int(get_first(masskey))
        h.color = sigCOLORS[i]
        h.legendstyle = 'LEP'
        h.markersize = 0.5

        hs.append( h )

    legItems = [h for h in hs]
    draw(hs, logy=True, ytitle='Normalized counts')
    legheader = 'm_{Z_{d}} = 1.2 GeV, lxy = 30 cm'
    leg = Legend(legItems, pad=canvas, margin=0.25, topmargin=0.02, entryheight=0.02, entrysep=0.01, textsize=12, header=legheader)
    leg.Draw()

    title = TitleAsLatex('[{}] '.format(chan.replace('mu', '#mu'))+htitle)
    title.Draw()
    draw_labels('59.74 fb^{-1} (13 TeV)', cms_position='left', extra_text='Simulation Preliminary')

    canvas.SaveAs('{}/ch{}_dpdphi.pdf'.format(outdir, chan))
    canvas.clear()


def plot_boundstatemass(chan):
    assert(chan in ['2mu2e', '4mu'])

    chandir = getattr(f, 'ch'+chan)
    masskeys_ = [k.name for k in chandir.keys()]
    # mzd=0.25
    masskeys = [k for k in masskeys_ if k.endswith('mA-0p25')]
    masskeys.sort(key=get_first)
    hs = []
    htitle = None
    for i, masskey in enumerate(masskeys):
        massdir = getattr(chandir, masskey)
        lifetimekeys_ = [k.name for k in massdir.keys()]
        # lxy=150
        lifetimekeys = [ k for k in lifetimekeys_ if k.startswith('lxy-150') ]
        if not lifetimekeys: continue

        lifetimedir = getattr(massdir, lifetimekeys[0])
        h = getattr(lifetimedir, 'psmass')

        h.scale(1./h.integral())
        if htitle is None: htitle = h.title
        h.title = 'm_{#chi#chi} = %d GeV' % int(get_first(masskey))
        h.color = sigCOLORS[i]
        h.legendstyle = 'LEP'
        h.markersize = 0.5

        hs.append( h )

    legItems = [h for h in hs]
    draw(hs, logy=False, ytitle='Normalized counts/1GeV')
    legheader = 'm_{Z_{d}} = 0.25 GeV, lxy = 150 cm'
    leg = Legend(legItems, pad=canvas, margin=0.25, topmargin=0.02, entryheight=0.02, entrysep=0.01, textsize=12, header=legheader)
    leg.Draw()

    title = TitleAsLatex('[{}] '.format(chan.replace('mu', '#mu'))+htitle)
    title.Draw()
    draw_labels('59.74 fb^{-1} (13 TeV)', cms_position='left', extra_text='Simulation Preliminary')

    canvas.SaveAs('{}/ch{}_boundstatemass.pdf'.format(outdir, chan))
    canvas.clear()


def routine(chan, masstag):
    massdir = getattr(getattr(f, 'ch'+chan), masstag)
    lifetimeTags = [x.name for x in massdir.keys()]

    get_lxy = lambda t : float(t.split('_')[0].split('-')[-1].replace('p', '.'))
    get_ctau = lambda t: float(t.split('_')[1].split('-')[-1].replace('p', '.'))

    lifetimeTags.sort(key=get_lxy)
    hs, legItems = [], []
    htitle = None
    for i, lifetimeTag in enumerate(lifetimeTags):
        h = getattr(massdir, lifetimeTag).dplxy
        if htitle is None: htitle = h.title
        h.title = 'lxy: {:g} (N={})'.format(get_lxy(lifetimeTag), h.integral(overflow=True))
        h.color = sigCOLORS[i]
        h.legendstyle = 'LEP'
        h.markersize = 0.5
        hs.append(h)
        legItems.append(h)

    xmin_, xmax_, ymin_, ymax_ = get_limits(hs, logy=True)
    draw(hs, logy=True, ylimits=(0.1, ymax_))
    legend = Legend(legItems, pad=canvas, margin=0.25, topmargin=0.02, entryheight=0.02, entrysep=0.01, textsize=12, header=masstag)
    legend.Draw()
    title = TitleAsLatex('[{}] '.format(chan.replace('mu', '#mu'))+htitle)
    title.Draw()
    draw_labels('59.74 fb^{-1} (13 TeV)', cms_position='left', extra_text='work-in-progress')

    canvas.SaveAs('{}/ch{}_dplxy__{}.png'.format(outdir, chan, masstag))
    canvas.Clear()

# routine('4mu', 'mXX-150_mA-0p25')
# routine('2mu2e', 'mXX-150_mA-0p25')

# for k in f.ch4mu.keys():
#     routine('4mu', k.name)
# for k in f.ch2mu2e.keys():
#     routine('2mu2e', k.name)

if __name__ == '__main__':

    f = root_open(fn)

    plot_pt('4mu',   'mu')
    plot_pt('2mu2e', 'mu')
    plot_pt('2mu2e', 'el')


    plot_dr('4mu',   'muon')
    plot_dr('2mu2e', 'muon')
    plot_dr('2mu2e', 'electron')


    plot_lxy('4mu')
    plot_lxy('2mu2e')


    plot_dphi('4mu')
    plot_dphi('2mu2e')


    plot_boundstatemass('4mu')
    plot_boundstatemass('2mu2e')

    f.close()