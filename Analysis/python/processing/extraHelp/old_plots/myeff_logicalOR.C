//run as root -l genTriEff.C

void myeff_logicalOR()
{
    TFile* file_1 = TFile::Open("../outputs/rootfiles/modules/genTriggerEfficiency2mu.root");
    
  // samples
    char S1[50] = "mXX-1000_mA-5_lxy-300", S2[50] = "mXX-100_mA-5_lxy-0p3", S3[50] = "mXX-500_mA-0p25_lxy-300", S4[50] = "mXX-1000_mA-5_lxy-30", 
    S5[50] = "mXX-500_mA-1p2_lxy-30", S6[50] = "mXX-100_mA-0p25_lxy-300", S7[50]= "mXX-1000_mA-5_lxy-150", S8[50] = "mXX-1000_mA-5_lxy-3", 
    S9[50] = "mXX-1000_mA-5_lxy-0p3", S0[50] = "mXX-200_mA-0p25_lxy-300", S11[50] = "mXX-100_mA-0p25_lxy-0p3", S12[50] = "mXX-100_mA-0p25_lxy-3",
    S13[50] = "mXX-100_mA-0p25_lxy-30",S14[50] = "mXX-100_mA-0p25_lxy-150", S15[50] = "mXX-500_mA-1p2_lxy-0p3", S16[50] = "mXX-500_mA-1p2_lxy-3", 
    S17[50] = "mXX-500_mA-1p2_lxy-150", S18[50] = "mXX-500_mA-1p2_lxy-300";
  //triggers
    char T1[50] = "DoubleL2Mu23NoVtx_2Cha", T2[50] = "DoubleL2Mu23NoVtx_2Cha_NoL2Matched", T3[50]= "DoubleL2Mu23NoVtx_2Cha_CosmicSeed", 
      T4[50] = "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched", T5[50] = "DoubleL2Mu25NoVtx_2Cha_Eta2p4", T6[50] = "DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4";
    
    
    TH1F *alldimu_1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S1));
    TH1F *alldimu_2 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S2));
    TH1F *alldimu_3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S3));
  	TH1F *alldimu_4 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S4));
    TH1F *alldimu_5 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S5));
    TH1F *alldimu_6 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S6));
    TH1F *alldimu_7 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S7));
    TH1F *alldimu_8 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S8));
    TH1F *alldimu_9 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S9));
    TH1F *alldimu_0 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S0));

    //All samples with Logical OR
    TH1F *dimu_s1tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S1));    TH1F *eff_s1tor = (TH1F*) dimu_s1tor->Clone();    
    TH1F *dimu_s2tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S2));    TH1F *eff_s2tor = (TH1F*) dimu_s2tor->Clone();
    TH1F *dimu_s3tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S3));    TH1F *eff_s3tor = (TH1F*) dimu_s3tor->Clone();
    TH1F *dimu_s4tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S4));    TH1F *eff_s4tor = (TH1F*) dimu_s4tor->Clone();
    TH1F *dimu_s5tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S5));    TH1F *eff_s5tor = (TH1F*) dimu_s5tor->Clone();
    TH1F *dimu_s6tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S6));    TH1F *eff_s6tor = (TH1F*) dimu_s6tor->Clone();
    TH1F *dimu_s7tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S7));    TH1F *eff_s7tor = (TH1F*) dimu_s7tor->Clone();
    TH1F *dimu_s8tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S8));    TH1F *eff_s8tor = (TH1F*) dimu_s8tor->Clone();
    TH1F *dimu_s9tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S9));    TH1F *eff_s9tor = (TH1F*) dimu_s9tor->Clone();
   	TH1F *dimu_s0tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S0));    TH1F *eff_s0tor = (TH1F*) dimu_s0tor->Clone();
    
    //TCanvas *c2 = new TCanvas("c2");
    TH1F *eff_comb_num = (TH1F*) dimu_s1tor->Clone();
    eff_comb_num->Add(dimu_s4tor);
    eff_comb_num->Add(dimu_s7tor);
    eff_comb_num->Add(dimu_s8tor);
    eff_comb_num->Add(dimu_s9tor);
    //eff_comb_num->Draw();
    
    //TCanvas *c3 = new TCanvas("c3");
    TH1F *eff_comb_den = (TH1F*) alldimu_1->Clone();
    eff_comb_den->Add(alldimu_4);
    eff_comb_den->Add(alldimu_7);
    eff_comb_den->Add(alldimu_8);
    eff_comb_den->Add(alldimu_9);
    //eff_comb_den->Draw();
    
    //TCanvas *c4 = new TCanvas ("c4");
    eff_comb_num->Divide(eff_comb_den);
    //eff_comb_num->Draw();
    
    eff_s1tor->Divide(alldimu_1);
    eff_s2tor->Divide(alldimu_2);
    eff_s3tor->Divide(alldimu_3);
    eff_s4tor->Divide(alldimu_4);
    eff_s5tor->Divide(alldimu_5);
    eff_s6tor->Divide(alldimu_6);
    eff_s7tor->Divide(alldimu_7);
	eff_s8tor->Divide(alldimu_8);
    eff_s9tor->Divide(alldimu_9);
    eff_s0tor->Divide(alldimu_0);
    
    TCanvas *can_LOR = new TCanvas("can_LOR","",1800,800);
    can_LOR->Divide(3,2);    
    can_LOR->cd(1);    
    eff_s1tor->SetLineColor(kBlack);    
    eff_s1tor->SetMarkerColor(kBlack);    
    eff_s1tor->SetMarkerStyle(20);    
    eff_s1tor->SetStats(kFALSE);    
    eff_s1tor->SetTitle(Form("Efficiency: %s, Logical OR; #Delta R; Efficiency",S1));    
    eff_s1tor->Draw();    
    can_LOR->cd(2);    
    eff_s2tor->SetLineColor(kBlue);    
    eff_s2tor->SetMarkerColor(kBlue);    
    eff_s2tor->SetMarkerStyle(21);   
    eff_s2tor->SetStats(kFALSE);    
    eff_s2tor->SetTitle(Form("Efficiency: %s, Logical OR; #Delta R; Efficiency",S2));    
    eff_s2tor->Draw();    
    can_LOR->cd(3);    
    eff_s3tor->SetLineColor(kGreen);   
    eff_s3tor->SetMarkerColor(kGreen);    
    eff_s3tor->SetMarkerStyle(22);    
    eff_s3tor->SetStats(kFALSE);    
    eff_s3tor->SetTitle(Form("Efficiency: %s, Logical OR; #Delta R; Efficiency",S3));    
    eff_s3tor->Draw();
    can_LOR->cd(4);    
    eff_s4tor->SetLineColor(kRed);    
    eff_s4tor->SetMarkerColor(kRed);    
    eff_s4tor->SetMarkerStyle(23);
    eff_s4tor->SetStats(kFALSE);    
    eff_s4tor->SetTitle(Form("Efficiency: %s, Logical OR; #Delta R; Efficiency",S4));    
    eff_s4tor->Draw();
    can_LOR->cd(5);    
    eff_s5tor->SetLineColor(kCyan);    
    eff_s5tor->SetMarkerColor(kCyan);    
    eff_s5tor->SetMarkerStyle(24);    
    eff_s5tor->SetStats(kFALSE);    
    eff_s5tor->SetTitle(Form("Efficiency: %s, Logical OR; #Delta R; Efficiency",S5));    
    eff_s5tor->Draw();
    
    can_LOR->cd(6);    
    eff_s6tor->SetLineColor(kMagenta);    
    eff_s6tor->SetMarkerColor(kMagenta);    
    eff_s6tor->SetMarkerStyle(25);
    eff_s6tor->SetStats(kFALSE);    
    eff_s6tor->SetTitle(Form("Efficiency: %s, Logical OR; #Delta R; Efficiency",S6));    
    eff_s6tor->Draw();    
    can_LOR->SaveAs("../outputs/plots/modules/genTriggerEfficiency/central_LogicalOR_can.pdf");

	eff_s7tor->SetLineColor(kPink);    
    eff_s7tor->SetMarkerColor(kPink);    
    eff_s7tor->SetMarkerStyle(26);
    
    eff_s8tor->SetLineColor(kViolet);    
    eff_s8tor->SetMarkerColor(kViolet);    
    eff_s8tor->SetMarkerStyle(27);
    
    eff_s9tor->SetLineColor(kGreen-1);    
    eff_s9tor->SetMarkerColor(kGreen-1);    
    eff_s9tor->SetMarkerStyle(28);
    
    eff_s0tor->SetLineColor(kYellow);    
    eff_s0tor->SetMarkerColor(kYellow);    
    eff_s0tor->SetMarkerStyle(29);
    
    //eff_comb_num->SetLineColor(kOrange+7);
    //eff_comb_num->SetMarkerColor(kOrange+7);
    //eff_comb_num->SetMarkerSize(2);
    //eff_comb_num->SetStats(0);
    //eff_comb_num->SetMarkerStyle(34);
    //TCanvas *c1 = new TCanvas ();
    /*eff_comb_num->SetTitle("Efficiency: Combined samples logical OR; #Delta R; Efficiency");
    eff_comb_num->Draw();
    TLegend *legtorcomb = new TLegend(.6, .7, .9, .898);
    legtorcomb->SetHeader("Samples","C");
    legtorcomb->SetBorderSize(0);
    legtorcomb->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    legtorcomb->AddEntry(eff_comb_num, "mXX-1000_mA-5_lxy", "P");
    legtorcomb->Draw();*/

    TCanvas* can_LORall = new TCanvas("can_LORall");  
    eff_s1tor->SetTitle("Efficiency: all samples Logical OR; #Delta R; Efficiency");
    eff_s1tor->SetStats(kFALSE);
    eff_s1tor->SetAxisRange(0.0,1.0,"Y");
    eff_s1tor->Draw();
    eff_s2tor->Draw("same");
    eff_s3tor->Draw("same");
    eff_s4tor->Draw("same");
    eff_s5tor->Draw("same");
    eff_s6tor->Draw("same");
    eff_s0tor->Draw("same");
    
    TLegend *legtorall = new TLegend(.6, .7, .9, .898);
    legtorall->SetHeader("Samples","C");
    legtorall->SetBorderSize(0);
    legtorall->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    legtorall->AddEntry(eff_s1tor, Form("%s", S1), "P");
    legtorall->AddEntry(eff_s2tor, Form("%s", S2), "P");
    legtorall->AddEntry(eff_s3tor, Form("%s", S3), "P");
    legtorall->AddEntry(eff_s4tor, Form("%s", S4), "P");
    legtorall->AddEntry(eff_s5tor, Form("%s", S5), "P");
    legtorall->AddEntry(eff_s6tor, Form("%s", S6), "P");
    legtorall->AddEntry(eff_s0tor, Form("%s", S0), "P");
    legtorall->Draw();
    can_LORall->SaveAs("../outputs/plots/modules/genTriggerEfficiency/central_LogicalOR_all.pdf");
    
    TCanvas* can_LORlxy = new TCanvas("can_LORlxy");  
    eff_s1tor->SetTitle("Efficiency: Different l_xy Logical OR; #Delta R; Efficiency");
    eff_s1tor->SetStats(kFALSE);
    eff_s1tor->SetAxisRange(0.0,1.0,"Y");
    eff_s1tor->Draw();
    eff_s4tor->Draw("same");
    eff_s7tor->Draw("same");
    eff_s8tor->Draw("same");
    eff_s9tor->Draw("same");
    eff_comb_num->Draw("same");
    
    TLegend *legtorlxy = new TLegend(.6, .7, .9, .898);
    legtorlxy->SetHeader("Samples","C");
    legtorlxy->SetBorderSize(0);
    legtorlxy->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    legtorlxy->AddEntry(eff_s9tor, Form("%s", S9), "P");
    legtorlxy->AddEntry(eff_s8tor, Form("%s", S8), "P");
    legtorlxy->AddEntry(eff_s4tor, Form("%s", S4), "P");
    legtorlxy->AddEntry(eff_s7tor, Form("%s", S7), "P");
    legtorlxy->AddEntry(eff_s1tor, Form("%s", S1), "P");
    //legtorlxy->AddEntry(eff_comb_num, "different l_{xy} Comb" , "P");
    legtorlxy->Draw();
    can_LORlxy->SaveAs("../outputs/plots/modules/genTriggerEfficiency/central_LogicalOR_lxy.pdf");
}









