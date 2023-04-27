void pT_TrigEff(const char *id, const char *file, const char *etype)
{
  TFile* file_1 = TFile::Open(Form("../outputs/rootfiles/modules/%s.root",file));
  
  // samples
  char
    S1[50] = "mXX-100_mA-0p25_lxy-300",
	S2[50] = "mXX-500_mA-1p2_lxy-3",
	S3[50] = "mXX-1000_mA-5_lxy-3";

 	//num all samples
    TH1F *num_s1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_pT",S1));	TH1F *eff_s1 = (TH1F*) num_s1->Clone();
    TH1F *num_s2 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_pT",S2));	TH1F *eff_s2 = (TH1F*) num_s2->Clone();
    TH1F *num_s3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_pT",S3));	TH1F *eff_s3 = (TH1F*) num_s3->Clone();
    //TH1F *num_s4 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_pT",S4));	TH1F *eff_s4 = (TH1F*) num_s4->Clone();
    //TH1F *num_s5 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_pT",S5));	TH1F *eff_s5 = (TH1F*) num_s5->Clone();

    //den all samples
    TH1F *den_s1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_pT",S1));
    TH1F *den_s2 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_pT",S2));        
    TH1F *den_s3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_pT",S3));
    //TH1F *den_s4 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_pT",S4));
  
    eff_s1->Divide(den_s1);
    eff_s2->Divide(den_s2);
    eff_s3->Divide(den_s3);
    //eff_s4->Divide(den_s4);
  
    eff_s1->SetLineColor(kBlack); 
    eff_s2->SetLineColor(kMagenta);
    eff_s3->SetLineColor(kBlue);
    //eff_s4->SetLineColor(kRed);
  
    eff_s1->SetMarkerColor(kBlack);
    eff_s2->SetMarkerColor(kMagenta);
    eff_s3->SetMarkerColor(kBlue);
    //eff_s4->SetMarkerColor(kRed);
          
    TCanvas *can_pT = new TCanvas("can_pT","",800,600);
    eff_s1->SetTitle("Leading muon p_{T}; p_{T} [GeV]; Efficiency");
    eff_s1->SetStats(kFALSE);
    eff_s1->SetAxisRange(0.0,1.2,"Y");
    eff_s1->Draw();
    eff_s2->Draw("same");
    eff_s3->Draw("same");
    //eff_s4->Draw("same");
    
    TLegend *leg_f1 = new TLegend(.3, .1, 0.6, .3);
    leg_f1->SetHeader("Samples","C");
    leg_f1->SetBorderSize(0);
    leg_f1->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    leg_f1->AddEntry(eff_s1, Form("%s",S1), "P");
    leg_f1->AddEntry(eff_s2, Form("%s",S2), "P");
    leg_f1->AddEntry(eff_s3, Form("%s",S3), "P");
    //leg_f1->AddEntry(eff_s4, Form("%s",S4), "P");
    leg_f1->Draw();
    can_pT->SaveAs(Form("../outputs/plots/modules/%s/%s_%s_TrEff2pvt_pT.png",file,id,etype));
}
