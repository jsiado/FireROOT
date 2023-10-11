import sys
import ROOT

from ROOT import gROOT, gPad, TEfficiency, TPad

#plots variables for all samples
def make_plots_samples():
    htod = ["gen_dR", "gen_pTl", "gen_pTs", "g1all_dR", "diff1_pT", "diff2_pT", "reco_dR", "g2all_dR", "lead_dR", "sub_dR", "reco_pTl", "reco_pTs", "lindex", "sindex"]
    #htod = ["gen_n","gen_dR", "gen_pTl", "gen_pTs","dsa_n", "pf_n", "reco_n", "g1all_dR", "diff1_pT", "diff2_pT", "reco_dR", "g2all_dR", "lead_dR", "sub_dR", "reco_pTl", "reco_pTs", "lindex", "sindex"]

#, "leadptband", "diff1_pTrebin", "diff1_pTrebin2"]
    #htod = ["diff1_pT", "diff2_pT", "reco_pTl", "reco_pTs"]
	#"gen_diff_pT", "reco_lindex","reco_sindex","reco_gen0p4", "reco_gen0p3", "reco_gen0p2"]
    #htod = ["gen_dR"]
    #htod = ["ljmu_n", "ljall_n"] #for ljsources
    for hd in htod:
        c1_ = ROOT.TCanvas(hd,hd, 600, 400)
        c1_.SetGrid(1,1)
        c1_.cd()
        leg1_ = ROOT.TLegend (.6, .6, .9, .9)
        leg1_.SetHeader("samples", "C")
        leg1_.SetBorderSize(0)
        leg1_.SetFillStyle(0)

        maxb = 0
        for i, sam in enumerate(samples):
            hist = fin.Get("ch" + ch + "/sig/" + sam + "/" + hd)
            maxy = hist.GetBinContent(hist.GetMaximumBin())
            if maxy > maxb:
                maxb = maxy

        for i,sam in enumerate(samples):
            hist = fin.Get("ch" + ch + "/sig/" + sam + "/" + hd)
            if i == 0:
                hist.SetStats(0)
                hist.SetAxisRange(0., maxb + maxb*0.2,"Y")
            hist.SetLineColor(colors[i])
            hist.SetMarkerColor(colors[i])
            hist.SetMarkerStyle(markers[i])
            leg1_.AddEntry(hist, sam, "p")
            hist.Draw("same")
        leg1_.Draw()
        if "dR" in hd:
            c1_.SaveAs('extraHelp/plots/' + str(np) + '_' + ch + '_' + hd + '.png')
        else:
            c1_.SaveAs('extraHelp/plots/' + str(np) + '_' + ch + '_' + hd + '.pdf')


def drboth():
    c4_ = ROOT.TCanvas("c4_","c4_", 600, 400)
    c4_.SetGrid(1,1)
    c4_.cd()
    leg4_ = ROOT.TLegend (.6, .6, 0.9, .9)
    leg4_.SetHeader(stest, "C")
    leg4_.SetBorderSize(0)
    leg4_.SetFillStyle(0)

    htod = ["gen_dR", "reco_dR"]
    maxb = 0
    for j, h in enumerate(htod):
        hist = fin.Get("ch" + ch + "/sig/" + stest + "/" + h)
        maxy = hist.GetBinContent(hist.GetMaximumBin())
        if maxy > maxb:
            maxb = maxy
    for i,h in enumerate(htod):
        hist = fin.Get("ch" + ch + "/sig/" + stest + "/" + h)
        hist.SetStats(0)
        hist.SetAxisRange(0., maxb + maxb*0.2,"Y")
        hist.SetLineColor(colors[i])
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerStyle(markers[i])
        hist.SetTitle("Comparing #Delta R gen and reco; #Delta R; Events")
        leg4_.AddEntry(hist, h, "p")
        hist.Draw("same")
    leg4_.Draw()
    c4_.SaveAs('extraHelp/plots/' + str(np) + '_' + ch + '_both_dR.png')


