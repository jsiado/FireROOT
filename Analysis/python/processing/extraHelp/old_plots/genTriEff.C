/*#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TH1F.h>
#include <TMath.h>
#include "Math/LorentzVector.h"
#include "TLorentzVector.h"
#include "TVector.h"
#include "TVector2.h"
#include "TVector3.h"
#include <vector>
#include <fstream>
#include <iostream>
#include "TClonesArray.h"
#include "TObject.h"
#include "TGraph.h"
#include "TGraphErrors.h"
#include "TStyle.h"
#include "TF1.h"
#include "TColor.h"
#include <stdio.h>
#include <TCanvas.h>
#include <TRandom.h>
#include <math.h>
#include <TF1Convolution.h>
#include <TStopwatch.h>
#include "TH1.h"
#include "TRandom3.h"
#include "TVirtualFitter.h"
#include "TPaveLabel.h"
#include <string>*/
 
//run as root -l genTriEff.C

void genTriEff()
{
    TFile* file_1 = TFile::Open("../outputs/rootfiles/modules/genTriggerEfficiency.root");
    
  // samples
    char S1[50] = "mXX-1000_mA-5_lxy-300", S2[50] = "mXX-100_mA-5_lxy-0p3", S3[50] = "mXX-500_mA-0p25_lxy-300", S4[50] = "mXX-1000_mA-5_lxy-30", S5[50] = "mXX-500_mA-1p2_lxy-30", 
    S6[50] = "mXX-100_mA-0p25_lxy-300", S7[50]= "mXX-1000_mA-5_lxy-150", S8[50] = "mXX-1000_mA-5_lxy-3", S9[50] = "mXX-1000_mA-5_lxy-0p3";
  //triggers
    char T1[50] = "DoubleL2Mu23NoVtx_2Cha", T2[50] = "DoubleL2Mu23NoVtx_2Cha_NoL2Matched", T3[50]= "DoubleL2Mu23NoVtx_2Cha_CosmicSeed", 
      T4[50] = "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched", T5[50] = "DoubleL2Mu25NoVtx_2Cha_Eta2p4", T6[50] = "DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4";
    
    
    //sample 1 mXX-1000_mA-5_lxy-300
    TH1F *alldimu_1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S1));
    TH1F *dimu_s1t1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_1",S1));
    TH1F *eff_s1t1 = (TH1F*) dimu_s1t1->Clone();
    TH1F *dimu_s1t2 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_2",S1));
    TH1F *eff_s1t2 = (TH1F*) dimu_s1t2->Clone();
    TH1F *dimu_s1t3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_3",S1));
    TH1F *eff_s1t3 = (TH1F*) dimu_s1t3->Clone();
    TH1F *dimu_s1t4 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_4",S1));
    TH1F *eff_s1t4 = (TH1F*) dimu_s1t4->Clone();
    TH1F *dimu_s1t5 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_5",S1));
    TH1F *eff_s1t5 = (TH1F*) dimu_s1t5->Clone();
    TH1F *dimu_s1t6 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_6",S1));
    TH1F *eff_s1t6 = (TH1F*) dimu_s1t6->Clone();
    
	/*TCanvas *cs1 = new TCanvas("cs1","mXX-1000_mA-5_lxy-300",1800,800);
    cs1->Divide(3,2);
    cs1->cd(1);
    eff_s1t1->Divide(alldimu_1);
    eff_s1t1->SetLineColor(kBlack);
    eff_s1t1->SetMarkerColor(kBlack);
    eff_s1t1->SetMarkerStyle(20);
    eff_s1t1->SetStats(kFALSE);
    eff_s1t1->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S1,T1));
    eff_s1t1->Draw();
    cs1->cd(2);
    eff_s1t2->Divide(alldimu_1);
    eff_s1t2->SetLineColor(kBlue);
    eff_s1t2->SetMarkerColor(kBlue);
    eff_s1t2->SetMarkerStyle(21);
    eff_s1t2->SetStats(kFALSE);
    eff_s1t2 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S1,T2));
    eff_s1t2->Draw();
    cs1->cd(3);
    eff_s1t3->Divide(alldimu_1);
    eff_s1t3->SetLineColor(kGreen);
    eff_s1t3->SetMarkerColor(kGreen);
    eff_s1t3->SetMarkerStyle(22);
    eff_s1t3->SetStats(kFALSE);
    eff_s1t3 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S1,T3));
    eff_s1t3->Draw();
    cs1->cd(4);
    eff_s1t4->Divide(alldimu_1);
    eff_s1t4->SetLineColor(kRed);
    eff_s1t4->SetMarkerColor(kRed);
    eff_s1t4->SetMarkerStyle(23);
    eff_s1t4->SetStats(kFALSE);
    eff_s1t4 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S1,T4));
    eff_s1t4->Draw();    
    cs1->cd(5);
    eff_s1t5->Divide(alldimu_1);
    eff_s1t5->SetLineColor(kCyan);
    eff_s1t5->SetMarkerColor(kCyan);
    eff_s1t5->SetMarkerStyle(24);
    eff_s1t5->SetStats(kFALSE);
    eff_s1t5->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S1,T5));
    eff_s1t5->Draw();
    cs1->cd(6);
    eff_s1t6->Divide(alldimu_1);
    eff_s1t6->SetLineColor(kMagenta);
    eff_s1t6->SetMarkerColor(kMagenta);
    eff_s1t6->SetStats(kFALSE);
    eff_s1t6->SetMarkerStyle(25);
    eff_s1t6->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S1,T6));
    eff_s1t6->Draw();
    cs1 -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/central_%s_can.pdf",S1));
    
    TCanvas* cans1tall = new TCanvas("cans1tall");
    eff_s1t1 -> SetTitle(Form("Efficiency: %s; #Delta R; Efficiency",S1));
    eff_s1t1 -> SetStats(kFALSE);
    eff_s1t1 -> Draw();
    eff_s1t1->SetAxisRange(0.0,1.0,"Y");
    eff_s1t2 -> Draw("same");
    eff_s1t3 -> Draw("same");
    eff_s1t4 -> Draw("same");
    eff_s1t5 -> Draw("same");
    eff_s1t6 -> Draw("same");
    TLegend *legs1tall = new TLegend(.6, .7, 0.9, .898);
    legs1tall->SetHeader("Triggers","C");
    legs1tall->SetBorderSize(0);
    legs1tall->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    legs1tall->AddEntry(eff_s1t1, Form("%s",T1), "P");
    legs1tall->AddEntry(eff_s1t2, Form("%s",T2), "P");
    legs1tall->AddEntry(eff_s1t3, Form("%s",T3), "P");
    legs1tall->AddEntry(eff_s1t4, Form("%s",T4), "P");
    legs1tall->AddEntry(eff_s1t5, Form("%s",T5), "P");
    legs1tall->AddEntry(eff_s1t6, Form("%s",T6), "P");
    legs1tall->Draw();
    cans1tall -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/central_%s_all.pdf",S1));*/
    
    //second sample mXX-100_mA-5_lxy-0p3    
    TH1F *alldimu_2 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S2));
    TH1F *dimu_s2t1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_1",S2));
    TH1F *eff_s2t1 = (TH1F*) dimu_s2t1->Clone();
    TH1F *dimu_s2t2 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_2",S2));
    TH1F *eff_s2t2 = (TH1F*) dimu_s2t2->Clone();
    TH1F *dimu_s2t3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_3",S2));
    TH1F *eff_s2t3 = (TH1F*) dimu_s2t3->Clone();
    TH1F *dimu_s2t4 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_4",S2));
    TH1F *eff_s2t4 = (TH1F*) dimu_s2t4->Clone();
    TH1F *dimu_s2t5 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_5",S2));
    TH1F *eff_s2t5 = (TH1F*) dimu_s2t5->Clone();
    TH1F *dimu_s2t6 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_6",S2));
    TH1F *eff_s2t6 = (TH1F*) dimu_s2t6->Clone();
    
    /*TCanvas *cs2 = new TCanvas("cs2","mXX-100_mA-5_lxy-0p3",1800,800);
    cs2->Divide(3,2);
    cs2->cd(1);
    eff_s2t1->Divide(alldimu_2);
    eff_s2t1->SetLineColor(kBlack);
    eff_s2t1->SetMarkerColor(kBlack);
    eff_s2t1->SetMarkerStyle(20);
    eff_s2t1->SetStats(kFALSE);
    eff_s2t1->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S2,T1));
    eff_s2t1->Draw();
    cs2->cd(2);
    eff_s2t2->Divide(alldimu_2);
    eff_s2t2->SetLineColor(kBlue);
    eff_s2t2->SetMarkerColor(kBlue);
    eff_s2t2->SetMarkerStyle(21);
    eff_s2t2->SetStats(kFALSE);
    eff_s2t2 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S2,T2));
    eff_s2t2->Draw();
    cs2->cd(3);
    eff_s2t3->Divide(alldimu_2);
    eff_s2t3->SetLineColor(kGreen);
    eff_s2t3->SetMarkerColor(kGreen);
    eff_s2t3->SetMarkerStyle(22);
    eff_s2t3->SetStats(kFALSE);
    eff_s2t3 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S2,T3));
    eff_s2t3->Draw();
    cs2->cd(4);
    eff_s2t4->Divide(alldimu_2);
    eff_s2t4->SetLineColor(kRed);
    eff_s2t4->SetMarkerColor(kRed);
    eff_s2t4->SetMarkerStyle(23);
    eff_s2t4->SetStats(kFALSE);
    eff_s2t4 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S2,T4));
    eff_s2t4->Draw();
    cs2->cd(5);
    eff_s2t5->Divide(alldimu_2);
    eff_s2t5->SetLineColor(kCyan);
    eff_s2t5->SetMarkerColor(kCyan);
    eff_s2t5->SetMarkerStyle(24);
    eff_s2t5->SetStats(kFALSE);
    eff_s2t5->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S2,T5));
    eff_s2t5->Draw();
    cs2->cd(6);
    eff_s2t6->Divide(alldimu_2);
    eff_s2t6->SetLineColor(kMagenta);
    eff_s2t6->SetMarkerColor(kMagenta);
    eff_s2t6->SetStats(kFALSE);
    eff_s2t6->SetMarkerStyle(25);
    eff_s2t6->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S2,T6));
    eff_s2t6->Draw();
    cs2 -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/central_%s_can.pdf",S2));

    TCanvas* cans2tall = new TCanvas("cans2tall");
    eff_s2t1 -> SetTitle(Form("Efficiency: %s; #Delta R; Efficiency",S2));
    eff_s2t1 -> SetStats(kFALSE);
    eff_s2t1 -> Draw();
    eff_s2t1->SetAxisRange(0.0,1.0,"Y");
    eff_s2t2 -> Draw("same");
    eff_s2t3 -> Draw("same");
    eff_s2t4 -> Draw("same");
    eff_s2t5 -> Draw("same");
    eff_s2t6 -> Draw("same");
    TLegend *legs2tall = new TLegend(.6, .7, 0.9, .898);
    legs2tall->SetHeader("Triggers","C");
    legs2tall->SetBorderSize(0);
    legs2tall->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    legs2tall->AddEntry(eff_s2t1, Form("%s",T1), "P");
    legs2tall->AddEntry(eff_s2t2, Form("%s",T2), "P");
    legs2tall->AddEntry(eff_s2t3, Form("%s",T3), "P");
    legs2tall->AddEntry(eff_s2t4, Form("%s",T4), "P");
    legs2tall->AddEntry(eff_s2t5, Form("%s",T5), "P");
    legs2tall->AddEntry(eff_s2t6, Form("%s",T6), "P");
    legs2tall->Draw();
    cans2tall -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/central_%s_all.pdf",S2));*/
    
  //Third sample mXX-500_mA-0p25_lxy-300
    TH1F *alldimu_3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S3));
    TH1F *dimu_s3t1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_1",S3));
    TH1F *eff_s3t1 = (TH1F*) dimu_s3t1->Clone();
    TH1F *dimu_s3t2 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_2",S3));
    TH1F *eff_s3t2 = (TH1F*) dimu_s3t2->Clone();
    TH1F *dimu_s3t3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_3",S3));
    TH1F *eff_s3t3 = (TH1F*) dimu_s3t3->Clone();
    TH1F *dimu_s3t4 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_4",S3));
    TH1F *eff_s3t4 = (TH1F*) dimu_s3t4->Clone();
    TH1F *dimu_s3t5 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_5",S3));
    TH1F *eff_s3t5 = (TH1F*) dimu_s3t5->Clone();
    TH1F *dimu_s3t6 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_6",S3));
    TH1F *eff_s3t6 = (TH1F*) dimu_s3t6->Clone();
    
   	/*TCanvas *cs3 = new TCanvas("cs3","mXX-500_mA-0p25_lxy-300",1800,800);
    cs3->Divide(3,2);
    cs3->cd(1);
    eff_s3t1->Divide(alldimu_3);
    eff_s3t1->SetLineColor(kBlack);
    eff_s3t1->SetMarkerColor(kBlack);
    eff_s3t1->SetMarkerStyle(20);
    eff_s3t1->SetStats(kFALSE);
    eff_s3t1->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S3,T1));
    eff_s3t1->Draw();
    cs3->cd(2);
    eff_s3t2->Divide(alldimu_3);
    eff_s3t2->SetLineColor(kBlue);
    eff_s3t2->SetMarkerColor(kBlue);
    eff_s3t2->SetMarkerStyle(21);
    eff_s3t2->SetStats(kFALSE);
    eff_s3t2 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S3,T2));
    eff_s3t2->Draw();
    cs3->cd(3);
    eff_s3t3->Divide(alldimu_3);
    eff_s3t3->SetLineColor(kGreen);
    eff_s3t3->SetMarkerColor(kGreen);
    eff_s3t3->SetMarkerStyle(22);
    eff_s3t3->SetStats(kFALSE);
    eff_s3t3 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S3,T3));
    eff_s3t3->Draw();
    cs3->cd(4);
    eff_s3t4->Divide(alldimu_3);
    eff_s3t4->SetLineColor(kRed);
    eff_s3t4->SetMarkerColor(kRed);
    eff_s3t4->SetMarkerStyle(23);
    eff_s3t4->SetStats(kFALSE);
    eff_s3t4 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S3,T4));
    eff_s3t4->Draw();
    cs3->cd(5);
    eff_s3t5->Divide(alldimu_3);
    eff_s3t5->SetLineColor(kCyan);
    eff_s3t5->SetMarkerColor(kCyan);
    eff_s3t5->SetMarkerStyle(24);
    eff_s3t5->SetStats(kFALSE);
    eff_s3t5->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S3,T5));
    eff_s3t5->Draw();
    cs3->cd(6);
    eff_s3t6->Divide(alldimu_3);
    eff_s3t6->SetLineColor(kMagenta);
    eff_s3t6->SetMarkerColor(kMagenta);
    eff_s3t6->SetStats(kFALSE);
    eff_s3t6->SetMarkerStyle(25);
    eff_s3t6->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S3,T6));
    eff_s3t6->Draw();
    cs3 -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/central_%s_can.pdf",S3));
    
    TCanvas* cans3tall = new TCanvas("cans3tall");
    eff_s3t1 -> SetTitle(Form("Efficiency: %s; #Delta R; Efficiency",S3));
    eff_s3t1 -> SetStats(kFALSE);
    eff_s3t1 -> Draw();
    eff_s3t1->SetAxisRange(0.0,1.0,"Y");
    eff_s3t2 -> Draw("same");
    eff_s3t3 -> Draw("same");
    eff_s3t4 -> Draw("same");
    eff_s3t5 -> Draw("same");
    eff_s3t6 -> Draw("same");
    TLegend *legs3tall = new TLegend(.6, .7, 0.9, .898);
    legs3tall->SetHeader("Triggers","C");
    legs3tall->SetBorderSize(0);
    legs3tall->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    legs3tall->AddEntry(eff_s3t1, Form("%s",T1), "P");
    legs3tall->AddEntry(eff_s3t2, Form("%s",T2), "P");
    legs3tall->AddEntry(eff_s3t3, Form("%s",T3), "P");
    legs3tall->AddEntry(eff_s3t4, Form("%s",T4), "P");
    legs3tall->AddEntry(eff_s3t5, Form("%s",T5), "P");
    legs3tall->AddEntry(eff_s3t6, Form("%s",T6), "P");
    legs3tall->Draw();
    cans3tall -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/central_%s_all.pdf",S3));*/
    
    //sample 4 mXX-1000_mA-5_lxy-30
    TH1F *alldimu_4 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S4));
    TH1F *dimu_s4t1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_1",S4));
    TH1F *eff_s4t1 = (TH1F*) dimu_s4t1->Clone();
    TH1F *dimu_s4t2 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_2",S4));
    TH1F *eff_s4t2 = (TH1F*) dimu_s4t2->Clone();
    TH1F *dimu_s4t3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_3",S4));
    TH1F *eff_s4t3 = (TH1F*) dimu_s4t3->Clone();
    TH1F *dimu_s4t4 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_4",S4));
    TH1F *eff_s4t4 = (TH1F*) dimu_s4t4->Clone();
    TH1F *dimu_s4t5 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_5",S4));
    TH1F *eff_s4t5 = (TH1F*) dimu_s4t5->Clone();
    TH1F *dimu_s4t6 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_6",S4));
    TH1F *eff_s4t6 = (TH1F*) dimu_s4t6->Clone();
    
    /*TCanvas *cs4 = new TCanvas("cs4","mXX-1000_mA-5_lxy-30",1800,800);
    cs4->Divide(3,2);
    cs4->cd(1);
    eff_s4t1->Divide(alldimu_4);
    eff_s4t1->SetLineColor(kBlack);
    eff_s4t1->SetMarkerColor(kBlack);
    eff_s4t1->SetMarkerStyle(20);
    eff_s4t1->SetStats(kFALSE);
    eff_s4t1->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S4,T1));
    eff_s4t1->Draw();
    cs4->cd(2);
    eff_s4t2->Divide(alldimu_4);
    eff_s4t2->SetLineColor(kBlue);
    eff_s4t2->SetMarkerColor(kBlue);
    eff_s4t2->SetMarkerStyle(21);
    eff_s4t2->SetStats(kFALSE);
    eff_s4t2 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S4,T2));
    eff_s4t2->Draw();
    cs4->cd(3);
    eff_s4t3->Divide(alldimu_4);
    eff_s4t3->SetLineColor(kGreen);
    eff_s4t3->SetMarkerColor(kGreen);
    eff_s4t3->SetMarkerStyle(22);
    eff_s4t3->SetStats(kFALSE);
    eff_s4t3 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S4,T3));
    eff_s4t3->Draw();
    cs4->cd(4);
    eff_s4t4->Divide(alldimu_4);
    eff_s4t4->SetLineColor(kRed);
    eff_s4t4->SetMarkerColor(kRed);
    eff_s4t4->SetMarkerStyle(23);
    eff_s4t4->SetStats(kFALSE);
    eff_s4t4 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S4,T4));
    eff_s4t4->Draw();
    cs4->cd(5);
    eff_s4t5->Divide(alldimu_4);
    eff_s4t5->SetLineColor(kCyan);
    eff_s4t5->SetMarkerColor(kCyan);
    eff_s4t5->SetMarkerStyle(24);
    eff_s4t5->SetStats(kFALSE);
    eff_s4t5->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S4,T5));
    eff_s4t5->Draw();
    cs4->cd(6);
    eff_s4t6->Divide(alldimu_4);
    eff_s4t6->SetLineColor(kMagenta);
    eff_s4t6->SetMarkerColor(kMagenta);
    eff_s4t6->SetStats(kFALSE);
    eff_s4t6->SetMarkerStyle(25);
    eff_s4t6->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S4,T6));
    eff_s4t6->Draw();
    cs4 -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/central_%s_can.pdf",S4));
    
    TCanvas* cans4tall = new TCanvas("cans4tall");
    eff_s4t1 -> SetTitle(Form("Efficiency: %s; #Delta R; Efficiency",S4));
    eff_s4t1 -> SetStats(kFALSE);
    eff_s4t1 -> Draw();
    eff_s4t1->SetAxisRange(0.0,1.0,"Y");
    eff_s4t2 -> Draw("same");
    eff_s4t3 -> Draw("same");
    eff_s4t4 -> Draw("same");
    eff_s4t5 -> Draw("same");
    eff_s4t6 -> Draw("same");
    TLegend *legs4tall = new TLegend(.6, .7, 0.9, .898);
    legs4tall->SetHeader("Triggers","C");
    legs4tall->SetBorderSize(0);
    legs4tall->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    legs4tall->AddEntry(eff_s4t1, Form("%s",T1), "P");
    legs4tall->AddEntry(eff_s4t2, Form("%s",T2), "P");
    legs4tall->AddEntry(eff_s4t3, Form("%s",T3), "P");
    legs4tall->AddEntry(eff_s4t4, Form("%s",T4), "P");
    legs4tall->AddEntry(eff_s4t5, Form("%s",T5), "P");
    legs4tall->AddEntry(eff_s4t6, Form("%s",T6), "P");
    legs4tall->Draw();
    cans4tall -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/central_%s_all.pdf",S4));*/
    
    //sample 5 mXX-500_mA-1p2_lxy-30 
    TH1F *alldimu_5 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S5));
    TH1F *dimu_s5t1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_1",S5));    
    TH1F *eff_s5t1 = (TH1F*) dimu_s5t1->Clone();
    TH1F *dimu_s5t2 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_2",S5));
    TH1F *eff_s5t2 = (TH1F*) dimu_s5t2->Clone();
    TH1F *dimu_s5t3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_3",S5));
    TH1F *eff_s5t3 = (TH1F*) dimu_s5t3->Clone();
    TH1F *dimu_s5t4 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_4",S5));
    TH1F *eff_s5t4 = (TH1F*) dimu_s5t4->Clone();
    TH1F *dimu_s5t5 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_5",S5));
    TH1F *eff_s5t5 = (TH1F*) dimu_s5t5->Clone();
    TH1F *dimu_s5t6 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_6",S5));
    TH1F *eff_s5t6 = (TH1F*) dimu_s5t6->Clone();
    
    /*TCanvas *cs5 = new TCanvas("cs5","mXX-500_mA-1p2_lxy-30",1800,800);
    cs5->Divide(3,2);
    cs5->cd(1);
    eff_s5t1->Divide(alldimu_5);
    eff_s5t1->SetLineColor(kBlack);
    eff_s5t1->SetMarkerColor(kBlack);
    eff_s5t1->SetMarkerStyle(20);
    eff_s5t1->SetStats(kFALSE);
    eff_s5t1->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S5,T1));
    eff_s5t1->Draw();
    cs5->cd(2);
    eff_s5t2->Divide(alldimu_5);
    eff_s5t2->SetLineColor(kBlue);
    eff_s5t2->SetMarkerColor(kBlue);
    eff_s5t2->SetMarkerStyle(21);
    eff_s5t2->SetStats(kFALSE);
    eff_s5t2 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S5,T2));
    eff_s5t2->Draw();
    cs5->cd(3);
    eff_s5t3->Divide(alldimu_5);
    eff_s5t3->SetLineColor(kGreen);
    eff_s5t3->SetMarkerColor(kGreen);
    eff_s5t3->SetMarkerStyle(22);
    eff_s5t3->SetStats(kFALSE);
    eff_s5t3 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S5,T3));
    eff_s5t3->Draw();
    cs5->cd(4);
    eff_s5t4->Divide(alldimu_5);
    eff_s5t4->SetLineColor(kRed);
    eff_s5t4->SetMarkerColor(kRed);
    eff_s5t4->SetMarkerStyle(23);
    eff_s5t4->SetStats(kFALSE);
    eff_s5t4 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S5,T4));
    eff_s5t4->Draw();
    cs5->cd(5);
    eff_s5t5->Divide(alldimu_5);
    eff_s5t5->SetLineColor(kCyan);
    eff_s5t5->SetMarkerColor(kCyan);
    eff_s5t5->SetMarkerStyle(24);
    eff_s5t5->SetStats(kFALSE);
    eff_s5t5->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S5,T5));
    eff_s5t5->Draw();
    cs5->cd(6);
    eff_s5t6->Divide(alldimu_5);
    eff_s5t6->SetLineColor(kMagenta);
    eff_s5t6->SetMarkerColor(kMagenta);
    eff_s5t6->SetStats(kFALSE);
    eff_s5t6->SetMarkerStyle(25);
    eff_s5t6->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S5,T6));
    eff_s5t6->Draw();
    cs5 -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/central_%s_can.pdf",S5));
    
    TCanvas* cans5tall = new TCanvas("cans5tall");
    eff_s5t1 -> SetTitle(Form("Efficiency: %s; #Delta R; Efficiency",S5));
    eff_s5t1 -> SetStats(kFALSE);
    eff_s5t1 -> Draw();
    eff_s5t1->SetAxisRange(0.0,1.0,"Y");
    eff_s5t2 -> Draw("same");
    eff_s5t3 -> Draw("same");
    eff_s5t4 -> Draw("same");
    eff_s5t5 -> Draw("same");
    eff_s5t6 -> Draw("same");
    TLegend *legs5tall = new TLegend(.6, .7, 0.9, .898);
    legs5tall->SetHeader("Triggers","C");
    legs5tall->SetBorderSize(0);
    legs5tall->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    legs5tall->AddEntry(eff_s5t1, Form("%s",T1), "P");
    legs5tall->AddEntry(eff_s5t2, Form("%s",T2), "P");
    legs5tall->AddEntry(eff_s5t3, Form("%s",T3), "P");
    legs5tall->AddEntry(eff_s5t4, Form("%s",T4), "P");
    legs5tall->AddEntry(eff_s5t5, Form("%s",T5), "P");
    legs5tall->AddEntry(eff_s5t6, Form("%s",T6), "P");
    legs5tall->Draw();
    cans5tall -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/central_%s_all.pdf",S5));*/
    
    //sample 6 mXX-100_mA-0p25_lxy-300 
    TH1F *alldimu_6 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S6));
    TH1F *dimu_s6t1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_1",S6));
    TH1F *eff_s6t1 = (TH1F*) dimu_s6t1->Clone();
    TH1F *dimu_s6t2 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_2",S6));
    TH1F *eff_s6t2 = (TH1F*) dimu_s6t2->Clone();
    TH1F *dimu_s6t3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_3",S6));
    TH1F *eff_s6t3 = (TH1F*) dimu_s6t3->Clone();
    TH1F *dimu_s6t4 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_4",S6));
    TH1F *eff_s6t4 = (TH1F*) dimu_s6t4->Clone();
    TH1F *dimu_s6t5 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_5",S6));
    TH1F *eff_s6t5 = (TH1F*) dimu_s6t5->Clone();
    TH1F *dimu_s6t6 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_6",S6));
    TH1F *eff_s6t6 = (TH1F*) dimu_s6t6->Clone();
    
    /*TCanvas *cs6 = new TCanvas("cs6","mXX-100_mA-0p25_lxy-300",1800,800);
    cs6->Divide(3,2);
    cs6->cd(1);
    eff_s6t1->Divide(alldimu_6);
    eff_s6t1->SetLineColor(kBlack);
    eff_s6t1->SetMarkerColor(kBlack);
    eff_s6t1->SetMarkerStyle(20);
    eff_s6t1->SetStats(kFALSE);
    eff_s6t1->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S6,T1));
    eff_s6t1->Draw();
    cs6->cd(2);
    eff_s6t2->Divide(alldimu_6);
    eff_s6t2->SetLineColor(kBlue);
    eff_s6t2->SetMarkerColor(kBlue);
    eff_s6t2->SetMarkerStyle(21);
    eff_s6t2->SetStats(kFALSE);
    eff_s6t2 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S6,T2));
    eff_s6t2->Draw();
    cs6->cd(3);
    eff_s6t3->Divide(alldimu_6);
    eff_s6t3->SetLineColor(kGreen);
    eff_s6t3->SetMarkerColor(kGreen);
    eff_s6t3->SetMarkerStyle(22);
    eff_s6t3->SetStats(kFALSE);
    eff_s6t3 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S6,T3));
    eff_s6t3->Draw();
    cs6->cd(4);
    eff_s6t4->Divide(alldimu_6);
    eff_s6t4->SetLineColor(kRed);
    eff_s6t4->SetMarkerColor(kRed);
    eff_s6t4->SetMarkerStyle(23);
    eff_s6t4->SetStats(kFALSE);
    eff_s6t4 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S6,T4));
    eff_s6t4->Draw();
    cs6->cd(5);
    eff_s6t5->Divide(alldimu_6);
    eff_s6t5->SetLineColor(kCyan);
    eff_s6t5->SetMarkerColor(kCyan);
    eff_s6t5->SetMarkerStyle(24);
    eff_s6t5->SetStats(kFALSE);
    eff_s6t5->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S6,T5));
    eff_s6t5->Draw();
    cs6->cd(6);
    eff_s6t6->Divide(alldimu_6);
    eff_s6t6->SetLineColor(kMagenta);
    eff_s6t6->SetMarkerColor(kMagenta);
    eff_s6t6->SetStats(kFALSE);
    eff_s6t6->SetMarkerStyle(25);
    eff_s6t6->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S6,T6));
    eff_s6t6->Draw();
    cs6 -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/central_%s_can.pdf",S6));
    
    TCanvas* cans6tall = new TCanvas("cans6tall");
    eff_s6t1 -> SetTitle(Form("Efficiency: %s; #Delta R; Efficiency",S6));
    eff_s6t1 -> SetStats(kFALSE);
    eff_s6t1 -> Draw();
    eff_s6t1->SetAxisRange(0.0,1.0,"Y");
    eff_s6t2 -> Draw("same");
    eff_s6t3 -> Draw("same");
    eff_s6t4 -> Draw("same");
    eff_s6t5 -> Draw("same");
    eff_s6t6 -> Draw("same");
    TLegend *legs6tall = new TLegend(.6, .7, .9, .898);
    legs6tall->SetHeader("Triggers","C");
    legs6tall->SetBorderSize(0);
    legs6tall->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    legs6tall->AddEntry(eff_s6t1, Form("%s", T1), "P");
    legs6tall->AddEntry(eff_s6t2, Form("%s", T2), "P");
    legs6tall->AddEntry(eff_s6t3, Form("%s", T3), "P");
    legs6tall->AddEntry(eff_s6t4, Form("%s", T4), "P");
    legs6tall->AddEntry(eff_s6t5, Form("%s", T5), "P");
    legs6tall->AddEntry(eff_s6t6, Form("%s", T6), "P");
    legs6tall->Draw();
    cans6tall -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/central_%s_all.pdf",S6));*/
    
    //sample 7. mxx_1000-mA_5-Lxy_150
    TH1F *alldimu_7 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S7));
    TH1F *dimu_s7t1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_1",S7));
    TH1F *eff_s7t1 = (TH1F*) dimu_s7t1->Clone();
    TH1F *dimu_s7t2 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_2",S7));
    TH1F *eff_s7t2 = (TH1F*) dimu_s7t2->Clone();
    TH1F *dimu_s7t3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_3",S7));
    TH1F *eff_s7t3 = (TH1F*) dimu_s7t3->Clone();
    TH1F *dimu_s7t4 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_4",S7));
    TH1F *eff_s7t4 = (TH1F*) dimu_s7t4->Clone();
    TH1F *dimu_s7t5 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_5",S7));
    TH1F *eff_s7t5 = (TH1F*) dimu_s7t5->Clone();
    TH1F *dimu_s7t6 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_6",S7));
    TH1F *eff_s7t6 = (TH1F*) dimu_s7t6->Clone();
    
    eff_s7t1->Divide(alldimu_7);
	eff_s7t2->Divide(alldimu_7);
	eff_s7t3->Divide(alldimu_7);
	eff_s7t4->Divide(alldimu_7);
	eff_s7t5->Divide(alldimu_7);
	eff_s7t6->Divide(alldimu_7);

    /*TCanvas *cs7 = new TCanvas("cs7","mXX-1000_mA-5_lxy-150",1800,800);
    cs7->Divide(3,2);
    cs7->cd(1);
    eff_s7t1->Divide(alldimu_7);
    eff_s7t1->SetLineColor(kBlack);
    eff_s7t1->SetMarkerColor(kBlack);
    eff_s7t1->SetMarkerStyle(20);
    eff_s7t1->SetStats(kFALSE);
    eff_s7t1->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S7,T1));
    eff_s7t1->Draw();
    cs7->cd(2);
    eff_s7t2->Divide(alldimu_7);
    eff_s7t2->SetLineColor(kBlue);
    eff_s7t2->SetMarkerColor(kBlue);
    eff_s7t2->SetMarkerStyle(21);
    eff_s7t2->SetStats(kFALSE);
    eff_s7t2 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S7,T2));
    eff_s7t2->Draw();
    cs7->cd(3);
    eff_s7t3->Divide(alldimu_7);
    eff_s7t3->SetLineColor(kGreen);
    eff_s7t3->SetMarkerColor(kGreen);
    eff_s7t3->SetMarkerStyle(22);
    eff_s7t3->SetStats(kFALSE);
    eff_s7t3 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S7,T3));
    eff_s7t3->Draw();
    cs7->cd(4);
    eff_s7t4->Divide(alldimu_7);
    eff_s7t4->SetLineColor(kRed);
    eff_s7t4->SetMarkerColor(kRed);
    eff_s7t4->SetMarkerStyle(23);
    eff_s7t4->SetStats(kFALSE);
    eff_s7t4 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S7,T4));
    eff_s7t4->Draw();    
    cs7->cd(5);
    eff_s7t5->Divide(alldimu_7);
    eff_s7t5->SetLineColor(kCyan);
    eff_s7t5->SetMarkerColor(kCyan);
    eff_s7t5->SetMarkerStyle(24);
    eff_s7t5->SetStats(kFALSE);
    eff_s7t5->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S7,T5));
    eff_s7t5->Draw();
    cs7->cd(6);
    eff_s7t6->Divide(alldimu_7);
    eff_s7t6->SetLineColor(kMagenta);
    eff_s7t6->SetMarkerColor(kMagenta);
    eff_s7t6->SetStats(kFALSE);
    eff_s7t6->SetMarkerStyle(25);
    eff_s7t6->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S7,T6));
    eff_s7t6->Draw();
    cs7 -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/central_%s_can.pdf",S7));
    
    TCanvas* cans7tall = new TCanvas("cans7tall");
    eff_s7t1 -> SetTitle(Form("Efficiency: %s; #Delta R; Efficiency",S7));
    eff_s7t1 -> SetStats(kFALSE);
    eff_s7t1 -> Draw();
    eff_s7t1->SetAxisRange(0.0,1.0,"Y");
    eff_s7t2 -> Draw("same");
    eff_s7t3 -> Draw("same");
    eff_s7t4 -> Draw("same");
    eff_s7t5 -> Draw("same");
    eff_s7t6 -> Draw("same");
    TLegend *legs7tall = new TLegend(.6, .7, 0.9, .898);
    legs7tall->SetHeader("Triggers","C");
    legs7tall->SetBorderSize(0);
    legs7tall->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    legs7tall->AddEntry(eff_s7t1, Form("%s",T1), "P");
    legs7tall->AddEntry(eff_s7t2, Form("%s",T2), "P");
    legs7tall->AddEntry(eff_s7t3, Form("%s",T3), "P");
    legs7tall->AddEntry(eff_s7t4, Form("%s",T4), "P");
    legs7tall->AddEntry(eff_s7t5, Form("%s",T5), "P");
    legs7tall->AddEntry(eff_s7t6, Form("%s",T6), "P");
    legs7tall->Draw();
    cans7tall -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/central_%s_all.pdf",S7));*/
    
    // Sample 8 mXX-1000_mA-5_lxy-3
    TH1F *alldimu_8 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S8));
    TH1F *dimu_s8t1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_1",S8));
    TH1F *eff_s8t1 = (TH1F*) dimu_s7t1->Clone();
    TH1F *dimu_s8t2 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_2",S8));
    TH1F *eff_s8t2 = (TH1F*) dimu_s7t2->Clone();
    TH1F *dimu_s8t3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_3",S8));
    TH1F *eff_s8t3 = (TH1F*) dimu_s7t3->Clone();
    TH1F *dimu_s8t4 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_4",S8));
    TH1F *eff_s8t4 = (TH1F*) dimu_s7t4->Clone();
    TH1F *dimu_s8t5 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_5",S8));
    TH1F *eff_s8t5 = (TH1F*) dimu_s7t5->Clone();
    TH1F *dimu_s8t6 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_6",S8));
    TH1F *eff_s8t6 = (TH1F*) dimu_s7t6->Clone();
	
	eff_s8t1->Divide(alldimu_8);
	eff_s8t2->Divide(alldimu_8);
	eff_s8t3->Divide(alldimu_8);
	eff_s8t4->Divide(alldimu_8);
	eff_s8t5->Divide(alldimu_8);
	eff_s8t6->Divide(alldimu_8);
	
    /*TCanvas *cs8 = new TCanvas("cs8","mXX-1000_mA-5_lxy-3",1800,800);
    cs8->Divide(3,2);
    
    cs8->cd(1);
    eff_s8t1->SetLineColor(kBlack);
    eff_s8t1->SetMarkerColor(kBlack);
    eff_s8t1->SetMarkerStyle(20);
    eff_s8t1->SetStats(kFALSE);
    eff_s8t1->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S8,T1));
    eff_s8t1->Draw();
    cs8->cd(2);
    eff_s8t2->SetLineColor(kBlue);
    eff_s8t2->SetMarkerColor(kBlue);
    eff_s8t2->SetMarkerStyle(21);
    eff_s8t2->SetStats(kFALSE);
    eff_s8t2 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S8,T2));
    eff_s8t2->Draw();
    cs8->cd(3);
    eff_s8t3->SetLineColor(kGreen);
    eff_s8t3->SetMarkerColor(kGreen);
    eff_s8t3->SetMarkerStyle(22);
    eff_s8t3->SetStats(kFALSE);
    eff_s8t3 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S8,T3));
    eff_s8t3->Draw();
    cs8->cd(4);
    eff_s8t4->SetLineColor(kRed);
    eff_s8t4->SetMarkerColor(kRed);
    eff_s8t4->SetMarkerStyle(23);
    eff_s8t4->SetStats(kFALSE);
    eff_s8t4 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S8,T4));
    eff_s8t4->Draw();    
    cs8->cd(5);
    eff_s8t5->SetLineColor(kCyan);
    eff_s8t5->SetMarkerColor(kCyan);
    eff_s8t5->SetMarkerStyle(24);
    eff_s8t5->SetStats(kFALSE);
    eff_s8t5->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S8,T5));
    eff_s8t5->Draw();
    cs8->cd(6);
    eff_s8t6->SetLineColor(kMagenta);
    eff_s8t6->SetMarkerColor(kMagenta);
    eff_s8t6->SetStats(kFALSE);
    eff_s8t6->SetMarkerStyle(25);
    eff_s8t6->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S8,T6));
    eff_s8t6->Draw();
    cs8 -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/central_%s_can.pdf",S8));
    
    TCanvas* cans8tall = new TCanvas("cans8tall");
    eff_s8t1 -> SetTitle(Form("Efficiency: %s; #Delta R; Efficiency",S8));
    eff_s8t1 -> SetStats(kFALSE);
    eff_s8t1 -> Draw();
    eff_s8t1->SetAxisRange(0.0,1.0,"Y");
    eff_s8t2 -> Draw("same");
    eff_s8t3 -> Draw("same");
    eff_s8t4 -> Draw("same");
    eff_s8t5 -> Draw("same");
    eff_s8t6 -> Draw("same");
    TLegend *legs8tall = new TLegend(.6, .7, 0.9, .898);
    legs8tall->SetHeader("Triggers","C");
    legs8tall->SetBorderSize(0);
    legs8tall->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    legs8tall->AddEntry(eff_s8t1, Form("%s",T1), "P");
    legs8tall->AddEntry(eff_s8t2, Form("%s",T2), "P");
    legs8tall->AddEntry(eff_s8t3, Form("%s",T3), "P");
    legs8tall->AddEntry(eff_s8t4, Form("%s",T4), "P");
    legs8tall->AddEntry(eff_s8t5, Form("%s",T5), "P");
    legs8tall->AddEntry(eff_s8t6, Form("%s",T6), "P");
    legs8tall->Draw();
    cans8tall -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/central_%s_all.pdf",S8));*/
    
    //Sample 9 mXX-1000_mA-5_lxy-0p3
    TH1F *alldimu_9 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S9));
    TH1F *dimu_s9t1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_1",S9));
    TH1F *eff_s9t1 = (TH1F*) dimu_s7t1->Clone();
    TH1F *dimu_s9t2 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_2",S9));
    TH1F *eff_s9t2 = (TH1F*) dimu_s7t2->Clone();
    TH1F *dimu_s9t3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_3",S9));
    TH1F *eff_s9t3 = (TH1F*) dimu_s7t3->Clone();
    TH1F *dimu_s9t4 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_4",S9));
    TH1F *eff_s9t4 = (TH1F*) dimu_s7t4->Clone();
    TH1F *dimu_s9t5 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_5",S9));
    TH1F *eff_s9t5 = (TH1F*) dimu_s7t5->Clone();
    TH1F *dimu_s9t6 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_6",S9));
    TH1F *eff_s9t6 = (TH1F*) dimu_s7t6->Clone();

	eff_s9t1->Divide(alldimu_9);
	eff_s9t2->Divide(alldimu_9);
	eff_s9t3->Divide(alldimu_9);
	eff_s9t4->Divide(alldimu_9);
	eff_s9t5->Divide(alldimu_9);
	eff_s9t6->Divide(alldimu_9);
   	TCanvas *cs9 = new TCanvas("cs9","mXX-1000_mA-5_lxy-0p3",1800,800);
    cs9->Divide(3,2);
    
    cs9->cd(1);
    eff_s9t1->SetLineColor(kBlack);
    eff_s9t1->SetMarkerColor(kBlack);
    eff_s9t1->SetMarkerStyle(20);
    eff_s9t1->SetStats(kFALSE);
    eff_s9t1->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S9,T1));
    eff_s9t1->Draw();
    cs9->cd(2);
    eff_s9t2->SetLineColor(kBlue);
    eff_s9t2->SetMarkerColor(kBlue);
    eff_s9t2->SetMarkerStyle(21);
    eff_s9t2->SetStats(kFALSE);
    eff_s9t2 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S9,T2));
    eff_s9t2->Draw();
    cs9->cd(3);
    eff_s9t3->SetLineColor(kGreen);
    eff_s9t3->SetMarkerColor(kGreen);
    eff_s9t3->SetMarkerStyle(22);
    eff_s9t3->SetStats(kFALSE);
    eff_s9t3 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S9,T3));
    eff_s9t3->Draw();
    cs9->cd(4);
    eff_s9t4->SetLineColor(kRed);
    eff_s9t4->SetMarkerColor(kRed);
    eff_s9t4->SetMarkerStyle(23);
    eff_s9t4->SetStats(kFALSE);
    eff_s9t4 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S9,T4));
    eff_s9t4->Draw();    
    cs9->cd(5);
    eff_s9t5->SetLineColor(kCyan);
    eff_s9t5->SetMarkerColor(kCyan);
    eff_s9t5->SetMarkerStyle(24);
    eff_s9t5->SetStats(kFALSE);
    eff_s9t5->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S9,T5));
    eff_s9t5->Draw();
    cs9->cd(6);
    eff_s9t6->SetLineColor(kMagenta);
    eff_s9t6->SetMarkerColor(kMagenta);
    eff_s9t6->SetStats(kFALSE);
    eff_s9t6->SetMarkerStyle(25);
    eff_s9t6->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S9,T6));
    eff_s9t6->Draw();
    cs9 -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/central_%s_can.pdf",S9));

    TCanvas* cans9tall = new TCanvas("cans9tall");
    eff_s9t1->SetTitle(Form("Efficiency: %s; #Delta R; Efficiency",S9));
    eff_s9t1->SetStats(kFALSE);
    eff_s9t1->Draw();
    eff_s9t1->SetAxisRange(0.0,1.0,"Y");
    eff_s9t2->Draw("same");
    eff_s9t3->Draw("same");
    eff_s9t4->Draw("same");
    eff_s9t5->Draw("same");
    eff_s9t6->Draw("same");
    TLegend *legs9tall = new TLegend(.6, .7, 0.9, .898);
    legs9tall->SetHeader("Triggers","C");
    legs9tall->SetBorderSize(0);
    legs9tall->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    legs9tall->AddEntry(eff_s9t1, Form("%s",T1), "P");
    legs9tall->AddEntry(eff_s9t2, Form("%s",T2), "P");
    legs9tall->AddEntry(eff_s9t3, Form("%s",T3), "P");
    legs9tall->AddEntry(eff_s9t4, Form("%s",T4), "P");
    legs9tall->AddEntry(eff_s9t5, Form("%s",T5), "P");
    legs9tall->AddEntry(eff_s9t6, Form("%s",T6), "P");
    legs9tall->Draw();
    cans9tall -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/central_%s_all.pdf",S9));
    
    //all samples for T1
    TCanvas* cansallt1 = new TCanvas("cansallt1");
    eff_s1t1->SetTitle(Form("Efficiency: all samples, %s; #Delta R; Efficiency",T1));
    eff_s1t1->SetStats(kFALSE);
    eff_s1t1->SetMarkerStyle(20);
    eff_s2t1->SetMarkerStyle(21);
    eff_s3t1->SetMarkerStyle(22);
    eff_s4t1->SetMarkerStyle(23);
    eff_s5t1->SetMarkerStyle(24);
    eff_s6t1->SetMarkerStyle(25);
    eff_s7t1->SetMarkerStyle(26);
    eff_s8t1->SetMarkerStyle(27);
	eff_s9t1->SetMarkerStyle(28);
    
    eff_s1t1->SetMarkerColor(kBlack);
    eff_s2t1->SetMarkerColor(kBlue);
    eff_s3t1->SetMarkerColor(kGreen);
    eff_s4t1->SetMarkerColor(kRed);
    eff_s5t1->SetMarkerColor(kCyan);
    eff_s6t1->SetMarkerColor(kMagenta);
    eff_s7t1->SetMarkerColor(kGreen-1);
    eff_s8t1->SetMarkerColor(kPink);
    eff_s9t1->SetMarkerColor(kViolet+8);
    
    eff_s1t1->SetLineColor(kBlack);
    eff_s2t1->SetLineColor(kBlue);
    eff_s3t1->SetLineColor(kGreen);
    eff_s4t1->SetLineColor(kRed);
    eff_s5t1->SetLineColor(kCyan);
    eff_s6t1->SetLineColor(kMagenta);
    eff_s7t1->SetLineColor(kGreen-1);
    eff_s8t1->SetLineColor(kPink);
    eff_s9t1->SetLineColor(kViolet+8);
    
    eff_s1t1->Draw();
    eff_s1t1->SetAxisRange(0.0,1.0,"Y");
	eff_s2t1->Draw("same");	
	eff_s3t1->Draw("same");	
	eff_s4t1->Draw("same");    
	eff_s5t1->Draw("same");    
	eff_s6t1->Draw("same");    
	eff_s7t1->Draw("same");    
	eff_s8t1->Draw("same");
    eff_s9t1->Draw("same");
    
    TLegend *legsallt1 = new TLegend(.6, .7, 0.9, .898);
    legsallt1->SetHeader("Samples", "C");
    legsallt1->SetBorderSize(0);
    legsallt1->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    legsallt1->AddEntry(eff_s1t1, Form("%s", S1), "L");
    legsallt1->AddEntry(eff_s2t1, Form("%s", S2), "L");
    legsallt1->AddEntry(eff_s3t1, Form("%s", S3), "L");
    legsallt1->AddEntry(eff_s4t1, Form("%s", S4), "L");
    legsallt1->AddEntry(eff_s5t1, Form("%s", S5), "L");
    legsallt1->AddEntry(eff_s6t1, Form("%s", S6), "L");
    legsallt1->AddEntry(eff_s7t1, Form("%s", S7), "L");
    legsallt1->AddEntry(eff_s8t1, Form("%s", S8), "L");
    legsallt1->AddEntry(eff_s9t1, Form("%s", S9), "L");
    legsallt1->Draw();
    cansallt1 -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/central_all_%s.pdf",T1));
    
    //all samples for T2
    TCanvas* cansallt2 = new TCanvas("cansallt2");
    eff_s1t2->SetTitle(Form("Efficiency: all samples, %s; #Delta R; Efficiency",T2));
    eff_s1t2->SetStats(kFALSE);
    eff_s1t2->SetMarkerStyle(20);
    eff_s2t2->SetMarkerStyle(21);
    eff_s3t2->SetMarkerStyle(22);
    eff_s4t2->SetMarkerStyle(23);
    eff_s5t2->SetMarkerStyle(24);
    eff_s6t2->SetMarkerStyle(25);
    
    eff_s1t2->SetMarkerColor(kBlack);
    eff_s2t2->SetMarkerColor(kBlue);
    eff_s3t2->SetMarkerColor(kGreen);
    eff_s4t2->SetMarkerColor(kRed);
    eff_s5t2->SetMarkerColor(kCyan);
    eff_s6t2->SetMarkerColor(kMagenta);
    
    eff_s1t2->SetLineColor(kBlack);
    eff_s2t2->SetLineColor(kBlue);
    eff_s3t2->SetLineColor(kGreen);
    eff_s4t2->SetLineColor(kRed);
    eff_s5t2->SetLineColor(kCyan);
    eff_s6t2->SetLineColor(kMagenta);
    
    eff_s1t2 -> Draw();
    eff_s1t2->SetAxisRange(0.0,1.0,"Y");
    eff_s2t2 -> Draw("same");
    eff_s3t2 -> Draw("same");
    eff_s4t2 -> Draw("same");
    eff_s5t2 -> Draw("same");
    eff_s6t2 -> Draw("same");
    
    TLegend *legsallt2 = new TLegend(.6, .7, 0.9, .898);
    legsallt2->SetHeader("Samples","C");
    legsallt2->SetBorderSize(0);
    legsallt2->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    legsallt2->AddEntry(eff_s1t2, Form("%s", S1), "P");
    legsallt2->AddEntry(eff_s2t2, Form("%s", S2), "P");
    legsallt2->AddEntry(eff_s3t2, Form("%s", S3), "P");
    legsallt2->AddEntry(eff_s4t2, Form("%s", S4), "P");
    legsallt2->AddEntry(eff_s5t2, Form("%s", S5), "P");
    legsallt2->AddEntry(eff_s6t2, Form("%s", S6), "P");
    legsallt2->Draw();
    cansallt2 -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/central_all_%s.pdf",T2));
    
    //All samples with Logical OR
    TH1F *dimu_s1tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S1));    TH1F *eff_s1tor = (TH1F*) dimu_s1tor->Clone();    
    TH1F *dimu_s2tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S2));    TH1F *eff_s2tor = (TH1F*) dimu_s2tor->Clone();
    TH1F *dimu_s3tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S3));    TH1F *eff_s3tor = (TH1F*) dimu_s3tor->Clone();
    TH1F *dimu_s4tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S4));    TH1F *eff_s4tor = (TH1F*) dimu_s4tor->Clone();
    TH1F *dimu_s5tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S5));    TH1F *eff_s5tor = (TH1F*) dimu_s5tor->Clone();
    TH1F *dimu_s6tor = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_OR",S6));    TH1F *eff_s6tor = (TH1F*) dimu_s6tor->Clone();
    
    TCanvas *can_LOR = new TCanvas("can_LOR","",1800,1200);
    can_LOR->Divide(3,2);    
    can_LOR->cd(1);    
    eff_s1tor->Divide(alldimu_1);    
    eff_s1tor->SetLineColor(kBlack);    
    eff_s1tor->SetMarkerColor(kBlack);    
    eff_s1tor->SetMarkerStyle(20);    
    eff_s1tor->SetStats(kFALSE);    
    eff_s1tor->SetTitle(Form("Efficiency: %s, Logical OR; #Delta R; Efficiency",S1));    
    eff_s1tor->Draw();    
    can_LOR->cd(2);    
    eff_s2tor->Divide(alldimu_2);    
    eff_s2tor->SetLineColor(kBlue);    
    eff_s2tor->SetMarkerColor(kBlue);    
    eff_s2tor->SetMarkerStyle(21);   
    eff_s2tor->SetStats(kFALSE);    
    eff_s2tor->SetTitle(Form("Efficiency: %s, Logical OR; #Delta R; Efficiency",S2));    
    eff_s2tor->Draw();    
    can_LOR->cd(3);    
    eff_s3tor->Divide(alldimu_3);    
    eff_s3tor->SetLineColor(kGreen);   
    eff_s3tor->SetMarkerColor(kGreen);    
    eff_s3tor->SetMarkerStyle(22);    
    eff_s3tor->SetStats(kFALSE);    
    eff_s3tor->SetTitle(Form("Efficiency: %s, Logical OR; #Delta R; Efficiency",S3));    
    eff_s3tor->Draw();
    can_LOR->cd(4);    
    eff_s4tor->Divide(alldimu_4);    
    eff_s4tor->SetLineColor(kRed);    
    eff_s4tor->SetMarkerColor(kRed);    
    eff_s4tor->SetMarkerStyle(23);
    eff_s4tor->SetStats(kFALSE);    
    eff_s4tor->SetTitle(Form("Efficiency: %s, Logical OR; #Delta R; Efficiency",S4));    
    eff_s4tor->Draw();
    can_LOR->cd(5);    
    eff_s5tor->Divide(alldimu_5);    
    eff_s5tor->SetLineColor(kCyan);    
    eff_s5tor->SetMarkerColor(kCyan);    
    eff_s5tor->SetMarkerStyle(24);    
    eff_s5tor->SetStats(kFALSE);    
    eff_s5tor->SetTitle(Form("Efficiency: %s, Logical OR; #Delta R; Efficiency",S5));    
    eff_s5tor->Draw();
    can_LOR->cd(6);    
    eff_s6tor->Divide(alldimu_6);    
    eff_s6tor->SetLineColor(kMagenta);    
    eff_s6tor->SetMarkerColor(kMagenta);    
    eff_s6tor->SetMarkerStyle(25);
    eff_s6tor->SetStats(kFALSE);    
    eff_s6tor->SetTitle(Form("Efficiency: %s, Logical OR; #Delta R; Efficiency",S6));    
    eff_s6tor->Draw();    
    can_LOR->SaveAs("../outputs/plots/modules/genTriggerEfficiency/central_LogicalOR_can.pdf");

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
    legtorall->Draw();
    can_LORall->SaveAs("../outputs/plots/modules/genTriggerEfficiency/central_LogicalOR_all.pdf");
}









