import json
import makeSampleSheet_v2
files = {"EOSPATH_SIG":"/store/group/lpcmetx/SIDM/TriggerStudy/newTRG/2018/CRAB_PrivateMC/", "EOSPATH_SIG2":{"2mu2e":"/store/group/lpcmetx/SIDM/TriggerStudy/newTRG/2018/CRAB_PrivateMC/"}
ds_4mu, ds_2mu2e = makeSampleSheet_v2.generate_signal_files(files)
with open("signal_4mu.json", "w") as outf:
    outf.write(json.dumps(ds_4mu, indent=4))
with open("signal_2mu2e.json", "w") as outf:
    outf.write(json.dumps(ds_2mu2e, indent=4))
