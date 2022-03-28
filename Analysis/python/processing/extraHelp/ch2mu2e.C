#include "f1_ch2mu2e.h"
//#include "myeff_ptvsdR.h"
//#include "myeff_dR.h"
//#include "myeff_trioverlap.h"
//#include "myeff_comblogicalOR.h"

//run as.........
// root -l
// .L extraHelp/TrEff2mu.C 
// .x extraHelp/TrEff2mu.C (date, "muon collection") 




void ch2mu2e(const char *date)
{
	//myeff_mueta(date, muon);
	f1_ch2mu2e(date);
	//myeff_dR(date, muon);
	//myeff_pT(date, muon);
	
	//myeff_comblogicalOR(num);
	//myeff_trioverlap(num);
	//myeff_rebinpT(num);
}
