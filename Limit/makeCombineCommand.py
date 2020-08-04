#!/usr/bin/env python
from __future__ import print_function
import os
import argparse

parser = argparse.ArgumentParser(description="Make Combine commands.")
parser.add_argument("--dir", "-d", type=str, help='datacard directory')
parser.add_argument("--channel", "-ch", type=str, default='merged', choices=['ch2mu2e', 'ch4mu', 'merged'], help='channels')
parser.add_argument("--masspoint", "-p", default=None, type=str, help='mass parameter point')
parser.add_argument("--method", "-M", type=str, default='HybridNew', choices=['HybridNew', 'Asymptotic'], help='combine method - HybridNew (DEFAULT), Asymptotic')
parser.add_argument("--mxx", default=None, type=str, help='mxx')
args = parser.parse_args()

get_first = lambda t: float(t.split('_')[0].split('-')[-1].replace('p', '.'))



if __name__ == "__main__":


    DATACARD_DIR = args.dir
    assert DATACARD_DIR and os.path.isdir(DATACARD_DIR)

    os.chdir('%s/%s' % (DATACARD_DIR, args.channel) )
    cwd = os.getcwd()

    for kmass in os.listdir('.'):
        if args.mxx and not kmass.startswith('mXX-%s_'%args.mxx): continue
        if args.masspoint and kmass != args.masspoint: continue
        if not os.path.isdir(kmass): continue
        os.chdir(kmass)
        dataCards = [f.replace('.txt', '') for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.txt')]
        dataCards.sort(key=get_first)

        for i, c in enumerate(dataCards):
            ctau = c.rsplit('-',1)[-1].replace('p', '.')
            dcpath = os.path.join(DATACARD_DIR, args.channel, kmass, c+'.txt')

            if args.method == 'Asymptotic':
                cmd = 'combineTool.py -M AsymptoticLimits -d {} -n .limit -m {} -s -1 --cminDefaultMinimizerStrategy=0 --there &'.format(dcpath, ctau)
                print(cmd)

            if args.method == 'HybridNew':
                quantiles = ('', '0.025', '0.16', '0.5', '0.84', '0.975')
                for q in quantiles:
                    cmd = 'combineTool.py'
                    # if get_first(c)==0.3 and not( kmass.startswith('mXX-150') or kmass.startswith('mXX-200') ):
                    #     cmd += ' -H AsymptoticLimits'

                    #################### exceptions found ####################
                    if kmass=='mXX-200_mA-5' and c=='lxy-0p3_ctau-0p2':
                        cmd += ' --rMax 3000'

                    if kmass=='mXX-500_mA-1p2' and c=='lxy-0p3_ctau-0p019':
                        cmd = cmd.replace('-H AsymptoticLimits', '--rMax 1000')
                    # if kmass=='mXX-150_mA-1p2' and c=='lxy-0p3_ctau-0p064':
                    #     cmd += ' --rMax 5000'
                    #########################################################

                    cmd += ' -M HybridNew -d {} -n .limit -m {} -s -1 --there'.format(dcpath, ctau)
                    if q != '': cmd += ' --expectedFromGrid={}'.format(q)
                    # cmd += ' >/dev/null 2>&1'
                    cmd += ' &'

                    print(cmd)
        os.chdir(cwd)



    # notes to myself
    # mXX-200-mA-5: first point, add --rMax 3000
