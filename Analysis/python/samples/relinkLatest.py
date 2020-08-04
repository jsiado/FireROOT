#!/usr/bin/python
""" python relinkLatest.py -f signal_2mu2e signal_2mu2e_scale -d 200522
"""
from __future__ import print_function
import argparse, os

parser = argparse.ArgumentParser(description="re-link latest shortcuts.")
parser.add_argument("--file", "-f",  type=str, nargs='*', help='softlinks to be redirected')
parser.add_argument("--date", "-d",  type=str, nargs=1, help='date version')
args = parser.parse_args()

SOFTLINK_BASE = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/samples/latest')
STORE_BASE = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/samples/store')





if __name__ == '__main__':
    for f in args.file:
        f_fullpath = os.path.join(SOFTLINK_BASE, '{}.json'.format(f))
        dest = os.path.join(STORE_BASE, '{}_{}.json'.format(f, args.date[0]))
        if not os.path.isfile(dest):
            print('{}_{}.json'.format(f, args.date[0])+' not found in:\n'+f_fullpath)
            print('Available choices are:')
            choices = []
            for file in os.listdir(STORE_BASE):
                if not file.endswith('.json'): continue
                filebasename, dateversion = file.replace('.json', '').rsplit('_',2)
                if f!=filebasename: continue
                choices.append(dateversion)
            print(choices)
            continue

        if os.path.islink(f_fullpath): os.remove(f_fullpath)
        os.chdir(SOFTLINK_BASE)
        os.symlink(os.path.relpath(dest, SOFTLINK_BASE), os.path.basename(f_fullpath))

