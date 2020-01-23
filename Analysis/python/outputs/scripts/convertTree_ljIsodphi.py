#!/usr/bin/env python
import os
from rootpy.io import root_open
from rootpy.tree import Tree
import ROOT

inname = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/ljIsodphi.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/ABCD')

if not os.path.isdir(outdir): os.makedirs(outdir)

inf = root_open(inname, 'read')

outname = os.path.join(outdir, 'abcdInputTree.root')
outf = root_open(outname, 'RECREATE')

tree1 = Tree('data__2mu2e')
tree1.create_branches({'v1': 'F', 'v2': 'F',})

tree2 = Tree('data__4mu')
tree2.create_branches({'v1': 'F', 'v2': 'F',})

x, y = ROOT.double(), ROOT.double()
g = getattr(inf, 'data__2mu2e__isodphi')
for i in range(g.GetN()):
    g.GetPoint(i, x, y)
    tree1.v1 = x
    tree1.v2 = 1-y
    tree1.fill()

g = getattr(inf, 'data__4mu__isodphi')
for i in range(g.GetN()):
    g.GetPoint(i, x, y)
    tree2.v1 = x
    tree2.v2 = 1-y
    tree2.fill()

tree1.write()
tree2.write()

outf.close()

inf.close()
