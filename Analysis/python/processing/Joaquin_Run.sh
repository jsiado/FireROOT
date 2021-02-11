#!/bin/bash

nohup ./module_runner.py -m MuonPtDSA -d sig -n -1 --private &> logs/MuonPtDSArun.out
nohup ./module_plotter.py -i MuonPtDSA -d mc --normsig 1 -x -1 --ymin 0 &> logs/MuonPtDSAplot.out
