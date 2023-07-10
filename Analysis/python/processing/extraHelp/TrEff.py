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

def myarg(argv):
        arg_id = ''
        arg_ch = ''
        arg_hp = "run as $ {0} -r <rt_file> -c <channel> ".format(argv[0])
        
        try:
                opts, args = getopt.getopt(argv[1:], "r:c:", ["help", "rt_file=", "channel="])
        except:
                print(arg_help)
                sys.exit(2)

        for opt, arg in opts:
                if opt in ("-h", "--help"):
                        sys.exit(2)
                elif opt in ("-r", "--rt_file"):
                        arg_id = arg
                elif opt in ("-c", "--channel"):
                        arg_ch = arg

        output = (str(arg_id)+' '+str(arg_ch)+' '+'\n')
        print(output)
        #fout = open("alltxt/mybike.txt", "a")
        #fout.write(output)
        #fout.close()
        return id

if __name__ == "__main__":
        ch = sys.argv[1]
        rt = sys.argv[2]
        #print (sys.argv[1])
	#id = 60
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
	
	variables = ["Mat_dR", "Tot_dR", "Mat_pT", "Tot_pT", "Mat_d0", "Tot_d0"]

	for var in variables:
		c = ROOT.TCanvas(var, "", 600, 600)
		leg = ROOT.TLegend (.5, .5, 0.85, .85)
		leg.SetHeader("Samples:","C");
		leg.SetBorderSize(0)
		i = 0
		maxi = 100
		
		for s in Samples:
			h = fin.Get(sam + s + var)
			if h.GetMaximum()>maxi:
				maxi = h.GetMaximum()
		
		for s in Samples:
			h = fin.Get(sam + s + var)
			h.SetStats(0)
			h.GetYaxis().SetRangeUser(0, maxi+50)
			
			'''if h.GetMaximum()>maxi:
				maxi = h.GetMaximum()
				h.GetYaxis().SetRangeUser(0, maxi+50)
				print(var, maxi)'''
			
			
			h.SetLineColor(color[i])
			leg.AddEntry(h, s, "l")
			h.Draw("hist same")
			i+=1

		c.Draw()
		leg.Draw()
		c.Print("../outputs/plots/TrEff/" + ch + "_" + var + ".png")
	fin.Close()

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


