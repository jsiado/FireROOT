void TEffeta(const char *id){
  TEfficiency* trEff = new TEfficiency("eff","my efficiency; x; y;#epsilon", 10,0,10,20,-5,15);
  TFile* f = TFile::Open("../outputs/rootfiles/modules/ObjTrEff2pvt.root");
  
  TCanvas *cane = new TCanvas("cane","",800,600);
  TLegend *leg_ = new TLegend(.6, .1, 0.9, .298);
  leg_->SetHeader("Samples:","C");
  leg_->SetBorderSize(0);
  leg_->SetLineColor(1);
  gStyle->SetFillColor(0);
  gStyle->SetCanvasColor(10);

  char
    S2[50] = "mXX-100_mA-0p25_lxy-300",
    S1[50] = "mXX-500_mA-1p2_lxy-3",
    S3[50] = "mXX-1000_mA-5_lxy-3";
  
  TH1F *num1 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Num_eta",S1));
  TH1F *den1 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Den_eta",S1));
  if(TEfficiency::CheckConsistency(*num1,*den1)){
    trEff = new TEfficiency(*num1,*den1);
    trEff->Draw();
    trEff->SetTitle("Leading muon #eta; #eta; Efficiency (#epsilon)");
    leg_->AddEntry(trEff, Form("%s",S1), "l");
  }

  TH1F *num2 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Num_eta",S2));
  TH1F *den2 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Den_eta",S2));
  if(TEfficiency::CheckConsistency(*num2,*den2)){
    trEff = new TEfficiency(*num2,*den2);
    trEff->SetLineColor(kBlue);
    trEff->Draw("same");
    leg_->AddEntry(trEff, Form("%s",S2), "l");
  }
  
  TH1F *num3 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Num_eta",S3));
  TH1F *den3 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Den_eta",S3));
  if(TEfficiency::CheckConsistency(*num3,*den3)){
    trEff = new TEfficiency(*num3,*den3);
    trEff->SetLineColor(kRed);
    trEff->Draw("same");
    leg_->AddEntry(trEff, Form("%s",S3), "l");
  }

  leg_->Draw();
  cane->SaveAs(Form("../outputs/plots/modules/ObjTrEff2pvt/%sTE_eta.png",id));
}
