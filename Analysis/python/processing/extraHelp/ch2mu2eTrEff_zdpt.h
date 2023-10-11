void ch2mu2eTrEff_zdpt(const char *np, const char *rt, const char *ch){
    TEfficiency* trEff = 0;//new TEfficiency("eff","my efficiency; x; y;#epsilon", 10,0,10,20,-5,15);
    TFile* f = TFile::Open(Form("../outputs/rootfiles/modules/%s.root",rt));
  
    char S1[50] = "mXX-100_mA-0p25_lxy-300",  
      S2[50] = "mXX-500_mA-0p25_lxy-300", 
      S3[50] = "mXX-500_mA-1p2_lxy-300",   
      S4[50] = "mXX-1000_mA-5_lxy-300",
      var[10] = "zdpt";
    
    TCanvas *cant = new TCanvas(var, var ,800,600);
    TLegend *legt = new TLegend(.50, .72, .88, .88);

    legt->SetHeader("Samples:","C");
    legt->SetBorderSize(0);
    legt->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);

    TH1F *num1 = (TH1F*)f->Get(Form("ch%s/sig/%s/Passed_%s",ch, S1, var));
    TH1F *den1 = (TH1F*)f->Get(Form("ch%s/sig/%s/Total_%s",ch, S1, var));
    if(TEfficiency::CheckConsistency(*num1,*den1))
      {
        trEff = new TEfficiency(*num1,*den1);
	trEff->SetLineColor(kBlack);
	trEff->Draw();
	gPad->Update();
	auto graph = trEff->GetPaintedGraph();
	graph->SetMinimum(0);
    	graph->SetMaximum(1.45);
	TAxis *axis = graph->GetXaxis();
	axis->SetLimits(0.,800.3);
    	gPad->Update();
	trEff->SetTitle(" ; Dark phton p_{T} [GeV]; Efficiency (#epsilon)");
	legt->AddEntry(trEff, Form("%s",S1), "l");
    }

    TH1F *num2 = (TH1F*)f->Get(Form("ch%s/sig/%s/Passed_%s",ch, S2, var));
    TH1F *den2 = (TH1F*)f->Get(Form("ch%s/sig/%s/Total_%s",ch, S2, var));
    if(TEfficiency::CheckConsistency(*num2,*den2))
      {
	trEff = new TEfficiency(*num2,*den2);
	trEff->SetLineColor(kRed);
	trEff->Draw("same");
	gPad->Update();
	auto graph = trEff->GetPaintedGraph();
	gPad->Update();
	legt->AddEntry(trEff, Form("%s",S2), "l");
      }

    TH1F *num3 = (TH1F*)f->Get(Form("ch%s/sig/%s/Passed_%s",ch, S3, var));
    TH1F *den3 = (TH1F*)f->Get(Form("ch%s/sig/%s/Total_%s",ch, S3, var));
    if(TEfficiency::CheckConsistency(*num3,*den3))
      {
	trEff = new TEfficiency(*num3,*den3);
	trEff->SetLineColor(kGreen);
	trEff->Draw("same");
	gPad->Update();
	auto graph = trEff->GetPaintedGraph();
	gPad->Update();
	legt->AddEntry(trEff, Form("%s",S3), "l");	
      }

    TH1F *num4 = (TH1F*)f->Get(Form("ch%s/sig/%s/Passed_%s",ch, S4, var));
    TH1F *den4 = (TH1F*)f->Get(Form("ch%s/sig/%s/Total_%s",ch, S4, var));
    if(TEfficiency::CheckConsistency(*num4,*den4))
      {
	trEff = new TEfficiency(*num4,*den4);
	trEff->SetLineColor(kBlue);
	trEff->Draw("same");
	gPad->Update();
	auto graph = trEff->GetPaintedGraph();
	gPad->Update();
	legt->AddEntry(trEff, Form("%s",S4), "l");
      }
    legt->Draw();
    cant->SaveAs(Form("extraHelp/plots/%s_%s_TrEff_%s.pdf",np, ch, var));
}
