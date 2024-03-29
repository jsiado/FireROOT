import sys
import ROOT
from plot_dict import *
from ROOT import gROOT, gPad, TEfficiency, TPad

if __name__ == "__main__":
    ''' run it as python extraHelp/TrEff.py rootfile channel. i.e $$ python extraHelp/TrEff.py 55 2mu2e '''

    rt = sys.argv[1]
    ch = sys.argv[2]

    path = "~/nobackup/SIDM_ana/Analysis/CMSSW_10_2_14/src/FireROOT/Analysis/python/outputs/rootfiles/modules/" + str(rt) + ".root"
    fin = ROOT.TFile(path, "READ")
    
    #samples
    S1 = "mXX-100_mA-0p25_lxy-300"
    S2 = "mXX-500_mA-0p25_lxy-300"
    S3 = "mXX-500_mA-1p2_lxy-300"
    S4 = "mXX-1000_mA-5_lxy-300"
    
    color, samples = [1,2,3,4], [S1, S2, S3, S4]
    sam = "ch" + str(ch)+ "/sig/"
    





    #var = ["Mat_dR", "Tot_dR", "Mat_pT", "Tot_pT", "Mat_d0", "Tot_d0", "Mat_lxy", "Tot_lxy"]
    var = ["dR", "pT"]

    for v in var:
        print ('=======',v)
        '''c = ROOT.TCanvas("c","c")
        c.SetGrid(1,1)
        c.cd()
        
        leg = ROOT.TLegend(0.4412607,0.1932773,0.8223496,0.4453782)
        leg.SetBorderSize(0)
        leg.SetHeader("Samples:","C");
        leg.SetBorderSize(0);
        leg.SetFillStyle(0)

        the_axis = ROOT.TH2F("he_axis",";e ;Efficiency ",50,0.0,0.5,12,0,1.4)
        the_axis.GetYaxis().SetTitleOffset(0.98)
        the_axis.SetStats(0)
        the_axis.Draw("same")'''

        for s in samples:
            num = fin.Get(sam + s + "/Mat_" + v)
            den = fin.Get(sam + s + "/Tot_" + v)
#            print(sam + s + "/Mat_" + v)
    
            '''eff = ROOT.TEfficiency(num, den)
            eff.SetLineColor(ROOT.kRed)
            eff.SetMarkerColor(ROOT.kRed)
    
            leg.AddEntry(eff, S2, "l")
            eff.Draw("pe same")'''
        
        '''c.Draw()
        leg.Draw()
        c.SaveAs("aaaa.png")
        c.Close()'''


    x = input("")











    '''num = fin.Get(sam + S2 + "Mat_dR")
    den = fin.Get(sam + S2 + "Tot_dR")
    
    c_met = ROOT.TCanvas("c_met","c_met")
    c_met.SetGrid(1,1)
    c_met.cd()

    h_eff_axis = ROOT.TH2F("h_met_axis",";E_{T}^{miss} [GeV];Efficiency of HLT_PFMET170")
    h_eff_axis.GetYaxis().SetTitleOffset(1.0)
    h_eff_axis.Draw()

    eff = ROOT.TEfficiency(num,den)
    eff.SetLineColor(ROOT.kRed)
    
    eff.Draw()
    
    c_met.SaveAs("estaesyque.pdf")'''


    '''for key in pairs:
        canvas=ROOT.TCanvas("TrEff", "TrEff")
        canvas.SetGrid()
        canvas.cd()

        legend = ROOT.TLegend(0.4412607,0.1932773,0.8223496,0.4453782)
        legend.SetFillStyle(1001)
        legend.SetBorderSize(0)


        for s in samples:
            num = fin.Get(sam + s + key)
            den = fin.Get(sam + s + pairs[key])

            eff = ROOT.TEfficiency(num,den)


            Efficiency = ROOT.TGraphAsymmErrors(num,den)
            Efficiency.SetLineColor(linecolor[1])
            Efficiency.SetMarkerStyle(markerstylesolid[1])
            Efficiency.SetMarkerColor(markercolor[1])
            Efficiency.SetMarkerSize(1.5)
            Efficiency.SetTitle("Trigger Efficiency")
            Efficiency.GetXaxis().SetTitle("p_{T}^{Miss}(GeV)")
            Efficiency.GetYaxis().SetTitle("Trigger Efficiency")
            Efficiency.GetYaxis().SetRange(0,2)
            Efficiency.Draw("ap same")
            legend.AddEntry(Efficiency,"MET Trigger","ep")

        legend.Draw("same")'''

            
        #for s in Samples:
         #   h = fin.Get(sam + s + var)
          #  h.SetStats(0)
           # #h.GetYaxis().SetRangeUser(0, maxi+50)
            #h.SetLineColor(color[i])
            #leg.AddEntry(h, s, "l")
            #h.Draw("hist same")
            #i+=1
        #c.Draw()
        #leg.Draw()
#        c.Print("../outputs/plots/TrEff/" + ch + "_" + var + ".png")'''
        
    #for num in pairs:
     #   print (num)
      #  print(pairs[num])
        
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
