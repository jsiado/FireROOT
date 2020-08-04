# SIDM/Limit

As of the current status, SIDM use ABCD method to estimate the background. It makes use of the `rateParam` feature
of the `combine` tool and fit the signal distribution to data to set limit on 95% CL upper limit on signal strength μ.
The signal yield is proportional to the DM bound state cross section, therefore limit is translated to σ(pp->XX).
We are assuming the decay branch fraction of XX->Zd+Zd is 100%.

* I drive the `CombineHarvestor` to write datacard for each signal masspoint;
  * The backbone of the datacard follow the [Example part III](http://cms-analysis.github.io/CombineHarvester/intro3.html) from CombineHarvestor documentation.
* then print out the `combine` command which will be executed. AsympotitcLimits are fast to run, there's no problem
to run them interactively. HybridNew are more time-consuming, especially `--LHCmode LHC-limits`, it's better to
submit those jobs to CERN condor (work on lxplus)
* then use `CombineTool.py` (part of `CombineHarvestor` package) to harvest the limit result at each lifetime point,
at each quantile, to a json file per signal mass point. I have to make sure all the combine jobs output a number for
each point at each quantile, so the structure of the json is intact. Otherwise the next plotting step will fail. In
case one point is failing, I have seen two reasons: 1. for CERN condor job, it exceeds the allowed max wall time, I
will increase that setting from 1 hour to 2 hours. 2. after a certain number of trails, combine still cannot reach
the 95% CL upper limit, this mostly happens to the shortest lifetime sample, where I have the minimum signal yields
after the displacement cut, the cross section limit for that can be as high as 100-1000 pb. I would add `--rMax 3000`
into the combine command to extend the range of the signal strength for combine to explore.
* last step is to convert the numerical values in the JSON file from last step to a brazilian-style limit band. I
copy/paste the `plotLimits.py` coming with the `CombineHarvestor` package and fix some options.

In short, steps are: make datacard; run `combineTool.py`; get combine result; make plots.

1. `Combine` documentation: http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/
2. `CombineHarvestor` doc: http://cms-analysis.github.io/CombineHarvester/index.html

## setup `combine` and `CombineHarvestor`
It's better to check out their documentations to make sure. The setup instruction is mentioned in the beginning.
```bash
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_2_13
cd CMSSW_10_2_13/src
cmsenv

### COMBINE ###
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
# update to the recommended tag
cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v8.1.0
scramv1 b clean; scramv1 b # always make a clean build

### COMBINEHARVESTOR ###
cd $CMSSW_BASE/src
git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
scram b
```

if you have not done so,
```bash
git clone https://github.com/phylsix/FireROOT.git
scram b
```

## commands
```bash
python makecard.py -ch <CHANNEL> --postfix <> --syst <0/1>
python makeCombineCommand.py -d <DIR> -ch <CHANNEL> -p <MASSTAG> -M <METHOD>
python harvestor.py -d <DIR> -ch <CHANNEL> -p <MASSTAG> -M <METHOD>
```

