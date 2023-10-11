import sys
import ROOT

from ROOT import gROOT, gPad, TEfficiency, TPad

#plots variables for all samples
def make_plots_samples():

    htod = ["ONETRG"]
    #htod = ["diff1_pT", "diff2_pT", "reco_pTl", "reco_pTs"]
    #htod = ["ljmu_n", "ljall_n"] #for ljsources

    for hd in htod:
        c1_ = ROOT.TCanvas(hd,hd, 600, 400)
        c1_.SetGrid(1,1)
        c1_.cd()
        leg1_ = ROOT.TLegend (.6, .6, .9, .9)
        leg1_.SetHeader("samples", "C")
        leg1_.SetBorderSize(0)
        leg1_.SetFillStyle(0)

        '''maxb = 0
        for i, sam in enumerate(samples):
            hist = fin.Get("ch" + ch + "/sig/" + sam + "/" + hd)
            maxy = hist.GetBinContent(hist.GetMaximumBin())
            if maxy > maxb:
                maxb = maxy'''

        hist = fin.Get("ch" + ch + "/sig/" + stest + "/" + hd)


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
        c1_.SaveAs('extraHelp/plots/' + str(np) + '_' + ch + '_' + hd + '.pdf')


def addtrg():
    for ch in channel:
        hist = fin.Get("ch" + ch + "/sig/" + stest + "/oneTRG")
        for i in range(hist.GetNbinsX()):
            print(ch, i+9, hist.GetBinContent(i))

                
    '''c1_ = ROOT.TCanvas("addtrg","addtrg", 600, 400)
    c1_.SetGrid(1,1)
    c1_.cd()
    leg4_ = ROOT.TLegend (.6, .6, 0.9, .9)
    leg4_.SetHeader(stest, "C")
    leg4_.SetBorderSize(0)
    leg4_.SetFillStyle(0)

    htod = ["oneTRG"]
    hist = fin.Get("ch" + ch + "/sig/" + stest + "/" + htod[0])

    hist.Draw()
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
        hist.SetTitle("Events passing any of the DiMu; TRG Path; Events")
        leg4_.AddEntry(hist, h, "p")
        hist.Draw("same")'''
    #leg4_.Draw()'''
    #c1_.SaveAs('extraHelp/plots/addtrg.pdf')


if __name__ == "__main__":
    ''' run it as 
    python extraHelp/additionalTRG.py iff channel root_file 
    i.e $$ python extraHelp/additionalTRG.py 55 "2mu2e" ljch2mu2eTrEff
    '''
    
    channel = ["2mu2e", "4mu"]
    #np = sys.argv[1] #plot differentiator
    #ch = sys.argv[1] #channel
    #rt = sys.argv[3] #root file

    fin = ROOT.TFile("~/nobackup/SIDM_ana/Analysis/CMSSW_10_2_14/src/FireROOT/Analysis/python/outputs/rootfiles/modules/additionalTRG.root", "READ")

    #samples
    S1 = "mXX-100_mA-0p25_lxy-300/"
    S2 = "mXX-500_mA-0p25_lxy-300/"
    S3 = "mXX-500_mA-1p2_lxy-300/"
    S4 = "mXX-1000_mA-5_lxy-300/"
    #S5 = "mXX-100_mA-5_lxy-0p3/"

    colors = [1,2,3,4,5]
    samples = [S1, S2, S3, S4]
    markers = [20,21,22,23,34, 35]

    stest = S4

    #make_plots_samples()
    addtrg()
    #drboth()
    #Plots_TriHist()


    x = str(raw_input("Done plotting...."))
