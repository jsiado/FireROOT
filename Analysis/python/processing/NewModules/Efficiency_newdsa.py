from rootpy.io import root_open
from rootpy.plotting.style import set_style
from rootpy.plotting import Canvas, Efficiency, Legend
import ROOT

import os
from FireROOT.Analysis.Utils import *


CMSSW_BASE = os.getenv('CMSSW_BASE')
oldfn1p2 = os.path.join(CMSSW_BASE, 'src/FireROOT/Analysis/python/outputs/rootfiles/modules/oldLjEfficiency.root')
oldd1p2 = root_open(oldfn1p2).ch2mu2e.sig

newfn1p2 = os.path.join(CMSSW_BASE, 'src/FireROOT/Analysis/python/outputs/rootfiles/modules/signalLjEfficiency.root')
newd1p2 = root_open(newfn1p2).ch2mu2e.sig

print 'la maria'
#oldfn0p25 = os.path.join(CMSSW_BASE, 'src/FireROOT/Analysis/python/outputs/rootfiles/modules/test4.root')
#oldd0p25 = root_open(oldfn0p25).ch2mu2e.sig

#newfn0p25 = os.path.join(CMSSW_BASE, 'src/FireROOT/Analysis/python/outputs/rootfiles/modules/test3.root')
#newd0p25 = root_open(newfn0p25).ch2mu2e.sig

set_style(MyStyle())
canvas = Canvas()

print 'la maria'

sample_names = [k.name for k in oldd1p2.keys()]
sample_names.sort(key=lambda x: float(x.split('mA-')[1].split('_')[0].replace('p', '.')))

print 'la maria'
print sample_names

#sample_names2 = [k.name for k in oldd0p25.keys()]
#sample_names2.sort(key=lambda x: float(x.split('mA-')[1].split('_')[0].replace('p', '.')))

def get_efficiency_graphs(d):
    efficiency_graphs = []
    #for s in sample_names2:
       # sample_dir = getattr(d2, s)
      #  numer_ = getattr(sample_dir, 'lxyDpToEl__match').clone()
      #  denom_ = getattr(sample_dir, 'lxyDpToEl__total').clone()
       # g = Efficiency(numer_, denom_).graph
       # efficiency_graphs.append(g)
    for s in sample_names:
        sample_dir = getattr(d, s)
        numer_ = getattr(sample_dir, 'lxyDpToEl__match').clone()
        denom_ = getattr(sample_dir, 'lxyDpToEl__total').clone()
        g = Efficiency(numer_, denom_).graph
        efficiency_graphs.append(g) 
    return efficiency_graphs


efficiency_graphs_old = get_efficiency_graphs(oldd1p2)
#efficiency_graphs_old.append(get_efficiency_graphs(oldd0p25))

#efficiency_graphs_old = get_efficiency_graphs(oldd1p2, oldd0p25)
#efficiency_graphs_old.append(get_efficiency_graphs(oldd0p25))
efficiency_graphs_new = get_efficiency_graphs(newd1p2)
#efficiency_graphs_new.append(get_efficiency_graphs(newd0p25))

canvas.clear()

for i, g in enumerate(efficiency_graphs_old):
    print(i)
    g.markercolor = sigCOLORS[i]
    g.markersize = 0.3
    g.linecolor = sigCOLORS[i]
    g.legendstyle = 'LEP'
    if i==0: g.drawstyle = 'APZ'
else:    g.drawstyle = 'PZ'

for i, g in enumerate(efficiency_graphs_new):
    g.markercolor = sigCOLORS[i]
    g.markersize = 0.75
    g.markerstyle = 'opencircle'
    g.linecolor = sigCOLORS[i]
    g.linestyle = 'solid'
    g.legendcolor = 'LEP'
    g.drawstyle = 'PZ'
        
draw(efficiency_graphs_old[:]+efficiecy_graphs_new[:], pad=canvas)
#draw(efficiency_graphs_old[:]+efficiency_graphs_new[:], pad=canvas)
leg = Legend(len(efficiency_graphs_old), margin=0.25, leftmargin=0.05,
             topmargin=0.02, entrysep=0.01, entryheight=0.03, textsize=14,
             header='mXX=500GeV, lxy=300cm')
leg.AddEntry(efficiency_graphs_old[0], 'm_{Z_{d}}=0.25GeV')
#leg.AddEntry(efficiency_graphs_old[0], 'm_{Z_{d}}=1.2GeV')
#leg.AddEntry(efficiency_graphs_old[2], 'm_{Z_{d}}=5   GeV')
leg.Draw()

#leg2 = Legend(len(efficiency_graphs_new), margin=0.25, leftmargin=0.45,
 #            topmargin=0.02, entrysep=0.01, entryheight=0.03, textsize=14,
  #           header='drop dEtaInSeed for electron ID')
#leg2.AddEntry(efficiency_graphs_new[0], 'm_{Z_{d}}=0.25GeV', style='LEP')
#leg2.AddEntry(efficiency_graphs_new[1], 'm_{Z_{d}}=1.2 GeV', style='LEP')
#leg2.AddEntry(efficiency_graphs_new[2], 'm_{Z_{d}}=5   GeV', style='LEP')
#leg2.Draw()

canvas.Draw()
canvas.SaveAs('mio.png')
