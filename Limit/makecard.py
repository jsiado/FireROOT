import CombineHarvester.CombineTools.ch as ch
import os
import argparse
from collections import defaultdict
from rootpy.io import root_open
from SIDM.Limit.limitutils import (optimized_boundary,
                                   abcd_bin_value,
                                   closure_uncertainty,
                                   genxsec,
                                   log)
import ROOT
ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.WARNING)

CATEGORIES = [
        (0, 'A0'), (1, 'B0'), (2, 'C0'), (3, 'D0'), # channel 4mu
        (4, 'A1'), (5, 'B1'), (6, 'C1'), (7, 'D1'), # channel 2mu2e
]

parser = argparse.ArgumentParser(description="make datacard")
parser.add_argument("--channel", "-ch", type=str, default='merged', choices=['ch2mu2e', 'ch4mu', 'merged'], help='channels')
parser.add_argument("--postfix", type=str, default=None, help='postfix, will make a separate directory')
parser.add_argument("--syst", type=int, default=1, choices=[0,1], help='1: add systematics (DEFAULT), 0: no systematics')
args = parser.parse_args()

logging = log['makecard']

get_first  = lambda t: float(t.split('_')[0].split('-')[-1].replace('p', '.'))
get_second = lambda t: float(t.split('_')[1].split('-')[-1].replace('p', '.'))

###################################
# figure out the signal/obs rates #
###################################

sig_rates = defaultdict(dict)
obs_rates = defaultdict(dict)
INPUTBASE = '/uscms_data/d3/wsi/lpcdm/CMSSW_10_2_14_EGamma/src/FireROOT/Analysis/python/outputs/rootfiles'
f = root_open(os.path.join(INPUTBASE, 'centralSig/leptonIDSyst.root'))
obsf = root_open(os.path.join(INPUTBASE, 'modules/myworkflow.root'))

if args.channel in ['ch4mu', 'merged']:
    chandir = f.ch4mu
    hObs = obsf.ch4mu.data.dphiIso2D # data ABCD histogram
    for kmass in chandir.keys():
        # mXX-800_mA-1p2'
        mxx = get_first(kmass.name)
        ma = get_second(kmass.name)
        massdir = getattr(chandir, kmass.name)
        for kdist in massdir.keys():
            lxy = get_first(kdist.name)
            h = getattr(massdir, kdist.name).dphiIso2D_nominal
            h.scale( 30./genxsec[mxx] ) # scale to 30 fb
            if h.integral()==0: continue # all bin value eq 0
            xbin, ybin = optimized_boundary('4mu', (mxx, ma, lxy))
            if xbin is None or ybin is None: continue

            _binValues = abcd_bin_value(h, (xbin, ybin))
            sig_rates[kmass.name][kdist.name] = dict(zip(['A0', 'B0', 'C0', 'D0'], _binValues))
            # logging.info( str((xbin, ybin)) + str(_binValues) )

            _obsValues = abcd_bin_value(hObs, (xbin, ybin))[:3] # blind region D
            _obsValues.append(_obsValues[1]*_obsValues[2]/_obsValues[0])
            obs_rates[kmass.name][kdist.name] = dict(zip(['A0', 'B0', 'C0', 'D0'], _obsValues))


if args.channel in ['ch2mu2e', 'merged']:
    chandir = f.ch2mu2e
    hObs = obsf.ch2mu2e.data.dphiEgmIso2D # data ABCD histogram
    for kmass in chandir.keys():
        # mXX-800_mA-1p2'
        mxx = get_first(kmass.name)
        ma = get_second(kmass.name)
        massdir = getattr(chandir, kmass.name)
        for kdist in massdir.keys():
            lxy = get_first(kdist.name)
            h = getattr(massdir, kdist.name).dphiIso2D_nominal
            h.scale( 30./genxsec[mxx] ) # scale to 30 fb
            if h.integral()==0:
                logging.warning('sample - ({}, {}, {}) has 0 event in the plane.'.format(mxx, ma, lxy))
                continue # all bin value eq 0
            xbin, ybin = optimized_boundary('2mu2e', (mxx, ma, lxy))
            if xbin is None or ybin is None: continue

            _binValues = abcd_bin_value(h, (xbin,ybin))
            if kdist.name not in sig_rates[kmass.name]:
                sig_rates[kmass.name][kdist.name] = {}
            sig_rates[kmass.name][kdist.name].update( dict(zip(['A1', 'B1', 'C1', 'D1'], _binValues)) )


            _obsValues = abcd_bin_value(hObs, (xbin, ybin))[:3] # blind region D
            _obsValues.append(_obsValues[1]*_obsValues[2]/_obsValues[0])
            if kdist.name not in obs_rates[kmass.name]:
                obs_rates[kmass.name][kdist.name] = {}
            obs_rates[kmass.name][kdist.name].update( dict(zip(['A1', 'B1', 'C1', 'D1'], _obsValues)) )

obsf.close()
f.close()
#print(sig_rates)


###########################################
# writing datacard with combine harvester #
###########################################
DATACARD_DIR = 'datacards'
if args.postfix: DATACARD_DIR = 'datacards.%s' % args.postfix
if args.syst==0: DATACARD_DIR +='.nosyst'

