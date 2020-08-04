#!/usr/bin/env python
from __future__ import print_function
import os, math
import json, argparse
from rootpy.io import root_open
from rootpy import asrootpy

from FireROOT.Analysis.Utils import *

fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/centralSig/leptonIDSyst.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/harvester_leptonIDSyst')



def variation_from_nominal(f, channel, obj):
    assert( channel in ['2mu2e', '4mu'])
    assert( obj in ['electron', 'photon', 'pfmuon'])

    res = {}

    nominal_tag = 'dphiIso2D_%s'%obj
    up_tag = 'dphiIso2D_%s_up'%obj
    low_tag = 'dphiIso2D_%s_low'%obj

    channelDir = getattr(f, 'ch%s'%channel).sig
    for d in channelDir.keys():
        nominal = getattr(getattr(channelDir, d.name), nominal_tag).integral()
        scaleup = getattr(getattr(channelDir, d.name), up_tag).integral()
        scalelo = getattr(getattr(channelDir, d.name), low_tag).integral()

        if nominal==0: continue
        res[d.name] = (scaleup-scalelo)/nominal

    return res


def variation_from_nominal_centralSig(f, channel, obj, method=2):
    """
    centralSig ROOT file structure.

    if method=1: variation = (up-low)/nominal
    if method=2: variation = max(|up-nominal|, |nominal-low|)/nominal
    """
    assert( channel in ['2mu2e', '4mu'])
    assert( obj in ['electron', 'photon', 'pfmuon'])

    res = {}

    nominal_tag = 'dphiIso2D_nominal'
    up_tag = 'dphiIso2D_%s_up'%obj
    low_tag = 'dphiIso2D_%s_low'%obj

    channelDir = getattr(f, 'ch%s'%channel)
    for massKey in channelDir.keys():
        massDir = getattr(channelDir, massKey.name)
        for lifetimeKey in massDir.keys():
            lifetimeDir = getattr(massDir, lifetimeKey.name)

            nominal = getattr(lifetimeDir, nominal_tag).integral()
            scaleup = getattr(lifetimeDir, up_tag).integral()
            scalelo = getattr(lifetimeDir, low_tag).integral()

            if nominal==0: continue
            if method==1: variation = (scaleup-scalelo)/nominal*100
            if method==2: variation = max(abs(scaleup-nominal), abs(nominal-scalelo))/nominal*100

            res['%s_%s'%(massKey.name, lifetimeKey.name)] = {
                'variation': variation,
                'count': nominal,
            }

    return res


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='havester_leptonIDSyst')
    parser.add_argument('--method', '-m', type=int, default=2, choices=[1,2], help='variation calculation method')
    parser.add_argument('--plot', action='store_true', help='make plots')
    args = parser.parse_args()

    if not os.path.isdir(outdir): os.makedirs(outdir)
    rawdata_dir = os.path.join(outdir, 'rawdata')
    if not os.path.isdir(rawdata_dir): os.makedirs(rawdata_dir)

    f = root_open(fn)


    print('=== 2mu2e')
    variation_electron = variation_from_nominal_centralSig(f, '2mu2e', 'electron')
    variation_photon   = variation_from_nominal_centralSig(f, '2mu2e', 'photon')
    variation_pfmuon   = variation_from_nominal_centralSig(f, '2mu2e', 'pfmuon')

    # print(variation_electron)
    # print(variation_photon)
    # print(variation_pfmuon)

    with open(os.path.join(rawdata_dir, 'ch2mu2e_variation_electron.json'), 'w') as outf:
        outf.write(json.dumps(variation_electron, indent=4))

    with open(os.path.join(rawdata_dir, 'ch2mu2e_variation_photon.json'), 'w') as outf:
        outf.write(json.dumps(variation_photon, indent=4))

    with open(os.path.join(rawdata_dir, 'ch2mu2e_variation_pfmuon.json'), 'w') as outf:
        outf.write(json.dumps(variation_pfmuon, indent=4))


    print('=== 4mu')
    variation_pfmuon_ch4mu = variation_from_nominal_centralSig(f, '4mu', 'pfmuon')

    # print(variation_pfmuon_ch4mu)

    with open(os.path.join(rawdata_dir, 'ch4mu_variation_pfmuon.json'), 'w') as outf:
        outf.write(json.dumps(variation_pfmuon_ch4mu, indent=4))


    f.close()

    if args.plot:
        import ROOT
        from rootpy.plotting.style import set_style
        from rootpy.plotting.base import convert_color
        from rootpy.plotting import Hist, Legend, Canvas

        set_style(MyStyle())
        ROOT.gStyle.SetOptFit(0)
        ROOT.gStyle.SetPadRightMargin(0.05)
        canvas = Canvas()

        def make_plot(raw_data, binning, title_text, outfn):
            h = Hist(*binning, drawstyle='hist e1', color=sigCOLORS[0], linewidth=2,
                    title=';Percent difference[%];Events')
            for sample, value in raw_data.items():
                h.Fill(value['variation'], value['count'])
            hc = asrootpy(h.GetCumulative())
            hc.linecolor='gold'
            hc.fillcolor = 'lightyellow'
            hc.fillstyle='solid'
            hc.scale(h.max(include_error=True)/hc.max())
            xmin_, xmax_, ymin_, ymax_ = get_limits([h, hc])
            draw([hc,h], ylimits=(0, ymax_))

            x95, x99 = None, None
            cumsum=0
            for i in range(1, h.GetNbinsX()+1):
                cumsum += h.GetBinContent(i)
                if x95 is None and cumsum/h.Integral()>0.95: x95=h.GetXaxis().GetBinUpEdge(i)
                if x99 is None and cumsum/h.Integral()>0.99: x99=h.GetXaxis().GetBinUpEdge(i)

            title = TitleAsLatex(title_text)
            title.Draw()

            # print(title_text, ROOT.gPad.GetUymax(), hc.max())
            # draw a second axis on the right.
            ROOT.gPad.SetTicks(1, 0) # Draw top ticks but not right ticks (https://root.cern.ch/root/roottalk/roottalk99/2908.html)
            low, high = 0, ROOT.gPad.GetUymax()/hc.max()
            raxis = ROOT.TGaxis(ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymin(), ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymax(), low, high, 510, "+L")
            raxis.SetLabelSize(0.03)
            raxis.SetLabelFont(42)
            raxis.SetLabelColor(convert_color('gold', 'root'))
            raxis.Draw()

            frame = canvas.FindObject('TFrame')
            lo, hi = frame.GetY1(), frame.GetY2()
            l95 = ROOT.TLine(x95, lo, x95, hi)
            l95.SetLineStyle(2)
            l95.SetLineColor(convert_color(sigCOLORS[1], 'root'))
            l95.SetLineWidth(2)
            l95.Draw()
            l99 = ROOT.TLine(x99, lo, x99, hi)
            l99.SetLineStyle(3)
            l99.SetLineColor(convert_color(sigCOLORS[2], 'root'))
            l99.Draw()

            leg = Legend(3, margin=0.25, leftmargin=0.45, topmargin=0.02, entrysep=0.01, entryheight=0.02, textsize=10)
            leg.AddEntry(hc, label='cumulative (norm.)', style='LF')
            leg.AddEntry(l95, label='95% @ {}'.format(x95), style='L')
            leg.AddEntry(l99, label='99% @ {}'.format(x99), style='L')
            leg.Draw()

            canvas.SaveAs(outfn)
            canvas.clear()


        make_plot(variation_pfmuon_ch4mu, (20,0,2),
                  title_text='[4#mu] PF muon variations from nominal',
                  outfn='{}/ch4mu_pfmuon.pdf'.format(outdir))

        make_plot(variation_pfmuon, (10,0,1),
                  title_text='[2#mu2e] PF muon variations from nominal',
                  outfn='{}/ch2mu2e_pfmuon.pdf'.format(outdir))

        make_plot(variation_electron, (40,0,10),
                  title_text='[2#mu2e] Electron variations from nominal',
                  outfn='{}/ch2mu2e_electron.pdf'.format(outdir))

        make_plot(variation_photon, (40,0,10),
                  title_text='[2#mu2e] Photon variations from nominal',
                  outfn='{}/ch2mu2e_photon.pdf'.format(outdir))
