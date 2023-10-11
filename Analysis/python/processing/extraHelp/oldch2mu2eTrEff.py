import sys
import ROOT

from ROOT import gROOT, gPad, TEfficiency, TPad

def nngen():
    c1_ = ROOT.TCanvas("c1_","c1_", 600, 400)
    c1_.SetGrid(1,1)
    c1_.cd()
    leg1_ = ROOT.TLegend (.6, .6, .9, .9)
    leg1_.SetHeader("samples", "C")
    leg1_.SetBorderSize(0)
    leg1_.SetFillStyle(0)
    
    htod = "ngenall"
    
    maxb = 0
    for i, sam in enumerate(samples):
        hist = fin.Get("ch" + ch[0] + "/sig/" + sam + "/" + htod)
        maxy = hist.GetBinContent(hist.GetMaximumBin())
        if maxy > maxb:
            maxb = maxy

    for i,sam in enumerate(samples):
        hist = fin.Get("ch" + ch[0] + "/sig/" + sam + "/" + htod)
        if i == 0:
            hist.SetStats(0)
            hist.SetAxisRange(0., maxb + maxb*0.2,"Y")
            hist.SetTitle("Number of gen muons; Muons;Events")
        hist.SetLineColor(colors[i])
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerStyle(markers[i])
        leg1_.AddEntry(hist, sam, "p")
        hist.Draw("same")
    leg1_.Draw()
    c1_.SaveAs('extraHelp/plots/' + str(np) + '_n_gen.pdf')



def ngen():
    htod = ["ngenall", "gen_dR"]
    for hd in htod:
        c1_ = ROOT.TCanvas("c1_","c1_", 600, 400)
        c1_.SetGrid(1,1)
        c1_.cd()
        leg1_ = ROOT.TLegend (.6, .6, .9, .9)
        leg1_.SetHeader("samples", "C")
        leg1_.SetBorderSize(0)
        leg1_.SetFillStyle(0)

        maxb = 0
        for i, sam in enumerate(samples):
            hist = fin.Get("ch" + ch[0] + "/sig/" + sam + "/" + hd)
            maxy = hist.GetBinContent(hist.GetMaximumBin())
            if maxy > maxb:
                maxb = maxy

        for i,sam in enumerate(samples):
            hist = fin.Get("ch" + ch[0] + "/sig/" + sam + "/" + hd)
            if i == 0:
                hist.SetStats(0)
                hist.SetAxisRange(0., maxb + maxb*0.2,"Y")
                hist.SetTitle("Number of gen muons; Muons;Events")
            hist.SetLineColor(colors[i])
            hist.SetMarkerColor(colors[i])
            hist.SetMarkerStyle(markers[i])
            leg1_.AddEntry(hist, sam, "p")
            hist.Draw("same")
        leg1_.Draw()
        c1_.SaveAs('extraHelp/plots/' + str(np) + '_' + hd+ '.pdf')




def drgen():
    c2_ = ROOT.TCanvas("c2_","c2_", 600, 400)
    c2_.SetGrid(1,1)
    c2_.cd()
    leg2_ = ROOT.TLegend (.6, .6, 0.9, .9)
    leg2_.SetHeader("Samples", "C")
    leg2_.SetBorderSize(0)
    leg2_.SetFillStyle(0)

    htod = "gen_dR"

    maxb = 0
    for j, sam in enumerate(samples):
        hist = fin.Get("ch" + ch[0] + "/sig/" + sam + "/" + htod)
        maxy = hist.GetBinContent(hist.GetMaximumBin())
        if maxy > maxb:
            maxb = maxy

    for i,sam in enumerate(samples):
        hist = fin.Get("ch" + ch[0] + "/sig/" + sam + "/" + htod)
        if i == 0:
            hist.SetStats(0)
            hist.SetAxisRange(0., maxb + maxb*0.1,"Y")
            hist.SetTitle("#Delta R for gen muons; #Delta R; Events")

        hist.SetLineColor(colors[i])
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerStyle(markers[i])
        leg2_.AddEntry(hist, sam, "p")
        hist.Draw("same")
    leg2_.Draw()
    c2_.Draw()
    c2_.SaveAs('extraHelp/plots/' + str(np) + '_dR_gen.png')