def Plots_TriHist():
    htod = ["dR", "pT", "eta", "d0", "ID", "zdpt", "zdlxy"]# need to add d0, zd for != lxy
    #htod = ["d0","pTlxys","pTlxym","pTlxyl"]
    for i, hd in enumerate(htod):
        can = ROOT.TCanvas(hd,hd, 600, 400)
        can.SetGrid(1,1)
        can.cd()
        leg = ROOT.TLegend (.6, .6, .9, .9)
        leg.SetHeader(stest, "C")
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)

        den = fin.Get("ch" + ch + "/sig/" + stest + "/Total_" + hd)
        maxy = den.GetBinContent(den.GetMaximumBin())
        num = fin.Get("ch" + ch + "/sig/" + stest + "/Passed_" + hd)
        den.SetAxisRange(0., 1.2*maxy, "Y")
        den.SetTitle("Passed and Total distributions")
        den.SetStats(0)
        den.SetLineColor(2)
        den.SetMarkerColor(2)
        den.SetMarkerStyle(22)
        num.SetLineColor(4)
        num.SetMarkerColor(4)
        num.SetMarkerStyle(23)
        leg.AddEntry(num, "Passed", "p")
        leg.AddEntry(den, "Total", "p")
        den.Draw("same")
        num.Draw("same")
        leg.Draw()
        if "dR" in hd:
            can.SaveAs('extraHelp/plots/' + str(np) + '_' + ch +'_trigger_hist_'+ hd + '.png')
        else:
            can.SaveAs('extraHelp/plots/' + str(np) + '_' + ch +'_trigger_hist_'+ hd + '.pdf')

#plots variables for all samples
def hptmuons():
    htod = ["pf_pT", "dsa_pT"]
    for hd in htod:
        cm1_ = ROOT.TCanvas(hd,hd, 600, 400)
        cm1_.SetGrid(1,1)
        cm1_.cd()
        leg1_ = ROOT.TLegend (.6, .6, .9, .9)
        leg1_.SetHeader("samples", "C")
        leg1_.SetBorderSize(0)
        leg1_.SetFillStyle(0)

        maxb = 0
        for i, sam in enumerate(samples):
            hist = fin.Get("ch" + ch + "/sig/" + sam + "/" + hd)
            maxy = hist.GetBinContent(hist.GetMaximumBin())
            if maxy > maxb:
                maxb = maxy

        for i,sam in enumerate(samples):
            hist = fin.Get("ch" + ch + "/sig/" + sam + "/" + hd)
            if i == 0:
                hist.SetStats(0)
                hist.SetAxisRange(0., maxb + maxb*0.2,"Y")
            hist.SetLineColor(colors[i])
            hist.SetMarkerColor(colors[i])
            hist.SetMarkerStyle(markers[i])
            leg1_.AddEntry(hist, sam, "p")
            hist.Draw("same")
        leg1_.Draw()
#        c1_.SaveAs('extraHelp/plots/' + str(np) + '_' + ch + '_' + hd + '.pdf')



if __name__ == "__main__":
    ''' run it as 
    python extraHelp/ch2mu2eTrEff.py diff channel root_file 
    i.e $$ python extraHelp/eff.py 55 "2mu2e" ljch2mu2eTrEff
    '''
    
    np = sys.argv[1] #plot differentiator
    ch = sys.argv[2] #channel
    rt = sys.argv[3] #root file

    fin = ROOT.TFile("~/nobackup/SIDM_ana/Analysis/CMSSW_10_2_14/src/FireROOT/Analysis/python/outputs/rootfiles/modules/" + rt +".root", "READ")
    fin2 = ROOT.TFile("~/nobackup/SIDM_ana/Analysis/CMSSW_10_2_14/src/FireROOT/Analysis/python/outputs/rootfiles/modules/" + rt +".root", "READ")

    #samples
    S1 = "mXX-100_mA-0p25_lxy-300/"
    S2 = "mXX-500_mA-0p25_lxy-300/"
    S3 = "mXX-500_mA-1p2_lxy-300/"
    S4 = "mXX-1000_mA-5_lxy-300/"
    #S5 = "mXX-100_mA-5_lxy-0p3/"

    colors = [1,2,3,4,5]
    samples = [S1, S2, S3, S4]
    markers = [20,21,22,23,34, 35]

    stest = S3

    #make_plots_samples()
    #drboth()
    #Plots_TriHist()
    hptmuons()
    
    x = str(raw_input("Done plotting...."))
