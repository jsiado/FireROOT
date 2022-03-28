#include <TROOT.h>
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
#include <string>
 
//run as root -l Extra_plots.C

void gen_eff(){
    TFile* file_1 = TFile::Open("../outputs/rootfiles/modules/genTriggerEfficiency.root");
    
    //samples
    char S1[50] = "mXX-1000_mA-5_lxy-300", S2[50] = "mXX-100_mA-5_lxy-0p3", S3[50] = "mXX-500_mA-0p25_lxy-300", S4[50] = "mXX-1000_mA-5_lxy-30", S5[50] = "mXX-500_mA-1p2_lxy-30", 
    S6[50] = "mXX-100_mA-0p25_lxy-300";
    //triggers
    char T1[50] = "DoubleL2Mu23NoVtx_2Cha", T2[50] = "DoubleL2Mu23NoVtx_2Cha_NoL2Matched", T3[50]= "DoubleL2Mu23NoVtx_2Cha_CosmicSeed", 
         T4[50] = "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched", T5[50] = "DoubleL2Mu25NoVtx_2Cha_Eta2p4", T6[50] = "DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4";
    
    TCanvas *cs1 = new TCanvas("cs1","mXX-1000_mA-5_lxy-300",1800,800);
    cs1->Divide(3,2);

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

    cs1->cd(1);
    eff_s1t1->Divide(alldimu_1);
    eff_s1t1->SetLineColor(kBlue);
    eff_s1t1->SetMarkerColor(kBlue);
    eff_s1t1->SetMarkerStyle(20);
    eff_s1t1->SetStats(kFALSE);
    eff_s1t1->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S1,T1));
    eff_s1t1->Draw();
    cs1->cd(2);
    eff_s1t2->Divide(alldimu_1);
    eff_s1t2->SetLineColor(kRed);
    eff_s1t2->SetMarkerColor(kRed);
    eff_s1t2->SetMarkerStyle(21);
    eff_s1t2->SetStats(kFALSE);
    eff_s1t2 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S1,T2));
    eff_s1t2->Draw();
    cs1->cd(3);
    eff_s1t3->Divide(alldimu_1);
    eff_s1t3->SetLineColor(kMagenta);
    eff_s1t3->SetMarkerColor(kMagenta);
    eff_s1t3->SetMarkerStyle(22);
    eff_s1t3->SetStats(kFALSE);
    eff_s1t3 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S1,T3));
    eff_s1t3->Draw();
    cs1->cd(4);
    eff_s1t4->Divide(alldimu_1);
    eff_s1t4->SetLineColor(kCyan);
    eff_s1t4->SetMarkerColor(kCyan);
    eff_s1t4->SetMarkerStyle(23);
    eff_s1t4->SetStats(kFALSE);
    eff_s1t4 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S1,T4));
    eff_s1t4->Draw();    
    cs1->cd(5);
    eff_s1t5->Divide(alldimu_1);
    eff_s1t5->SetLineColor(kGreen);
    eff_s1t5->SetMarkerColor(kGreen);
    eff_s1t5->SetMarkerStyle(24);
    eff_s1t5->SetStats(kFALSE);
    eff_s1t5->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S1,T5));
    eff_s1t5->Draw();
    cs1->cd(6);
    eff_s1t6->Divide(alldimu_1);
    eff_s1t6->SetLineColor(kOrange+7);
    eff_s1t6->SetMarkerColor(kOrange+7);
    eff_s1t6->SetStats(kFALSE);
    eff_s1t6->SetMarkerStyle(25);
    eff_s1t6->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S1,T6));
    eff_s1t6->Draw();
    cs1 -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/finmyeff_%s_can.pdf",S1));
    
    TCanvas* cans1tall = new TCanvas("cans1tall");
    eff_s1t1 -> SetTitle(Form("Efficiency: %s; #Delta R; Efficiency",S1));
    eff_s1t1 -> SetStats(kFALSE);
    eff_s1t1 -> Draw();
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
    legs1tall->AddEntry(eff_s1t1, Form("%s",T1), "L");
    legs1tall->AddEntry(eff_s1t2, Form("%s",T2), "L");
    legs1tall->AddEntry(eff_s1t3, Form("%s",T3), "L");
    legs1tall->AddEntry(eff_s1t4, Form("%s",T4), "L");
    legs1tall->AddEntry(eff_s1t5, Form("%s",T5), "L");
    legs1tall->AddEntry(eff_s1t6, Form("%s",T6), "L");
    legs1tall->Draw();
    cans1tall -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/finmyeff_%s_all.pdf",S1));
    
    //second sample
    TCanvas *cs2 = new TCanvas("cs2","mXX-100_mA-5_lxy-0p3",1800,800);
    cs2->Divide(3,2);

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
    
    cs2->cd(1);
    eff_s2t1->Divide(alldimu_2);
    eff_s2t1->SetLineColor(kBlue);
    eff_s2t1->SetMarkerColor(kBlue);
    eff_s2t1->SetMarkerStyle(20);
    eff_s2t1->SetStats(kFALSE);
    eff_s2t1->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S2,T1));
    eff_s2t1->Draw();
    cs2->cd(2);
    eff_s2t2->Divide(alldimu_2);
    eff_s2t2->SetLineColor(kRed);
    eff_s2t2->SetMarkerColor(kRed);
    eff_s2t2->SetMarkerStyle(21);
    eff_s2t2->SetStats(kFALSE);
    eff_s2t2 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S2,T2));
    eff_s2t2->Draw();
    cs2->cd(3);
    eff_s2t3->Divide(alldimu_2);
    eff_s2t3->SetLineColor(kMagenta);
    eff_s2t3->SetMarkerColor(kMagenta);
    eff_s2t3->SetMarkerStyle(22);
    eff_s2t3->SetStats(kFALSE);
    eff_s2t3 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S2,T3));
    eff_s2t3->Draw();
    cs2->cd(4);
    eff_s2t4->Divide(alldimu_2);
    eff_s2t4->SetLineColor(kCyan);
    eff_s2t4->SetMarkerColor(kCyan);
    eff_s2t4->SetMarkerStyle(23);
    eff_s2t4->SetStats(kFALSE);
    eff_s2t4 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S2,T4));
    eff_s2t4->Draw();
    cs2->cd(5);
    eff_s2t5->Divide(alldimu_2);
    eff_s2t5->SetLineColor(kGreen);
    eff_s2t5->SetMarkerColor(kGreen);
    eff_s2t5->SetMarkerStyle(24);
    eff_s2t5->SetStats(kFALSE);
    eff_s2t5->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S2,T5));
    eff_s2t5->Draw();
    cs2->cd(6);
    eff_s2t6->Divide(alldimu_2);
    eff_s2t6->SetLineColor(kOrange+7);
    eff_s2t6->SetMarkerColor(kOrange+7);
    eff_s2t6->SetStats(kFALSE);
    eff_s2t6->SetMarkerStyle(25);
    eff_s2t6->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S2,T6));
    eff_s2t6->Draw();
    cs2 -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/finmyeff_%s_can.pdf",S2));

    TCanvas* cans2tall = new TCanvas("cans2tall");
    eff_s2t1 -> SetTitle(Form("Efficiency: %s; #Delta R; Efficiency",S2));
    eff_s2t1 -> SetStats(kFALSE);
    eff_s2t1 -> Draw();
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
    legs2tall->AddEntry(eff_s2t1, "DoubleL2Mu23NoVtx_2Cha", "L");
    legs2tall->AddEntry(eff_s2t2, "DoubleL2Mu23NoVtx_2Cha_NoL2Matched", "L");
    legs2tall->AddEntry(eff_s2t3, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed", "L");
    legs2tall->AddEntry(eff_s2t4, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched", "L");
    legs2tall->AddEntry(eff_s2t5, "DoubleL2Mu25NoVtx_2Cha_Eta2p4", "L");
    legs2tall->AddEntry(eff_s2t6, "DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4", "L");
    legs2tall->Draw();
    cans2tall -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/finmyeff_%s_all.pdf",S2));
    
    //sample 3
    TCanvas *cs3 = new TCanvas("cs3","mXX-500_mA-0p25_lxy-300",1800,800);
    cs3->Divide(3,2);

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
    
    cs3->cd(1);
    eff_s3t1->Divide(alldimu_3);
    eff_s3t1->SetLineColor(kBlue);
    eff_s3t1->SetMarkerColor(kBlue);
    eff_s3t1->SetMarkerStyle(20);
    eff_s3t1->SetStats(kFALSE);
    eff_s3t1->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S3,T1));
    eff_s3t1->Draw();
    cs3->cd(2);
    eff_s3t2->Divide(alldimu_3);
    eff_s3t2->SetLineColor(kRed);
    eff_s3t2->SetMarkerColor(kRed);
    eff_s3t2->SetMarkerStyle(21);
    eff_s3t2->SetStats(kFALSE);
    eff_s3t2 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S3,T2));
    eff_s3t2->Draw();
    cs3->cd(3);
    eff_s3t3->Divide(alldimu_3);
    eff_s3t3->SetLineColor(kMagenta);
    eff_s3t3->SetMarkerColor(kMagenta);
    eff_s3t3->SetMarkerStyle(22);
    eff_s3t3->SetStats(kFALSE);
    eff_s3t3 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S3,T3));
    eff_s3t3->Draw();
    cs3->cd(4);
    eff_s3t4->Divide(alldimu_3);
    eff_s3t4->SetLineColor(kCyan);
    eff_s3t4->SetMarkerColor(kCyan);
    eff_s3t4->SetMarkerStyle(23);
    eff_s3t4->SetStats(kFALSE);
    eff_s3t4 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S3,T4));
    eff_s3t4->Draw();
    cs3->cd(5);
    eff_s3t5->Divide(alldimu_3);
    eff_s3t5->SetLineColor(kGreen);
    eff_s3t5->SetMarkerColor(kGreen);
    eff_s3t5->SetMarkerStyle(24);
    eff_s3t5->SetStats(kFALSE);
    eff_s3t5->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S3,T5));
    eff_s3t5->Draw();
    cs3->cd(6);
    eff_s3t6->Divide(alldimu_3);
    eff_s3t6->SetLineColor(kOrange+7);
    eff_s3t6->SetMarkerColor(kOrange+7);
    eff_s3t6->SetStats(kFALSE);
    eff_s3t6->SetMarkerStyle(25);
    eff_s3t6->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S3,T6));
    eff_s3t6->Draw();
    cs3 -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/finmyeff_%s_can.pdf",S3));

    TCanvas* cans3tall = new TCanvas("cans3tall");
    eff_s3t1 -> SetTitle(Form("Efficiency: %s; #Delta R; Efficiency",S3));
    eff_s3t1 -> SetStats(kFALSE);
    eff_s3t1 -> Draw();
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
    legs3tall->AddEntry(eff_s3t1, "DoubleL2Mu23NoVtx_2Cha", "L");
    legs3tall->AddEntry(eff_s3t2, "DoubleL2Mu23NoVtx_2Cha_NoL2Matched", "L");
    legs3tall->AddEntry(eff_s3t3, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed", "L");
    legs3tall->AddEntry(eff_s3t4, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched", "L");
    legs3tall->AddEntry(eff_s3t5, "DoubleL2Mu25NoVtx_2Cha_Eta2p4", "L");
    legs3tall->AddEntry(eff_s3t6, "DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4", "L");
    legs3tall->Draw();
    cans3tall -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/finmyeff_%s_all.pdf",S3));

    //sample 4
    TCanvas *cs4 = new TCanvas("cs4","mXX-1000_mA-5_lxy-30",1800,800);
    cs4->Divide(3,2);

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
    
    cs4->cd(1);
    eff_s4t1->Divide(alldimu_4);
    eff_s4t1->SetLineColor(kBlue);
    eff_s4t1->SetMarkerColor(kBlue);
    eff_s4t1->SetMarkerStyle(20);
    eff_s4t1->SetStats(kFALSE);
    eff_s4t1->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S4,T1));
    eff_s4t1->Draw();
    cs4->cd(2);
    eff_s4t2->Divide(alldimu_4);
    eff_s4t2->SetLineColor(kRed);
    eff_s4t2->SetMarkerColor(kRed);
    eff_s4t2->SetMarkerStyle(21);
    eff_s4t2->SetStats(kFALSE);
    eff_s4t2 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S4,T2));
    eff_s4t2->Draw();
    cs4->cd(3);
    eff_s4t3->Divide(alldimu_4);
    eff_s4t3->SetLineColor(kMagenta);
    eff_s4t3->SetMarkerColor(kMagenta);
    eff_s4t3->SetMarkerStyle(22);
    eff_s4t3->SetStats(kFALSE);
    eff_s4t3 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S4,T3));
    eff_s4t3->Draw();
    cs4->cd(4);
    eff_s4t4->Divide(alldimu_4);
    eff_s4t4->SetLineColor(kCyan);
    eff_s4t4->SetMarkerColor(kCyan);
    eff_s4t4->SetMarkerStyle(23);
    eff_s4t4->SetStats(kFALSE);
    eff_s4t4 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S4,T4));
    eff_s4t4->Draw();
    cs4->cd(5);
    eff_s4t5->Divide(alldimu_4);
    eff_s4t5->SetLineColor(kGreen);
    eff_s4t5->SetMarkerColor(kGreen);
    eff_s4t5->SetMarkerStyle(24);
    eff_s4t5->SetStats(kFALSE);
    eff_s4t5->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S4,T5));
    eff_s4t5->Draw();
    cs4->cd(6);
    eff_s4t6->Divide(alldimu_4);
    eff_s4t6->SetLineColor(kOrange+7);
    eff_s4t6->SetMarkerColor(kOrange+7);
    eff_s4t6->SetStats(kFALSE);
    eff_s4t6->SetMarkerStyle(25);
    eff_s4t6->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S4,T6));
    eff_s4t6->Draw();
    cs4 -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/finmyeff_%s_can.pdf",S4));

    TCanvas* cans4tall = new TCanvas("cans4tall");
    eff_s4t1 -> SetTitle(Form("Efficiency: %s; #Delta R; Efficiency",S4));
    eff_s4t1 -> SetStats(kFALSE);
    eff_s4t1 -> Draw();
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
    legs4tall->AddEntry(eff_s4t1, "DoubleL2Mu23NoVtx_2Cha", "L");
    legs4tall->AddEntry(eff_s4t2, "DoubleL2Mu23NoVtx_2Cha_NoL2Matched", "L");
    legs4tall->AddEntry(eff_s4t3, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed", "L");
    legs4tall->AddEntry(eff_s4t4, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched", "L");
    legs4tall->AddEntry(eff_s4t5, "DoubleL2Mu25NoVtx_2Cha_Eta2p4", "L");
    legs4tall->AddEntry(eff_s4t6, "DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4", "L");
    legs4tall->Draw();
    cans4tall -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/finmyeff_%s_all.pdf",S4));

    //sample 5
    TCanvas *cs5 = new TCanvas("cs5","mXX-500_mA-1p2_lxy-30",1800,800);
    cs5->Divide(3,2);

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
    
    cs5->cd(1);
    eff_s5t1->Divide(alldimu_5);
    eff_s5t1->SetLineColor(kBlue);
    eff_s5t1->SetMarkerColor(kBlue);
    eff_s5t1->SetMarkerStyle(20);
    eff_s5t1->SetStats(kFALSE);
    eff_s5t1->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S5,T1));
    eff_s5t1->Draw();
    cs5->cd(2);
    eff_s5t2->Divide(alldimu_5);
    eff_s5t2->SetLineColor(kRed);
    eff_s5t2->SetMarkerColor(kRed);
    eff_s5t2->SetMarkerStyle(21);
    eff_s5t2->SetStats(kFALSE);
    eff_s5t2 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S5,T2));
    eff_s5t2->Draw();
    cs5->cd(3);
    eff_s5t3->Divide(alldimu_5);
    eff_s5t3->SetLineColor(kMagenta);
    eff_s5t3->SetMarkerColor(kMagenta);
    eff_s5t3->SetMarkerStyle(22);
    eff_s5t3->SetStats(kFALSE);
    eff_s5t3 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S5,T3));
    eff_s5t3->Draw();
    cs5->cd(4);
    eff_s5t4->Divide(alldimu_5);
    eff_s5t4->SetLineColor(kCyan);
    eff_s5t4->SetMarkerColor(kCyan);
    eff_s5t4->SetMarkerStyle(23);
    eff_s5t4->SetStats(kFALSE);
    eff_s5t4 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S5,T4));
    eff_s5t4->Draw();
    cs5->cd(5);
    eff_s5t5->Divide(alldimu_5);
    eff_s5t5->SetLineColor(kGreen);
    eff_s5t5->SetMarkerColor(kGreen);
    eff_s5t5->SetMarkerStyle(24);
    eff_s5t5->SetStats(kFALSE);
    eff_s5t5->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S5,T5));
    eff_s5t5->Draw();
    cs5->cd(6);
    eff_s5t6->Divide(alldimu_5);
    eff_s5t6->SetLineColor(kOrange+7);
    eff_s5t6->SetMarkerColor(kOrange+7);
    eff_s5t6->SetStats(kFALSE);
    eff_s5t6->SetMarkerStyle(25);
    eff_s5t6->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S5,T6));
    eff_s5t6->Draw();
    cs5 -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/finmyeff_%s_can.pdf",S5));

    TCanvas* cans5tall = new TCanvas("cans5tall");
    eff_s5t1 -> SetTitle(Form("Efficiency: %s; #Delta R; Efficiency",S5));
    eff_s5t1 -> SetStats(kFALSE);
    eff_s5t1 -> Draw();
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
    legs5tall->AddEntry(eff_s5t1, "DoubleL2Mu23NoVtx_2Cha", "L");
    legs5tall->AddEntry(eff_s5t2, "DoubleL2Mu23NoVtx_2Cha_NoL2Matched", "L");
    legs5tall->AddEntry(eff_s5t3, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed", "L");
    legs5tall->AddEntry(eff_s5t4, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched", "L");
    legs5tall->AddEntry(eff_s5t5, "DoubleL2Mu25NoVtx_2Cha_Eta2p4", "L");
    legs5tall->AddEntry(eff_s5t6, "DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4", "L");
    legs5tall->Draw();
    cans5tall -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/finmyeff_%s_all.pdf",S5));

    //sample 6
    TCanvas *cs6 = new TCanvas("cs6","mXX-100_mA-0p25_lxy-300",1800,800);
    cs6->Divide(3,2);

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
    
    cs6->cd(1);
    eff_s6t1->Divide(alldimu_6);
    eff_s6t1->SetLineColor(kBlue);
    eff_s6t1->SetMarkerColor(kBlue);
    eff_s6t1->SetMarkerStyle(20);
    eff_s6t1->SetStats(kFALSE);
    eff_s6t1->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S6,T1));
    eff_s6t1->Draw();
    cs6->cd(2);
    eff_s6t2->Divide(alldimu_6);
    eff_s6t2->SetLineColor(kRed);
    eff_s6t2->SetMarkerColor(kRed);
    eff_s6t2->SetMarkerStyle(21);
    eff_s6t2->SetStats(kFALSE);
    eff_s6t2 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S6,T2));
    eff_s6t2->Draw();
    cs6->cd(3);
    eff_s6t3->Divide(alldimu_6);
    eff_s6t3->SetLineColor(kMagenta);
    eff_s6t3->SetMarkerColor(kMagenta);
    eff_s6t3->SetMarkerStyle(22);
    eff_s6t3->SetStats(kFALSE);
    eff_s6t3 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S6,T3));
    eff_s6t3->Draw();
    cs6->cd(4);
    eff_s6t4->Divide(alldimu_6);
    eff_s6t4->SetLineColor(kCyan);
    eff_s6t4->SetMarkerColor(kCyan);
    eff_s6t4->SetMarkerStyle(23);
    eff_s6t4->SetStats(kFALSE);
    eff_s6t4 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S6,T4));
    eff_s6t4->Draw();
    cs6->cd(5);
    eff_s6t5->Divide(alldimu_6);
    eff_s6t5->SetLineColor(kGreen);
    eff_s6t5->SetMarkerColor(kGreen);
    eff_s6t5->SetMarkerStyle(24);
    eff_s6t5->SetStats(kFALSE);
    eff_s6t5->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S6,T5));
    eff_s6t5->Draw();
    cs6->cd(6);
    eff_s6t6->Divide(alldimu_6);
    eff_s6t6->SetLineColor(kOrange+7);
    eff_s6t6->SetMarkerColor(kOrange+7);
    eff_s6t6->SetStats(kFALSE);
    eff_s6t6->SetMarkerStyle(25);
    eff_s6t6->SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S6,T6));
    eff_s6t6->Draw();
    cs6 -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/finmyeff_%s_can.pdf",S6));

    TCanvas* cans6tall = new TCanvas("cans6tall");
    eff_s6t1 -> SetTitle(Form("Efficiency: %s; #Delta R; Efficiency",S6));
    eff_s6t1 -> SetStats(kFALSE);
    eff_s6t1 -> Draw();
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
    legs6tall->AddEntry(eff_s6t1, Form("%s", T1), "L");
    legs6tall->AddEntry(eff_s6t2, Form("%s", T2), "L");
    legs6tall->AddEntry(eff_s6t3, Form("%s", T3), "L");
    legs6tall->AddEntry(eff_s6t4, Form("%s", T4), "L");
    legs6tall->AddEntry(eff_s6t5, Form("%s", T5), "L");
    legs6tall->AddEntry(eff_s6t6, Form("%s", T6), "L");
    legs6tall->Draw();
    cans6tall -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/finmyeff_%s_all.pdf",S6));

    //all samples for T1
    TCanvas* cansallt1 = new TCanvas("cansallt1");
    eff_s1t1 -> SetTitle("Efficiency: all samples, DoubleL2Mu23NoVtx_2Cha; #Delta R; Efficiency");
    eff_s1t1 -> SetStats(kFALSE);
    eff_s1t1->SetMarkerStyle(20);
    eff_s2t1->SetMarkerStyle(21);                                                                                                                                                            
    eff_s3t1->SetMarkerStyle(22);                                                                                                                                                                eff_s4t1->SetMarkerStyle(23);                                                                                                                                                            
    eff_s5t1->SetMarkerStyle(24);
    eff_s6t1->SetMarkerStyle(25);

    eff_s1t1->SetMarkerColor(kBlue);                                                                                                                                                        
    eff_s2t1->SetMarkerColor(kRed);                                                                                                                                                          
    eff_s3t1->SetMarkerColor(kCyan);                                                                                                                                                      
    eff_s4t1->SetMarkerColor(kMagenta);                                                                                                                                                  
    eff_s5t1->SetMarkerColor(kGreen);
    eff_s6t1->SetMarkerColor(kOrange+7);

    eff_s1t1->SetLineColor(kBlue);                                                                                                                                                          
    eff_s2t1->SetLineColor(kRed);                                                                                                                                                            
    eff_s3t1->SetLineColor(kCyan);                                                                                                                                                        
    eff_s4t1->SetLineColor(kMagenta);                                                                                                                                            
    eff_s5t1->SetLineColor(kGreen);
    eff_s6t1->SetLineColor(kOrange+7);
                                                                                                                                                           
    eff_s1t1 -> Draw();                                                                                                                                                                      
    eff_s2t1 -> Draw("same");                                                                                                                                                                
    eff_s3t1 -> Draw("same");                                                                                                                                                                
    eff_s4t1 -> Draw("same");                                                                                                                                                                
    eff_s5t1 -> Draw("same");
    eff_s6t1 -> Draw("same");

    TLegend *legsallt1 = new TLegend(.6, .7, 0.9, .898);                                                                                                                                     
    legsallt1->SetHeader("Samples","C");                                                                                                                                                     
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
    legsallt1->Draw();                                                                                                                                                                       
    cansallt1 -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/finmyeff_all_%s.pdf",T1));

    //all samples for T2
    TCanvas* cansallt2 = new TCanvas("cansallt2");
    eff_s1t2 -> SetTitle("Efficiency: all samples, DoubleL2Mu23NoVtx_2Cha_NoL2Matched; #Delta R; Efficiency");
    eff_s1t2 -> SetStats(kFALSE);
    eff_s1t2->SetMarkerStyle(20);
    eff_s2t2->SetMarkerStyle(21);
    eff_s3t2->SetMarkerStyle(22);
    eff_s4t2->SetMarkerStyle(23);
    eff_s5t2->SetMarkerStyle(24);
    eff_s6t2->SetMarkerStyle(25);

    eff_s1t2->SetMarkerColor(kBlue);
    eff_s2t2->SetMarkerColor(kRed);
    eff_s3t2->SetMarkerColor(kCyan);
    eff_s4t2->SetMarkerColor(kMagenta);
    eff_s5t2->SetMarkerColor(kGreen);
    eff_s6t2->SetMarkerColor(kOrange+7);

    eff_s1t2->SetLineColor(kBlue);
    eff_s2t2->SetLineColor(kRed);
    eff_s3t2->SetLineColor(kCyan);
    eff_s4t2->SetLineColor(kMagenta);
    eff_s5t2->SetLineColor(kGreen);
    eff_s6t2->SetLineColor(kOrange+7);

    eff_s1t2 -> Draw();
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
    cansallt2 -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/finmyeff_all_%s.pdf",T2));
    
    //2d map pt vs dR
    TCanvas* can_ptdR = new TCanvas("can_ptdR");
    TH2F *ptdR_s1 = (TH2F*)file_1->Get(Form("ch2mu2e/sig/%s/ptvsdR2",S1));
    TH2F *ptdR_s2 = (TH2F*)file_1->Get(Form("ch2mu2e/sig/%s/ptvsdR2",S2));
    TH2F *ptdR_s3 = (TH2F*)file_1->Get(Form("ch2mu2e/sig/%s/ptvsdR2",S3));
    TH2F *ptdR_s4 = (TH2F*)file_1->Get(Form("ch2mu2e/sig/%s/ptvsdR2",S4));
    TH2F *ptdR_s5 = (TH2F*)file_1->Get(Form("ch2mu2e/sig/%s/ptvsdR2",S5));
    TH2F *ptdR_s6 = (TH2F*)file_1->Get(Form("ch2mu2e/sig/%s/ptvsdR2",S6));
    ptdR_s1->SetMarkerStyle(20);
    ptdR_s2->SetMarkerStyle(21);                                                                     
    ptdR_s3->SetMarkerStyle(22);                                                                                                                                                             
    ptdR_s4->SetMarkerStyle(23);                                                                                                                                                            
    ptdR_s5->SetMarkerStyle(24);
    ptdR_s6->SetMarkerStyle(25);

    ptdR_s1->SetMarkerColor(kBlue);                                                                                                                                                       
    ptdR_s2->SetMarkerColor(kRed);
    ptdR_s3->SetMarkerColor(kCyan);
    ptdR_s4->SetMarkerColor(kMagenta);
    ptdR_s5->SetMarkerColor(kGreen);
    ptdR_s6->SetMarkerColor(kOrange+7);
    //kViolet+8 kGreen-1, kPink-9, kCyan-5
    
    ptdR_s1->SetLineColor(kBlue);
    ptdR_s2->SetLineColor(kRed);                                                                                                                                        
    ptdR_s3->SetLineColor(kCyan);                                                                                                                                                         
    ptdR_s4->SetLineColor(kMagenta);
    ptdR_s5->SetLineColor(kGreen);
    ptdR_s6->SetLineColor(kOrange+7);
    ptdR_s1->SetStats(0);
                                                                                                                                          
    ptdR_s1->Draw();
    ptdR_s2->Draw("same");
    ptdR_s3->Draw("same");
    ptdR_s4->Draw("same"); 
    ptdR_s5->Draw("same");
    ptdR_s6->Draw("same");
    
    TLegend *leg_ptdR = new TLegend(.6, .7, 0.9, .898);
    leg_ptdR->SetHeader("Samples","C");      
    leg_ptdR->SetBorderSize(0);             
    leg_ptdR->SetLineColor(1);                                                                                                                                                               
    gStyle->SetFillColor(0);                                                                                                                                                                 
    gStyle->SetCanvasColor(10);                                                                                                                                                   
    leg_ptdR->AddEntry(ptdR_s1, "mXX-1000_mA-5_lxy-300", "L");                                                                                                                               
    leg_ptdR->AddEntry(ptdR_s2, "mXX-100_mA-5_lxy-0p3", "L");                                                                                                                                
    leg_ptdR->AddEntry(ptdR_s3, "mXX-500_mA-0p25_lxy-300", "L");                                                                                                                             
    leg_ptdR->AddEntry(ptdR_s4, "mXX-1000_mA-5_lxy-30", "L");
    leg_ptdR->AddEntry(ptdR_s5, "mXX-500_mA-1p2_lxy-30", "L");
    leg_ptdR->AddEntry(ptdR_s6, "mXX-100_mA-0p25_lxy-300", "L");
    leg_ptdR->Draw();                                                                                                                                                                        
    can_ptdR -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/finmyeff_ptvsdR.pdf");
    
    /*u_2 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S2));
    TH1F *dimu_s2t1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_1",S2));
    TH1F *eff_s2t1 = (TH1F*) dimu_s2t1->Clone();
    TH1F *dimu_s2t2 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_2",S2));
    TH1F *eff_s2t2 = (TH1F*) dimu_s2t2->Clone();
    TH1F *dimu_s2t3 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_3",S2));
    TH1F *eff_s2t3 = (TH1F*) dimu_s2t3->Clone();
    TH1F *dimu_s2t4 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_4",S2));
    TH1F *eff_s2t4 = (TH1F*) dimu_s2t4->Clone();
    cs2->cd(1);
    eff_s2t1->Divide(alldimu_2);
    eff_s2t1->SetLineColor(1);
    eff_s2t1->SetMarkerColor(1);
    eff_s2t1 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S2,T1));
    eff_s2t1 -> Draw();
    cs2->cd(2);
    eff_s2t2->Divide(alldimu_2);
    eff_s2t2->SetLineColor(2);
    eff_s2t2->SetMarkerColor(2);
    eff_s2t2 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S2,T2));
    eff_s2t2->Draw();
    cs2->cd(3);
    eff_s2t3->Divide(alldimu_2);
    eff_s2t3->SetLineColor(3);
    eff_s2t3->SetMarkerColor(3);
    eff_s2t3 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S2,T3));
    eff_s2t3->Draw();
    cs2->cd(4);
    eff_s2t4->Divide(alldimu_2);
    eff_s2t4->SetLineColor(4);
    eff_s2t4->SetMarkerColor(4);
    eff_s2t4 -> SetTitle(Form("Efficiency: %s, %s; #Delta R; Efficiency",S2,T4));
    eff_s2t4->Draw();
    TCanvas* cans2tall = new TCanvas("cans2tall");
    eff_s2t1 -> SetTitle(Form("Efficiency: %s; #Delta R; Efficiency",S2));
    eff_s2t1 -> SetStats(kFALSE);
    eff_s2t1 -> Draw();
    eff_s2t2 -> Draw("same");
    eff_s2t3 -> Draw("same");
    eff_s2t4 -> Draw("same");
    TLegend *legs2tall = new TLegend(.6, .7, 0.9, .898);
    legs2tall->SetHeader("Triggers","C");
    legs2tall->SetBorderSize(0);
    legs2tall->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    legs2tall->AddEntry(eff_s2t1, "Double", "L");
    legs2tall->AddEntry(eff_s2t2, "DoubleL2Mu23NoVtx_2Cha_NoL2Matched", "L");
    legs2tall->AddEntry(eff_s2t3, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed", "L");
    legs2tall->AddEntry(eff_s2t4, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched", "L");
    legs2tall->Draw();
    cans2tall -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/fmyeff_%s_all.pdf",S2));
			



    TH1F *alldimu_2 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu",S2));
    TH1F *dimu_s2t1 = (TH1F*)file_1->Get(Form("ch2mu2e/sig/%s/allDimu_1",S2));
    TH1F *eff_s2t1 = (TH1F*) dimu_s2t1->Clone();
    TH1F *dimu_s2t2 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-100_mA-5_lxy-0p3/allDimu_2");
    TH1F *eff_s2t2 = (TH1F*) dimu_s2t2->Clone();
    TH1F *dimu_s2t3 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-100_mA-5_lxy-0p3/allDimu_3");
    TH1F *eff_s2t3 = (TH1F*) dimu_s2t3->Clone();
    TH1F *dimu_s2t4 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-100_mA-5_lxy-0p3/allDimu_4");
    TH1F *eff_s2t4 = (TH1F*) dimu_s2t4->Clone();

    eff_s2t1->Divide(alldimu_2);
    eff_s2t1->SetLineColor(1);
    eff_s2t1->SetMarkerColor(1);
    eff_s2t2->Divide(alldimu_2);
    eff_s2t2->SetLineColor(2);
    eff_s2t2->SetMarkerColor(2);
    eff_s2t3->Divide(alldimu_2);
    eff_s2t3->SetLineColor(3);
    eff_s2t3->SetMarkerColor(3);
    eff_s2t4->Divide(alldimu_2);
    eff_s2t4->SetLineColor(4);
    eff_s2t4->SetMarkerColor(4);

    TCanvas* cans2t1 = new TCanvas("cans2t1");
    eff_s2t1 -> SetTitle("Efficiency: mXX-100_mA-5_lxy-0p3, DoubleL2Mu23NoVtx_2Cha");
    eff_s2t1 -> GetXaxis()->SetTitle("#Delta R");
    eff_s2t1 -> GetYaxis()->SetTitle("Efficiency");
    eff_s2t1 -> SetStats(kFALSE);
    eff_s2t1 -> Draw();
    cans2t1 -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/fmyeff_mXX-100_mA-5_lxy-0p3_DoubleL2Mu23NoVtx_2Cha.pdf");
    TCanvas* cans2t2 = new TCanvas("cans2t2");
    eff_s2t2 -> SetTitle("Efficiency: mXX-100_mA-5_lxy-0p3, DoubleL2Mu23NoVtx_2Cha_NoL2Matched");
    eff_s2t2 -> GetXaxis()->SetTitle("#Delta R");
    eff_s2t2 -> GetYaxis()->SetTitle("Efficiency");
    eff_s2t2 -> SetStats(kFALSE);
    eff_s2t2 -> Draw();
    cans2t2 -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/fmyeff_mXX-100_mA-5_lxy-0p3_DoubleL2Mu23NoVtx_2Cha_NoL2Matched.pdf");
    TCanvas* cans2t3 = new TCanvas("cans2t3");
    eff_s2t3 -> SetTitle("Efficiency: mXX-100_mA-5_lxy-0p3, DoubleL2Mu23NoVtx_2Cha_CosmicSeed");
    eff_s2t3 -> GetXaxis()->SetTitle("#Delta R");
    eff_s2t3 -> GetYaxis()->SetTitle("Efficiency");
    eff_s2t3 -> SetStats(kFALSE);
    eff_s2t3 -> Draw();
    cans2t3 -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/fmyeff_mXX-100_mA-5_lxy-0p3_DoubleL2Mu23NoVtx_2Cha_CosmicSeed.pdf");
    TCanvas* cans2t4 = new TCanvas("cans2t4");
    eff_s2t4 -> SetTitle("Efficiency: mXX-100_mA-5_lxy-0p3, DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched");
    eff_s2t4 -> GetXaxis()->SetTitle("#Delta R");
    eff_s2t4 -> GetYaxis()->SetTitle("Efficiency");
    eff_s2t4 -> SetStats(kFALSE);
    eff_s2t4 -> Draw();
    cans2t4 -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/fmyeff_mXX-100_mA-5_lxy-0p3_DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched.pdf");
    TCanvas* cans2tall = new TCanvas("cans2tall");
    eff_s2t1 -> SetTitle("Efficiency: mXX-100_mA-5_lxy-0p3; #Delta R; Efficiency");
    eff_s2t1 -> SetStats(kFALSE);
    eff_s2t1 -> Draw();
    eff_s2t2 -> Draw("same");
    eff_s2t3 -> Draw("same");
    eff_s2t4 -> Draw("same");
    TLegend *legs2tall = new TLegend(.6, .7, 0.9, .898);
    legs1tall->SetHeader("Triggers","C"); // option "C" allows to center the header
    legs2tall->SetBorderSize(0);
    legs2tall->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    legs2tall->AddEntry(eff_s2t1, "DoubleL2Mu23NoVtx_2Cha", "L");
    legs2tall->AddEntry(eff_s2t2, "DoubleL2Mu23NoVtx_2Cha_NoL2Matched", "L");
    legs2tall->AddEntry(eff_s2t3, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed", "L");
    legs2tall->AddEntry(eff_s2t4, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched", "L");
    legs2tall->Draw();
    cans2tall -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/fmyeff_%s_all.pdf",S2));

    TH1F *alldimu_3 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-500_mA-0p25_lxy-300/allDimu");
    TH1F *dimu_s3t1 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-500_mA-0p25_lxy-300/allDimu_1");
    TH1F *eff_s3t1 = (TH1F*) dimu_s3t1->Clone();
    TH1F *dimu_s3t2 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-500_mA-0p25_lxy-300/allDimu_2");
    TH1F *eff_s3t2 = (TH1F*) dimu_s3t2->Clone();
    TH1F *dimu_s3t3 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-500_mA-0p25_lxy-300/allDimu_3");
    TH1F *eff_s3t3 = (TH1F*) dimu_s3t3->Clone();
    TH1F *dimu_s3t4 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-500_mA-0p25_lxy-300/allDimu_4");
    TH1F *eff_s3t4 = (TH1F*) dimu_s3t4->Clone();

    eff_s3t1->Divide(alldimu_3);
    eff_s3t1->SetLineColor(1);
    eff_s3t1->SetMarkerColor(1);
    eff_s3t2->Divide(alldimu_3);
    eff_s3t2->SetLineColor(2);
    eff_s3t2->SetMarkerColor(2);
    eff_s3t3->Divide(alldimu_3);
    eff_s3t3->SetLineColor(3);
    eff_s3t3->SetMarkerColor(3);
    eff_s3t4->Divide(alldimu_3);
    eff_s3t4->SetLineColor(4);
    eff_s3t4->SetMarkerColor(4);

    TCanvas* cans3t1 = new TCanvas("cans3t1");
    eff_s3t1 -> SetTitle("Efficiency: mXX-500_mA-0p25_lxy-300, DoubleL2Mu23NoVtx_2Cha");
    eff_s3t1 -> GetXaxis()->SetTitle("#Delta R");
    eff_s3t1 -> GetYaxis()->SetTitle("Efficiency");
    eff_s3t1 -> SetStats(kFALSE);
    eff_s3t1 -> Draw();
    cans3t1 -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/fmyeff_mXX-500_mA-0p25_lxy-300_DoubleL2Mu23NoVtx_2Cha.pdf");
    TCanvas* cans3t2 = new TCanvas("cans3t2");
    eff_s3t2 -> SetTitle("Efficiency: mXX-500_mA-0p25_lxy-300, DoubleL2Mu23NoVtx_2Cha_NoL2Matched");
    eff_s3t2 -> GetXaxis()->SetTitle("#Delta R");
    eff_s3t2 -> GetYaxis()->SetTitle("Efficiency");
    eff_s3t2 -> SetStats(kFALSE);
    eff_s3t2 -> Draw();
    cans3t2 -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/fmyeff_mXX-500_mA-0p25_lxy-300_DoubleL2Mu23NoVtx_2Cha_NoL2Matched.pdf");
    TCanvas* cans3t3 = new TCanvas("cans3t3");
    eff_s3t3 -> SetTitle("Efficiency: mXX-500_mA-0p25_lxy-300, DoubleL2Mu23NoVtx_2Cha_CosmicSeed");
    eff_s3t3 -> GetXaxis()->SetTitle("#Delta R");
    eff_s3t3 -> GetYaxis()->SetTitle("Efficiency");
    eff_s3t3 -> SetStats(kFALSE);
    eff_s3t3 -> Draw();
    cans3t3 -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/fmyeff_mXX-500_mA-0p25_lxy-300_DoubleL2Mu23NoVtx_2Cha_CosmicSeed.pdf");
    TCanvas* cans3t4 = new TCanvas("cans3t4");
    eff_s3t4 -> SetTitle("Efficiency: mXX-500_mA-0p25_lxy-300, DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched");
    eff_s3t4 -> GetXaxis()->SetTitle("#Delta R");
    eff_s3t4 -> GetYaxis()->SetTitle("Efficiency");
    eff_s3t4 -> SetStats(kFALSE);
    eff_s3t4 -> Draw();
    cans3t4 -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/fmyeff_mXX-500_mA-0p25_lxy-300_DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched.pdf");
    TCanvas* cans3tall = new TCanvas("cans3tall");
    eff_s3t1 -> SetTitle("Efficiency: mXX-500_mA-0p25_lxy-300");
    eff_s3t1 -> GetXaxis()->SetTitle("#Delta R");
    eff_s3t1 -> GetYaxis()->SetTitle("Efficiency");
    eff_s3t1 -> SetAxisRange(0.0,1.0,"Y");
    eff_s3t1 -> SetStats(kFALSE);
    eff_s3t1 -> Draw();
    eff_s3t2 -> Draw("same");
    eff_s3t3 -> Draw("same");
    eff_s3t4 -> Draw("same");
    TLegend *legs3tall = new TLegend(.6, .7, 0.9, .898);
    legs3tall->SetHeader("Triggers","C"); // option "C" allows to center the header                                                                                                           
    legs3tall->SetBorderSize(0);
    legs3tall->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    legs3tall->AddEntry(eff_s3t1, "DoubleL2Mu23NoVtx_2Cha", "L");
    legs3tall->AddEntry(eff_s3t2, "DoubleL2Mu23NoVtx_2Cha_NoL2Matched", "L");
    legs3tall->AddEntry(eff_s3t3, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed", "L");
    legs3tall->AddEntry(eff_s3t4, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched", "L");
    legs3tall->Draw();
    cans3tall -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/fmyeff_mXX-500_mA-0p25_lxy-300_all.pdf");

    

    TH1F *alldimu_4 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-1000_mA-5_lxy-30/allDimu");
    TH1F *dimu_s4t1 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-1000_mA-5_lxy-30/allDimu_1");
    TH1F *eff_s4t1 = (TH1F*) dimu_s4t1->Clone();
    TH1F *dimu_s4t2 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-1000_mA-5_lxy-30/allDimu_2");
    TH1F *eff_s4t2 = (TH1F*) dimu_s4t2->Clone();
    TH1F *dimu_s4t3 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-1000_mA-5_lxy-30/allDimu_3");
    TH1F *eff_s4t3 = (TH1F*) dimu_s4t3->Clone();
    TH1F *dimu_s4t4 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-1000_mA-5_lxy-30/allDimu_4");
    TH1F *eff_s4t4 = (TH1F*) dimu_s4t4->Clone();

    eff_s4t1->Divide(alldimu_4);
    eff_s4t1->SetLineColor(1);
    eff_s4t1->SetMarkerColor(1);
    eff_s4t1->SetMarkerStyle(20);
    eff_s4t2->Divide(alldimu_4);
    eff_s4t2->SetLineColor(2);
    eff_s4t2->SetMarkerColor(2);
    eff_s4t1->SetMarkerStyle(21);
    eff_s4t3->Divide(alldimu_4);
    eff_s4t3->SetLineColor(3);
    eff_s4t3->SetMarkerColor(3);
    eff_s4t1->SetMarkerStyle(22);
    eff_s4t4->Divide(alldimu_4);
    eff_s4t4->SetLineColor(4);
    eff_s4t4->SetMarkerColor(4);
    eff_s4t1->SetMarkerStyle(3);

    TCanvas* cans4t1 = new TCanvas("cans4t1");
    eff_s4t1 -> SetTitle("Efficiency: mXX-1000_mA-5_lxy-30, DoubleL2Mu23NoVtx_2Cha");
    eff_s4t1 -> GetXaxis()->SetTitle("#Delta R");
    eff_s4t1 -> GetYaxis()->SetTitle("Efficiency");
    eff_s4t1 -> SetStats(kFALSE);
    eff_s4t1 -> Draw();
    cans4t1 -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/fmyeff_mXX-1000_mA-5_lxy-30_DoubleL2Mu23NoVtx_2Cha.pdf");
    TCanvas* cans4t2 = new TCanvas("cans4t2");
    eff_s4t2 -> SetTitle("Efficiency: mXX-1000_mA-5_lxy-30, DoubleL2Mu23NoVtx_2Cha_NoL2Matched");
    eff_s4t2 -> GetXaxis()->SetTitle("#Delta R");
    eff_s4t2 -> GetYaxis()->SetTitle("Efficiency");
    eff_s4t2 -> SetStats(kFALSE);
    eff_s4t2 -> Draw();
    cans4t2 -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/fmyeff_mXX-1000_mA-5_lxy-30_DoubleL2Mu23NoVtx_2Cha_NoL2Matched.pdf");
    TCanvas* cans4t3 = new TCanvas("cans4t3");
    eff_s4t3 -> SetTitle("Efficiency: mXX-1000_mA-5_lxy-30, DoubleL2Mu23NoVtx_2Cha_CosmicSeed");
    eff_s4t3 -> GetXaxis()->SetTitle("#Delta R");
    eff_s4t3 -> GetYaxis()->SetTitle("Efficiency");
    eff_s4t3 -> SetStats(kFALSE);
    eff_s4t3 -> Draw();
    cans4t3 -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/fmyeff_mXX-1000_mA-5_lxy-30_DoubleL2Mu23NoVtx_2Cha_CosmicSeed.pdf");
    TCanvas* cans4t4 = new TCanvas("cans4t4");
    eff_s4t4 -> SetTitle("Efficiency: mXX-1000_mA-5_lxy-30, DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched");
    eff_s4t4 -> GetXaxis()->SetTitle("#Delta R");
    eff_s4t4 -> GetYaxis()->SetTitle("Efficiency");
    eff_s4t4 -> SetStats(kFALSE);
    eff_s4t4 -> Draw();
    cans4t4 -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/fmyeff_mXX-1000_mA-5_lxy-30_DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched.pdf");
    TCanvas* cans4tall = new TCanvas("cans4tall");
    eff_s4t1 -> SetTitle("Efficiency: mXX-1000_mA-5_lxy-30");
    eff_s4t1 -> GetXaxis()->SetTitle("#Delta R");
    eff_s4t1 -> GetYaxis()->SetTitle("Efficiency");
    eff_s4t1 -> SetAxisRange(0.0,1.0,"Y");
    eff_s4t1 -> SetStats(kFALSE);
    eff_s4t1 -> Draw();
    eff_s4t2 -> Draw("same");
    eff_s4t3 -> Draw("same");
    eff_s4t4 -> Draw("same");
    TLegend *legs4tall = new TLegend(.6, .7, 0.9, .898);
    legs1tall->SetHeader("Triggers","C"); // option "C" allows to center the header                                                                                                          
    legs4tall->SetBorderSize(0);
    legs4tall->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    legs4tall->AddEntry(eff_s4t1, "DoubleL2Mu23NoVtx_2Cha", "L");
    legs4tall->AddEntry(eff_s4t2, "DoubleL2Mu23NoVtx_2Cha_NoL2Matched", "L");
    legs4tall->AddEntry(eff_s4t3, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed", "L");
    legs4tall->AddEntry(eff_s4t4, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched", "L");
    legs4tall->Draw();
    cans4tall -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/fmyeff_mXX-1000_mA-5_lxy-30_all.pdf");

    TH1F *alldimu_5 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-500_mA-1p2_lxy-30/allDimu");
    TH1F *dimu_s5t1 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-500_mA-1p2_lxy-30/allDimu_1");
    TH1F *eff_s5t1 = (TH1F*) dimu_s5t1->Clone();
    TH1F *dimu_s5t2 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-500_mA-1p2_lxy-30/allDimu_2");
    TH1F *eff_s5t2 = (TH1F*) dimu_s5t2->Clone();
    TH1F *dimu_s5t3 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-500_mA-1p2_lxy-30/allDimu_3");
    TH1F *eff_s5t3 = (TH1F*) dimu_s5t3->Clone();
    TH1F *dimu_s5t4 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-500_mA-1p2_lxy-30/allDimu_4");
    TH1F *eff_s5t4 = (TH1F*) dimu_s5t4->Clone();

    eff_s5t1->Divide(alldimu_5);
    eff_s5t1->SetLineColor(1);
    eff_s5t1->SetMarkerColor(1);
    eff_s5t1->SetMarkerStyle(1);
    eff_s5t2->Divide(alldimu_5);
    eff_s5t2->SetLineColor(2);
    eff_s5t2->SetMarkerColor(2);
    eff_s5t1->SetMarkerStyle(2);
    eff_s5t3->Divide(alldimu_5);
    eff_s5t3->SetLineColor(3);
    eff_s5t3->SetMarkerColor(3);
    eff_s5t1->SetMarkerStyle(3);
    eff_s5t4->Divide(alldimu_5);
    eff_s5t4->SetLineColor(4);
    eff_s5t4->SetMarkerColor(4);
    eff_s5t1->SetMarkerStyle(4);

    TCanvas* cans5t1 = new TCanvas("cans5t1");
    eff_s5t1 -> SetTitle("Efficiency: mXX-500_mA-1p2_lxy-30, DoubleL2Mu23NoVtx_2Cha");
    eff_s5t1 -> GetXaxis()->SetTitle("#Delta R");
    eff_s5t1 -> GetYaxis()->SetTitle("Efficiency");
    eff_s5t1 -> SetStats(kFALSE);
    eff_s5t1 -> Draw();
    cans5t1 -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/fmyeff_mXX-500_mA-1p2_lxy-30_DoubleL2Mu23NoVtx_2Cha.pdf");
    TCanvas* cans5t2 = new TCanvas("cans5t2");
    eff_s5t2 -> SetTitle("Efficiency: mXX-500_mA-1p2_lxy-30, DoubleL2Mu23NoVtx_2Cha_NoL2Matched");
    eff_s5t2 -> GetXaxis()->SetTitle("#Delta R");
    eff_s5t2 -> GetYaxis()->SetTitle("Efficiency");
    eff_s5t2 -> SetStats(kFALSE);
    eff_s5t2 -> Draw();
    cans5t2 -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/fmyeff_mXX-500_mA-1p2_lxy-30_DoubleL2Mu23NoVtx_2Cha_NoL2Matched.pdf");
    TCanvas* cans5t3 = new TCanvas("cans5t3");
    eff_s5t3 -> SetTitle("Efficiency: mXX-500_mA-1p2_lxy-30, DoubleL2Mu23NoVtx_2Cha_CosmicSeed");
    eff_s5t3 -> GetXaxis()->SetTitle("#Delta R");
    eff_s5t3 -> GetYaxis()->SetTitle("Efficiency");
    eff_s5t3 -> SetStats(kFALSE);
    eff_s5t3 -> Draw();
    cans5t3 -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/fmyeff_mXX-500_mA-1p2_lxy-30_DoubleL2Mu23NoVtx_2Cha_CosmicSeed.pdf");
    TCanvas* cans5t4 = new TCanvas("cans5t4");
    eff_s5t4 -> SetTitle("Efficiency: mXX-500_mA-1p2_lxy-30, DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched");
    eff_s5t4 -> GetXaxis()->SetTitle("#Delta R");
    eff_s5t4 -> GetYaxis()->SetTitle("Efficiency");
    eff_s5t4 -> SetStats(kFALSE);
    eff_s5t4 -> Draw();
    cans5t4 -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/fmyeff_mXX-500_mA-1p2_lxy-30_DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched.pdf");
    TCanvas* cans5tall = new TCanvas("cans5tall");
    eff_s5t1 -> SetTitle("Efficiency: mXX-500_mA-1p2_lxy-30");
    eff_s5t1 -> GetXaxis()->SetTitle("#Delta R");
    eff_s5t1 -> GetYaxis()->SetTitle("Efficiency");
    eff_s5t1 -> SetAxisRange(0.0,1.0,"Y");
    eff_s5t1 -> SetStats(kFALSE);
    eff_s5t1 -> Draw();
    eff_s5t2 -> Draw("same");
    eff_s5t3 -> Draw("same");
    eff_s5t4 -> Draw("same");
    TLegend *legs5tall = new TLegend(.6, .7, 0.9, .898);
    legs1tall->SetHeader("Triggers","C");
    legs5tall->SetBorderSize(0);
    legs5tall->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    legs5tall->AddEntry(eff_s5t1, "DoubleL2Mu23NoVtx_2Cha", "L");
    legs5tall->AddEntry(eff_s5t2, "DoubleL2Mu23NoVtx_2Cha_NoL2Matched", "L");
    legs5tall->AddEntry(eff_s5t3, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed", "L");
    legs5tall->AddEntry(eff_s5t4, "DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched", "L");
    legs5tall->Draw();
    cans5tall -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/fmyeff_mXX-500_mA-1p2_lxy-30_all.pdf");







































    //2d plot
    TCanvas* can_ptdR = new TCanvas("can_ptdR");
    TH2F *ptdR_s1 = (TH2F*)file_1->Get("ch2mu2e/sig/mXX-1000_mA-5_lxy-300/ptvsdR");
    TH2F *ptdR_s2 = (TH2F*)file_1->Get("ch2mu2e/sig/mXX-100_mA-5_lxy-0p3/ptvsdR");
    TH2F *ptdR_s3 = (TH2F*)file_1->Get("ch2mu2e/sig/mXX-500_mA-0p25_lxy-300/ptvsdR");
    TH2F *ptdR_s4 = (TH2F*)file_1->Get("ch2mu2e/sig/mXX-1000_mA-5_lxy-30/ptvsdR");
    TH2F *ptdR_s5 = (TH2F*)file_1->Get("ch2mu2e/sig/mXX-500_mA-1p2_lxy-30/ptvsdR");
    ptdR_s1->SetMarkerStyle(20);
    ptdR_s2->SetMarkerStyle(21);
    ptdR_s3->SetMarkerStyle(22);
    ptdR_s4->SetMarkerStyle(23);
    ptdR_s5->SetMarkerStyle(24);
    ptdR_s1->SetMarkerColor(kBlue+2);
    ptdR_s2->SetMarkerColor(kRed);
    ptdR_s3->SetMarkerColor(kMagenta);
    ptdR_s4->SetMarkerColor(kYellow);
    ptdR_s5->SetMarkerColor(kGreen);
    ptdR_s1->SetLineColor(kBlue+2);
    ptdR_s2->SetLineColor(kRed);
    ptdR_s3->SetLineColor(kMagenta);
    ptdR_s4->SetLineColor(kYellow);
    ptdR_s5->SetLineColor(kGreen);
    ptdR_s1->SetStats(0);
    ptdR_s1->Draw();
    ptdR_s2->Draw("same");
    ptdR_s3->Draw("same");
    ptdR_s4->Draw("same");
    ptdR_s5->Draw("same");
    TLegend *leg_ptdR = new TLegend(.6, .7, 0.9, .898);
    leg_ptdR->SetHeader("Samples","C");
    leg_ptdR->SetBorderSize(0);
    leg_ptdR->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    leg_ptdR->AddEntry(ptdR_s1, "mXX-1000_mA-5_lxy-300", "L");
    leg_ptdR->AddEntry(ptdR_s2, "mXX-100_mA-5_lxy-0p3", "L");
    leg_ptdR->AddEntry(ptdR_s3, "mXX-500_mA-0p25_lxy-300", "L");
    leg_ptdR->AddEntry(ptdR_s4, "mXX-1000_mA-5_lxy-30", "L");
    leg_ptdR->AddEntry(ptdR_s5, "mXX-500_mA-1p2_lxy-30", "L");
    leg_ptdR->Draw();
    can_ptdR -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/fmyeff_ptvsdR.pdf");













    //all samples for T1
    TCanvas* cansallt1 = new TCanvas("cansallt1");
    eff_s1t1 -> SetTitle("Efficiency: all samples, DoubleL2Mu23NoVtx_2Cha; #Delta R; Efficiency");
    eff_s1t1 -> SetStats(kFALSE);
    eff_s1t1->SetMarkerStyle(20);
    eff_s2t1->SetMarkerStyle(21);
    eff_s3t1->SetMarkerStyle(22);
    eff_s4t1->SetMarkerStyle(23);
    eff_s5t1->SetMarkerStyle(24);
    eff_s1t1->SetMarkerColor(kBlue+2);
    eff_s2t1->SetMarkerColor(kRed);
    eff_s3t1->SetMarkerColor(kMagenta);
    eff_s4t1->SetMarkerColor(kYellow);
    eff_s5t1->SetMarkerColor(kGreen);
    eff_s1t1->SetLineColor(kBlue+2);
    eff_s2t1->SetLineColor(kRed);
    eff_s3t1->SetLineColor(kMagenta);
    eff_s4t1->SetLineColor(kYellow);
    eff_s5t1->SetLineColor(kGreen);
    eff_s1t1 -> Draw(); 
    eff_s2t1 -> Draw("same");
    eff_s3t1 -> Draw("same");
    eff_s4t1 -> Draw("same");
    eff_s5t1 -> Draw("same");
    TLegend *legsallt1 = new TLegend(.6, .7, 0.9, .898);
    legsallt1->SetHeader("Samples","C");
    legsallt1->SetBorderSize(0);
    legsallt1->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    legsallt1->AddEntry(eff_s1t1, "mXX-1000_mA-5_lxy-300 ", "L");
    legsallt1->AddEntry(eff_s2t1, "mXX-100_mA-5_lxy-0p3", "L");
    legsallt1->AddEntry(eff_s3t1, "mXX-500_mA-0p25_lxy-300", "L");
    legsallt1->AddEntry(eff_s4t1, "mXX-1000_mA-5_lxy-30", "L");
    legsallt1->AddEntry(eff_s5t1, "mXX-500_mA-1.2_lxy-30", "L");
    legsallt1->Draw();
    cansallt1 -> SaveAs(Form("../outputs/plots/modules/genTriggerEfficiency/fmyeff_all_%s.pdf",T1));*/
    
}



