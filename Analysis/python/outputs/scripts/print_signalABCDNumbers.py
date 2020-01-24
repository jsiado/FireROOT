#!/usr/bin/env python
from __future__ import print_function
import os
from FireROOT.Analysis.Utils import *
# from rootpy.plotting import Hist, HistStack, Legend, Canvas
from rootpy.io import root_open

inname = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/signalABCDNumbers.root')

def formatABCD(h, isdata=False, ref=None):
    a = '{:.3E}'.format(h.GetBinContent(2,2))
    b = '{:.3E}'.format(h.GetBinContent(2,1))
    c = '{:.3E}'.format(h.GetBinContent(1,2))
    d = '{:.3E}'.format(h.GetBinContent(1,1))

    """
    c | a
    -----
    d | b
    """

    res = [
        'C:{} | A:{}'.format(c, a),
        '-'*25,
        'D:{} | B:{}'.format(d, b),
    ]
    if ref:
        res[0] = 'C:{} | A:{} ({:.3g}%)'.format(c, a, float(a)/ref*100)
    if isdata:
        res[0] = 'C:{} | A: BLINDED'.format(c)

    return '\n'.join(res)

f = root_open(inname)

samples = 'mXX-150_mA-0p25_lxy-300|mXX-500_mA-1p2_lxy-300|mXX-800_mA-5_lxy-300'.split('|')
samples.extend( 'mXX-100_mA-5_lxy-0p3|mXX-1000_mA-0p25_lxy-0p3'.split('|') )


CHAN = ['4mu', '2mu2e']
pointsToScan = [1, 0.1, 0.05, 0.01]
s_pointsToScan = [str(v).replace('.', 'p') for v in pointsToScan]

for ch in CHAN:
    print('#'*50)
    print(ch.center(50, ' '))
    print('#'*50)
    for s in samples:
        print(s)
        h = getattr(f, s+'__'+ch)
        print(formatABCD(h))
        print()
    print('_'*50)
    print('Background')
    print(formatABCD(sumHistStack(getattr(f, 'bkg__'+ch))))
    print('_'*50)
    print('Data')
    print(formatABCD(getattr(f, 'data__'+ch), isdata=False))

for p in s_pointsToScan:
    print('>>>', p)
    for ch in CHAN:

        print('#'*50)
        print(ch.center(50, ' '))
        print('#'*50)
        for s in samples:
            print(s)
            ref = getattr(f, s+'__'+ch).GetBinContent(2,2)
            h = getattr(f, s+'__'+ch+'__'+p)
            print(formatABCD(h, ref=ref))
            print()
        print('_'*50)
        print('Background')
        ref = sumHistStack(getattr(f, 'bkg__'+ch)).GetBinContent(2,2)
        print(formatABCD(sumHistStack(getattr(f, 'bkg__'+ch+'__'+p)), ref=ref))
        print('_'*50)
        print('Data')
        print(formatABCD(getattr(f, 'data__'+ch+'__'+p), isdata=False))
