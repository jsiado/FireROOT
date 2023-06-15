void TEffdiffd0dR(const char *id){
    TEfficiency* trEff = 0;//new TEfficiency("eff","my efficiency; x; y;#epsilon", 10,0,10,20,-5,15);
    TFile* f = TFile::Open(Form("../outputs/rootfiles/modules/out_%s.root",id));
  
    TCanvas *canddr = new TCanvas("canddr","",800,600);
    TLegend *leg_ = new TLegend(.2, .1, 0.45, .35);
    leg_->SetHeader("d_{0} [#mu m]:","C");
    leg_->SetBorderSize(0);
    leg_->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    canddr->Draw("0,0,1,100");
    
    char S4[50] = "mXX-100_mA-0p25_lxy-300",
         S2[50] = "mXX-500_mA-0p25_lxy-300",
         S3[50] = "mXX-500_mA-1p2_lxy-300", 
         S1[50] = "mXX-1000_mA-5_lxy-300";
	
    TH1F *numl2 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Num_dRd0l2",S3));
    TH1F *denl2 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Den_dRd0l2",S3));
    if(TEfficiency::CheckConsistency(*numl2,*denl2))
    {
        trEff = new TEfficiency(*numl2,*denl2);
		trEff->SetLineColor(kMagenta);
		//trEff->SetTitle(
		trEff->Draw();
		gPad->Update();
		auto graph = trEff->GetPaintedGraph();
		graph->SetMinimum(0);
		graph->SetMaximum(1.4);
		//graph->GetXaxis()->SetRange(0., 1.);
		gPad->Update();
		trEff->SetTitle(Form(" %s; #Delta R(#mu_{1},#mu_{2}); Efficiency (#epsilon)",S3));
		leg_->AddEntry(trEff, "d_{0} < 200 ", "l");
    }

    TH1F *numl5 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Num_dRd0l5",S3));
    TH1F *denl5 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Den_dRd0l5",S3));
    if(TEfficiency::CheckConsistency(*numl5,*denl5))
    {
    	trEff = new TEfficiency(*numl5,*denl5);
    	trEff->SetLineColor(kBlue);
    	trEff->Draw("same");
    	trEff->SetTitle(Form(" %s; #Delta R(#mu_{1},#mu_{2}); Efficiency (#epsilon)",S3));
    	leg_->AddEntry(trEff, "200 < d_{0} < 500", "l");
    }
    
    TH1F *numm5 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Num_dRd0m5",S3));
    TH1F *denm5 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Den_dRd0m5",S3));
    if(TEfficiency::CheckConsistency(*numm5,*denm5))
    {
    	trEff = new TEfficiency(*numm5,*denm5);
    	trEff->SetLineColor(kBlack);
    	trEff->Draw("same");
    	trEff->SetTitle(" ; #Delta R(#mu_{1},#mu_{2}); Efficiency (#epsilon)");
    	leg_->AddEntry(trEff, "d_{0} > 500", "l");
    }

  leg_->Draw();
  // canddr->SaveAs(Form("../outputs/plots/modules/out_%s/%sTE_dRdiffd0dR.png",id, id));

  TH1F *numf = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Num_dRfbin",S3));
  TH1F *denf = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Den_dRfbin",S3));
  if(TEfficiency::CheckConsistency(*numf,*denf))
    {
      trEff = new TEfficiency(*numf,*denf);
      trEff->SetLineColor(kOrange);
      trEff->Draw("same");
      trEff->SetTitle(" ; #Delta R(#mu_{1},#mu_{2}); Efficiency (#epsilon)");
      leg_->AddEntry(trEff, "d_{0} extended", "l");
    }

  leg_->Draw();
  canddr->SaveAs(Form("../outputs/plots/modules/out_%s/%sTE_dRdiffd0dR.png",id, id));

}
