#!/usr/bin/env python

'''generate sample sheet for central signal samples
'''
from __future__ import print_function

import json
import os
from os.path import join
from datetime import datetime

from FireROOT.Analysis.samples.makeSampleSheet import stage_out_json, total_event_number
from FireROOT.Analysis.samples.signalnumbers import genxsec, darkphotonbr
from Firefighter.ffConfig.datasetUtils import sigmc_ctau2lxy
from Firefighter.ffConfig.production.Autumn18.sigmc.central.generateyaml import (
    get_valid_datasets,
    parseSignalDataset
)

def getNtupleListFromDataJS(dn):
    f = '/publicweb/w/wsi/public/lpcdm/sigsamplemon/data.js'
    storeInfo = json.loads(open(f).read().replace('var data=', ''))['store']
    res = []
    for entry in storeInfo:
        if entry['name']==dn: #and entry['jobstatus']=="COMPLETED":
            res = entry['ntuplefiles']
            break
    return res

def getGFEFromDataJS(dn):
    '''genfilter efficiencies'''
    f = '/publicweb/w/wsi/public/lpcdm/sigsamplemon/data.js'
    storeInfo = json.loads(open(f).read().replace('var data=', ''))['store']
    res = []
    for entry in storeInfo:
        if entry['name']==dn and entry['genfiltereff']!="":
            res = [float(d) for d in entry['genfiltereff'].split('+-')]
            break
    return res



if __name__ == "__main__":

    outdir = join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/samples/store')
    shortcutdir = join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/samples/latest')
    if not os.path.isdir(outdir): os.makedirs(outdir)
    if not os.path.isdir(shortcutdir): os.makedirs(shortcutdir)


    ffntuplesColl = {'2mu2e': {}, '4mu': {}}
    scalesColl = {'2mu2e': {}, '4mu': {}}
    for d in get_valid_datasets():
        channel, mxx, ma, ctau = parseSignalDataset(d)
        lxy = sigmc_ctau2lxy(float(mxx), float(ma), float(ctau))
        key = 'mXX-{}_mA-{}_lxy-{}_ctau-{}'.format(
            mxx, ma.replace('.', 'p'), str(lxy).replace('.', 'p'), ctau.replace('.', 'p'))
        ffntuplesColl[channel][key] = getNtupleListFromDataJS(d)
        # prepare for scale
        _xsec = genxsec.get(int(mxx), 0)
        _brs = 0
        if '2e' in channel: _brs = darkphotonbr['ee'].get(float(ma),0) * darkphotonbr['mumu'].get(float(ma),0) * 2
        else: _brs = darkphotonbr['mumu'].get(float(ma),0) * darkphotonbr['mumu'].get(float(ma),0)
        _eff = getGFEFromDataJS(d)
        _eff = _eff[0] if _eff else 0

        scalesColl[channel][key] = _xsec * _brs * _eff


    for chan in ffntuplesColl:
        outfn = join(outdir, "centralSig_{}_{}.json".format(chan, datetime.now().strftime('%y%m%d')))
        shortcutfn = join(shortcutdir, 'centralSig_{}.json'.format(chan))
        stage_out_json(outfn, ffntuplesColl[chan], shortcutdir, shortcutfn)
        print('Saved to:', outfn)


    # scales
    for chan, info in scalesColl.items():
        for i, key in enumerate(info, start=1):
            print('[{} {}/{}]'.format(chan, i, len(info)))
            filelist = ffntuplesColl[chan][key]
            if not filelist or scalesColl[chan][key]==0: continue
            nevents = total_event_number(filelist)
            scalesColl[chan][key] /= nevents

    for chan in scalesColl:
        outfn = join(outdir, "centralSigScale_{}_{}.json".format(chan, datetime.now().strftime('%y%m%d')))
        shortcutfn = join(shortcutdir, 'centralSigScale_{}.json'.format(chan))
        stage_out_json(outfn, scalesColl[chan], shortcutdir, shortcutfn)
        print('Saved to:', outfn)
