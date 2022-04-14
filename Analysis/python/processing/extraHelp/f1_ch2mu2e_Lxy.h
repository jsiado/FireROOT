void f1_ch2mu2e_Lxy(const char *date, const char *samp)
{
//plot efficiency for different values of Lxy, mA, and mXX	
//	cout<<date<<endl;
	TFile* file_1 = TFile::Open(Form("../outputs/rootfiles/modules/ch2mu2eTrEff_%s.root",samp));
	
	// samples
	char S1[50] = "mXX-1000_mA-5_lxy-300", S2[50] = "mXX-100_mA-5_lxy-0p3", S3[50] = "mXX-500_mA-0p25_lxy-300", S5[50] = "mXX-1000_mA-5_lxy-30", 
	S4[50] = "mXX-500_mA-1p2_lxy-30", S6[50] = "mXX-100_mA-0p25_lxy-300", S7[50]= "mXX-1000_mA-5_lxy-150", S16[50] = "mXX-1000_mA-5_lxy-3", 
	S9[50] = "mXX-1000_mA-5_lxy-0p3", S0[50] = "mXX-200_mA-0p25_lxy-300", S11[50] = "mXX-100_mA-0p25_lxy-0p3", S12[50] = "mXX-100_mA-0p25_lxy-3",
	S13[50] = "mXX-100_mA-0p25_lxy-30",S14[50] = "mXX-100_mA-0p25_lxy-150", S15[50] = "mXX-500_mA-1p2_lxy-0p3", S8[50] = "mXX-500_mA-1p2_lxy-3", 
	S17[50] = "mXX-500_mA-1p2_lxy-150", S18[50] = "mXX-500_mA-1p2_lxy-300";

//for (int ii=1; ii<5; ii++)
//{
    //num all samples
	//TH1F *num_s8 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_dR",S8));	TH1F *eff_s8 = (TH1F*) num_s8->Clone();
	//TH1F *num_s4 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_dR",S4));	TH1F *eff_s4 = (TH1F*) num_s4->Clone();
	TH1F *num_s1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_dR",S1));	TH1F *eff_s1 = (TH1F*) num_s1->Clone();
	TH1F *num_s3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_dR",S3));	TH1F *eff_s3 = (TH1F*) num_s3->Clone();
	TH1F *num_s6 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_dR",S6));	TH1F *eff_s6 = (TH1F*) num_s6->Clone();
	

    //den all samples
	//TH1F *den_s8 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_dR",S8));        
	//TH1F *den_s4 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_dR",S4));
	TH1F *den_s1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_dR",S1));
	TH1F *den_s3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_dR",S3));
	TH1F *den_s6 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_dR",S6));

 
	//eff_s8->Divide(den_s8);
	//eff_s4->Divide(den_s4);
	eff_s1->Divide(den_s1);
	eff_s3->Divide(den_s3);
	eff_s6->Divide(den_s6);
	    
	//eff_s8->SetLineColor(kBlack); 
	//eff_s4->SetLineColor(kBlue); 
	eff_s1->SetLineColor(kGreen);
	eff_s3->SetLineColor(kBlack);
	eff_s6->SetLineColor(kBlue);
	
	//eff_s8->SetMarkerColor(kBlack);
	//eff_s4->SetMarkerColor(kBlue);
	eff_s1->SetMarkerColor(kGreen);
	eff_s3->SetMarkerColor(kBlack);
	eff_s6->SetMarkerColor(kBlue);
	//eff_s8->Draw();
	
	//diffetent lxy
	TCanvas *can_lxy = new TCanvas("can_lxy","",800,600);
	eff_s1->SetTitle("; #delta R; Efficiency");
	eff_s1->SetStats(kFALSE);
	eff_s1->SetAxisRange(0.0,2.0,"Y");
	eff_s1->Draw();
	eff_s3->Draw("same");
	eff_s6->Draw("same");
    
	TLegend *leg_f1x = new TLegend(.6, .7, 0.9, .898);    
	leg_f1x->SetHeader("Samples","C");
	leg_f1x->SetBorderSize(0);    
	leg_f1x->SetLineColor(1);    
	gStyle->SetFillColor(0);    
	gStyle->SetCanvasColor(10);    
	leg_f1x->AddEntry(eff_s1, Form("%s",S8), "P");
	leg_f1x->AddEntry(eff_s3, Form("%s",S4), "P");  
	leg_f1x->AddEntry(eff_s6, Form("%s",S1), "P");   
	leg_f1x->Draw();
	can_lxy->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_Lxy_%s.pdf",date,samp));
	can_lxy->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_Lxy_%s.png",date,samp));
	
	//diffetent mA
	/*TCanvas *can_mA = new TCanvas("can_mA","",800,600);
	//eff_s3->SetTitle("#epsilon _{T}: Different m_{A}; #delta R; Efficiency");
	eff_s3->SetTitle("; #delta R; Efficiency");
	eff_s3->SetStats(kFALSE);
	eff_s3->SetAxisRange(0.0,2.0,"Y");
	eff_s3->Draw();
	eff_s1->Draw("same");
    
	TLegend *leg_f1a = new TLegend(.6, .7, 0.9, .898);    
	leg_f1a->SetHeader("Samples","C");
	leg_f1a->SetBorderSize(0);    
	leg_f1a->SetLineColor(1);    
	gStyle->SetFillColor(0);    
	gStyle->SetCanvasColor(10);    
	leg_f1a->AddEntry(eff_s3, Form("%s",S3), "P");
	leg_f1a->AddEntry(eff_s1, Form("%s",S1), "P");   
	leg_f1a->Draw();
	can_mA->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_mA_%s.pdf",date,samp));
	can_mA->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_mA_%s.png",date,samp));
	
	//diffetent mXX
	TCanvas *can_mx = new TCanvas("can_mx","",800,600);
	eff_s3->SetTitle("; #delta R; Efficiency");
	eff_s3->SetStats(kFALSE);
	eff_s3->SetAxisRange(0.0,2.0,"Y");
	eff_s3->Draw();
	eff_s6->Draw("same");
    
	TLegend *leg_f1m = new TLegend(.6, .7, 0.9, .898);    
	leg_f1m->SetHeader("Samples","C");
	leg_f1m->SetBorderSize(0);    
	leg_f1m->SetLineColor(1);    
	gStyle->SetFillColor(0);    
	gStyle->SetCanvasColor(10);    
	leg_f1m->AddEntry(eff_s3, Form("%s",S3), "P");
	leg_f1m->AddEntry(eff_s6, Form("%s",S6), "P");   
	leg_f1m->Draw();
	can_mx->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_mx_%s.pdf",date,samp));
	can_mx->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_mx_%s.png",date,samp));*/
	
}


