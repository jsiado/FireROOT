import sys
import ROOT

from ROOT import gROOT, gPad, TEfficiency, TPad

	
def ch4muEff():        
        eff1 = TEfficiency("eff1", "eff def", 10, 0,1, 10, 0, 1)

	c2 = ROOT.TCanvas("can2", "", 600, 600)
	leg = ROOT.TLegend (.5, .2, 0.85, .55)
	leg.SetHeader("Samples:","C");
	leg.SetBorderSize(0)
	
	eff1 = ROOT.TEfficiency(ns1, ds1)
	eff1.SetLineColor(1)
        eff1.SetTitle(" ; #Delta R(#mu_{1},#mu_{2}); Efficiency (#epsilon)");
	eff1.Draw()
	leg.AddEntry(eff1, S1, "l")
	
	eff2 = ROOT.TEfficiency(ns2, ds2)
	eff2.SetLineColor(2)
	eff2.Draw("same")
	leg.AddEntry(eff2, S2, "l")
	
	eff3 = ROOT.TEfficiency(ns3, ds3)
	eff3.SetLineColor(3)
	eff3.Draw("same")
	leg.AddEntry(eff3, S3, "l")
	
	eff4 = ROOT.TEfficiency(ns4, ds4)
	eff4.SetLineColor(4)
	eff4.Draw("same")
	leg.AddEntry(eff4, S4, "l")
	
	leg.Draw()
	c2.Draw()
        
        x =input("")
	
if __name__ == "__main__":
    ''' run it as python extraHelp/TrEff.py rootfile channel. i.e $$ python extraHelp/eff.py 55 2mu2e '''
    rt = sys.argv[1]
    ch = sys.argv[2]
    print (rt)
    path = "~/nobackup/SIDM_ana/Analysis/CMSSW_10_2_14/src/FireROOT/Analysis/python/outputs/rootfiles/modules/out_55.root"
    
    fin = ROOT.TFile(path, "READ")
    
    #samples
    S1 = "mXX-100_mA-0p25_lxy-300/"
    S2 = "mXX-500_mA-0p25_lxy-300/"
    S3 = "mXX-500_mA-1p2_lxy-300/"
    S4 = "mXX-1000_mA-5_lxy-300/"
    
    color = [1,2,3,4]
    Samples = [S1, S2, S3, S4]
    
    sam = "ch" + str(ch)+ "/sig/"
    var = ["Mat_dR", "Tot_dR", "Mat_pT", "Tot_pT", "Mat_d0", "Tot_d0", "Mat_lxy", "Tot_lxy"]

    ns1 = fin.Get(sam + S1 + var[0])
    ds1 = fin.Get(sam + S1 + var[1])
    ns2 = fin.Get(sam + S2 + var[0])
    ds2 = fin.Get(sam + S2 + var[1])
    ns3 = fin.Get(sam + S3 + var[0])
    ds3 = fin.Get(sam + S3 + var[1])
    ns4 = fin.Get(sam + S4 + var[0])
    ds4 = fin.Get(sam + S4 + var[1])

    nsi = [ns1, ns2, ns3, ns4]
    dsi = [ds1, ds2, ds3, ds4]

    ch4muEff()


