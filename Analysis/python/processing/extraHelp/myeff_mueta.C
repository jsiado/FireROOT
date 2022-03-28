//run as root -l myeff_mueta.C

//void myeff_mueta(const char *num)
void mueta(int num)
{
    TFile* file_1 = TFile::Open("../outputs/rootfiles/modules/genTriggerEfficiency2mu.root");
   
	// samples
	char S1[50] = "mXX-1000_mA-5_lxy-300", S2[50] = "mXX-100_mA-5_lxy-0p3", S3[50] = "mXX-500_mA-0p25_lxy-300", S4[50] = "mXX-1000_mA-5_lxy-30", 
    S5[50] = "mXX-500_mA-1p2_lxy-30", S6[50] = "mXX-100_mA-0p25_lxy-300", S7[50]= "mXX-1000_mA-5_lxy-150", S8[50] = "mXX-1000_mA-5_lxy-3", 
    S9[50] = "mXX-1000_mA-5_lxy-0p3", S0[50] = "mXX-200_mA-0p25_lxy-300", S11[50] = "mXX-100_mA-0p25_lxy-0p3", S12[50] = "mXX-100_mA-0p25_lxy-3",
    S13[50] = "mXX-100_mA-0p25_lxy-30",S14[50] = "mXX-100_mA-0p25_lxy-150", 
    S15[50] = "mXX-500_mA-1p2_lxy-0p3", S16[50] = "mXX-500_mA-1p2_lxy-3", S17[50] = "mXX-500_mA-1p2_lxy-150", S18[50] = "mXX-500_mA-1p2_lxy-300", 
    S19[50]="mXX-500_mA-5_lxy-0p3", S20[50]="mXX-500_mA-5_lxy-3", S21[50]="mXX-500_mA-5_lxy-30", S22[50]="mXX-500_mA-5_lxy-150", S23[50]="mXX-500_mA-5_lxy-300";
  
  	//triggers
    char T1[50] = "DoubleL2Mu23NoVtx_2Cha", T2[50] = "DoubleL2Mu23NoVtx_2Cha_NoL2Matched", T3[50]= "DoubleL2Mu23NoVtx_2Cha_CosmicSeed", 
	T4[50] = "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched", T5[50] = "DoubleL2Mu25NoVtx_2Cha_Eta2p4", T6[50] = "DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4";	
	
	   
    TH1F *mueta_s1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/subleaMuEta",S1));  mueta_s1->Sumw2();
    TH1F *mueta_s2 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/subleaMuEta",S2));  mueta_s2->Sumw2();    
    TH1F *mueta_s3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/subleaMuEta",S3));  mueta_s3->Sumw2();    
    TH1F *mueta_s4 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/subleaMuEta",S4));  mueta_s4->Sumw2();    
    TH1F *mueta_s5 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/subleaMuEta",S5));  mueta_s5->Sumw2();    
    TH1F *mueta_s6 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/subleaMuEta",S6));  mueta_s6->Sumw2();
    TH1F *mueta_s7 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/subleaMuEta",S7));  mueta_s7->Sumw2();
    TH1F *mueta_s8 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/subleaMuEta",S8));  mueta_s8->Sumw2();
    TH1F *mueta_s9 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/subleaMuEta",S9));  mueta_s9->Sumw2();
    TH1F *mueta_s0 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/subleaMuEta",S0));  mueta_s0->Sumw2();
	
	TCanvas* can_mueta = new TCanvas("can_mueta"); 
    mueta_s1->SetStats(0);    
    
    mueta_s1->SetLineColor(kBlack); 
    mueta_s2->SetLineColor(kBlue); 
    mueta_s3->SetLineColor(kGreen); 
    mueta_s4->SetLineColor(kRed); 
    mueta_s5->SetLineColor(kCyan); 
    mueta_s6->SetLineColor(kMagenta);
    mueta_s7->SetLineColor(kPink);
    mueta_s8->SetLineColor(kViolet);
    mueta_s9->SetLineColor(kGreen-1);
    mueta_s0->SetLineColor(kYellow);
    
    mueta_s1->SetMarkerColor(kBlack); 
    mueta_s2->SetMarkerColor(kBlue); 
    mueta_s3->SetMarkerColor(kGreen);     
    mueta_s4->SetMarkerColor(kRed); 
    mueta_s5->SetMarkerColor(kCyan); 	
    mueta_s6->SetMarkerColor(kMagenta);
    mueta_s7->SetMarkerColor(kPink);
    mueta_s8->SetMarkerColor(kViolet);
    mueta_s9->SetMarkerColor(kGreen-1);
    mueta_s0->SetMarkerColor(kYellow);
    
    mueta_s1->SetMarkerStyle(20); 
    mueta_s2->SetMarkerStyle(21); 
    mueta_s3->SetMarkerStyle(22);     
    mueta_s4->SetMarkerStyle(23); 
    mueta_s5->SetMarkerStyle(24); 
    mueta_s6->SetMarkerStyle(25);    
    mueta_s7->SetMarkerStyle(26);
    mueta_s8->SetMarkerStyle(27);
    mueta_s9->SetMarkerStyle(28);
    mueta_s0->SetMarkerStyle(29);
    
    mueta_s1->Scale(1.0/mueta_s1->Integral()); 
    mueta_s2->Scale(1.0/mueta_s2->Integral());    
    mueta_s3->Scale(1.0/mueta_s3->Integral()); 
    mueta_s4->Scale(1.0/mueta_s4->Integral());    
    mueta_s5->Scale(1.0/mueta_s5->Integral()); 
    mueta_s6->Scale(1.0/mueta_s6->Integral());
    mueta_s7->Scale(1.0/mueta_s7->Integral());
    mueta_s8->Scale(1.0/mueta_s8->Integral());
    mueta_s9->Scale(1.0/mueta_s9->Integral());
    mueta_s0->Scale(1.0/mueta_s0->Integral());
    
    mueta_s1->SetAxisRange(0.0,0.04,"Y");
    mueta_s1->GetYaxis()->SetTitle("Entries Normalized");
    
    mueta_s1->Draw(); 
    mueta_s2->Draw("same"); 
    mueta_s3->Draw("same"); 
    mueta_s4->Draw("same"); 
    mueta_s5->Draw("same"); 
    mueta_s6->Draw("same");
    mueta_s0->Draw("same");
    
    
    TLegend *leg_mueta = new TLegend(.6, .7, 0.9, .898);    
    leg_mueta->SetHeader("Samples","C");
    leg_mueta->SetBorderSize(0);    
    leg_mueta->SetLineColor(1);    
    gStyle->SetFillColor(0);    
    gStyle->SetCanvasColor(10);    
    leg_mueta->AddEntry(mueta_s1, Form("%s",S1), "P");    
    leg_mueta->AddEntry(mueta_s2, Form("%s",S2), "P");    
    leg_mueta->AddEntry(mueta_s3, Form("%s",S3), "P");    
    leg_mueta->AddEntry(mueta_s4, Form("%s",S4), "P");    
    leg_mueta->AddEntry(mueta_s5, Form("%s",S5), "P");    
    leg_mueta->AddEntry(mueta_s6, Form("%s",S6), "P");
    leg_mueta->AddEntry(mueta_s0, Form("%s",S0), "P");
    leg_mueta->Draw();    
    can_mueta->SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency2mu/%i_central_mueta.pdf",num));
    
    //all mu eta for != lxy
    TCanvas* can_muetalxy = new TCanvas("can_muetalxy"); 
    mueta_s1->SetStats(0);    
    
    
    mueta_s1->SetAxisRange(0.0,0.04,"Y");   
    mueta_s1->GetYaxis()->SetTitle("Entries Normalized");
    
    mueta_s1->Draw(); 
    mueta_s4->Draw("same"); 
    mueta_s7->Draw("same"); 
    mueta_s8->Draw("same");
    mueta_s9->Draw("same");    
    
    TLegend *leg_muetalxy = new TLegend(.6, .7, 0.9, .898);    
    leg_muetalxy->SetHeader("Samples","C");    
    leg_muetalxy->SetBorderSize(0);    
    leg_muetalxy->SetLineColor(1);    
    gStyle->SetFillColor(0);    
    gStyle->SetCanvasColor(10);    
    leg_muetalxy->AddEntry(mueta_s9, Form("%s",S9), "P");    
    leg_muetalxy->AddEntry(mueta_s8, Form("%s",S8), "P");    
    leg_muetalxy->AddEntry(mueta_s4, Form("%s",S4), "P");    
    leg_muetalxy->AddEntry(mueta_s7, Form("%s",S7), "P");    
    leg_muetalxy->AddEntry(mueta_s1, Form("%s",S1), "P");    
    leg_muetalxy->Draw();    
    can_muetalxy->SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency2mu/%i_muetalxy.pdf",num));	
}

void myeff_mueta()
{
	int num;
	cout<<"give me a number: "<<;
	cin>>num;
	mueta(num);
}




