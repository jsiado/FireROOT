void el_dR_ch2mu2eTrEff(const char *date, const char *filter, const char *muon)
{
	TFile* file_1 = TFile::Open(Form("../outputs/rootfiles/modules/el%s_ch2mu2eTrEff.root",muon));
	//TFile* file_1 = TFile::Open("../outputs/rootfiles/modules/el_ch2mu2eTrEff.root");
	
	// samples
	char S1[50] = "mXX-1000_mA-5_lxy-300", S2[50] = "mXX-100_mA-5_lxy-0p3", S3[50] = "mXX-500_mA-0p25_lxy-300", S4[50] = "mXX-1000_mA-5_lxy-30", 
	S5[50] = "mXX-500_mA-1p2_lxy-30", S6[50] = "mXX-100_mA-0p25_lxy-300", S7[50]= "mXX-1000_mA-5_lxy-150", S8[50] = "mXX-1000_mA-5_lxy-3", 
	S9[50] = "mXX-1000_mA-5_lxy-0p3", S0[50] = "mXX-200_mA-0p25_lxy-300", S11[50] = "mXX-100_mA-0p25_lxy-0p3", S12[50] = "mXX-100_mA-0p25_lxy-3",
	S13[50] = "mXX-100_mA-0p25_lxy-30",S14[50] = "mXX-100_mA-0p25_lxy-150", S15[50] = "mXX-500_mA-1p2_lxy-0p3", S16[50] = "mXX-500_mA-1p2_lxy-3", 
	S17[50] = "mXX-500_mA-1p2_lxy-150", S18[50] = "mXX-500_mA-1p2_lxy-300";
  
    //num all samples
	TH1F *num_s1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_dR",S1));	TH1F *eff_s1 = (TH1F*) num_s1->Clone();
	TH1F *num_s2 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_dR",S2));	TH1F *eff_s2 = (TH1F*) num_s2->Clone();
	TH1F *num_s3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_dR",S3));	TH1F *eff_s3 = (TH1F*) num_s3->Clone();
	TH1F *num_s4 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_dR",S4));	TH1F *eff_s4 = (TH1F*) num_s4->Clone();
	TH1F *num_s5 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_dR",S5));	TH1F *eff_s5 = (TH1F*) num_s5->Clone();
	TH1F *num_s6 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_dR",S6));	TH1F *eff_s6 = (TH1F*) num_s6->Clone();
	

    //den all samples
	TH1F *den_s1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_dR",S1));
	TH1F *den_s2 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_dR",S2));     
	TH1F *den_s3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_dR",S3));
	TH1F *den_s4 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_dR",S4));
	TH1F *den_s5 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_dR",S5));
	TH1F *den_s6 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_dR",S6));
    
    
	eff_s1->Divide(den_s1);
	eff_s2->Divide(den_s2);
	eff_s3->Divide(den_s3);
	eff_s4->Divide(den_s4);
	eff_s5->Divide(den_s5);
	eff_s6->Divide(den_s6);
    
	eff_s1->SetLineColor(kBlack); 
	eff_s2->SetLineColor(kMagenta);
	eff_s3->SetLineColor(kBlue);
	eff_s4->SetLineColor(kRed);
	eff_s5->SetLineColor(kOrange);
	eff_s6->SetLineColor(kGreen);
    
	eff_s1->SetMarkerColor(kBlack);
	eff_s2->SetMarkerColor(kMagenta);
	eff_s3->SetMarkerColor(kBlue);
	eff_s4->SetMarkerColor(kRed);
	eff_s5->SetMarkerColor(kOrange);
	eff_s6->SetMarkerColor(kGreen);
	
	TCanvas *can_f1 = new TCanvas("can_f1","",800,600);
	eff_s1->SetTitle(Form("#Delta R of %s muons ; #Delta R; Efficiency",muon));
	eff_s1->SetStats(kFALSE);
	eff_s1->SetAxisRange(0.0,1.1,"Y");
	eff_s1->Draw();
	eff_s2->Draw("same");
	eff_s3->Draw("same");
	eff_s4->Draw("same");
	eff_s5->Draw("same");
	eff_s6->Draw("same");
    
	TLegend *leg_f1 = new TLegend(.6, .7, 0.9, .898);    
	leg_f1->SetHeader("Samples","C");
	leg_f1->SetBorderSize(0);    
	leg_f1->SetLineColor(1);    
	gStyle->SetFillColor(0);    
	gStyle->SetCanvasColor(10);    
	leg_f1->AddEntry(eff_s1, Form("%s",S1), "P");
	leg_f1->AddEntry(eff_s2, Form("%s",S2), "P");    
	leg_f1->AddEntry(eff_s3, Form("%s",S3), "P");
	leg_f1->AddEntry(eff_s4, Form("%s",S4), "P");
	leg_f1->AddEntry(eff_s5, Form("%s",S5), "P");    
	leg_f1->AddEntry(eff_s6, Form("%s",S6), "P");    
	leg_f1->Draw();    
	can_f1->SaveAs(Form("../outputs/plots/modules/el_ch2mu2eTrEff/elte_%s_dR_%s_%s.pdf",date,filter,muon));
	can_f1->SaveAs(Form("../outputs/plots/modules/el_ch2mu2eTrEff/elte_%s_dR_%s_%s.png",date,filter,muon));
}


