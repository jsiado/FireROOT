#!/usr/bin/env python
from __future__ import print_function
import os
import math
import logging
from collections import OrderedDict
import pandas as pd
from rootpy.io import root_open
from FireROOT.Analysis.Utils import *

def check_abcd(h, xbound, ybound):
    c = h.integral(1,xbound,1,ybound)
    d = h.integral(xbound+1,h.GetNbinsX(),1,ybound)
    a = h.integral(1,xbound,ybound+1,h.GetNbinsY())
    b = h.integral(xbound+1,h.GetNbinsX(),ybound+1,h.GetNbinsY())

    d_pred_val = b*c/float(a)
    d_pred_err = d_pred_val*math.sqrt(1/float(a)+1/float(b)+1/float(c))

    close = True
    if d-math.sqrt(d)>d_pred_val+d_pred_err or d+math.sqrt(d)<d_pred_val-d_pred_err: close =False

    xval = h.xedges(xbound+1)
    yval = h.yedges(ybound+1)

    msg = '[{:.2f}:{:.2f}] {:8g}{:8g}{:8g}{:8g}+/-{:.2f} | {:8.2f}+/-{:6.2f}'.format(
        xval, yval, a, b, c, d, math.sqrt(d), d_pred_val, d_pred_err,
    )

    if close: print(colorMsg(msg, OKGREEN))
    else: print(colorMsg(msg, WARNING))


def dump_abcd(h, xbound, ybound,):
    c = h.integral(1,xbound,1,ybound)
    d = h.integral(xbound+1,h.GetNbinsX(),1,ybound)
    a = h.integral(1,xbound,ybound+1,h.GetNbinsY())
    b = h.integral(xbound+1,h.GetNbinsX(),ybound+1,h.GetNbinsY())

    return dict(A=a, B=b, C=c, D=d)


def calculate_closure(d, add_close=False, add_diff=False):
    """input from output of `dump_abcd`"""
    res = {}
    d_obs = d.pop('D')
    res.update(d)
    res['D_obs'] = '{:g} +/- {:.2f}'.format(d_obs, math.sqrt(d_obs))
    a, b, c = res['A'], res['B'], res['C']
    d_pred_val = b*c/float(a)
    d_pred_err = d_pred_val*math.sqrt(1/float(a)+1/float(b)+1/float(c))
    res['D_pred'] = '{:.2f} +/- {:.2f}'.format(d_pred_val, d_pred_err)

    if add_close:
        close = True
        if d_obs-math.sqrt(d_obs)>d_pred_val+d_pred_err or \
           d_obs+math.sqrt(d_obs)<d_pred_val-d_pred_err: close =False
        res['close'] = close
    if add_diff:
        res['|d_diff|/d'] = '{:.1f}%'.format(abs(d_pred_val-d_obs)/d_obs*100)

    return res


####################
# VR 4mu
####################

fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/proxy_4mu.root')
f = root_open(fn)

# check signals
data = OrderedDict()
for k in sigTAGS:
    h = getattr(f.ch4mu.sig, k).dphiIso2Dinit
    data[k]=dump_abcd(h, 14, 8)

hd = f.ch4mu.data.dphiIso2Dinit
data['VR data']=dump_abcd(hd, 14, 8)

df = pd.DataFrame(data)
print('---  4mu')
print(df.T.round(2))


## check closure with 4 representative boundaries
closure_data = OrderedDict()
xbins = (14,16,18)
ybins = (8 ,12,16)
for x in xbins:
    for y in ybins:
        xbound, ybound = hd.xedges(x+1), hd.yedges(y+1)
        tag = '[{:.1f}pi, {:.1f}]'.format(x*0.05, ybound)
        closure_data[tag] = calculate_closure(dump_abcd(hd, x, y), add_close=False, add_diff=True)


df = pd.DataFrame(closure_data)
print('+'*79)
print(df.T)
print('_'*79)


## check yield after the displacement cut and scaling
logging.info('Scale to predicted SR yields.')
hd = f.ch4mu.data.dphiIso2D
hd.scale(84.2/hd.integral())
xybins = [(19, 8), (19, 10), (19, 12)]
closure_data = OrderedDict()
for x_, y_ in xybins:
    xbound, ybound = hd.xedges(x_+1), hd.yedges(y_+1)
    tag = '[{:.2f}pi, {:.2f}]'.format(x_*0.05, ybound)
    closure_data[tag] = calculate_closure(dump_abcd(hd, x_, y_), add_close=False, add_diff=False)
logging.info('Dumping yields in ABCD bins.')
df = pd.DataFrame(closure_data)
print('+'*79)
print(df.T)
print('_'*79)

f.close()


####################
# VR 2mu2e
####################

fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/proxy/proxy_2mu2e.root')
f = root_open(fn)

# check signal contamination
data = OrderedDict()
for k in sigTAGS:
    h = getattr(f.ch2mu2e.sig, k).dphiIso2Dinit
    data[k]=dump_abcd(h, 14, 4)

hd = f.ch2mu2e.data.dphiIso2Dinit
data['VR data']=dump_abcd(hd, 14, 4)

df = pd.DataFrame(data)
print('---  2mu2e')
print(df.T.round(2))

## check closure with 4 representative boundaries
closure_data = OrderedDict()
xbins = (14,16,18)
ybins = ( 2, 4, 6)
for x in xbins:
    for y in ybins:
        xbound, ybound = hd.xedges(x+1), hd.yedges(y+1)
        tag = '[{:.1f}pi, {:.2f}]'.format(x*0.05, ybound)
        closure_data[tag] = calculate_closure(dump_abcd(hd, x, y), add_close=False, add_diff=True)


df = pd.DataFrame(closure_data)
print('+'*79)
print(df.T)
print('_'*79)
f.close()
