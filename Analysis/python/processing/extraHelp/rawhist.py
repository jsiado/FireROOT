import sys
import ROOT

from ROOT import gROOT, gPad, TEfficiency, TPad

def ch4muNumdR():
	cr = ROOT.TCanvas("canr", "", 600, 600)
	leg = ROOT.TLegend (.5, .5, 0.85, .85)
	leg.SetHeader("Samples:","C");
	leg.SetBorderSize(0)

	i, nmax = 0, 0

	for nd in nsi:
		if nd.GetMaximum()>nmax:
			nmax = nd.GetMaximum()

	for ns in nsi:
	    ns.SetStats(0)
	    ns.GetYaxis().SetRangeUser(0, nmax+50)
	    ns.SetLineColor(color[i])
	    leg.AddEntry(ns, Samples[i], "l")
	    ns.Draw("hist same")
	    i+=1
    
	leg.Draw()
	cr.Print("ch4muNum.pdf")

def plotNum():
        cnum = ROOT.TCanvas("cann", "", 600, 600)
        leg = ROOT.TLegend (.5, .5, 0.85, .85)
        leg.SetHeader("Samples:","C");
        leg.SetBorderSize(0)

        i, nmax = 0, 0

        for nd in nsi:
                if nd.GetMaximum()>nmax:
                        nmax = nd.GetMaximum()

        for ns in nsi:
            ns.SetStats(0)
            ns.GetYaxis().SetRangeUser(0, nmax+50)
            ns.SetLineColor(color[i])
            leg.AddEntry(ns, Samples[i], "l")
            ns.Draw("hist same")
            i+=1

        leg.Draw()
        cp.Print("ch4muNum.pdf")
	
def ch4muDendR():
	c1 = ROOT.TCanvas("can1", "", 600, 600)
	leg = ROOT.TLegend (.5, .5, 0.85, .85)
	leg.SetHeader("Samples:","C");
	leg.SetBorderSize(0)

	i, nmax = 0, 0
	
	for nd in dsi:
		if nd.GetMaximum()>nmax:
			nmax = nd.GetMaximum()

	for ns in dsi:
	    ns.SetStats(0)
	    ns.GetYaxis().SetRangeUser(0, nmax+50)
	    ns.SetLineColor(color[i])
	    leg.AddEntry(ns, Samples[i], "l")
	    ns.Draw("hist same")
	    i+=1
    
	leg.Draw()
	c1.Print("ch4muDen.pdf")
	
	
def ch4muEff():
        #TEfficiency eff1 = 0 
  #      TEfficiency (eff1 , const char *title, Int_t nbinsx, Double_t xlow, Double_t xup, Int_t nbinsy, Double_t ylow, Double_t yup) 
        #eff1 = TEfficiency("eff1","my efficiency;x;y;#epsilon",10,0,10,20,0,1);
        eff1 = TEfficiency("eff1", "eff def", 10, 0,1, 10, 0, 1)

	c2 = ROOT.TCanvas("can2", "", 600, 600)
	leg = ROOT.TLegend (.5, .2, 0.85, .55)
	leg.SetHeader("Samples:","C");
	leg.SetBorderSize(0)
	
	eff1 = ROOT.TEfficiency(ns1, ds1)
	eff1.SetLineColor(1)
	#eff1.SetRangeUser(0,1, "Y")
        eff1.SetTitle(" ; #Delta R(#mu_{1},#mu_{2}); Efficiency (#epsilon)");
	eff1.Draw()
	#gpad.Update()
	#gr = eff1.GetPaintedGraph()
	#gr.SetMinimum(0)
	#gr.SetMaximum(1)
	#gpad.Update()
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
	
	
	'''i = 0
	
	for ij in range(len(nsi)):
		eff = ROOT.TEfficiency(nsi[ij], dsi[ij])
		eff.SetLineColor(color[i])
		eff.Draw("same")
		leg.AddEntry(eff, Samples[i], "l")
		i+=1
	c2.Draw()
	leg.Draw()'''
	c2.Print("ch4muEffdR.pdf")

#def plotnum():