void TriEff2mu(){
    TFile* file_1 = TFile::Open("../outputs/rootfiles/modules/genTriggerEfficiency.root");
    string trigger[3] = { "DoubleL2Mu23NoVtx_2Cha", "DoubleL2Mu25NoVtx_2Cha", "DoubleL2Mu23NoVtx_2Cha_NoL2Matched"};
    string sample[6] = { "mXX-100_mA-0p25_lxy-300", "mXX-100_mA-5_lxy-0p3", "mXX-500_mA-0p25_lxy-300", "mXX-500_mA-1p2_lxy-30", "mXX-1000_mA-5_lxy-30", "mXX-1000_mA-5_lxy-300"};
      
    TH1F *iso24_1 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-100_mA-0p25_lxy-300/iso24");
    TH1F *dimu_1 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-100_mA-0p25_lxy-300/Dimu_2");
    TH1F *eff_1 = (TH1F*) dimu_1->Clone();
    
    TH1F *iso24_2 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-100_mA-5_lxy-0p3/iso24");
    TH1F *dimu_2 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-100_mA-5_lxy-0p3/Dimu_2");
    TH1F *eff_2 = (TH1F*) dimu_2->Clone();

    TH1F *iso24_3 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-500_mA-0p25_lxy-300/iso24");
    TH1F *dimu_3 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-500_mA-0p25_lxy-300/Dimu_2");
    TH1F *eff_3 = (TH1F*) dimu_3->Clone();

    TH1F *iso24_4 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-500_mA-1p2_lxy-30/iso24");
    TH1F *dimu_4 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-500_mA-1p2_lxy-30/Dimu_2");
    TH1F *eff_4 = (TH1F*) dimu_4->Clone();

    TH1F *iso24_5 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-1000_mA-5_lxy-30/iso24");
    TH1F *dimu_5 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-1000_mA-5_lxy-30/Dimu_2");
    TH1F *eff_5 = (TH1F*) dimu_5->Clone();

    TH1F *iso24_6 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-1000_mA-5_lxy-300/iso24");
    TH1F *dimu_6 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-1000_mA-5_lxy-300/Dimu_2");
    TH1F *eff_6 = (TH1F*) dimu_6->Clone();

    TH1F *iso24_7 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-1000_mA-5_lxy-300/iso24");
    TH1F *dimu_7 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-1000_mA-5_lxy-300/Dimu_2");
    TH1F *eff_7 = (TH1F*) dimu_7->Clone();

    TH1F *iso24_8 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-1000_mA-5_lxy-300/iso24");
    TH1F *dimu_8 = (TH1F*)file_1->Get("ch2mu2e/sig/mXX-1000_mA-5_lxy-300/Dimu_3");
    TH1F *eff_8 = (TH1F*) dimu_8->Clone();



    dimu_2->SetLineColor(2);
    dimu_3->SetLineColor(3);
    dimu_4->SetLineColor(4);
    dimu_5->SetLineColor(5);
    dimu_6->SetLineColor(6);
    dimu_7->SetLineColor(7);
    dimu_8->SetLineColor(8);

    /*dimu_1->Scale(5);
    dimu_2->Scale(5);
    dimu_2->Scale();
    dimu_6->Scale(5);*/

    
    //create dR distribution
    TCanvas* candR = new TCanvas("candR");
    candR->cd();
    dimu_1->SetTitle("#DeltaR Distributions: DoubleL2Mu25NoVtx_2Cha");
    dimu_1->GetXaxis()->SetTitle("#DeltaR");
    dimu_1->GetYaxis()->SetTitle("# Events");
    dimu_1->SetAxisRange(0.0,1000,"Y");
    dimu_1->SetStats(kFALSE);
    dimu_1->Draw("hist");
    dimu_2->Draw("same, hist");
    dimu_3->Draw("same, hist");
    dimu_4->Draw("same, hist");
    dimu_5->Draw("same, hist");
    dimu_6->Draw("same, hist");
    
    TLegend *legdR = new TLegend(.8, .7, 0.9, .898);
    legdR->SetHeader("M_{xx} M_{A} L_{xy}","C"); // option "C" allows to center the header
    legdR->SetBorderSize(0);
    legdR->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    legdR->AddEntry(dimu_1, "100  0.25 300", "L");
    legdR->AddEntry(dimu_2, "100  5    0.3 ", "L");
    legdR->AddEntry(dimu_3, "500  0.25 300", "L");
    legdR->AddEntry(dimu_4, "500  1.2  30", "L");
    legdR->AddEntry(dimu_5, "1000 5    30", "L");
    legdR->AddEntry(dimu_6, "1000 5    300", "L");
    legdR->Draw();
    candR->SaveAs("../outputs/plots/modules/genTriggerEfficiency/eff_dR_distribution_DoubleL2Mu25NoVtx_2Cha.pdf");
    
    
    eff_1->Divide(iso24_1);
    eff_2->Divide(iso24_2);
    eff_2->SetLineColor(2);
    eff_2->SetMarkerColor(2);
    eff_3->Divide(iso24_3);
    eff_3->SetLineColor(3);
    eff_3->SetMarkerColor(3);
    eff_4->Divide(iso24_4);
    eff_4->SetLineColor(4);
    eff_4->SetMarkerColor(4);
    eff_5->Divide(iso24_5);
    eff_5->SetLineColor(5);
    eff_5->SetMarkerColor(5);
    eff_6->Divide(iso24_6);
    eff_6->SetLineColor(6);
    eff_6->SetMarkerColor(6);
    eff_7->Divide(iso24_7);
    eff_7->SetLineColor(7);
    eff_7->SetMarkerColor(7);
    eff_8->Divide(iso24_8);
    eff_8->SetLineColor(8);
    eff_8->SetMarkerColor(8);
    
    
    TCanvas* can1 = new TCanvas("can1");
    eff_1 -> SetTitle("Efficiency: mXX-100_mA-0p25_lxy-300");
    eff_1 -> GetXaxis()->SetTitle("#Delta R");
    eff_1 -> GetYaxis()->SetTitle("Efficiency");
    eff_1-> SetStats(kFALSE);
    eff_1 -> Draw();
    can1 -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/eff_DoubleL2Mu25NoVtx_2Cha_100-0p25-300.pdf");

    TCanvas* can2 = new TCanvas("can2");
    eff_2 -> SetTitle("Efficiency: mXX-100_mA-5_lxy-0p3");
    eff_2 -> GetXaxis()->SetTitle("#Delta R");
    eff_2 -> GetYaxis()->SetTitle("Efficiency");
    eff_2-> SetStats(kFALSE);
    eff_2 -> Draw();
    can2 -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/eff_DoubleL2Mu25NoVtx_2Cha_100-5-0p3.pdf");

    TCanvas* can3 = new TCanvas("can3");
    eff_3 -> SetTitle("Efficiency: mXX-500_mA-0p25_lxy-300");
    eff_3 -> GetXaxis()->SetTitle("#Delta R");
    eff_3 -> GetYaxis()->SetTitle("Efficiency");
    eff_3-> SetStats(kFALSE);
    eff_3 -> Draw();
    can3 -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/eff_DoubleL2Mu25NoVtx_2Cha_500-0p25-300.pdf");

    TCanvas* can4 = new TCanvas("can4");
    eff_4 -> SetTitle("Efficiency: mXX-500_mA-1p2_lxy-30");
    eff_4  -> GetXaxis()->SetTitle("#Delta R");
    eff_4 -> GetYaxis()->SetTitle("Efficiency");
    eff_4-> SetStats(kFALSE);
    eff_4 -> Draw();
    can4 -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/eff_DoubleL2Mu25NoVtx_2Cha_500-1p2-30.pdf");

    TCanvas* can5 = new TCanvas("can5");
    eff_5 -> SetTitle("Efficiency: mXX-1000_mA-5_lxy-30");
    eff_5 -> GetXaxis()->SetTitle("#Delta R");
    eff_5 -> GetYaxis()->SetTitle("Efficiency");
    eff_5-> SetStats(kFALSE);
    eff_5 -> Draw();
    can5 -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/eff_DoubleL2Mu25NoVtx_2Cha_1000-5-30.pdf");

    TCanvas* can6 = new TCanvas("can6");
    eff_6 -> SetTitle("Efficiency: mXX-1000_mA-5_lxy-300");
    eff_6 -> GetXaxis()->SetTitle("#Delta R");
    eff_6 -> GetYaxis()->SetTitle("Efficiency");
    eff_6-> SetStats(kFALSE);
    eff_6 -> Draw();
    can6 -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/eff_DoubleL2Mu25NoVtx_2Cha_1000-5-300.pdf");

    /*TCanvas* can7 = new TCanvas("can7");
    eff_6 -> SetTitle("mXX-1000_mA-5_lxy-300");
    eff_6 -> GetXaxis()->SetTitle("#Delta R");
    eff_6 -> GetYaxis()->SetTitle("Efficiency");
    eff_6 -> SetStats(kFALSE);
    eff_6 -> Draw();
    eff_7 -> Draw("same");
    eff_8 -> Draw("same");
    TLegend *legc7 = new TLegend(.6, .7, 0.9, .898);
    legc7->SetHeader("Trigger","C"); // option "C" allows to center the header
    legc7->SetBorderSize(0);
    legc7->SetLineColor(1);
    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);
    legc7->AddEntry(eff_6, "DoubleL2Mu23NoVtx_2Cha", "L");
    legc7->AddEntry(eff_7, "DoubleL2Mu25NoVtx_2Cha", "L");
    legc7->AddEntry(eff_8, "DoubleL2Mu23NoVtx_2Cha_NoL2Matched", "L");
    legc7->Draw();
    can7 -> SaveAs("../outputs/plots/modules/genTriggerEfficiency/eff_over_mXX-1000_mA-5_lxy-300.pdf");*/
}

