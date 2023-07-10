void TEFirstBin(const char *id){
	 
    TFile* f = TFile::Open(Form("../outputs/rootfiles/modules/out_%s.root",id));
	
	
	char S1[50] = "mXX-100_mA-0p25_lxy-300",  S4[50] = "mXX-500_mA-0p25_lxy-300", S3[50] = "mXX-500_mA-1p2_lxy-300",   S2[50] = "mXX-1000_mA-5_lxy-300";
	
	TCanvas *cs1 = new TCanvas("cs1","",1200,800);
    cs1->Divide(2,2);
    cs1->cd(1);
	
	TH1F *num2 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Num_dR",S3));
	num2->Draw();
	   
	cs1->cd(2);	
	TH1F *den2 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Den_dR",S3));
	den2->Draw();

	cs1->cd(3);
	TH1F *num3 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Num_dRfbin",S3));
	num3->Draw();

	cs1->cd(4);
	TH1F *den3 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Den_dRfbin",S3));
	den3->Draw();
   
    cs1->SaveAs(Form("../outputs/plots/modules/out_%s/%sTE_fbin_S3.png",id, id));

}