def drreco():
    c3_ = ROOT.TCanvas("c3_","c3_", 600, 400)
    c3_.SetGrid(1,1)
    c3_.cd()
    leg3_ = ROOT.TLegend (.6, .6, 0.9, .9)
    leg3_.SetHeader("Samples", "C")
    leg3_.SetBorderSize(0)
    leg3_.SetFillStyle(0)

    htod = "reco_dR"
    maxb = 0
    for j, sam in enumerate(samples):
        hist = fin.Get("ch" + ch[0] + "/sig/" + sam + "/" + htod)
        maxy = hist.GetBinContent(hist.GetMaximumBin())
        if maxy > maxb:
            maxb = maxy

    for i,sam in enumerate(samples):
        hist = fin.Get("ch" + ch[0] + "/sig/" + sam + "/" + htod)
        hist.SetStats(0)
        hist.SetAxisRange(0., maxb + maxb*0.1,"Y")
        hist.SetLineColor(colors[i])
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerStyle(markers[i])
        hist.SetTitle("#Delta R reco; #Delta R; Events")
        leg3_.AddEntry(hist, sam, "p")
        hist.Draw("same")
    leg3_.Draw()
    c3_.SaveAs('extraHelp/plots/' + str(np) + '_dR_reco.png')


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
        hist = fin.Get("ch" + ch[0] + "/sig/" + stest + "/" + h)
        maxy = hist.GetBinContent(hist.GetMaximumBin())
        if maxy > maxb:
            maxb = maxy

    for i,h in enumerate(htod):
        hist = fin.Get("ch" + ch[0] + "/sig/" + stest + "/" + h)
        hist.SetStats(0)
        hist.SetAxisRange(0., maxb + maxb*0.1,"Y")
        hist.SetLineColor(colors[i])
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerStyle(markers[i])
        hist.SetTitle("Comparing #Delta R gen and reco; #Delta R; Events")
        leg4_.AddEntry(hist, h, "p")
        hist.Draw("same")
    leg4_.Draw()
    c4_.SaveAs('extraHelp/plots/' + str(np) + '_dR_both.png')

def matching_Hists():
    c5_ = ROOT.TCanvas("c5_","c5_", 600, 400)
    c5_.SetGrid(1,1)
    c5_.cd()
    leg5_ = ROOT.TLegend (.6, .6, .9, .9)
    leg5_.SetBorderSize(0)
    leg5_.SetFillStyle(0)
    
    htod = ["eff_num", "eff_den"]
    maxb = 0
    for i, h in enumerate(htod):
        hist = fin.Get("ch" + ch[0] + "/sig/" + stest + "/" + h)
        maxy = hist.GetBinContent(hist.GetMaximumBin())
        if maxy > maxb:
            maxb = maxy
    for i,h in enumerate(htod):
        hist = fin.Get("ch" + ch[0] + "/sig/" + stest + "/" + h)
        hist.SetAxisRange(0., maxb+ 0.15*maxb,"Y")
        hist.SetStats(0)
        hist.SetLineColor(colors[i])
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerStyle(markers[i])
        hist.SetTitle("Leading p_{T} gen muons; p_{T}^{gen} [GeV]; Events")
        leg5_.AddEntry(hist, h[4:], "p")
        hist.Draw("same")
    leg5_.Draw()
    c5_.SaveAs('extraHelp/plots/' + str(np) + '_pT_match_hist.pdf')


def pT_TriHist():
    c6_ = ROOT.TCanvas("c6_","c6_", 600, 400)
    c6_.SetGrid(1,1)
    c6_.cd()
    leg6_ = ROOT.TLegend (.6, .6, .9, .9)
    leg6_.SetBorderSize(0)
    leg6_.SetFillStyle(0)
    
    htod = ["Match_pT", "Total_pT"]
    maxb = 0
    for i, h in enumerate(htod):
        hist = fin.Get("ch" + ch[0] + "/sig/" + stest + "/" + h)
        maxy = hist.GetBinContent(hist.GetMaximumBin())
        if maxy > maxb:
            maxb = maxy
    for i,h in enumerate(htod):
        hist = fin.Get("ch" + ch[0] + "/sig/" + stest + "/" + h)
        hist.SetAxisRange(0., maxb + 0.15*maxb ,"Y")
        hist.SetStats(0)
        hist.SetLineColor(colors[i])
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerStyle(markers[i])
        hist.SetTitle(" ; p_{T lea}^{gen} [GeV]; Events")
        leg6_.AddEntry(hist, h[:], "p")
        hist.Draw("same")
    leg6_.Draw()
    c6_.SaveAs('extraHelp/plots/' + str(np) + '_pT_trigger_hist.pdf')


