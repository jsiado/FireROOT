#!/usr/bin/env python
from __future__  import print_function
import json
import os
import shutil
import ROOT

proxydir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/samples/merged/proxy')
if not os.path.isdir(proxydir): os.makedirs(proxydir)

# shortcut = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/samples/latest/proxy_backgrounds.json')
shortcut = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/samples/latest/proxy_data2018.json')

flist = json.load(open(os.path.realpath(shortcut)))
if 'data' in os.path.basename(shortcut):
    flist = {'data': flist}



for group in flist:
    for tag in flist[group]:
        merger = ROOT.TFileMerger(ROOT.kFALSE, ROOT.kFALSE)
        merger.SetMsgPrefix('FireROOT')
        merger.SetPrintLevel(1)
        merger.AddObjectNames('ffNtuplizer')
        outname = '{}.root'.format(tag)
        merger.OutputFile(outname)
        for f in flist[group][tag]: merger.AddFile(f)
        merger.PartialMerge( ROOT.TFileMerger.kAll | ROOT.TFileMerger.kRegular | ROOT.TFileMerger.kOnlyListed )
        shutil.move(os.path.join(os.getcwd(), outname), os.path.join(proxydir, outname))
        print(tag,'] ==> ', os.path.join(proxydir, outname))

