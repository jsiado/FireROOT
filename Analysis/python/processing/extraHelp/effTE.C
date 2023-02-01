#include "TEffdR.h"
#include "TEffpT.h"
#include "TEffeta.h"
#include "TEffd0.h"

//run as.........
// root -l
// .L extraHelp/TrEff2mu.C 
// .x extraHelp/TrEff2mu.C ("date", "which file", "etype") 

// file --> File to open and plot efficiency either event or object level (EveTrEff2pvt or ObjTrEff2pvt)
// date --> a number 
// etype --> either (obj or eve) for storing the outputs

void effTE(const char *id)
{
	TEffdR(id);
	TEffpT(id);
	//TEffeta(id);
	//TEffd0(id);
	//TEffalldR(id);
}