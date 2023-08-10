#include "allTrEff.h"
#include "TEffpT.h"
#include "TEffeta.h"
#include "TEffd0.h"
#include "TEffpl.h"
#include "TEffdiffd0dR.h"
#include "TEffdiffd0pT.h"
#include "TEFirstBin.h"
#include "TEffLxy.h"

//run as.........
// root -l
// .L extraHelp/TrEff2mu.C 
// .x extraHelp/TrEff2mu.C ("date", "which file", "etype") 
//
// file --> File to open and plot efficiency either event or object level (EveTrEff2pvt or ObjTrEff2pvt)
// date --> a number 
// etype --> either (obj or eve) for storing the outputs

void effTE(const char *rf, const char *ch, const char *var)
{
    allTrEff(rf, ch, var);
    //  TEffpT(id, ch);
    //TEffeta(id);
    //    TEffd0(id, ch);
    //TEffpl(id);
//    TEffdiffd0dR(id);
//    TEffdiffd0pT(id);
//    TEFirstBin(id);
//	TEffLxy(id, ch);
}
