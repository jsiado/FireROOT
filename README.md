# FireROOT

## setup
```bash
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_2_14
cd CMSSW_10_2_14/src
cmsenv

git clone https://github.com/jsiado/FireROOT.git
scram b -j4
```

##  test
```bash
cd $CMSSW_BASE/src/FireROOT/Analysis/python/processing
# SR
./module_runner.py -m myworkflow -n -1&
# VR
./module_runner.py -m proxy_4mu --proxy -ch 4mu -d mc -n -1&
```

## plots
```bash
cd $CMSSW_BASE/src/FireROOT/Analysis/python/processing
# SR
./module_plotter.py -i myworkflow
# VR
./module_plotter.py -i proxy_4mu -s proxy -d mc
```