for kmass in sig_rates:
    massproxies = list(sig_rates[kmass].keys()) # lxy-30_ctau-9p6
    for m in massproxies:
        cb = ch.CombineHarvester()
        cb.SetVerbosity(0)

        if len(sig_rates[kmass][m])==8: cats_ = CATEGORIES
        else:
            if 'A0' in sig_rates[kmass][m]: cats_ = [(0, 'A0'), (1, 'B0'), (2, 'C0'), (3, 'D0'),] # channel 4mu
            if 'A1' in sig_rates[kmass][m]: cats_ = [(0, 'A1'), (1, 'B1'), (2, 'C1'), (3, 'D1'),] # channel 2mu2e

        cb.AddObservations( ['*'], [''], ['13TeV'], [''],          cats_)
        cb.AddProcesses(    ['*'], [''], ['13TeV'], [''], ['sig'], cats_, True)
        cb.AddProcesses(    ['*'], [''], ['13TeV'], [''], ['bkg'], cats_, False)

        cb.ForEachObs(lambda x: x.set_rate(obs_rates[kmass][m][x.bin()]))
        cb.cp().process(['sig']).ForEachProc(lambda x: x.set_rate(sig_rates[kmass][m][x.bin()]))
        cb.cp().process(['bkg']).ForEachProc(lambda x: x.set_rate(1))


        if 'A0' in [x[1] for x in cats_]:
            cb.cp().process(['bkg']).bin(['A0', 'B0', 'C0']).AddSyst(cb, 'scale_$PROCESS_$BIN', 'rateParam', ch.SystMap('bin')
                    (['A0'], float(obs_rates[kmass][m]['A0']))
                    (['B0'], float(obs_rates[kmass][m]['B0']))
                    (['C0'], float(obs_rates[kmass][m]['C0']))
                )

            cb.cp().process(['bkg']).bin(['D0']).AddSyst(cb, 'scale_$PROCESS_$BIN', 'rateParam', ch.SystMap()
                    (('(@0*@1/@2)', ','.join(['scale_$PROCESS_%s0'%x for x in list('BCA')])))
                )


        if 'A1' in [x[1] for x in cats_]:
            cb.cp().process(['bkg']).bin(['A1', 'B1', 'C1']).AddSyst(cb, 'scale_$PROCESS_$BIN', 'rateParam', ch.SystMap('bin')
                    (['A1'], float(obs_rates[kmass][m]['A1']))
                    (['B1'], float(obs_rates[kmass][m]['B1']))
                    (['C1'], float(obs_rates[kmass][m]['C1']))
                )

            cb.cp().process(['bkg']).bin(['D1']).AddSyst(cb, 'scale_$PROCESS_$BIN', 'rateParam', ch.SystMap()
                    (('(@0*@1/@2)', ','.join(['scale_$PROCESS_%s1'%x for x in list('BCA')])))
                )



        if args.syst==1:
            mxx = get_first(kmass)
            ma  = get_second(kmass)
            lxy = get_first(m)

            ## luminosity
            cb.cp().process(['sig']).AddSyst(cb, 'lumi', 'lnN', ch.SystMap()(1.025))

            ## channel 4mu
            if 'A0' in [x[1] for x in cats_]:

                ### lepton ID - pfmuon
                cb.cp().process(['sig']).bin(['A0', 'B0', 'C0', 'D0']).AddSyst(
                    cb, 'lepID_4mu_pfmu', 'lnN', ch.SystMap()(1.007)
                )
                ### closure
                cb.cp().process(['bkg']).bin(['D0']).AddSyst(
                    cb, 'closure_4mu', 'lnN', ch.SystMap()(
                        1 + closure_uncertainty('4mu', optimized_boundary('4mu', (mxx, ma, lxy)))
                    )
                )

            ## channel 2mu2e
            if 'A1' in [x[1] for x in cats_]:

                ### lepton ID - electron
                cb.cp().process(['sig']).bin(['A1', 'B1', 'C1', 'D1']).AddSyst(
                    cb, 'lepID_2mu2e_electron', 'lnN', ch.SystMap()(1.0125))
                ### lepton ID - photon
                cb.cp().process(['sig']).bin(['A1', 'B1', 'C1', 'D1']).AddSyst(
                    cb, 'lepID_2mu2e_photon', 'lnN', ch.SystMap()(1.07))
                ### lepton ID - pfmuon
                cb.cp().process(['sig']).bin(['A1', 'B1', 'C1', 'D1']).AddSyst(
                    cb, 'lepID_2mu2e_pfmu', 'lnN', ch.SystMap()(1.001))
                ### closure
                cb.cp().process(['bkg']).bin(['D1']).AddSyst(
                    cb, 'closure_2mu2e', 'lnN', ch.SystMap()(
                        1 + closure_uncertainty('2mu2e', optimized_boundary('2mu2e', (mxx, ma, lxy)))
                    )
                )


        try: os.makedirs('{}/{}/{}'.format(DATACARD_DIR, args.channel, kmass))
        except: pass

        cb.WriteDatacard('{}/{}/{}/{}.txt'.format(DATACARD_DIR, args.channel, kmass, m))

