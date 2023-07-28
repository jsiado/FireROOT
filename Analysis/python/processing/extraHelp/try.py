import ROOT
import math 
import time
from plot_dict import *


rfile = ROOT.TFile("~/nobackup/SIDM_ana/Analysis/CMSSW_10_2_14/src/FireROOT/Analysis/python/outputs/rootfiles/modules/out_53.root")
#workdir =file.GetDirectory("metTrigAnalyzerNanoAOD")

num = rfile.Get("ch2mu2e/sig/mXX-500_mA-0p25_lxy-300/Mat_dR")
den = rfile.Get("ch2mu2e/sig/mXX-500_mA-0p25_lxy-300/Tot_dR")



#Numerator = workdir.Get("h_met_passtrig")
#Denominator = workdir.Get("h_met_all")


Efficiency = ROOT.TGraphAsymmErrors(num,den)
#Efficiency.SetLineColor(linecolor[1])
#Efficiency.SetMarkerStyle(markerstylesolid[1])
#Efficiency.SetMarkerColor(markercolor[1])
#Efficiency.SetMarkerSize(1.5)
Efficiency.SetTitle("Trigger Efficiency")
Efficiency.GetXaxis().SetTitle("p_{T}^{Miss}(GeV)")
Efficiency.GetYaxis().SetTitle("Trigger Efficiency")
Efficiency.GetYaxis().SetRange(0,2) 

legend = ROOT.TLegend(0.4412607,0.1932773,0.8223496,0.4453782)
legend.SetFillStyle(1001)
legend.SetBorderSize(0)
legend.AddEntry(Efficiency,"MET Trigger","ep")

canvas=ROOT.TCanvas("Trigger Efficicency", "Trigger Efficiency")
canvas.SetGrid()
Efficiency.Draw("ap")
legend.Draw("same")

canvas.SaveAs("Efficiency.pdf")

