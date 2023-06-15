void TEffpl(const char *id){
    TEfficiency* trEff = 0;//new TEfficiency("eff","my efficiency; x; y;#epsilon", 10,0,10,20,-5,15);
    TFile* f = TFile::Open(Form("../outputs/rootfiles/modules/out_%s.root",id));
  
    TCanvas *canl = new TCanvas("canl","",800,600);
    TLegend *leg_ = new TLegend(.2, .1, 0.45, .35);
    leg_->SetHeader("Samples:","C");
    leg_->SetBorderSize(0);
    leg_->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    canl->Draw("0,0,1,100");
    
    char S4[50] = "mXX-100_mA-0p25_lxy-300",
         S2[50] = "mXX-500_mA-0p25_lxy-300",
         S3[50] = "mXX-500_mA-1p2_lxy-300", 
         S1[50] = "mXX-1000_mA-5_lxy-300";
	
    TH1F *num2a = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TOa2_Num_dR",S2));
    TH1F *den2a = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TOa2_Den_dR",S2));
    if(TEfficiency::CheckConsistency(*num2a,*den2a)){
        trEff = new TEfficiency(*num2a,*den2a);
	trEff->SetLineColor(kMagenta);
	//trEff->SetAxisRange(0.0,0.25,"X");
	trEff->Draw();
	trEff->SetTitle(" bb; #Delta R(#mu_{1},#mu_{2}); Efficiency (#epsilon)");
	leg_->AddEntry(trEff, "d_0 > 200 ", "l");
    }

    TH1F *num2s = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TOs2_Num_dR",S2));
    TH1F *den2s = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TOs2_Den_dR",S2));
    if(TEfficiency::CheckConsistency(*num2s,*den2s)){
      trEff = new TEfficiency(*num2s,*den2s);
      trEff->SetLineColor(kGray);
      //trEff->SetAxisRange(0.0,0.25,"X");                                                                                                                                                  
      trEff->Draw("same");
      trEff->SetTitle(" ; #Delta R(#mu_{1},#mu_{2}); Efficiency (#epsilon)");
      leg_->AddEntry(trEff, "d_0 < 200", "l");
      }

  leg_->Draw();
  canl->SaveAs(Form("../outputs/plots/modules/out_%s/%sTE_dRd0cut.png",id, id));
}
