void f1_ch2mu2e(const char *date)
{	
//	cout<<date<<endl;
	TFile* file_1 = TFile::Open("../outputs/rootfiles/modules/ch2mu2eTrEff.root");
	
	// samples
	char S1[50] = "mXX-1000_mA-5_lxy-300", S2[50] = "mXX-100_mA-5_lxy-0p3", S3[50] = "mXX-500_mA-0p25_lxy-300", S4[50] = "mXX-1000_mA-5_lxy-30", 
	S5[50] = "mXX-500_mA-1p2_lxy-30", S6[50] = "mXX-100_mA-0p25_lxy-300", S7[50]= "mXX-1000_mA-5_lxy-150", S8[50] = "mXX-1000_mA-5_lxy-3", 
	S9[50] = "mXX-1000_mA-5_lxy-0p3", S0[50] = "mXX-200_mA-0p25_lxy-300", S11[50] = "mXX-100_mA-0p25_lxy-0p3", S12[50] = "mXX-100_mA-0p25_lxy-3",
	S13[50] = "mXX-100_mA-0p25_lxy-30",S14[50] = "mXX-100_mA-0p25_lxy-150", S15[50] = "mXX-500_mA-1p2_lxy-0p3", S16[50] = "mXX-500_mA-1p2_lxy-3", 
	S17[50] = "mXX-500_mA-1p2_lxy-150", S18[50] = "mXX-500_mA-1p2_lxy-300";
  
	//triggers
	char Tf1[50] = "DoubleL2Mu23NoVtx_2Cha", Tf2[50] = "DoubleL2Mu23NoVtx_2Cha_NoL2Matched", Tf3[50]= "DoubleL2Mu23NoVtx_2Cha_CosmicSeed", 
      Tf4[50] = "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched", Tf5[50] = "DoubleL2Mu25NoVtx_2Cha_Eta2p4", T6f[50] = "DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4";
    
    //num all samples
	TH1F *num_s1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/f_TO_Num",S1));	TH1F *eff_s1 = (TH1F*) num_s1->Clone();
	TH1F *num_s3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/f_TO_Num",S3));	TH1F *eff_s3 = (TH1F*) num_s3->Clone();
	TH1F *num_s6 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/f_TO_Num",S6));	TH1F *eff_s6 = (TH1F*) num_s6->Clone();
	

    //den all samples
	TH1F *den_s1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/f_TO_Den",S1));        
    TH1F *den_s3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/f_TO_Den",S3));
    TH1F *den_s6 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/f_TO_Den",S6));
    
    
    eff_s1->Divide(den_s1);
    eff_s3->Divide(den_s3);
    eff_s6->Divide(den_s6);
    
    eff_s1->SetLineColor(kBlack); 
    eff_s3->SetLineColor(kBlue); 
    eff_s6->SetLineColor(kGreen);
    
    eff_s1->SetMarkerColor(kBlack); 
    eff_s3->SetMarkerColor(kBlue); 
    eff_s6->SetMarkerColor(kGreen);
    
    
    
    
    TCanvas *can_f1 = new TCanvas("can_f1","",800,600);
    eff_s1->SetTitle("Efficiency: ; #delta R; Efficiency");
    eff_s1->SetStats(kFALSE);
    eff_s1->SetAxisRange(0.0,1.0,"Y");
    eff_s1->Draw();
    eff_s3->Draw("same");
    eff_s6->Draw("same");
    
    TLegend *leg_f1 = new TLegend(.6, .7, 0.9, .898);    
    leg_f1->SetHeader("Samples","C");
    leg_f1->SetBorderSize(0);    
    leg_f1->SetLineColor(1);    
    gStyle->SetFillColor(0);    
    gStyle->SetCanvasColor(10);    
    leg_f1->AddEntry(eff_s1, Form("%s",S1), "P");    
    leg_f1->AddEntry(eff_s3, Form("%s",S3), "P");    
    leg_f1->AddEntry(eff_s6, Form("%s",S6), "P");    
    //leg_mueta->AddEntry(mueta_s4, Form("%s",S4), "P");    
    //leg_mueta->AddEntry(mueta_s5, Form("%s",S5), "P");    
    //leg_mueta->AddEntry(mueta_s6, Form("%s",S6), "P");
    //leg_mueta->AddEntry(mueta_s0, Form("%s",S0), "P");
    leg_f1->Draw();    
    //can_f1ueta->SaveAs(Form("../outputs/plots/modules/TrEff2mu/%i_%s_mueta.pdf",date,muon));
    
	can_f1->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_f.pdf",date));
	can_f1->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_f.png",date));
}


