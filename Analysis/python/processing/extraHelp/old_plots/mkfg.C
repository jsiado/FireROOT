#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TH1F.h>
#include <TMath.h>
#include "Math/LorentzVector.h"
#include "TLorentzVector.h"
#include <fstream>
#include <iostream>
#include "TF1.h"
#include <stdio.h>
#include <TCanvas.h>
#include <TRandom.h>
#include <math.h>
#include <TF1Convolution.h>
#include <TStopwatch.h>
#include "TRandom3.h"
#include <string>
 
//run as root -l mkfg.C

void trieff(){
  TEfficiency* trEff = new TEfficiency("eff","my efficiency; x; y;#epsilon", 10,0,10,20,-5,15);
  TFile* f = TFile::Open("../outputs/rootfiles/modules/ObjTrEff2pvt.root");
  
  TCanvas *can_dR = new TCanvas("can_dR","",800,600);
  TLegend *leg_ = new TLegend(.6, .1, 0.9, .298);
  leg_->SetHeader("Samples:","C");
  leg_->SetBorderSize(0);
  leg_->SetLineColor(1);
  gStyle->SetFillColor(0);
  gStyle->SetCanvasColor(10);

  char
    S1[50] = "mXX-100_mA-0p25_lxy-300",
    S2[50] = "mXX-500_mA-1p2_lxy-3",
    S3[50] = "mXX-1000_mA-5_lxy-3";
  
  TH1F *num_s1 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Num_dR",S1));
  TH1F *den_s1 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Den_dR",S1));
  if(TEfficiency::CheckConsistency(*num_s1,*den_s1)){
    trEff = new TEfficiency(*num_s1,*den_s1);
    trEff->Draw();
    trEff->SetTitle("#Delta R of muons ; #Delta R(#mu_{1},#mu_{2}); Efficiency (#epsilon)");
    leg_->AddEntry(trEff, Form("%s",S1), "l");
  }

  TH1F *num_s2 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Num_dR",S2));
  TH1F *den_s2 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Den_dR",S2));
  if(TEfficiency::CheckConsistency(*num_s2,*den_s2)){
    trEff = new TEfficiency(*num_s2,*den_s2);
    trEff->SetLineColor(kBlue);
    trEff->Draw("same");
    leg_->AddEntry(trEff, Form("%s",S2), "l");
  }
  
  TH1F *num_s3 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Num_dR",S3));
  TH1F *den_s3 = (TH1F*)f->Get(Form("ch2mu2e/sig/%s/TO_Den_dR",S3));
  if(TEfficiency::CheckConsistency(*num_s3,*den_s3)){
    trEff = new TEfficiency(*num_s3,*den_s3);
    trEff->SetLineColor(kRed);
    trEff->Draw("same");
    leg_->AddEntry(trEff, Form("%s",S3), "l");
  }

  leg_->Draw();
  can_dR->SaveAs("../outputs/plots/modules/ObjTrEff2pvt/2022_10_24_dR.png");
}

void mkfg()
{
  trieff();
}
