#include "el_dR_ch2mu2eTrEff.h"
#include "el_pT_ch2mu2eTrEff.h"
#include "el_eta_ch2mu2eTrEff.h"
#include "el_d0_ch2mu2eTrEff.h"
//#include "f1_ch2mu2e_Lxy.h"
//#include "f1_ch2mu2e_ss.h"
//#include "f1_ch2mu2e_mulxy.h"

//run as.........
// root -l
// .L extraHelp/TrEff2mu.C 
// .x extraHelp/TrEff2mu.C (date, "muon collection") 


void el_ch2mu2eTrEff(const char *date, const char *filter, const char *muon)
{
	el_dR_ch2mu2eTrEff(date, filter, muon);
	//el_pT_ch2mu2eTrEff(date, filter, muon);
	//el_eta_ch2mu2eTrEff(date, filter, muon);
	//el_d0_ch2mu2eTrEff(date, filter, muon);
}