def dR_TriHist():
    c7_ = ROOT.TCanvas("c7_","c7_", 600, 400)
    c7_.SetGrid(1,1)
    c7_.cd()
    leg7_ = ROOT.TLegend (.6, .6, .9, .9)
    leg7_.SetBorderSize(0)
    leg7_.SetFillStyle(0)
    
    htod = ["Match_dR", "Total_dR"]
    maxb = 0
    for i, h in enumerate(htod):
        hist = fin.Get("ch" + ch[0] + "/sig/" + stest + "/" + h)
        maxy = hist.GetBinContent(hist.GetMaximumBin())
        if maxy > maxb:
            maxb = maxy
    for i,h in enumerate(htod):
        hist = fin.Get("ch" + ch[0] + "/sig/" + stest + "/" + h)
        if i == 0:
            hist.SetAxisRange(0., maxb + 0.15*maxb ,"Y")
            hist.SetStats(0)
            hist.SetTitle("; Reco #Delta R; Events")
        hist.SetLineColor(colors[i])
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerStyle(markers[i])
        leg7_.AddEntry(hist, h[:], "p")
        hist.Draw("same")
    leg7_.Draw()
    c7_.SaveAs('extraHelp/plots/' + str(np) + '_dR_trigger_hist.pdf')


def pT_diff1():
    c8_ = ROOT.TCanvas("c8_","c8_", 600, 400)
    c8_.SetGrid(1,1)
    c8_.cd()
    leg8_ = ROOT.TLegend (.6, .6, .9, .9)
    leg8_.SetBorderSize(0)
    leg8_.SetFillStyle(0)

    htod = "diff1"
    maxb = 0
    for i, sam in enumerate(samples):
        hist = fin.Get("ch" + ch[0] + "/sig/" + sam + "/" + htod)
        maxy = hist.GetBinContent(hist.GetMaximumBin())
        if maxy > maxb:
            maxb = maxy
    for i,sam in enumerate(samples):
        hist = fin.Get("ch" + ch[0] + "/sig/" + sam + "/" + htod)
        if i == 0:
            hist.SetAxisRange(0., maxb + 0.15*maxb ,"Y")
            hist.SetStats(0)
            #hist.SetTitle("; Rec #Delta R; Events")
        hist.SetLineColor(colors[i])
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerStyle(markers[i])
        leg8_.AddEntry(hist, sam, "p")
        hist.Draw("same")
    leg8_.Draw()
    c8_.SaveAs('extraHelp/plots/' + str(np) + '_pT_diff1.pdf')


def pT_gen_lead():
    c9_ = ROOT.TCanvas("c9_","c9_", 600, 400)
    c9_.SetGrid(1,1)
    c9_.cd()
    leg9_ = ROOT.TLegend (.6, .6, .9, .9)
    leg9_.SetBorderSize(0)
    leg9_.SetFillStyle(0)

    htod = "gen_pTl"
    maxb = 0
    for i, sam in enumerate(samples):
        hist = fin.Get("ch" + ch[0] + "/sig/" + sam + "/" + htod)
        maxy = hist.GetBinContent(hist.GetMaximumBin())
        if maxy > maxb:
            maxb = maxy
    for i,sam in enumerate(samples):
        hist = fin.Get("ch" + ch[0] + "/sig/" + sam + "/" + htod)
        if i == 0:
            hist.SetAxisRange(0., maxb + 0.15*maxb ,"Y")
            hist.SetStats(0)
        hist.SetLineColor(colors[i])
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerStyle(markers[i])
        leg9_.AddEntry(hist, sam, "p")
        hist.Draw("same")
    leg9_.Draw()
    c9_.SaveAs('extraHelp/plots/' + str(np) + '_pT_gen_lead.pdf')