void Triggers(){
    TFile* file_1 = TFile::Open("../outputs/rootfiles/modules/additionalTRG.root");
    TH1 *trgm = (TH1*)file_1->Get("ch4mu/sig/mXX-100_mA-0p25_lxy-300/oneTRG");
    TH1 *trge = (TH1*)file_1->Get("ch2mu2e/sig/mXX-100_mA-0p25_lxy-300/oneTRG");
    
    double bni;
    int i;
    cout<<"---------Sample: mXX-100_mA-0p25_lxy-300"<<endl;
    for(i= 0; i<301;i++){
      if (trgm->GetBinContent(i)>0 || trge-> GetBinContent(i)>0){
	cout<<i-1<<" 4mu "<<trgm->GetBinContent(i)<<" --2mu2e "<<trge->GetBinContent(i)<<endl;
      }    }
    cout<<endl;

    cout<<"-------Sample: mXX-100_mA-5_lxy-0p3"<<endl;
    TH1 *trgm1 = (TH1*)file_1->Get("ch4mu/sig/mXX-100_mA-5_lxy-0p3/oneTRG");
    TH1 *trge1 = (TH1*)file_1->Get("ch2mu2e/sig/mXX-100_mA-5_lxy-0p3/oneTRG");
    for(i= 0; i<301;i++){
	if (trgm1->GetBinContent(i)>0 || trge1-> GetBinContent(i)>0){
	  cout<<i-1<<" 4mu "<<trgm1->GetBinContent(i)<<" --2mu2e "<<trge1->GetBinContent(i)<<endl;
	}   }
    cout<<endl;
    
    cout<<"------Sample: mXX-500_mA-0p25_lxy-300"<<endl;
    TH1 *trgm2 = (TH1*)file_1->Get("ch4mu/sig/mXX-500_mA-0p25_lxy-300/oneTRG");
    TH1 *trge2 = (TH1*)file_1->Get("ch2mu2e/sig/mXX-500_mA-0p25_lxy-300/oneTRG");
    for(i= 0; i<301;i++){
	if (trgm2->GetBinContent(i)>0 || trge2-> GetBinContent(i)>0){
	  cout<<i-1<<" 4mu "<<trgm2->GetBinContent(i)<<" --2mu2e "<<trge2->GetBinContent(i)<<endl;
	}      }
    cout<<endl;
    
    cout<<"-----Sample: mXX-500_mA-1p2_lxy-300"<<endl;
    TH1 *trgm3 = (TH1*)file_1->Get("ch4mu/sig/mXX-500_mA-1p2_lxy-300/oneTRG");
    TH1 *trge3 = (TH1*)file_1->Get("ch2mu2e/sig/mXX-500_mA-1p2_lxy-300/oneTRG");
    for(i= 0; i<301;i++){
	if (trgm3->GetBinContent(i)>0 || trge3-> GetBinContent(i)>0){
	  cout<<i-1<<" 4mu "<<trgm3->GetBinContent(i)<<" --2mu2e "<<trge3->GetBinContent(i)<<endl;
	}      }
    cout<<endl;
    
    cout<<"Sample: mXX-1000_mA-5_lxy-300"<<endl;
    TH1 *trgm4 = (TH1*)file_1->Get("ch4mu/sig/mXX-1000_mA-5_lxy-300/oneTRG");
    TH1 *trge4 = (TH1*)file_1->Get("ch2mu2e/sig/mXX-1000_mA-5_lxy-300/oneTRG");
    for(i= 0; i<301;i++){
	if (trgm4->GetBinContent(i)>0 || trge4-> GetBinContent(i)>0){
	  cout<<i-1<<" 4mu "<<trgm4->GetBinContent(i)<<" --2mu2e "<<trge4->GetBinContent(i)<<endl;
	}      }
}

