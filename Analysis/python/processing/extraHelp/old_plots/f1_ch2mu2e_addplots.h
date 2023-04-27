void f1_ch2mu2e_addplots(const char *date, const char *filter)
{	
//	cout<<date<<endl;
	TFile* file_1 = TFile::Open(Form("../outputs/rootfiles/modules/ch2mu2eTrEff_%s.root",filter));
	
	// samples
	char S1[50] = "mXX-1000_mA-5_lxy-300", S2[50] = "mXX-100_mA-5_lxy-0p3", S3[50] = "mXX-500_mA-0p25_lxy-300", S4[50] = "mXX-1000_mA-5_lxy-30", 
	S5[50] = "mXX-500_mA-1p2_lxy-30", S6[50] = "mXX-100_mA-0p25_lxy-300", S7[50]= "mXX-1000_mA-5_lxy-150", S8[50] = "mXX-1000_mA-5_lxy-3", 
	S9[50] = "mXX-1000_mA-5_lxy-0p3", S0[50] = "mXX-200_mA-0p25_lxy-300", S11[50] = "mXX-100_mA-0p25_lxy-0p3", S12[50] = "mXX-100_mA-0p25_lxy-3",
	S13[50] = "mXX-100_mA-0p25_lxy-30",S14[50] = "mXX-100_mA-0p25_lxy-150", S15[50] = "mXX-500_mA-1p2_lxy-0p3", S16[50] = "mXX-500_mA-1p2_lxy-3", 
	S17[50] = "mXX-500_mA-1p2_lxy-150", S18[50] = "mXX-500_mA-1p2_lxy-300";
 	
 	//number of TO 
	TH1F *num_s1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_n",S1));
	TH1F *num_s3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_n",S3));
	
	num_s1->SetLineColor(kBlack); 
	num_s3->SetLineColor(kBlue); 
    
	num_s1->SetMarkerColor(kBlack);
	num_s3->SetMarkerColor(kBlue); 
	
	TCanvas *can_ton = new TCanvas("can_ton","",800,600);
	num_s3->SetTitle("# of trigger objects; # of TO; Entries");
	num_s3->SetStats(kFALSE);
	num_s3->Draw();
	num_s1->Draw("same");
    
	TLegend *leg_ton = new TLegend(.6, .7, 0.9, .898);    
	leg_ton->SetHeader("Samples","C");
	leg_ton->SetBorderSize(0);    
	leg_ton->SetLineColor(1);    
	gStyle->SetFillColor(0);    
	gStyle->SetCanvasColor(10);    
	leg_ton->AddEntry(num_s1, Form("%s",S1), "P");    
	leg_ton->AddEntry(num_s3, Form("%s",S3), "P");        
	leg_ton->Draw();    
	can_ton->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_TOn.pdf",date));
	//can_ton->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_TOn.png",date));
	
	//number of muons matched to a TO 
	TH1F *rmto_s1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/RMTO_match",S1));
	TH1F *rmto_s3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/RMTO_match",S3));
	
	rmto_s1->SetLineColor(kBlack); 
	rmto_s3->SetLineColor(kBlue); 
    
	rmto_s1->SetMarkerColor(kBlack);
	rmto_s3->SetMarkerColor(kBlue); 
	
	TCanvas *can_rmton = new TCanvas("can_rmton","",800,600);
	rmto_s3->SetTitle("# muons matched to trigger objects; # of muons; Entries");
	rmto_s3->SetStats(kFALSE);
	rmto_s3->Draw();
	rmto_s1->Draw("same");
    
	TLegend *leg_rmton = new TLegend(.6, .7, 0.9, .898);    
	leg_rmton->SetHeader("Samples","C");
	leg_rmton->SetBorderSize(0);    
	leg_rmton->SetLineColor(1);    
	gStyle->SetFillColor(0);    
	gStyle->SetCanvasColor(10);    
	leg_rmton->AddEntry(rmto_s1, Form("%s",S1), "P");    
	leg_rmton->AddEntry(rmto_s3, Form("%s",S3), "P");        
	leg_rmton->Draw();    
	can_rmton->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_RMTOn.pdf",date));
	//can_rmton->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_RMTOn.png",date));
	
	
	//TO pid 
	/*TH1F *topid_s1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_pid",S1));
	TH1F *topid_s3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/TO_pid",S3));
	
	topid_s1->SetLineColor(kBlack); 
	topid_s3->SetLineColor(kBlue); 
    
	topid_s1->SetMarkerColor(kBlack);
	topid_s3->SetMarkerColor(kBlue); 
	
	TCanvas *can_tod = new TCanvas("can_tod","",800,600);
	topid_s3->SetTitle("Trigger object IDs; ID ; Entries");
	topid_s3->SetStats(kFALSE);
	topid_s3->Draw();
	topid_s1->Draw("same");
    
	TLegend *leg_tod = new TLegend(.6, .7, 0.9, .898);    
	leg_tod->SetHeader("Samples","C");
	leg_tod->SetBorderSize(0);    
	leg_tod->SetLineColor(1);    
	gStyle->SetFillColor(0);    
	gStyle->SetCanvasColor(10);    
	leg_tod->AddEntry(topid_s1, Form("%s",S1), "P");    
	leg_tod->AddEntry(topid_s3, Form("%s",S3), "P");        
	leg_tod->Draw();    
	can_tod->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_TOid.pdf",date));
	can_tod->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_TOid.png",date));*/
	
	//number of Reco muons 
	TH1F *remu_s1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/RM_n",S1));
	TH1F *remu_s3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/RM_n",S3));
	
	remu_s1->SetLineColor(kBlack); 
	remu_s3->SetLineColor(kBlue); 
    
	remu_s1->SetMarkerColor(kBlack);
	remu_s3->SetMarkerColor(kBlue); 
	
	TCanvas *can_rmn = new TCanvas("can_rmn","",800,600);
	remu_s1->SetTitle("# of Reco Muons; # of RM ; Entries");
	remu_s1->SetStats(kFALSE);
	remu_s1->Draw();
	remu_s3->Draw("same");
    
	TLegend *leg_rmn = new TLegend(.6, .7, 0.9, .898);    
	leg_rmn->SetHeader("Samples","C");
	leg_rmn->SetBorderSize(0);    
	leg_rmn->SetLineColor(1);    
	gStyle->SetFillColor(0);    
	gStyle->SetCanvasColor(10);    
	leg_rmn->AddEntry(remu_s1, Form("%s",S1), "P");    
	leg_rmn->AddEntry(remu_s3, Form("%s",S3), "P");        
	leg_rmn->Draw();    
	can_rmn->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_RMn.pdf",date));
	//can_rmn->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_RMn.png",date));
	
	//dR of Reco muons 
	TH1F *remudr_s1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/RM_dR",S1));
	TH1F *remudr_s3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/RM_dR",S3));
	
	remudr_s1->SetLineColor(kBlack); 
	remudr_s3->SetLineColor(kBlue); 
    
	remudr_s1->SetMarkerColor(kBlack);
	remudr_s3->SetMarkerColor(kBlue); 
	
	TCanvas *can_rmdr = new TCanvas("can_rmdr","",800,600);
	remudr_s3->SetTitle("#Delta R of Reco Muons; #Delta R; Entries");
	remudr_s3->SetStats(kFALSE);
	remudr_s3->Draw();
	remudr_s1->Draw("same");
    
	TLegend *leg_rmdr = new TLegend(.6, .7, 0.9, .898);    
	leg_rmdr->SetHeader("Samples","C");
	leg_rmdr->SetBorderSize(0);    
	leg_rmdr->SetLineColor(1);    
	gStyle->SetFillColor(0);    
	gStyle->SetCanvasColor(10);    
	leg_rmdr->AddEntry(remudr_s1, Form("%s",S1), "P");    
	leg_rmdr->AddEntry(remudr_s3, Form("%s",S3), "P");        
	leg_rmdr->Draw();    
	can_rmdr->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_RMdr.pdf",date));
	//can_rmdr->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_RMdr.png",date));
	
	//pT of Reco muons 
	TH1F *remupT_s1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/RM_pT",S1));
	TH1F *remupT_s3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/RM_pT",S3));
	
	remupT_s1->SetLineColor(kBlack); 
	remupT_s3->SetLineColor(kBlue); 
    
	remupT_s1->SetMarkerColor(kBlack);
	remupT_s3->SetMarkerColor(kBlue); 
	
	TCanvas *can_rmpT = new TCanvas("can_rmpT","",800,600);
	remupT_s3->SetTitle("p_{T} of Reco Muons; p_{T} [GeV]; Entries");
	remupT_s3->SetStats(kFALSE);
	remupT_s3->Draw();
	remupT_s1->Draw("same");
    
	TLegend *leg_rmpT = new TLegend(.6, .7, 0.9, .898);    
	leg_rmpT->SetHeader("Samples","C");
	leg_rmpT->SetBorderSize(0);    
	leg_rmpT->SetLineColor(1);    
	gStyle->SetFillColor(0);    
	gStyle->SetCanvasColor(10);    
	leg_rmpT->AddEntry(remupT_s1, Form("%s",S1), "P");    
	leg_rmpT->AddEntry(remupT_s3, Form("%s",S3), "P");        
	leg_rmpT->Draw();    
	can_rmpT->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_RMpT.pdf",date));
	//can_rmpT->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_RMpT.png",date));
	
	//min dR of muon and TO 
	TH1F *mdrRMTO_s1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/min_dR_RMTO",S1));
	TH1F *mdrRMTO_s3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/min_dR_RMTO",S3));
	
	mdrRMTO_s1->SetLineColor(kBlack); 
	mdrRMTO_s3->SetLineColor(kBlue); 
    
	mdrRMTO_s1->SetMarkerColor(kBlack);
	mdrRMTO_s3->SetMarkerColor(kBlue); 
	
	TCanvas *can_mdrrmto = new TCanvas("can_mdrrmto","",800,600);
	mdrRMTO_s3->SetTitle("Min dR of muon and TO ; #Delta R; Entries");
	mdrRMTO_s3->SetStats(kFALSE);
	mdrRMTO_s3->Draw();
	mdrRMTO_s1->Draw("same");
    
	TLegend *leg_mdrrmto = new TLegend(.6, .7, 0.9, .898);    
	leg_mdrrmto->SetHeader("Samples","C");
	leg_mdrrmto->SetBorderSize(0);    
	leg_mdrrmto->SetLineColor(1);    
	gStyle->SetFillColor(0);    
	gStyle->SetCanvasColor(10);    
	leg_mdrrmto->AddEntry(mdrRMTO_s1, Form("%s",S1), "P");    
	leg_mdrrmto->AddEntry(mdrRMTO_s3, Form("%s",S3), "P");        
	leg_mdrrmto->Draw();    
	can_mdrrmto->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_minRMTO.pdf",date));
	//can_mdrrmto->SaveAs(Form("../outputs/plots/modules/ch2mu2eTrEff/eff_%s_minRMTO.png",date));
}
