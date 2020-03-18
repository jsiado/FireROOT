#!/usr/bin/env python
from __future__ import print_function
import os
import math
from rootpy.io import root_open

fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/bjets.root')
f = root_open(fn)


def dumpABCD(ab, cd, val=math.pi/2):
    a = ab.integral(xbin2=ab.axis(0).FindBin(val)-1) 
    b = ab.integral(xbin1=ab.axis(0).FindBin(val)) 
    c = cd.integral(xbin2=cd.axis(0).FindBin(val)-1) 
    d = cd.integral(xbin1=cd.axis(0).FindBin(val)) 

    pred = float(b)*c/a
    syst = pred*math.sqrt(1/float(a) + 1/float(b) + 1/float(c))

    res = [
            #'A:{} | B:{} || total:{}'.format(a, b, ab.integral(overflow=True)),
            'A:{} | B:{}'.format(a, b,),
        '-'*25,
        # 'C:{} | D:{} || total:{}'.format(c, d, cd.integral(overflow=True)),
        'C:{} | D:{}'.format(c, d,),
        '+'*10,
        'obs: {} +/- {:.2f}'.format(d, math.sqrt(d)),
        'pred: {:.2f} +/- {:.2f}'.format(pred, syst),
    ]

    return '\n'.join(res)

h_sIso = f.ch4mu.data.dphi_siso
h_sIsoInv = f.ch4mu.data.dphi_sisoinv

for v in [math.pi/2, 2, 2.5]:
    print('deltaPhi={}'.format(v).center(50, '_'))
    print(dumpABCD(ab=h_sIsoInv, cd=h_sIso, val=v))


f.close()
