//samples used: 
void lxyStudy_dR(const char *date)
{
	//TFile* file_1 = TFile::Open(Form("../outputs/rootfiles/modules/allEventsch2mu2eTrEff.root",muon));
	TFile* file_1 = TFile::Open("../outputs/rootfiles/modules/allEvents.root");
	
	// samples
	char
	S11[50] = "mXX-100_mA-0p25_lxy-0p3",	S0[50] = "mXX-200_mA-0p25_lxy-300",	S3[50]  = "mXX-500_mA-0p25_lxy-300",	S9[50] = "mXX-1000_mA-5_lxy-0p3",
	S12[50] = "mXX-100_mA-0p25_lxy-3",											S15[50] = "mXX-500_mA-1p2_lxy-0p3",		S8[50] = "mXX-1000_mA-5_lxy-3",
	S13[50] = "mXX-100_mA-0p25_lxy-30",											S16[50] = "mXX-500_mA-1p2_lxy-3",		S4[50] = "mXX-1000_mA-5_lxy-30",
	S6[50]  = "mXX-100_mA-0p25_lxy-300", 										S5[50]  = "mXX-500_mA-1p2_lxy-30",		S7[50] = "mXX-1000_mA-5_lxy-150",
	S14[50] = "mXX-100_mA-0p25_lxy-150",										S17[50] = "mXX-500_mA-1p2_lxy-150",		S1[50] = "mXX-1000_mA-5_lxy-300",
	S2[50]  = "mXX-100_mA-5_lxy-0p3",											S18[50] = "mXX-500_mA-1p2_lxy-300";
  	
    //num all samples
	TH1F *hist_s5 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/dsapt",S5));
	TH1F *hist_s16 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/dsapt",S16));
	TH1F *hist_s18 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/dsapt",S18));
	//hist_s1->Draw();
	//hist_s1
	//cout<<"la marica"<<endl;
	TCanvas *can_c1 = new TCanvas("can_c1","",800,600);
	hist_s5->SetTitle("dsa p_t; #Delta R; Efficiency");
	hist_s5->SetStats(kFALSE);
	//hist_s5->SetAxisRange(0.0,1.1,"Y");
	hist_s5->Draw();
	hist_s16->Draw("same");
	hist_s18->Draw("same");
	
	TLegend *leg_s = new TLegend(.6, .7, 0.9, .898);    
	leg_s->SetHeader("Samples","C");
	leg_s->SetBorderSize(0);    
	leg_s->SetLineColor(1);    
	gStyle->SetFillColor(0);    
	gStyle->SetCanvasColor(10);
	leg_s->AddEntry(hist_s5, Form("%s",S5), "P");
	leg_s->AddEntry(hist_s16, Form("%s",S16), "P");
	leg_s->AddEntry(hist_s18, Form("%s",S18), "P");
	leg_s->Draw();
	
}
