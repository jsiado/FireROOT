void TEffpT(const char *id){
	TEfficiency* trEff = 0;//new TEfficiency("eff","my efficiency; x; y;#epsilon",100,0,600);
	//TEfficiency* trEff = new TEfficiency("eff","my efficiency;x;y;#epsilon",100,0,10);

	TFile* f = TFile::Open(Form("../outputs/rootfiles/modules/out_%s.root",id));
  
	TCanvas *canp = new TCanvas("canp","",800,600);
	//canp->SetLogy();
	canp->Draw();
	TLegend *leg_ = new TLegend(.6, .1, 0.9, .298);
	leg_->SetHeader("Samples:","C");
	leg_->SetBorderSize(0);
	leg_->SetLineColor(1);
	gStyle->SetFillColor(0);
	gStyle->SetCanvasColor(10);
  
	//canp->Draw("");


  char
    //original samples
    /*
	S2[50]="mXX-100_mA-0p25_lxy-300",
	S1[50] = "mXX-500_mA-1p2_lxy-3",                                                                                                                     
	S3[50] = "mXX-1000_mA-5_lxy-3",
    */

    //same lxy samples 
//    S1[50] = "mXX-1000_mA-5_lxy-3",
  //  S2[50] = "mXX-500_mA-0p25_lxy-3",
    S1[50] = "mXX-100_mA-0p25_lxy-300",
	S2[50] = "mXX-500_mA-0p25_lxy-300",
	S3[50] = "mXX-500_mA-1p2_lxy-300",
	S4[50] = "mXX-1000_mA-5_lxy-300";
//    S3[50] = "mXX-100_mA-0p25_lxy-3";
  
  TH1F *num1 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Num_pT",S1));
  TH1F *den1 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Den_pT",S1));
  if(TEfficiency::CheckConsistency(*num1,*den1)){
    trEff = new TEfficiency(*num1,*den1);
	//trEff->SetRangeUser(0, 600, "X");
	//trEff->SetAxisRange(0, 1.5, "Y");
    trEff->Draw();
    //auto graph = trEff->GetPaintedGraph(); 
	//graph->SetAxisRange(0,100, "X");
	//graph->SetMaximum(1);
    trEff->SetTitle(" ; p_{T} [GeV]; Efficiency (#epsilon)");
	//trEff->SetMaximum(2);
    leg_->AddEntry(trEff, Form("%s",S1), "l");
  }
  //delete num1;

  TH1F *num2 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Num_pT",S2));
  TH1F *den2 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Den_pT",S2));
  if(TEfficiency::CheckConsistency(*num2,*den2)){
    trEff = new TEfficiency(*num2,*den2);
    trEff->SetLineColor(kBlue);
    trEff->Draw("same");
    leg_->AddEntry(trEff, Form("%s",S2), "l");
  }
  
  TH1F *num3 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Num_pT",S3));
  TH1F *den3 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Den_pT",S3));
  if(TEfficiency::CheckConsistency(*num3,*den3)){
    trEff = new TEfficiency(*num3,*den3);
    trEff->SetLineColor(kRed);
    trEff->Draw("same");
    leg_->AddEntry(trEff, Form("%s",S3), "l");
  }
  
	TH1F *num4 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Num_pT",S4));
	TH1F *den4 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Den_pT",S4));
	if(TEfficiency::CheckConsistency(*num4,*den4)){
		trEff = new TEfficiency(*num4,*den4);
		trEff->SetLineColor(kMagenta);
		trEff->Draw("same");
		leg_->AddEntry(trEff, Form("%s",S4), "l");
  }  

  leg_->Draw();
  canp->SaveAs(Form("../outputs/plots/extras/%sTE_pT.png",id));
}