def pT_gen_sub():
    c10_ = ROOT.TCanvas("c10_","c10_", 600, 400)
    c10_.SetGrid(1,1)
    c10_.cd()
    leg10_ = ROOT.TLegend (.6, .6, .9, .9)
    leg10_.SetBorderSize(0)
    leg10_.SetFillStyle(0)

    htod = "gen_pTs"
    maxb = 0
    for i, sam in enumerate(samples):
        hist = fin.Get("ch" + ch[0] + "/sig/" + sam + "/" + htod)
        maxy = hist.GetBinContent(hist.GetMaximumBin())
        if maxy > maxb:
            maxb = maxy
    for i,sam in enumerate(samples):
        hist = fin.Get("ch" + ch[0] + "/sig/" + sam + "/" + htod)
        if i == 0:
            hist.SetAxisRange(0., maxb + 0.15*maxb ,"Y")
            hist.SetStats(0)
        hist.SetLineColor(colors[i])
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerStyle(markers[i])
        leg10_.AddEntry(hist, sam, "p")
        hist.Draw("same")
    leg10_.Draw()
    c10_.SaveAs('extraHelp/plots/' + str(np) + '_pT_gen_sub.pdf')


def dR_all_gen1_recos():
    c11_ = ROOT.TCanvas("c11_","c11_", 600, 400)
    c11_.SetGrid(1,1)
    c11_.cd()
    leg11_ = ROOT.TLegend (.6, .6, .9, .9)
    leg11_.SetBorderSize(0)
    leg11_.SetFillStyle(0)

    htod = "dR_g1all"
    maxb = 0
    for i, sam in enumerate(samples):
        hist = fin.Get("ch" + ch[0] + "/sig/" + sam + "/" + htod)
        maxy = hist.GetBinContent(hist.GetMaximumBin())
        if maxy > maxb:
            maxb = maxy
    for i,sam in enumerate(samples):
        hist = fin.Get("ch" + ch[0] + "/sig/" + sam + "/" + htod)
        if i == 0:
            hist.SetAxisRange(0., maxb + 0.15*maxb ,"Y")
            hist.SetStats(0)
        hist.SetLineColor(colors[i])
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerStyle(markers[i])
        leg11_.AddEntry(hist, sam, "p")
        hist.Draw("same")
    leg11_.Draw()
    c11_.SaveAs('extraHelp/plots/' + str(np) + '_pT_gen_sub.pdf')


def dR_0p4_gen1_recos():
    c12_ = ROOT.TCanvas("c12_","c12_", 600, 400)
    c12_.SetGrid(1,1)
    c12_.cd()
    leg11_ = ROOT.TLegend (.6, .6, .9, .9)
    leg11_.SetBorderSize(0)
    leg11_.SetFillStyle(0)

    htod = "dR_g1all"
    maxb = 0
    for i, sam in enumerate(samples):
        hist = fin.Get("ch" + ch[0] + "/sig/" + sam + "/" + htod)
        maxy = hist.GetBinContent(hist.GetMaximumBin())
        if maxy > maxb:
            maxb = maxy
    for i,sam in enumerate(samples):
        hist = fin.Get("ch" + ch[0] + "/sig/" + sam + "/" + htod)
        if i == 0:
            hist.SetAxisRange(0., maxb + 0.15*maxb ,"Y")
            hist.SetStats(0)
        hist.SetLineColor(colors[i])
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerStyle(markers[i])
        leg11_.AddEntry(hist, sam, "p")
        hist.Draw("same")
    leg11_.Draw()
    c11_.SaveAs('extraHelp/plots/' + str(np) + '_pT_gen_sub.pdf')

