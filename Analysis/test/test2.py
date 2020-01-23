from rootpy.plotting import F1, Hist, HistStack, Graph, Canvas, set_style
from rootpy.plotting.utils import draw
from rootpy.interactive import wait
from math import sin

set_style('ATLAS')

mus = (0, -1, 2)
sigmas = (2, 1, 0.5)
events = (1000, 2000, 100)
colors = ('lawngreen', 'forestgreen', 'mistyrose')
styles = ('\\', '/', '-')

canvas = Canvas()
objects = []

# create a stack
stack = HistStack()
stack.Add(Hist(100, -5, 5, color='salmon', drawstyle='hist', fillstyle='solid' ).FillRandom(
          F1('TMath::Gaus(x, 2, 1)'), 500))
stack.Add(Hist(100, -5, 5, color='powderblue', drawstyle='hist', fillstyle='solid').FillRandom(
          F1('TMath::Gaus(x, 2, 0.6)'), 300))
objects.append(stack)

_sumStack = None
for h in stack.GetHists():
    if _sumStack is None: _sumStack = h.Clone()
    else: _sumStack.Add(h)

# _sumStack.fillstyle = '/'
# stack.markerstyle = 0
stackError = _sumStack.poisson_errors()
stackError.fillstyle = '/'
stackError.fillcolor = 'black'
stackError.drawstyle = '2'
# stack.Draw('HIST')
# stackError.Draw('2 [] same')
objects.append(stackError)

import ROOT

from FireROOT.Analysis.Utils import *
ROOT.gPad.SetLogy(True)
draw(objects, xtitle='Some Variable [Units]', ytitle='Events', ypadding=0.05, logy=True, ylimits=(1e-3, 1e3) )

print(ROOT.gStyle.GetPadTopMargin())
label = ROOT.TLatex(ROOT.gStyle.GetPadLeftMargin(), 0.9+ROOT.gStyle.GetPadTopMargin(), 'This is a title')
label.SetTextFont(43)
label.SetTextAlign(11)
label.SetTextSize(25)
label.SetNDC()
label.Draw()
# canvas.Modified()
# canvas.Update()

canvas.Print('test2.pdf')