if __name__ == "__main__":
    ''' 
    run it as python extraHelp/TrEff.py rootfile channel. i.e $$ python extraHelp/TrEff.py 55 2mu2e
    '''
    rt = sys.argv[1]
    ch = sys.argv[2]

    path = "~/nobackup/SIDM_ana/Analysis/CMSSW_10_2_14/src/FireROOT/Analysis/python/outputs/rootfiles/modules/"
    root_file = "out_" + str(rt) + ".root"
    fin = ROOT.TFile(path+ root_file, "READ")
    
    #samples
    S1 = "mXX-100_mA-0p25_lxy-300/"
    S2 = "mXX-500_mA-0p25_lxy-300/"
    S3 = "mXX-500_mA-1p2_lxy-300/"
    S4 = "mXX-1000_mA-5_lxy-300/"
    
    color = [1,2,3,4]
    Samples = [S1, S2, S3, S4]
    
    sam = "ch" + str(ch)+ "/sig/"
    variables = ["Mat_dR", "Tot_dR", "Mat_pT", "Tot_pT", "Mat_d0", "Tot_d0", "Mat_lxy", "Tot_lxy"]
    
    '''for var in variables:
        c = ROOT.TCanvas(var, "", 600, 600)
        leg = ROOT.TLegend (.5, .5, 0.85, .85)
        leg.SetHeader("Samples:","C");
        leg.SetBorderSize(0)
        i, maxi = 0, 100
        
        for s in Samples:
            h = fin.Get(sam + s + var)
            if h.GetMaximum()>maxi:
                maxi = h.GetMaximum()
                            
        for s in Samples:
            h = fin.Get(sam + s + var)
            h.SetStats(0)
            h.GetYaxis().SetRangeUser(0, maxi+50)
            h.SetLineColor(color[i])
            leg.AddEntry(h, s, "l")
            h.Draw("hist same")
            i+=1
        c.Draw()
        leg.Draw()
        c.Print("../outputs/plots/TrEff/" + ch + "_" + var + ".png")'''
        
        
        #eff start here
        #eff1 = TEfficiency("eff1", "eff def", 10, 0,1, 10, 0, 1)
        #c2 = ROOT.TCanvas("can2", "", 600, 600)
    pairs = {"Mat_dR":"Tot_dR", "Mat_p":"Tot_pT"}
    print (pairs.keys)
    #for i in pairs.Keys:
    '''num = fin.Get(sam +s + num)

        #num = fin.Get(sam + s + var)
        den
        Efficiency = ROOT.TGraphAsymmErrors(Numerator,Denominator,'MET')
        Efficiency.SetLineColor(linecolor[1])
        Efficiency.SetMarkerStyle(markerstylesolid[1])
        Efficiency.SetMarkerColor(markercolor[1])
        Efficiency.SetMarkerSize(1.5)
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


    leg = ROOT.TLegend (.5, .2, 0.85, .55)
    leg.SetHeader("Samples:","C");
    leg.SetBorderSize(0)

    eff1 = ROOT.TEfficiency(ns1, ds1)
    eff1.SetLineColor(1)
    eff1.SetTitle(" ; #Delta R(#mu_{1},#mu_{2}); Efficiency (#epsilon)");
    eff1.Draw()                                                                                                                                              
    leg.AddEntry(eff1, S1, "l")
    eff2 = ROOT.TEfficiency(ns2, ds2)'''



    
 
        
    '''rtfile = "out_" + id + ".root"
    fin = ROOT.TFile(path+rtfile, "READ")

    numr, denr = "/Mat_dR", "/Tot_dR"
    
    ns1 = fin.Get(ch + S1 + numr)
    ds1 = fin.Get(ch + S1 + denr)
    ns2 = fin.Get(ch + S2 + numr)
    ds2 = fin.Get(ch + S2 + denr)
    ns3 = fin.Get(ch + S3 + numr)
    ds3 = fin.Get(ch + S3 + denr)
    ns4 = fin.Get(ch + S4 + numr)
    ds4 = fin.Get(ch + S4 + denr)

    nsi = [ns1, ns2, ns3, ns4]
    dsi = [ds1, ds2, ds3, ds4]

    #ch4muNumdR()
    #ch4muDendR()
    ch4muEff()'''


