#!/usr/bin/env python
from __future__ import print_function
import argparse
import json
import shutil
import os
from SIDM.Limit.limitutils import log

parser = argparse.ArgumentParser(description="limit harvestor.")
parser.add_argument("--dir", "-d", type=str, help='datacard directory')
parser.add_argument("--channel", "-ch", type=str, default='merged', choices=['ch2mu2e', 'ch4mu', 'merged'], help='channels')
parser.add_argument("--masspoint", "-p", type=str, help='mass parameter point')
parser.add_argument("--method", "-M", type=str, default='HybridNew', choices=['HybridNew', 'Asymptotic'], help='combine method - HybridNew (DEFAULT), Asymptotic')
parser.add_argument("--xsec", "-x", default=30., type=float, help='orignal cross section')
args = parser.parse_args()


if __name__ == '__main__':


    logging = log['harvestor']

    DATACARD_DIR = args.dir
    assert DATACARD_DIR and os.path.isdir(DATACARD_DIR)

    DATACARDCHANNEL_DIR = DATACARD_DIR+'/'+args.channel

    cwd = os.getcwd()
    os.chdir('%s/%s' % (DATACARDCHANNEL_DIR, args.masspoint))


    ###########################################
    #             collect limit               #
    ###########################################

    cmd = 'combineTool.py -M CollectLimits higgsCombine.limit.%s*.root -o %s.limits.json' % (args.method, args.method)
    logging.info('Collect limit: %s' % cmd)
    os.system(cmd)


    ###########################################
    #              scale limit                #
    ###########################################

    LIMIT_JSON = '%s.limits.json' % args.method
    LIMIT_ORIG = '%s.limits.orig.json' % args.method

    if os.path.isfile(LIMIT_ORIG):
        logging.info('orignal limits found, using **%s**.' % LIMIT_ORIG)
        limits = json.load(open(LIMIT_ORIG))
    else:
        limits = json.load(open(LIMIT_JSON))

    # logging.info('Dump limits before scale (30fb)')
    # print(json.dumps(limits, indent=4))

    for kCTau in limits:
        ## scaling, such that the limit is on signal strength as if the xsec is 1pb
        scaled = {}
        for k, v in limits[kCTau].items():
            scaled[k] = v * args.xsec / 1000

        limits[kCTau] = scaled

    # logging.info('Dump limits after scale (1pb)')
    # print(json.dumps(limits, indent=4))

    # copy original limits.json to a different file
    if not os.path.isfile(LIMIT_ORIG):
        logging.info('Back up %s ==> %s' % (LIMIT_JSON, LIMIT_ORIG))
        shutil.copy(LIMIT_JSON, LIMIT_ORIG)

    # dump the fixed limits.json
    logging.info('Write the updated one to: %s' % LIMIT_JSON)
    with open(LIMIT_JSON, 'w') as outf:
        outf.write(json.dumps(limits, indent=4))

    cmd = 'diff -y %s %s' % (LIMIT_ORIG, LIMIT_JSON)
    logging.info('$ '+cmd)
    os.system(cmd)
    print()

    # remove combine_logger.out
    if os.path.isfile('combine_logger.out'):
        logging.info('Delete combine_logger.out')
        os.remove('combine_logger.out')

    os.chdir(cwd)


    ###########################################
    #              making plot                #
    ###########################################

    logging.info('Generating plots')
    output_dir = os.path.join(DATACARD_DIR.replace('datacards', 'limitplots'), args.channel,)
    try: os.makedirs(output_dir)
    except: pass
    output_fn = '%s__%s' % (args.method, args.masspoint)
    cmd = 'python plotLimits.py --input %s -o %s -p %s' % (os.path.join(DATACARDCHANNEL_DIR, args.masspoint, LIMIT_JSON),
                                                           os.path.join(output_dir, output_fn),
                                                           args.masspoint)
    logging.info('$ '+cmd)
    os.system(cmd)