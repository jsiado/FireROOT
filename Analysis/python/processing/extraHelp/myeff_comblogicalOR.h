//run as root -l genTriEff.C

void myeff_comblogicalOR(int num)
{
    TFile* file_1 = TFile::Open("../outputs/rootfiles/modules/genTriggerEfficiency2mu.root");
    
  // samples
    char S1[50] = "mXX-1000_mA-5_lxy-300", S2[50] = "mXX-100_mA-5_lxy-0p3", S3[50] = "mXX-500_mA-0p25_lxy-300", S4[50] = "mXX-1000_mA-5_lxy-30", 
    S5[50] = "mXX-500_mA-1p2_lxy-30", S6[50] = "mXX-100_mA-0p25_lxy-300", S7[50]= "mXX-1000_mA-5_lxy-150", S8[50] = "mXX-1000_mA-5_lxy-3", 
    S9[50] = "mXX-1000_mA-5_lxy-0p3", S0[50] = "mXX-200_mA-0p25_lxy-300", S11[50] = "mXX-100_mA-0p25_lxy-0p3", S12[50] = "mXX-100_mA-0p25_lxy-3",
    S13[50] = "mXX-100_mA-0p25_lxy-30",S14[50] = "mXX-100_mA-0p25_lxy-150", 
    S15[50] = "mXX-500_mA-1p2_lxy-0p3", S16[50] = "mXX-500_mA-1p2_lxy-3", S17[50] = "mXX-500_mA-1p2_lxy-150", S18[50] = "mXX-500_mA-1p2_lxy-300", 
    S19[50]="mXX-500_mA-5_lxy-0p3", S20[50] = "mXX-500_mA-5_lxy-3", S21[50] = "mXX-500_mA-5_lxy-30", S22[50] = "mXX-500_mA-5_lxy-150", S23[50]="mXX-500_mA-5_lxy-300";
  //triggers
    char T1[50] = "DoubleL2Mu23NoVtx_2Cha", T2[50] = "DoubleL2Mu23NoVtx_2Cha_NoL2Matched", T3[50]= "DoubleL2Mu23NoVtx_2Cha_CosmicSeed", 
      T4[50] = "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched", T5[50] = "DoubleL2Mu25NoVtx_2Cha_Eta2p4", T6[50] = "DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4";
    
    
    TH1F *alldimu_1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S1));
    //TH1F *alldimu_2 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S2));
    //TH1F *alldimu_3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S3));
  	TH1F *alldimu_4 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S4));
    TH1F *alldimu_5 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S5));
    TH1F *alldimu_6 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S6));
    TH1F *alldimu_7 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S7));
    TH1F *alldimu_8 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S8));
    TH1F *alldimu_9 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S9));
    //TH1F *alldimu_0 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S0));
    TH1F *alldimu_11 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S11));
    TH1F *alldimu_12 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S12));
    TH1F *alldimu_13 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S13));
  	TH1F *alldimu_14 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S14));
    TH1F *alldimu_15 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S15));
    TH1F *alldimu_16 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S16));
    TH1F *alldimu_17 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S17));
    TH1F *alldimu_18 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S18));
    TH1F *alldimu_19 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S19));
    TH1F *alldimu_20 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S20));
    TH1F *alldimu_21 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S21));
    TH1F *alldimu_22 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S22));
    TH1F *alldimu_23 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S23));

    //All samples with Logical OR Combined
    TH1F *dimu_s1tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S1));    TH1F *eff_s1tor = (TH1F*) dimu_s1tor->Clone();    
    //TH1F *dimu_s2tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S2));    TH1F *eff_s2tor = (TH1F*) dimu_s2tor->Clone();
    //TH1F *dimu_s3tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S3));    TH1F *eff_s3tor = (TH1F*) dimu_s3tor->Clone();
    TH1F *dimu_s4tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S4));    TH1F *eff_s4tor = (TH1F*) dimu_s4tor->Clone();
    TH1F *dimu_s5tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S5));    TH1F *eff_s5tor = (TH1F*) dimu_s5tor->Clone();
    TH1F *dimu_s6tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S6));    TH1F *eff_s6tor = (TH1F*) dimu_s6tor->Clone();
    TH1F *dimu_s7tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S7));    TH1F *eff_s7tor = (TH1F*) dimu_s7tor->Clone();
    TH1F *dimu_s8tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S8));    TH1F *eff_s8tor = (TH1F*) dimu_s8tor->Clone();
    TH1F *dimu_s9tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S9));    TH1F *eff_s9tor = (TH1F*) dimu_s9tor->Clone();
   	//TH1F *dimu_s0tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S0));    TH1F *eff_s0tor = (TH1F*) dimu_s0tor->Clone();
   	TH1F *dimu_s11tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S11));    TH1F *eff_s11tor = (TH1F*) dimu_s11tor->Clone();    
    TH1F *dimu_s12tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S12));    TH1F *eff_s12tor = (TH1F*) dimu_s12tor->Clone();
    TH1F *dimu_s13tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S13));    TH1F *eff_s13tor = (TH1F*) dimu_s13tor->Clone();
    TH1F *dimu_s14tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S14));    TH1F *eff_s14tor = (TH1F*) dimu_s14tor->Clone();
    TH1F *dimu_s15tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S15));    TH1F *eff_s15tor = (TH1F*) dimu_s15tor->Clone();
    TH1F *dimu_s16tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S16));    TH1F *eff_s16tor = (TH1F*) dimu_s16tor->Clone();
    TH1F *dimu_s17tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S17));    TH1F *eff_s17tor = (TH1F*) dimu_s17tor->Clone();
    TH1F *dimu_s18tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S18));    TH1F *eff_s18tor = (TH1F*) dimu_s18tor->Clone();
    TH1F *dimu_s19tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S19));    TH1F *eff_s19tor = (TH1F*) dimu_s19tor->Clone();
   	TH1F *dimu_s20tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S20));    TH1F *eff_s20tor = (TH1F*) dimu_s20tor->Clone();
   	TH1F *dimu_s21tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S21));    TH1F *eff_s21tor = (TH1F*) dimu_s21tor->Clone();    
    TH1F *dimu_s22tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S22));    TH1F *eff_s22tor = (TH1F*) dimu_s22tor->Clone();
    TH1F *dimu_s23tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S23));    TH1F *eff_s23tor = (TH1F*) dimu_s23tor->Clone();
    
    TCanvas *cs1 = new TCanvas("ccs1");//for 1000 5 lxy
    TH1F *eff_comb_num1 = (TH1F*) dimu_s1tor->Clone();
    eff_comb_num1->Add(dimu_s4tor);
    eff_comb_num1->Add(dimu_s7tor);
    eff_comb_num1->Add(dimu_s8tor);
    eff_comb_num1->Add(dimu_s9tor);
    TH1F *eff_comb_den1 = (TH1F*) alldimu_1->Clone();
    eff_comb_den1->Add(alldimu_4);
    eff_comb_den1->Add(alldimu_7);
    eff_comb_den1->Add(alldimu_8);
    eff_comb_den1->Add(alldimu_9);
    
    TH1F *eff_comb_num2 = (TH1F*) dimu_s5tor->Clone();
    eff_comb_num2->Add(dimu_s15tor);
    eff_comb_num2->Add(dimu_s16tor);
    eff_comb_num2->Add(dimu_s17tor);
    eff_comb_num2->Add(dimu_s18tor);
    TH1F *eff_comb_den2 = (TH1F*) alldimu_5->Clone();
    eff_comb_den2->Add(alldimu_15);
    eff_comb_den2->Add(alldimu_16);
    eff_comb_den2->Add(alldimu_17);
    eff_comb_den2->Add(alldimu_18);
    
    TH1F *eff_comb_num3 = (TH1F*) dimu_s6tor->Clone();
    eff_comb_num3->Add(dimu_s11tor);
    eff_comb_num3->Add(dimu_s12tor);
    eff_comb_num3->Add(dimu_s13tor);
    eff_comb_num3->Add(dimu_s14tor);
    TH1F *eff_comb_den3 = (TH1F*) alldimu_6->Clone();
    eff_comb_den3->Add(alldimu_11);
    eff_comb_den3->Add(alldimu_12);
    eff_comb_den3->Add(alldimu_13);
    eff_comb_den3->Add(alldimu_14);
    
    TH1F *eff_comb_num4 = (TH1F*) dimu_s19tor->Clone();
    eff_comb_num4->Add(dimu_s20tor);
    eff_comb_num4->Add(dimu_s21tor);
    eff_comb_num4->Add(dimu_s22tor);
    eff_comb_num4->Add(dimu_s23tor);
    TH1F *eff_comb_den4 = (TH1F*) alldimu_19->Clone();
    eff_comb_den4->Add(alldimu_20);
    eff_comb_den4->Add(alldimu_21);
    eff_comb_den4->Add(alldimu_22);
    eff_comb_den4->Add(alldimu_23);
    
    
    
    //TCanvas *c4 = new TCanvas ("c4");
    eff_comb_num1->Divide(eff_comb_den1);
    eff_comb_num1->SetTitle("Efficiency: combined l_{xy}; #Delta R; Efficiency");
    eff_comb_num1->SetStats(kFALSE);
    eff_comb_num2->Divide(eff_comb_den2);
    eff_comb_num3->Divide(eff_comb_den3);
    eff_comb_num4->Divide(eff_comb_den4);
    
    eff_comb_num1->SetLineColor(kBlue);
    eff_comb_num2->SetLineColor(kGreen-7);
    eff_comb_num3->SetLineColor(kRed);
    eff_comb_num3->SetLineColor(kBlack);
    
    eff_comb_num1->SetMarkerColor(kBlue);
    eff_comb_num2->SetMarkerColor(kGreen-7);
    eff_comb_num3->SetMarkerColor(kRed);
    eff_comb_num4->SetMarkerColor(kBlack);
        
    eff_comb_num1->SetMarkerStyle(20);
    eff_comb_num2->SetMarkerStyle(21);
    eff_comb_num3->SetMarkerStyle(22);
    eff_comb_num4->SetMarkerStyle(23);
    
    //eff_comb_num1->Draw();
    
    eff_comb_num1->Draw();
    eff_comb_num2->Draw("same");
    eff_comb_num3->Draw("same");
    eff_comb_num4->Draw("same");
    
    TLegend *legtorall = new TLegend(.6, .7, .9, .898);
    legtorall->SetHeader("Samples","C");
    legtorall->SetBorderSize(0);
    legtorall->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    legtorall->AddEntry(eff_comb_num1, "m_{xx}-1000_M_{A}-5_L_{xy}", "P");
    legtorall->AddEntry(eff_comb_num2, "m_{xx}-100_M_{A}-0p25_L_{xy}", "P");
    legtorall->AddEntry(eff_comb_num3, "m_{xx}-500_M_{A}-1p2_L_{xy}", "P");
    legtorall->AddEntry(eff_comb_num4, "m_{xx}-500_M_{A}-5_L_{xy}", "P");
    legtorall->Draw();
    
    cs1->SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency2mu/%i_LogicalOR_comb.pdf",num));
    
    /*eff_s1tor->Divide(alldimu_1);
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
    can_LORlxy->SaveAs("../outputs/plots/modules/genTriggerEfficiency/central_LogicalOR_lxy.pdf");*/
}









