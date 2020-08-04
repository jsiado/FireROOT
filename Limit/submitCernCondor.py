#!/usr/bin/env python
import os
import sys
import subprocess
import argparse
from glob import glob


CMSSW_BASE = os.environ['CMSSW_BASE']
USER       = os.environ['USER']
HOME       = os.environ['HOME']

parser = argparse.ArgumentParser()
parser.add_argument("--dir", "-d", dest='DIR', type=str, help='datacard directory')
parser.add_argument("--channel", "-ch", dest='CHANNEL', type=str, default='merged', choices=['ch2mu2e', 'ch4mu', 'merged'], help='channels')
parser.add_argument("--masspoint", "-p", dest='MASSPOINT', default=None, type=str, help='mass parameter point')
parser.add_argument('--use-proxy', dest='PROXY', action='store_true', help='whether to ship the GRID certificate with the jobs')
parser.add_argument("--method", "-M", dest='METHOD', type=str, default='HybridNew', choices=['HybridNew', 'Asymptotic'], help='combine method - HybridNew (DEFAULT), Asymptotic')
parser.add_argument('--flavour', "-F", dest='FLAVOUR', default='microcentury',
                    choices=['espresso', 'microcentury', 'longlunch', 'workday', 'tomorrow', 'testmatch', 'nextweek'],
                    help='which condor job flavour to use\n'+\
"""
espresso     = 20 minutes
microcentury = 1 hour (DEFAULT)
longlunch    = 2 hours
workday      = 8 hours
tomorrow     = 1 day
testmatch    = 3 days
nextweek     = 1 week
""")
args = parser.parse_args()

METHOD = args.METHOD
FLAVOUR = args.FLAVOUR


###############################
#### BUILD INPUT ARGUMENTS ####
###############################
os.chdir(CMSSW_BASE+'/src/SIDM/Limit')
CARDDIR = '{}/{}'.format(args.DIR, args.CHANNEL)
if args.MASSPOINT: CARDS = glob(CARDDIR+'/{}/*.txt'.format(args.MASSPOINT))
else:             CARDS = glob(CARDDIR+'/*/*.txt')
ArgsList = []
for i, card in enumerate(sorted(CARDS, key=lambda c: float(os.path.basename(c).split('_')[0].split('-')[-1].replace('p', '.')))):
    CTAU = card.rsplit('-',1)[-1].replace('.txt', '').replace('p', '.')
    if METHOD == 'Asymptotic':
        ArgsList.append('-M AsymptoticLimits -d {} -n .limit -m {} --cminDefaultMinimizerStrategy=0 --there'.format(card, CTAU))

    elif METHOD == 'HybridNew':
        argPart = '-M HybridNew -d {} -n .limit -m {} -s -1 --there'.format(card, CTAU)
        if i==0: argPart += ' --rMax=3000'
        for quantile in ('', '0.025', '0.16', '0.5', '0.84', '0.975'):
            if quantile == '':
                ArgsList.append(argPart)
            else:
                ArgsList.append('{} --expectedFromGrid={}'.format(argPart, quantile))


condorExecutable = '''\
#!/bin/bash
export SCRAM_ARCH='slc7_amd64_gcc700'
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd {CMSSW_BASE}/src/
eval `scramv1 runtime -sh`
cd SIDM/Limit/
combineTool.py $@
'''

condorSubmit = '''\
universe               = vanilla
executable             = condorExecutable.sh
getenv                 = True
'''
condorSubmitAdd = '''\
output                 = logs/run{runNum}/{logname}_{index}.out
log                    = logs/run{runNum}/{logname}_{index}.log
error                  = logs/run{runNum}/{logname}_{index}.err
arguments              = {ARGS}
{proxy_literal}
should_transfer_files  = NO
+JobFlavour            = "{flavour}"
queue 1
'''

###########################
### Submit and run jobs ###
###########################

if args.PROXY:
    # prepare the grid certificate
    proxy = '{HOME}/private/.proxy'.format(**locals())
    if not os.path.isfile(proxy) or\
        int( subprocess.check_output(
            'echo $(expr (date +%s) - $(date +%s -r {}) )'.format(proxy),
            shell=True) ) > 6*3600:
        print('GRID certificate not found or older than 6 hours, a new one need to be created.')
        subprocess.call('voms-proxy-init --voms cms --valid 168:00 -out {}'.format(proxy), shell=True)

    # export the environment variable related to the certificate
    os.environ['X509_USER_PROXY'] = proxy

    PROXY_LITERAL = 'x509userproxy = $ENV(X509_USER_PROXY)\nuse_x509userproxy = true'

else:
    PROXY_LITERAL = '#'

# make the log directory
try: os.makedirs('logs')
except: pass

executableName = 'condorExecutable.sh'
open(executableName, 'w').write(condorExecutable.format(**locals()))

# get the number of run* directories, and make the next one
numberOfExistingRuns = len([rundir for rundir in os.listdir('logs') if rundir.startswith('run')])
runNum = numberOfExistingRuns+1
os.makedirs('logs/run{}'.format(runNum))

# make the submit file
submitName = 'condorSubmit'
for index, ARGS in enumerate(ArgsList):
    condorSubmit += condorSubmitAdd.format(runNum=runNum,
                                           logname = 'combine{}'.format(METHOD),
                                           index =index,
                                           ARGS = ARGS,
                                           flavour = FLAVOUR,
                                           proxy_literal = PROXY_LITERAL,)
open(submitName, 'w').write(condorSubmit)
print(' {} '.format(executableName).center(80, '#'))
print(open(executableName).read())
print(' COMBINE COMMANDS '.center(80, '#'))
# print(open(submitName).read())
for _ in ArgsList: print('combineTool.py '+_)

if raw_input('Does this seem good? [Y/n]').lower() in ['', 'y', 'yes']:
    print('Okay, submit')
else:
    sys.exit('No? exiting.')

subprocess.call('chmod +x {}'.format(executableName), shell=True)
subprocess.call('condor_submit {}'.format(submitName), shell=True)
subprocess.call('cp {} {} logs/run{}'.format(executableName, submitName, runNum), shell=True)
subprocess.call('rm {}'.format(submitName), shell=True)
