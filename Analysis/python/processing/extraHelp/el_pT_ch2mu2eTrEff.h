void el_pT_ch2mu2eTrEff(const char *date, const char *filter, const char *muon)
{
	//TFile* file_1 = TFile::Open("../outputs/rootfiles/modules/el_ch2mu2eTrEff.root");
	TFile* file_1 = TFile::Open(Form("../outputs/rootfiles/modules/el%s_ch2mu2eTrEff.root",muon));
//	TFile* file_1 = TFile::Open(Form("../outputs/rootfiles/modules/ch2mu2eTrEff_%s.root",filter));
	
	// samples
	char 
	S1[50] = "mXX-1000_mA-5_lxy-300", S2[50] = "mXX-100_mA-5_lxy-0p3", S3[50] = "mXX-500_mA-0p25_lxy-300", S4[50] = "mXX-1000_mA-5_lxy-30", 
	S5[50] = "mXX-500_mA-1p2_lxy-30", S6[50] = "mXX-100_mA-0p25_lxy-300", S7[50]= "mXX-1000_mA-5_lxy-150", S8[50] = "mXX-1000_mA-5_lxy-3", 
	S9[50] = "mXX-1000_mA-5_lxy-0p3", S0[50] = "mXX-200_mA-0p25_lxy-300", S11[50] = "mXX-100_mA-0p25_lxy-0p3", S12[50] = "mXX-100_mA-0p25_lxy-3",
	S13[50] = "mXX-100_mA-0p25_lxy-30",S14[50] = "mXX-100_mA-0p25_lxy-150", S15[50] = "mXX-500_mA-1p2_lxy-0p3", S16[50] = "mXX-500_mA-1p2_lxy-3", 
	S17[50] = "mXX-500_mA-1p2_lxy-150", S18[50] = "mXX-500_mA-1p2_lxy-300";
  
    //num all samples
	TH1F *num_s1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_pT",S1));	TH1F *eff_s1 = (TH1F*) num_s1->Clone();
	TH1F *num_s2 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_pT",S2));	TH1F *eff_s2 = (TH1F*) num_s2->Clone();
	TH1F *num_s3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_pT",S3));	TH1F *eff_s3 = (TH1F*) num_s3->Clone();
	TH1F *num_s4 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_pT",S4));	TH1F *eff_s4 = (TH1F*) num_s4->Clone();
	TH1F *num_s5 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_pT",S5));	TH1F *eff_s5 = (TH1F*) num_s5->Clone();
	TH1F *num_s6 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_pT",S6));	TH1F *eff_s6 = (TH1F*) num_s6->Clone();
	

    //den all samples
	TH1F *den_s1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_pT",S1));
	TH1F *den_s2 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_pT",S2));        
	TH1F *den_s3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_pT",S3));
	TH1F *den_s4 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_pT",S4));
	TH1F *den_s5 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_pT",S5));
	TH1F *den_s6 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_pT",S6));
    
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
    
    TCanvas *can_pT = new TCanvas("can_pT","",800,600);
	eff_s1->SetTitle(Form("Leading %s muon p_{T}; p_{T} [GeV]; Efficiency",muon));
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
	can_pT->SaveAs(Form("../outputs/plots/modules/el_ch2mu2eTrEff/elte_%s_pT_%s_%s.pdf",date, filter, muon));
	can_pT->SaveAs(Form("../outputs/plots/modules/el_ch2mu2eTrEff/elte_%s_pT_%s_%s.png",date, filter, muon));
	
	
	//pT zoom in
	/*TH1F *nums_s1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_pT_zoom",S1));	TH1F *effs_s1 = (TH1F*) nums_s1->Clone();
	TH1F *nums_s3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_pT_zoom",S3));	TH1F *effs_s3 = (TH1F*) nums_s3->Clone();
	TH1F *nums_s6 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_pT_zoom",S6));	TH1F *effs_s6 = (TH1F*) nums_s6->Clone();
	

    //den all samples
	TH1F *dens_s1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_pT_zoom",S1));        
	TH1F *dens_s3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_pT_zoom",S3));
	TH1F *dens_s6 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_pT_zoom",S6));
    
    
	effs_s1->Divide(dens_s1);
	effs_s3->Divide(dens_s3);
	effs_s6->Divide(dens_s6);
    
	effs_s1->SetLineColor(kBlack); 
	effs_s3->SetLineColor(kBlue); 
	effs_s6->SetLineColor(kGreen);
    
	effs_s1->SetMarkerColor(kBlack); 
	effs_s3->SetMarkerColor(kBlue); 
	effs_s6->SetMarkerColor(kGreen);
	TCanvas *can_pTs = new TCanvas("can_pTs","",800,600);
    //if (ii == 1){ eff_s1->SetTitle("Efficiency: Leading muon ; #delta R; Efficiency");}
    //if (ii == 2){ eff_s1->SetTitle("Efficiency: Sub-leading muon ; #delta R; Efficiency");}
    //if (ii == 3){ eff_s1->SetTitle("Efficiency: Logical AND; #delta R; Efficiency");}
    //if (ii == 4){ 
	effs_s1->SetTitle("; p_{T} [GeV]; Efficiency");
	effs_s1->SetStats(kFALSE);
	effs_s1->SetAxisRange(0.0,1.1,"Y");
	effs_s1->Draw();
	effs_s3->Draw("same");
	effs_s6->Draw("same");
    
	TLegend *leg_f1s = new TLegend(.6, .7, 0.9, .898);
	leg_f1s->SetHeader("Samples","C");
	leg_f1s->SetBorderSize(0);
	leg_f1s->SetLineColor(1);
	gStyle->SetFillColor(0);
	gStyle->SetCanvasColor(10);
	leg_f1s->AddEntry(effs_s1, Form("%s",S1), "P");
	leg_f1s->AddEntry(effs_s3, Form("%s",S3), "P");
	leg_f1s->AddEntry(effs_s6, Form("%s",S6), "P");
	leg_f1s->Draw();
	can_pTs->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_pTs_%s.pdf",date, filter));
	//can_pT->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_%s.png",date, filter));
	
	TCanvas *can_pTs = new TCanvas("can_pTs","",800,600);
	//eff_s1->SetTitle("Efficiency: Leading muon p_{T}; p_{T}; Efficiency");
	eff_s1->SetTitle(" ; p_{T} [GeV]; Efficiency");
	eff_s1->SetStats(kFALSE);
	eff_s1->SetAxisRange(0.0,1.0,"Y");
	eff_s1->SetAxisRange(0.0,200,"X");
	//eff_s1->Draw();
	//eff_s3->Draw("same");
	//eff_s6->Draw("same");
    
	TLegend *leg_f1s = new TLegend(.6, .7, 0.9, .898);    
	leg_f1s->SetHeader("Samples","C");
	leg_f1s->SetBorderSize(0);    
	leg_f1s->SetLineColor(1);    
	gStyle->SetFillColor(0);    
	gStyle->SetCanvasColor(10);    
	leg_f1s->AddEntry(eff_s1, Form("%s",S1), "P");    
	leg_f1s->AddEntry(eff_s3, Form("%s",S3), "P");    
	leg_f1s->AddEntry(eff_s6, Form("%s",S6), "P");    
	leg_f1s->Draw();
	//can_pTs->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_noptcs_%s.pdf",date,samp));
	//can_pTs->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_noptcs_%s.png",date,samp));
	
	TCanvas *can_pTnc = new TCanvas("can_pTnc","",800,600);
	//eff_s1->SetTitle("Efficiency: Leading muon p_{T}; p_{T}; Efficiency");
	eff_s1->SetTitle(" ; p_{T} [GeV]; Efficiency");
	eff_s1->SetStats(kFALSE);
	eff_s1->SetAxisRange(0.0,1.0,"Y");
	eff_s1->SetAxisRange(0.0,500,"X");
	//eff_s1->Draw();
	//eff_s3->Draw("same");
	//eff_s6->Draw("same");
    
	TLegend *leg_f1s = new TLegend(.6, .7, 0.9, .898);    
	leg_f1s->SetHeader("Samples","C");
	leg_f1s->SetBorderSize(0);    
	leg_f1s->SetLineColor(1);    
	gStyle->SetFillColor(0);    
	gStyle->SetCanvasColor(10);    
	leg_f1s->AddEntry(eff_s1, Form("%s",S1), "P");    
	leg_f1s->AddEntry(eff_s3, Form("%s",S3), "P");    
	leg_f1s->AddEntry(eff_s6, Form("%s",S6), "P");    
	leg_f1s->Draw();
	//can_pTnc->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_noptc1_%s.pdf",date,samp));
	//can_pTnc->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_noptc1_%s.png",date,samp));*/
}


