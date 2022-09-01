#include "dR_TrigEff.h"
#include "pT_TrigEff.h"
#include "eta_TrigEff.h"
#include "d0_TrigEff.h"
//#include "f1_ch2mu2e_Lxy.h"
//#include "f1_ch2mu2e_ss.h"
//#include "f1_ch2mu2e_mulxy.h"

//run as.........
// root -l
// .L extraHelp/TrEff2mu.C 
// .x extraHelp/TrEff2mu.C ("date", "which file", "etype") 

// file --> File to open and plot efficiency either event or object level (EveTrEff2pvt or ObjTrEff2pvt)
// date --> a number 
// etype --> either (obj or eve) for storing the outputs

void TrigEff(const char *id, const char *file, const char *etype)
{
    dR_TrigEff(id, file, etype);
    pT_TrigEff(id, file, etype);
    eta_TrigEff(id,file, etype);
    d0_TrigEff(id, file, etype);
}
