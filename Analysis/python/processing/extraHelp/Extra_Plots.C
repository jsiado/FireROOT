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
void TriEff(){
    TFile* file_1 = TFile::Open("../outputs/rootfiles/modules/TriggerEfficiency.root");
    TH1F *tag = (TH1F*)file_1->Get("ch4mu/sig/mXX-100_mA-0p25_lxy-300/tagpt");
    TH1F *pro = (TH1F*)file_1->Get("ch4mu/sig/mXX-100_mA-0p25_lxy-300/probept");
    TH1F *eff = (TH1F*) pro->Clone();
    //eff->GetXaxis()->SetTitle("X axis title");
    // c1 = new TCanvas("c1","Efficiency",200,10,700,500);
    int i;
    for (i=0; i< 350; i++){
      if (tag->GetBinContent(i)>0)
	cout<<i<<" "<<pro->GetBinContent(i)<<" "<<tag->GetBinContent(i)<<endl;
    }
    eff->Divide(tag);
    eff->SetTitle("Efficiency");
    eff->GetXaxis()->SetTitle("pt");
    eff->GetYaxis()->SetTitle("Efficiency");
    eff->Draw();
    //canL1Pt->SaveAs("First_Lepton_Pt.png");
    eff->SaveAs("../outputs/plots/modules/TriggerEfficiency/mc_4mu_efficiency.png");
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
  TriEff();
}