void Efficiency_DSA(){
  TFile* newfile = TFile::Open("../../outputs/rootfiles/modules/DSAEfficiency.root");
  TFile* oldfile = TFile::Open("../../outputs/rootfiles/modules/signalLjEfficiency.root");

  TH1 *mat4Mu = (TH1*)newfile->Get("ch4mu/sig/mXX-150_mA-0p25_lxy-300/lxyDpToMu__match");
  TH1 *tot4Mu = (TH1*)newfile->Get("ch4mu/sig/mXX-150_mA-0p25_lxy-300/lxyDpToMu__total");
  
  mat4Mu -> SetMarkerStyle(2);
  mat4Mu -> SetLineColor(2);
  mat4Mu -> SetMarkerColor(2);
  
  tot4Mu -> SetMarkerStyle(4);
  tot4Mu -> SetMarkerColor(4);
  tot4Mu -> SetLineColor(4);
  
  mat4Mu->SetStats(kFALSE);
  tot4Mu->SetStats(kFALSE);
  
  //  eff_ = Efficiency(mat4Mu, tot4Mu);

  mat4Mu->Draw();
  tot4Mu->Draw("same");
  //eff_->Draw("same");
}

void Extra_Plots()
{
  // Efficiency_newID();
  // Triggers();
  //TriEff2mu();
  //allEff();
  //mynewEff2();
  //mynewEff3();
  gen_eff();
}
