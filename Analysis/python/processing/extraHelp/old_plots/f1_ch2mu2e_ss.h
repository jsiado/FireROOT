void f1_ch2mu2e_ss(const char *date, const char *samp)
{	
//	cout<<date<<endl;
	TFile* file_1 = TFile::Open(Form("../outputs/rootfiles/modules/ch2mu2eTrEff_%s.root",samp));
	
	// samples
	char S1[50] = "mXX-1000_mA-5_lxy-300", S2[50] = "mXX-100_mA-5_lxy-0p3", S3[50] = "mXX-500_mA-0p25_lxy-300", S4[50] = "mXX-1000_mA-5_lxy-30", 
	S5[50] = "mXX-500_mA-1p2_lxy-30", S6[50] = "mXX-100_mA-0p25_lxy-300", S7[50]= "mXX-1000_mA-5_lxy-150", S8[50] = "mXX-1000_mA-5_lxy-3", 
	S9[50] = "mXX-1000_mA-5_lxy-0p3", S0[50] = "mXX-200_mA-0p25_lxy-300", S11[50] = "mXX-100_mA-0p25_lxy-0p3", S12[50] = "mXX-100_mA-0p25_lxy-3",
	S13[50] = "mXX-100_mA-0p25_lxy-30",S14[50] = "mXX-100_mA-0p25_lxy-150", S15[50] = "mXX-500_mA-1p2_lxy-0p3", S16[50] = "mXX-500_mA-1p2_lxy-3", 
	S17[50] = "mXX-500_mA-1p2_lxy-150", S18[50] = "mXX-500_mA-1p2_lxy-300";
  
	//triggers
	//char Tf1[50] = "DoubleL2Mu23NoVtx_2Cha", Tf2[50] = "DoubleL2Mu23NoVtx_2Cha_NoL2Matched", Tf3[50]= "DoubleL2Mu23NoVtx_2Cha_CosmicSeed", 
      //Tf4[50] = "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched", Tf5[50] = "DoubleL2Mu25NoVtx_2Cha_Eta2p4", T6f[50] = "DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4";

//for (int ii=1; ii<5; ii++)
//{
    //num all samples
	TH1F *num_s1r = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_dR",S1));	TH1F *eff_s1r = (TH1F*) num_s1r->Clone();
	TH1F *num_s1p = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_pT",S1));	TH1F *eff_s1p = (TH1F*) num_s1p->Clone();
	TH1F *num_s1e = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Num_eta",S1));	TH1F *eff_s1e = (TH1F*) num_s1e->Clone();
	

    //den all samples
	TH1F *den_s1r = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_dR",S1));        
	TH1F *den_s1p = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_pT",S1));
	TH1F *den_s1e = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_Den_eta",S1));
    
    
	eff_s1r->Divide(den_s1r);
	eff_s1p->Divide(den_s1p);
	eff_s1e->Divide(den_s1e);
    
	TCanvas *can_f1r = new TCanvas("can_f1r","",800,600);
	eff_s1r->SetTitle("Efficiency: #Delta R between muons ; #delta R; Efficiency");
	eff_s1r->SetStats(kFALSE);
	eff_s1r->SetAxisRange(0.0,2.0,"Y");
	eff_s1r->Draw();
	can_f1r->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_ssdR_%s.pdf",date,samp));
	can_f1r->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_ssdR_%s.png",date,samp));
	
	TCanvas *can_f1p = new TCanvas("can_f1p","",800,600);
	eff_s1p->SetTitle("Efficiency: p_T leading muon ; p_T; Efficiency");
	eff_s1p->SetStats(kFALSE);
	eff_s1p->SetAxisRange(0.0,2.0,"Y");
	eff_s1p->Draw();
	can_f1p->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_sspT_%s.pdf",date,samp));
	can_f1p->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_sspT_%s.png",date,samp));
	
	TCanvas *can_f1e = new TCanvas("can_f1e","",800,600);
	eff_s1e->SetTitle("Efficiency: #eta leading muon ; #eta; Efficiency");
	eff_s1e->SetStats(kFALSE);
	eff_s1e->SetAxisRange(0.0,2.0,"Y");
	eff_s1e->Draw();
	can_f1e->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_sseta_%s.pdf",date,samp));
	can_f1e->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_sseta_%s.png",date,samp));
}


