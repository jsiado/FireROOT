#!/usr/bin/env python
import os
from rootpy.io import root_open
from rootpy.plotting import Hist, Hist2D
import ROOT
import numpy as np

M_PI = ROOT.Math.Pi()
inname = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/ABCD/abcdInputTree.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/ABCD')
if not os.path.isdir(outdir): os.makedirs(outdir)


def getRegion(x, y):
    if x > M_PI/2:
        return 'A' if y>0.9 else 'B'
    else:
        return 'C' if y>0.9 else 'D'


def getValRegion(x, y):
    if getRegion(x, y) != 'B':
        return 'N'

    if x > 2.8:
        return 'A' if y>0.8 else 'B'
    else:
        return 'C' if y>0.8 else 'D'

inf = root_open(inname, 'read')

outname = os.path.join(outdir, 'abcdInputHistograms.root')
outf = root_open(outname, 'RECREATE')

leftBound = 0.5
hists1 = dict(
    A=Hist(10, M_PI/2, M_PI, type='D', name='data_A__2mu2e'),
    B=Hist(10, M_PI/2, M_PI, type='D', name='data_B__2mu2e'),
    C=Hist(10, leftBound, M_PI/2, type='D', name='data_C__2mu2e'),
    D=Hist(10, leftBound, M_PI/2, type='D', name='data_D__2mu2e'),
    valA=Hist(5, 2.8, M_PI, type='D', name='data_valA__2mu2e'),
    valB=Hist(5, 2.8, M_PI, type='D', name='data_valB__2mu2e'),
    valC=Hist(5, M_PI/2, 2.8, type='D', name='data_valC__2mu2e'),
    valD=Hist(5, M_PI/2, 2.8, type='D', name='data_valD__2mu2e'),
    blinded=Hist2D(list(np.linspace(leftBound, M_PI/2, 10, endpoint=False))+list(np.linspace(M_PI/2, M_PI, 11)), [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.92, 0.94, 0.96, 0.98, 1], type='D', name='data_blinded__2mu2e'),
    unblinded=Hist2D(list(np.linspace(leftBound, M_PI/2, 10, endpoint=False))+list(np.linspace(M_PI/2, M_PI, 11)), [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.92, 0.94, 0.96, 0.98, 1], type='D', name='data_unblinded__2mu2e'),
)
hist1Aux = dict(
    numer=Hist(list(np.linspace(leftBound, M_PI/2, 10, endpoint=False))+list(np.linspace(M_PI/2, M_PI, 11)), type='D', name='data_AC__2mu2e'),
    denom=Hist(list(np.linspace(leftBound, M_PI/2, 10, endpoint=False))+list(np.linspace(M_PI/2, M_PI, 11)), type='D', name='data_BD__2mu2e'),
    valNumer=Hist(list(np.linspace(M_PI/2, 2.8, 5, endpoint=False))+list(np.linspace(2.8, M_PI, 6)), type='D', name='data_valAC__2mu2e'),
    valDenom=Hist(list(np.linspace(M_PI/2, 2.8, 5, endpoint=False))+list(np.linspace(2.8, M_PI, 6)), type='D', name='data_valBD__2mu2e'),
)

tree1 = inf.data__2mu2e
for event in tree1:
    x, y = event.v1, event.v2
    region = getRegion(x, y)
    hists1[region].Fill(x)

    if region in list('AC'): hist1Aux['numer'].Fill(x)
    if region in list('BD'): hist1Aux['denom'].Fill(x)

    valRegion = getValRegion(x, y)
    if valRegion!='N':
        hists1['val'+valRegion].Fill(x)
        if valRegion in list('AC'): hist1Aux['valNumer'].Fill(x)
        if valRegion in list('BD'): hist1Aux['valDenom'].Fill(x)


    hists1['unblinded'].Fill(x, y)
    if region!='A':
        hists1['blinded'].Fill(x, y)

for h in hists1.values():
    h.Write()

tfratio = hist1Aux['numer'].Clone("data_TF__2mu2e")
tfratio.Divide(hist1Aux['denom'])
tfratio.Write()
valtfratio = hist1Aux['valNumer'].Clone("data_valTF__2mu2e")
valtfratio.Divide(hist1Aux['valDenom'])
valtfratio.Write()

hists2 = dict(
    A=Hist(3, M_PI/2, M_PI, type='D', name='data_A__4mu'),
    B=Hist(3, M_PI/2, M_PI, type='D', name='data_B__4mu'),
    C=Hist(3, leftBound, M_PI/2, type='D', name='data_C__4mu'),
    D=Hist(3, leftBound, M_PI/2, type='D', name='data_D__4mu'),
    valA=Hist(2, 2.8, M_PI, type='D', name='data_valA__4mu'),
    valB=Hist(2, 2.8, M_PI, type='D', name='data_valB__4mu'),
    valC=Hist(2, M_PI/2, 2.8, type='D', name='data_valC__4mu'),
    valD=Hist(2, M_PI/2, 2.8, type='D', name='data_valD__4mu'),
    blinded=Hist2D(list(np.linspace(leftBound, M_PI/2, 3, endpoint=False))+list(np.linspace(M_PI/2, M_PI, 4)), [0.5, 0.8, 0.9, 0.95, 1], type='D', name='data_blinded__4mu'),
    unblinded=Hist2D(list(np.linspace(leftBound, M_PI/2, 3, endpoint=False))+list(np.linspace(M_PI/2, M_PI, 4)), [0.5, 0.8, 0.9, 0.95, 1], type='D', name='data_unblinded__4mu'),
)
hist2Aux = dict(
    numer=Hist(list(np.linspace(leftBound, M_PI/2, 3, endpoint=False))+list(np.linspace(M_PI/2, M_PI, 4)), type='D', name='data_AC__4mu'),
    denom=Hist(list(np.linspace(leftBound, M_PI/2, 3, endpoint=False))+list(np.linspace(M_PI/2, M_PI, 4)), type='D', name='data_BD__4mu'),
    valNumer=Hist(list(np.linspace(M_PI/2, 2.8, 2, endpoint=False))+list(np.linspace(2.8, M_PI, 3)), type='D', name='data_valAC__4mu'),
    valDenom=Hist(list(np.linspace(M_PI/2, 2.8, 2, endpoint=False))+list(np.linspace(2.8, M_PI, 3)), type='D', name='data_valBD__4mu'),
)


tree2 = inf.data__4mu
for event in tree2:
    x, y = event.v1, event.v2
    region = getRegion(x, y)
    hists2[region].Fill(x)

    if region in list('AC'): hist2Aux['numer'].Fill(x)
    if region in list('BD'): hist2Aux['denom'].Fill(x)

    valRegion = getValRegion(x, y)
    if valRegion!='N':
        hists2['val'+valRegion].Fill(x)
        if valRegion in list('AC'): hist2Aux['valNumer'].Fill(x)
        if valRegion in list('BD'): hist2Aux['valDenom'].Fill(x)

    hists2['unblinded'].Fill(x, y)
    if region!='A':
        hists2['blinded'].Fill(x, y)

for h in hists2.values():
    h.Write()

tfratio = hist2Aux['numer'].Clone("data_TF__4mu")
tfratio.Divide(hist2Aux['denom'])
tfratio.Write()
valtfratio = hist2Aux['valNumer'].Clone("data_valTF__4mu")
valtfratio.Divide(hist2Aux['valDenom'])
valtfratio.Write()

outf.close()

inf.close()
