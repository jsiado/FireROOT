//#include "f1_ch2mu2e_dR.h"
#include "OTe_ch2mu2e_pT.h"
//#include "f1_ch2mu2e_eta.h"
//#include "f1_ch2mu2e_Lxy.h"
//#include "f1_ch2mu2e_ss.h"
//#include "f1_ch2mu2e_mulxy.h"
//#include "f1_ch2mu2e_addplots.h"

//#include "myeff_ptvsdR.h"
//#include "myeff_dR.h"
//#include "myeff_trioverlap.h"
//#include "myeff_comblogicalOR.h"

//run as.........
// root -l
// .L extraHelp/TrEff2mu.C 
// .x extraHelp/TrEff2mu.C (date, "muon collection") 


void OTech2mu2e(const char *date)
{
	//f1_ch2mu2e_dR(date, filter);
	OTe_ch2mu2e_pT(date);
	//f1_ch2mu2e_eta(date, filter);
	//f1_ch2mu2e_mulxy(date);
	//f1_ch2mu2e_addplots(date, filter);
	//f1_ch2mu2e_Lxy(date, samp);
	//f1_ch2mu2e_ss(date, samp);
}
