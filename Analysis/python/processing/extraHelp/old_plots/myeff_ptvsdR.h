void myeff_ptvsdR(int date, const char *muon)
{
	//char C[10] = "dsa";
	TFile* file_1 = TFile::Open(Form("../outputs/rootfiles/modules/%sTrEff2mu.root",muon));
	
 	// samples
    char S1[50] = "mXX-1000_mA-5_lxy-300", S2[50] = "mXX-100_mA-5_lxy-0p3", S3[50] = "mXX-500_mA-0p25_lxy-300", S4[50] = "mXX-1000_mA-5_lxy-30", S5[50] = "mXX-500_mA-1p2_lxy-30", 
    S6[50] = "mXX-100_mA-0p25_lxy-300", S7[50]= "mXX-1000_mA-5_lxy-150", S8[50] = "mXX-1000_mA-5_lxy-3", S9[50] = "mXX-1000_mA-5_lxy-0p3", S0[50] = "mXX-200_mA-0p25_lxy-300";
  	
  	//triggers
    char T1[50] = "DoubleL2Mu23NoVtx_2Cha", T2[50] = "DoubleL2Mu23NoVtx_2Cha_NoL2Matched", T3[50]= "DoubleL2Mu23NoVtx_2Cha_CosmicSeed", 
    T4[50] = "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched", T5[50] = "DoubleL2Mu25NoVtx_2Cha_Eta2p4", T6[50] = "DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4";
    
    TH2F *ptdR_s1 = (TH2F*)file_1->Get(Form("ch2mu2e/sig/%s/ptvsdR",S1));
    TH2F *ptdR_s2 = (TH2F*)file_1->Get(Form("ch2mu2e/sig/%s/ptvsdR",S2));
    TH2F *ptdR_s3 = (TH2F*)file_1->Get(Form("ch2mu2e/sig/%s/ptvsdR",S3));
    TH2F *ptdR_s4 = (TH2F*)file_1->Get(Form("ch2mu2e/sig/%s/ptvsdR",S4));
    TH2F *ptdR_s5 = (TH2F*)file_1->Get(Form("ch2mu2e/sig/%s/ptvsdR",S5));
    TH2F *ptdR_s6 = (TH2F*)file_1->Get(Form("ch2mu2e/sig/%s/ptvsdR",S6));
    TH2F *ptdR_s7 = (TH2F*)file_1->Get(Form("ch2mu2e/sig/%s/ptvsdR",S7));
    TH2F *ptdR_s8 = (TH2F*)file_1->Get(Form("ch2mu2e/sig/%s/ptvsdR",S8));
    TH2F *ptdR_s9 = (TH2F*)file_1->Get(Form("ch2mu2e/sig/%s/ptvsdR",S9));
    TH2F *ptdR_s0 = (TH2F*)file_1->Get(Form("ch2mu2e/sig/%s/ptvsdR",S0));
 
	TCanvas* can_ptdR = new TCanvas("can_ptdR");   
    ptdR_s1->SetMarkerStyle(20);
    ptdR_s2->SetMarkerStyle(21);
    ptdR_s3->SetMarkerStyle(22);
    ptdR_s4->SetMarkerStyle(23);
    ptdR_s5->SetMarkerStyle(24);
    ptdR_s6->SetMarkerStyle(25);
    ptdR_s7->SetMarkerStyle(26);
    ptdR_s8->SetMarkerStyle(27);
    ptdR_s9->SetMarkerStyle(28);
    ptdR_s0->SetMarkerStyle(29);
    
    ptdR_s1->SetMarkerColor(kBlack);
    ptdR_s2->SetMarkerColor(kBlue);
    ptdR_s3->SetMarkerColor(kGreen);
    ptdR_s4->SetMarkerColor(kRed);
    ptdR_s5->SetMarkerColor(kCyan);
    ptdR_s6->SetMarkerColor(kMagenta);
    ptdR_s7->SetMarkerColor(kPink);
    ptdR_s8->SetMarkerColor(kViolet);
    ptdR_s9->SetMarkerColor(kGreen-1);
    ptdR_s0->SetMarkerColor(kYellow);
    
    ptdR_s1->SetLineColor(kBlack);
    ptdR_s2->SetLineColor(kBlue);
    ptdR_s3->SetLineColor(kGreen);
    ptdR_s4->SetLineColor(kRed);
    ptdR_s5->SetLineColor(kCyan);
    ptdR_s6->SetLineColor(kMagenta);
    ptdR_s6->SetLineColor(kPink);
    ptdR_s6->SetLineColor(kViolet);
    ptdR_s6->SetLineColor(kGreen-1);
    ptdR_s0->SetLineColor(kYellow);
    
    ptdR_s1->SetStats(0);
    ptdR_s1->SetTitle(Form("p_{T} vs dR: %s muons",muon));
    
    ptdR_s1->Draw();
    ptdR_s2->Draw("same");
    ptdR_s3->Draw("same");
    ptdR_s4->Draw("same"); 
    ptdR_s5->Draw("same");
    ptdR_s6->Draw("same");
    ptdR_s0->Draw("same");
    
    TLegend *leg_ptdR = new TLegend(.6, .7, 0.9, .898);
    leg_ptdR->SetHeader("Samples","C");      
    leg_ptdR->SetBorderSize(0);             
    leg_ptdR->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    leg_ptdR->AddEntry(ptdR_s1, Form("%s",S1), "P");
    leg_ptdR->AddEntry(ptdR_s2, Form("%s",S2), "P");
    leg_ptdR->AddEntry(ptdR_s3, Form("%s",S3), "P");
    leg_ptdR->AddEntry(ptdR_s4, Form("%s",S4), "P");
    leg_ptdR->AddEntry(ptdR_s5, Form("%s",S5), "P");
    leg_ptdR->AddEntry(ptdR_s6, Form("%s",S6), "P");
    leg_ptdR->AddEntry(ptdR_s0, Form("%s",S0), "P");
    leg_ptdR->Draw();
    can_ptdR -> SaveAs(Form("../outputs/plots/modules/TrEff2mu/%i_%s_ptvsdR.pdf",date,muon));
    
    //pt vs dR for != lxy
    TCanvas* can_ptdRlxy = new TCanvas("can_ptdRlxy");
    ptdR_s4->SetTitle(Form("p_{T} vs dR: %s muons",muon));
    ptdR_s4->SetStats(0);
    ptdR_s4->Draw();
    ptdR_s1->Draw("same");
    //ptdR_s4->Draw("same");
    ptdR_s7->Draw("same");
    ptdR_s8->Draw("same"); 
    ptdR_s9->Draw("same");
    
    TLegend *leg_ptdRlxy = new TLegend(.6, .7, 0.9, .898);
    leg_ptdRlxy->SetHeader("Samples","C");      
    leg_ptdRlxy->SetBorderSize(0);             
    leg_ptdRlxy->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    leg_ptdRlxy->AddEntry(ptdR_s9, Form("%s",S9), "P");
    leg_ptdRlxy->AddEntry(ptdR_s8, Form("%s",S8), "P");
    leg_ptdRlxy->AddEntry(ptdR_s4, Form("%s",S4), "P");
    leg_ptdRlxy->AddEntry(ptdR_s7, Form("%s",S7), "P");
    leg_ptdRlxy->AddEntry(ptdR_s1, Form("%s",S1), "P");
    leg_ptdRlxy->Draw();
    can_ptdRlxy->SaveAs(Form("../outputs/plots/modules/TrEff2mu/%i_%s_ptvsdRlxy.pdf",date,muon));
}
    
    
    
    
    
    
    
