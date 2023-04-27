#include "myeff_mueta.h"
#include "myeff_ptvsdR.h"
#include "myeff_dR.h"
//#include "myeff_trioverlap.h"
#include "myeff_comblogicalOR.h"
#include "myeff_pT.h"
#include "myeff_rebinpT.h"

//run as.........
// root -l
// .L extraHelp/TrEff2mu.C 
// .x extraHelp/TrEff2mu.C (date, "muon collection") 


void TrEff2mu(int date, const char *muon)
{
	//myeff_mueta(date, muon);
	myeff_ptvsdR(date, muon);
	myeff_dR(date, muon);
	myeff_pT(date, muon);
	
	//myeff_comblogicalOR(num);
	//myeff_trioverlap(num);
	//myeff_rebinpT(num);
}
