#!/usr/bin/env python
import ROOT
from rootpy.plotting import Canvas, Hist, Legend
from rootpy.plotting.style import get_style
from rootpy.plotting.style.cmstdr.labels import CMS_label
from rootpy.interactive import wait

from rootpy.logger import log
log = log[__name__]

INTERACTIVE = True

def test_cmstdr():
    style = get_style('CMSTDR')
    style.SetTitleSize(0.03, "XYZ")
    style.SetLabelSize(0.03, "XYZ")
    with style:
        canvas = Canvas()
        hpx = Hist(100, -4, 4, name="hpx", title="This is the px distribution")
        ROOT.gRandom.SetSeed()
        for i in range(1000):
            hpx.Fill(ROOT.gRandom.Gaus())
        hpx.GetXaxis().SetTitle("random variable [unit]")
        hpx.GetYaxis().SetTitle("#frac{dN}{dr} [unit^{-1}]")
        hpx.SetMaximum(100.)
        hpx.Draw()
        l, p = CMS_label("Testing 2050", sqrts=100)
        l.SetTextSize(0.04)
        p.SetTextSize(0.04)
        # if INTERACTIVE:
        #     wait()
        canvas.SaveAs('test_style.pdf')


def test_mystyle():
    from rootpy.plotting.style import set_style
    from FireROOT.Analysis.Utils import MyStyle
    set_style(MyStyle())

    canvas = Canvas()
    hpx = Hist(100, -4, 4, name="hpx", title="This is the px distribution")
    ROOT.gRandom.SetSeed()
    for i in range(1000):
        hpx.Fill(ROOT.gRandom.Gaus())
    hpx.Fill(5, 20)
    hpx.GetXaxis().SetTitle("random variable [unit]")
    hpx.GetYaxis().SetTitle("#frac{dN}{dr} [unit^{-1}]")
    hpx.SetMaximum(100.)
    hpx.Draw()

    leg = Legend([hpx], leftmargin=0.05, margin=0.1, entryheight=0.02, textsize=12)
    leg.Draw()

    canvas.SaveAs('test_style.pdf')

if __name__ == '__main__':
    log.info('start')
    test_mystyle()
    log.info('end')