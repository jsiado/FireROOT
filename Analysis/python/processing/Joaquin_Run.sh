#!/bin/bash

#dia=$(date +"%y%m%d_%H%M")
dia=$(date +"%y%m%d")
#$echo "${dia}"

nohup ./module_runner.py -m MuonPtDSA_newID -d sig -n -1 --private &> logs/MuonPtDSA_newIDRun_${dia}.out
#nohup ./module_runner.py -m ljpairDphi -d sig -n -1 --private &> logs/ljpairDphiRun_${dia}.out
#nohup ./module_runner.py -m EfficiencyDSAPt -d sig -n -1 --private &> logs/EfficiencyDSAPtRun_${dia}.out
echo "runner done."

nohup ./module_plotter.py -i MuonPtDSA_newID -d mc --normsig 1 -x -1 --ymin 0 &> logs/MuonPtDSA_newIDPlot_${dia}.out
#nohup ./module_plotter.py -i ljpairDphi -d mc --normsig 1 -x -1 --ymin 0 &> logs/ljpairDphiPlot_${dia}.out
#nohup ./module_plotter.py -i EfficiencyDSAPt -d mc --normsig 1 -x -1 --ymin 0 &> logs/EfficiencyDSAPtPlot${dia}.out
echo "plotting done"
