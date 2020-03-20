#!/usr/bin/env python
from __future__ import print_function
import os
import math
from rootpy.io import root_open


sampleSig = 'mXX-150_mA-0p25_lxy-300|mXX-500_mA-1p2_lxy-300|mXX-800_mA-5_lxy-300'.split('|')
sampleSig.extend( 'mXX-100_mA-5_lxy-0p3|mXX-1000_mA-0p25_lxy-0p3'.split('|') )

fn_2mu2e = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/val2mu2e.root')
fn_4mu   = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/bjets.root')
f_2mu2e, f_4mu = root_open(fn_2mu2e), root_open(fn_4mu)

def dumpABCD(ab, cd, val=math.pi/2, isdata=False):
    a = ab.integral(xbin2=ab.axis(0).FindBin(val)-1) 
    b = ab.integral(xbin1=ab.axis(0).FindBin(val)) 
    c = cd.integral(xbin2=cd.axis(0).FindBin(val)-1) 
    d = cd.integral(xbin1=cd.axis(0).FindBin(val)) 

    res = [
        'A:{:.2g} | B:{:.2g}'.format(a, b),
        '-'*25,
        'C:{:.2g} | D:{:.2g}'.format(c, d),
    ]
    if isdata:
        # res[2] = 'C:{:.2g} | D: BLINDED'.format(c)
        res.append('pred: {:.2f} +/- {:.2f}'.format(b*c/a, b*c/a*math.sqrt(1/a+1/b+1/c)))
        res.append('obs: {} +/- {:.2f}'.format(d, math.sqrt(d)))

    return '\n'.join(res)

def checkAll(dphiCut=math.pi/2, channel='both'):
    assert(dphiCut>0 and dphiCut<math.pi)
    assert(channel in ['both', '4mu', '2mu2e'])

    if channel=='both' or channel=='4mu':
        print('#'*50)
        print('channel: 4mu'.center(50, ' '))
        print('#'*50)
        for s in sampleSig:
            h_sIso = getattr(f_4mu.ch4mu.sig, s).dphi_siso
            h_sIsoInv = getattr(f_4mu.ch4mu.sig, s).dphi_sisoinv
            print('>>', s)
            print(dumpABCD(ab=h_sIsoInv, cd=h_sIso, val=dphiCut))
            print()
        
        print('_'*50)
        h_sIso = f_4mu.ch4mu.data.dphi_siso
        h_sIsoInv = f_4mu.ch4mu.data.dphi_sisoinv
        print('>> data')
        print(dumpABCD(ab=h_sIsoInv, cd=h_sIso, val=dphiCut, isdata=True))
    
    if channel=='both':
        print('\n\n\n')
        
    if channel=='both' or channel=='2mu2e':
        print('#'*50)
        print('channel: 2mu2e'.center(50, ' '))
        print('#'*50)
        for s in sampleSig:
            h_sIso = getattr(f_2mu2e.ch2mu2e.sig, s).dphi_siso
            h_sIsoInv = getattr(f_2mu2e.ch2mu2e.sig, s).dphi_sisoInv
            print('>>', s)
            print(dumpABCD(ab=h_sIsoInv, cd=h_sIso, val=dphiCut))
            print()
        
        print('_'*50)
        h_sIso = f_2mu2e.ch2mu2e.data.dphi_siso
        h_sIsoInv = f_2mu2e.ch2mu2e.data.dphi_sisoInv
        print('>> data')
        print(dumpABCD(ab=h_sIsoInv, cd=h_sIso, val=dphiCut, isdata=True))

checkAll()

f_2mu2e.close()
f_4mu.close()
