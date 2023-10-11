#include "ch2mu2eTrEff_dR.h"
#include "ch2mu2eTrEff_pT.h"
#include "ch2mu2eTrEff_eta.h"
#include "ch2mu2eTrEff_d0.h"
#include "ch2mu2eTrEff_ID.h"
#include "ch2mu2eTrEff_zdlxy.h"
#include "ch2mu2eTrEff_zdpt.h"
#include "ch2mu2eTrEff_pTlxys.h"
#include "ch2mu2eTrEff_pTlxym.h"
#include "ch2mu2eTrEff_pTlxyl.h"
#include "ch2mu2eTrEff_pTlxyx.h"
//run as.........
// root -l
// .L extraHelp/TrEff2mu.C 
// .x extraHelp/TrEff2mu.C ("ID", "channel", "root_file") 
//
// ID ----> A number to differentiate plots
// root_file --> File to open and plot efficiency
// channel---> either 2mu2e or 4mu for storing the output plots

void ch2mu2eTrEff(const char *np, const char *rt, const char *ch)
{
    ch2mu2eTrEff_dR(np, rt, ch);
    ch2mu2eTrEff_pT(np, rt, ch);
    ch2mu2eTrEff_eta(np, rt, ch);
    ch2mu2eTrEff_ID(np, rt, ch);
    ch2mu2eTrEff_zdlxy(np, rt, ch);
    ch2mu2eTrEff_zdpt(np, rt, ch);
    ch2mu2eTrEff_d0(np, rt, ch);
    //ch2mu2eTrEff_pTlxys(np, rt, ch);
    //ch2mu2eTrEff_pTlxym(np, rt, ch);
    //ch2mu2eTrEff_pTlxyl(np, rt, ch);
    //ch2mu2eTrEff_pTlxyx(np, rt, ch);
}
