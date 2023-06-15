void TEffeta(const char *id){
    TEfficiency* trEff = 0;//new TEfficiency("eff","my efficiency; x; y;#epsilon", 10,0,10,20,-5,15);
    TFile* f = TFile::Open(Form("../outputs/rootfiles/modules/out_%s.root",id));

    TCanvas *cane = new TCanvas("cane","",800,600);
    TLegend *leg_ = new TLegend(.2, .1, 0.45, .35);
    leg_->SetHeader("Samples:","C");
    leg_->SetBorderSize(0);
    leg_->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    cane->Draw("0,0,1,100");
    
    char S1[50] = "mXX-100_mA-0p25_lxy-300",  S2[50] = "mXX-500_mA-0p25_lxy-300", S3[50] = "mXX-500_mA-1p2_lxy-300",   S4[50] = "mXX-1000_mA-5_lxy-300";
	
    TH1F *num2 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Num_eta",S2));
    TH1F *den2 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Den_eta",S2));
    if(TEfficiency::CheckConsistency(*num2,*den2)){
        trEff = new TEfficiency(*num2,*den2);
	trEff->SetLineColor(kMagenta);
	trEff->Draw();
	trEff->SetTitle(" ; #eta ; Efficiency (#epsilon)");
	leg_->AddEntry(trEff, Form("%s",S2), "l");
    }

    TH1F *num4 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Num_eta",S4));
    TH1F *den4 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Den_eta",S4));
    if(TEfficiency::CheckConsistency(*num4,*den4)){
        trEff = new TEfficiency(*num4,*den4);
	trEff->SetLineColor(kGray);
	trEff->Draw("same");
	leg_->AddEntry(trEff, Form("%s",S4), "l");
    }
  
    TH1F *num1 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Num_eta",S1));
    TH1F *den1 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Den_eta",S1));
    if(TEfficiency::CheckConsistency(*num1,*den1)){
        trEff = new TEfficiency(*num1,*den1);
	trEff->SetLineColor(kBlue);
	trEff->Draw("same");
	leg_->AddEntry(trEff, Form("%s",S1), "l");
    }
  
    TH1F *num3 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Num_eta",S3));
    TH1F *den3 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Den_eta",S3));
    if(TEfficiency::CheckConsistency(*num3,*den3)){
        trEff = new TEfficiency(*num3,*den3);
	trEff->SetLineColor(kBlack);
	trEff->Draw("same");
	leg_->AddEntry(trEff, Form("%s",S3), "l");
    }  	

  leg_->Draw();
  //  cane->SaveAs(Form("../outputs/plots/extras/%sTE_eta.png",id));
  cane->SaveAs(Form("../outputs/plots/modules/out_%s/%sTE_eta.png",id, id));
}
