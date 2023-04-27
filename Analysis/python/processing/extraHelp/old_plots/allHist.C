void allHist(const char *id){
    TEfficiency* trEff = 0;//new TEfficiency("eff","my efficiency; x; y;#epsilon", 10,0,10,20,-5,15);
    TFile* f = TFile::Open(Form("../outputs/rootfiles/modules/out_%s.root",id));
  
    TCanvas *can = new TCanvas("can","",800,600);
    //can->SetLogy();
    TLegend *leg_ = new TLegend(.6, .6, 0.85, .85);
    leg_->SetHeader("Samples:","C");
    leg_->SetBorderSize(0);
    leg_->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    can->Draw();
    
    char S1[50] = "mXX-100_mA-0p25_lxy-300",  S2[50] = "mXX-500_mA-0p25_lxy-300", S3[50] = "mXX-500_mA-1p2_lxy-300",   S4[50] = "mXX-1000_mA-5_lxy-300";
	
    TH1F *ReMu_d02 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/ReMu_d0",S2));
    ReMu_d02->SetLineColor(kBlack);
    ReMu_d02->SetMarkerColor(kBlack);
    ReMu_d02->SetMarkerStyle(20);
    ReMu_d02->SetStats(kFALSE);
    ReMu_d02->Draw();
    ReMu_d02->SetTitle(" d_{0} distributions; d_{0} [cm]; Entries");
    leg_->AddEntry(ReMu_d02, Form("%s",S2), "l");
    leg_->Draw();

    TH1F *ReMu_d01 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/ReMu_d0",S1));
    ReMu_d01->SetLineColor(kMagenta);
    ReMu_d01->SetMarkerColor(kMagenta);
    ReMu_d01->SetMarkerStyle(21);
    ReMu_d01->SetStats(kFALSE);
    ReMu_d01->Draw("same");
    leg_->AddEntry(ReMu_d01, Form("%s",S1), "l");
    leg_->Draw();

    TH1F *ReMu_d03 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/ReMu_d0",S3));
    ReMu_d03->SetLineColor(kBlue);
    ReMu_d03->SetMarkerColor(kBlue);
    ReMu_d03->SetMarkerStyle(22);
    ReMu_d03->SetStats(kFALSE);
    ReMu_d03->Draw("same");
    leg_->AddEntry(ReMu_d03, Form("%s",S3), "l");
    leg_->Draw();
    
    can->SaveAs(Form("../outputs/plots/extras/%sallHist.png",id));
    
}