def dR_all_gen1_recos():
    c11_ = ROOT.TCanvas("c11_","c11_", 600, 400)
    c11_.SetGrid(1,1)
    c11_.cd()
    leg11_ = ROOT.TLegend (.6, .6, .9, .9)
    leg11_.SetBorderSize(0)
    leg11_.SetFillStyle(0)

    htod = "dR_g1all"
    maxb = 0
    for i, sam in enumerate(samples):
        hist = fin.Get("ch" + ch[0] + "/sig/" + sam + "/" + htod)
        maxy = hist.GetBinContent(hist.GetMaximumBin())
        if maxy > maxb:
            maxb = maxy
    for i,sam in enumerate(samples):
        hist = fin.Get("ch" + ch[0] + "/sig/" + sam + "/" + htod)
        if i == 0:
            hist.SetAxisRange(0., maxb + 0.15*maxb ,"Y")
            hist.SetStats(0)
        hist.SetLineColor(colors[i])
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerStyle(markers[i])
        leg11_.AddEntry(hist, sam, "p")
        hist.Draw("same")
    leg11_.Draw()
    c11_.SaveAs('extraHelp/plots/' + str(np) + '_pT_gen_sub.pdf')

def make_a_plot():
    canvas = ROOT.TCanvas("canvas","canvas", 600, 400)
    canvas.SetGrid(1,1)
    canvas.cd()
    leg = ROOT.TLegend (.6, .6, .9, .9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    maxb = 0
    for i, sam in enumerate(samples):
        hist = fin.Get("ch" + ch[0] + "/sig/" + sam + "/" + htod)
        maxy = hist.GetBinContent(hist.GetMaximumBin())
        if maxy > maxb:
            maxb = maxy
    for i,sam in enumerate(samples):
        hist = fin.Get("ch" + ch[0] + "/sig/" + sam + "/" + htod)
        if i == 0:
            hist.SetAxisRange(0., maxb + 0.15*maxb ,"Y")
            hist.SetStats(0)
        hist.SetLineColor(colors[i])
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerStyle(markers[i])
        leg.AddEntry(hist, sam, "p")
        hist.Draw("same")
    leg.Draw()
    canvas.SaveAs('extraHelp/plots/' + str(np) + '_' + htod +'.pdf')

def make_plots():

    #htod = ["dR_g1all", "dR_g2all"]

    x = 1
    #for hd in htod:
    if x ==1:
        canvas = ROOT.TCanvas("canvas","canvas", 600, 400)
        canvas.SetGrid(1,1)
        canvas.cd()

        leg = ROOT.TLegend (.6, .6, .9, .9)
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)

        maxb = 0
        for sam in enumerate(samples):
            print("ch" + ch[0] + "/sig/" + sam + "dR_g1all")
            hist = fin.Get("ch" + ch[0] + "/sig/" + sam + "dR_g1all")
            maxy = hist.GetBinContent(hist.GetMaximumBin())
            if maxy > maxb:
                maxb = maxy

        for i,sam in enumerate(samples):
            hist = fin.Get("ch" + ch[0] + "/sig/" + sam + "dR_g1all")
            if i == 0:
                hist.SetAxisRange(0., maxb + 0.15*maxb ,"Y")
                hist.SetStats(0)
            hist.SetLineColor(colors[i])
            hist.SetMarkerColor(colors[i])
            hist.SetMarkerStyle(markers[i])
            leg.AddEntry(hist, sam, "p")
            hist.Draw("same")
        leg.Draw()
        canvas.SaveAs('extraHelp/plots/' + str(np) + '_' + "dR_g1all" +'.pdf')




if __name__ == "__main__":
    ''' run it as python extraHelp/ch2mu2eTrEff.py  i.e $$ python extraHelp/eff.py 55 2mu2e '''
    np = sys.argv[1] #plot differentiator

    fin = ROOT.TFile("~/nobackup/SIDM_ana/Analysis/CMSSW_10_2_14/src/FireROOT/Analysis/python/outputs/rootfiles/modules/ch2mu2eTrEff_rmpt.root", "READ")

    #samples
    S1 = "mXX-100_mA-0p25_lxy-300/"
    S2 = "mXX-500_mA-0p25_lxy-300/"
    S3 = "mXX-500_mA-1p2_lxy-300/"
    S4 = "mXX-1000_mA-5_lxy-300/"

    colors = [1,2,3,4]
    samples = [S1, S2, S3, S4]
    markers = [20,21,22,23,34]
    ch = ["2mu2e", "4mu"]

    stest = S4

    ngen()
    #drgen()
    #drreco()
    #drboth()
    #matching_Hists()
    #pT_TriHist()
    #dR_TriHist()
    #pT_diff1()
    #pT_gen_lead()
    #pT_gen_sub()
    #make_plots()


    x = input("")
