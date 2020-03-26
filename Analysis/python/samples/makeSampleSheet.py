#!/usr/bin/env python
"""generate data sample list, until proper sample management tool show up.
"""

from __future__ import print_function
import argparse
import json
import os
from datetime import datetime
from os.path import basename, join, relpath
from multiprocessing import Pool, TimeoutError

from rootpy.io import root_open
from FireROOT.Analysis.samples.eospaths import *
from FireROOT.Analysis.commonhelpers import eosfindfile, eosls


def list_files(dir, pattern=None):
    """
    wrapper of `eos find` subcommand to list files recursively, excluding failed crab job output

    :param str dir: eos directory
    :param str pattern: restrict pattern of file names
    :return: a list of file names
    :rtype: list
    """
    return [f for f in eosfindfile(dir, pattern=pattern) if f and "/failed" not in f]


def last_submit_timestamp(parentPathOfTimestamps):
    timestamps = eosls(parentPathOfTimestamps)
    last_ts = sorted(timestamps, key=lambda x: datetime.strptime(x, "%y%m%d_%H%M%S"))[-1]
    return datetime.strptime(last_ts, "%y%m%d_%H%M%S")


def latest_files(parentPathOfTimestamps, pattern=None):
    """
    list file names of latest batch job submission

    :param str parentPathOfTimestamps: eos directory up to timestamp level
    :param str pattern: restrict pattern of file names
    :return: a list of file names
    :rtype: list
    """
    try:
        timestampdirs = eosls(parentPathOfTimestamps)
        timestampdirs = sorted(timestampdirs, key=lambda x: datetime.strptime(x, "%y%m%d_%H%M%S"))
        latest = join(parentPathOfTimestamps, timestampdirs[-1])

        return list_files(latest, pattern=pattern)
    except Exception as e:
        print(e)
        print("Error when stat eos path: {}! Empty list returned".format(parentPathOfTimestamps))
        return []


def generate_data_files(filedict=EOSPATHS_DATA):
    print("[generate_data_files()]")
    return {k: latest_files(v) for k, v in filedict.items()}


def generate_background_files(eospathdict=EOSPATHS_BKG, forscale=False):
    print("[generate_background_files(forscale={})]".format(forscale))
    _dirmap = eospathdict
    if forscale:
        _dirmap = EOSPATHS_BKGAOD

    ## get max(latest) timestamp
    ## Note: for scale, it will scan AOD skim submissions, we do not put limit on
    ## submission timestamps as it can span over a longer time.
    if forscale is False:
        timestamps = []
        for group in _dirmap:
            for tag in _dirmap[group]:
                for path in _dirmap[group][tag]:
                    timestamps.append(sorted(eosls(path), key=lambda x: datetime.strptime(x, "%y%m%d_%H%M%S"))[-1])
        maxts = sorted(timestamps, key=lambda x: datetime.strptime(x, "%y%m%d_%H%M%S"))[-1]
        maxts = datetime.strptime(maxts, "%y%m%d_%H%M%S")

    generated = dict()
    for group in _dirmap:
        generated[group] = {}
        for tag in _dirmap[group]:
            generated[group][tag] = []
            for path in _dirmap[group][tag]:
                # if forscale is False:
                #     if (maxts - last_submit_timestamp(path)).seconds > 60*60: continue
                generated[group][tag].extend(latest_files(path, pattern='*ffNtuple*.root'))

    return generated


def remove_empty_file(filepath):
    """given a file, if the tree has non-zero number of events, return filepath"""
    try:
        f = root_open(filepath)
        t = f.ffNtuplizer.ffNtuple
        return filepath if t.get_entries() else None
    except:
        return None


def remove_empty_files(filelist):
    """given a list of files, return all files with a tree of non-zero number of events"""
    pool = Pool(processes=12)
    res = pool.map(remove_empty_file, filelist)
    res = [f for f in res if f]
    pool.close()
    return res


def clean_background_files(filedict):
    """parse all background files, remove empty tree files
    """
    print("[clean_background_files]")
    cleaneddict = filedict
    for i, group in enumerate(cleaneddict, start=1):
        print("[{}/{}] {}".format(i, len(cleaneddict), group))
        for tag in cleaneddict[group]:
            files = cleaneddict[group][tag]
            cleaneddict[group][tag] = remove_empty_files(files)
    return cleaneddict


def processed_genwgt_sum(ntuplefile):
    """Given a ntuplefile path, return the sum of gen weights."""
    import uproot
    f_ = uproot.open(ntuplefile)
    key_ = f_.allkeys(filtername=lambda k: k.endswith(b"weight"))
    if key_:
        key_ = key_[0]
        return f_[key_]['weight'].array().sum()
    else:
        key_ = f_.allkeys(filtername=lambda k: k.endswith(b"history"))[0]
        return f_[key_].values[3]  # 0: run, 1: lumi, 2: events, 3: genwgtsum


def total_genwgt_sum(filelist):
    """Given a list of ntuple files, return the total sum of gen weights"""
    pool = Pool(processes=12)
    res = pool.map(processed_genwgt_sum, filelist)
    pool.close()
    return sum(res)


def generate_background_scale(filedict):
    """parse all files to get number of events processed => scale
        scale = xsec/#genwgtsum, scale*lumi-> gen weight
    """
    from FireROOT.Analysis.samples.xsecs import BKG_XSEC

    generated = dict()
    print('[generate_background_scale]')
    for i, group in enumerate(filedict, start=1):
        print("[{}/{}] {}".format(i, len(filedict), group))
        generated[group] = {}

        for tag in filedict[group]:
            xsec = BKG_XSEC[group][tag]
            sumgenwgt = total_genwgt_sum(filedict[group][tag])
            try:
                generated[group][tag] = xsec / sumgenwgt
            # nevents = total_event_number(filedict[group][tag])
            # generated[group][tag] = xsec / nevents
            except ZeroDivisionError:
                print(group, tag, 'has zero sum gen weight, scale set as 0')
                generated[group][tag] = 0

    return generated


def generate_signal_files(filedicts):
    """generate private signal file list json"""
    print("[generate_signal_files]")

    EOSPATH_SIG, EOSPATH_SIG2 = filedicts

    paramsubdirs = eosls(EOSPATH_SIG)
    json_4mu, json_2mu2e = {}, {}
    for subdir in paramsubdirs:
        if 'MDp-0p8' in subdir or 'MDp-2p5' in subdir:
            continue # skipping unrequested darkphoton mass points

        if '4Mu' in subdir:
            key = subdir.replace('SIDM_BsTo2DpTo4Mu_', '').split('_ctau')[0]\
                        .replace('MBs', 'mXX').replace('MDp', 'mA')
            key += '_lxy-300' # mXX-1000_mA-0p25_lxy-300
            json_4mu[key] = latest_files(join(EOSPATH_SIG, subdir))
        if '2Mu2e' in subdir:
            key = subdir.replace('SIDM_BsTo2DpTo2Mu2e_', '').split('_ctau')[0]\
                        .replace('MBs', 'mXX').replace('MDp', 'mA')
            key += '_lxy-300'
            json_2mu2e[key] = latest_files(join(EOSPATH_SIG, subdir))

    ## samples with new naming
    for subdir in eosls(EOSPATH_SIG2['4mu']):
        key = subdir.split('_ctau')[0]  # mXX-100_mA-5_lxy-0p3
        json_4mu[key] = latest_files(join(EOSPATH_SIG2['4mu'], subdir))
    for subdir in eosls(EOSPATH_SIG2['2mu2e']):
        key = subdir.split('_ctau')[0]  # mXX-100_mA-5_lxy-0p3
        json_2mu2e[key] = latest_files(join(EOSPATH_SIG2['2mu2e'], subdir))

    return json_4mu, json_2mu2e


def processed_event_number(ntuplefile):
    """Given a ntuplefile path, return the number of events it ran over."""
    import uproot
    f_ = uproot.open(ntuplefile)
    key_ = f_.allkeys(filtername=lambda k: k.endswith(b"history"))[0]
    return f_[key_].values[2]  # 0: run, 1: lumi, 2: events


def total_event_number(filelist):
    """Given a list of ntuple files, return the total number of events processed"""
    pool = Pool(processes=12)
    res = pool.map(processed_event_number, filelist)
    pool.close()
    return sum(res)


def generate_signal_scale(fl_4mu, fl_2mu2e):

    from FireROOT.Analysis.samples.signalnumbers import genfiltereff, genxsec, darkphotonbr
    print("[generate_signal_scale]")

    filelists = {}
    filelists['2mu2e'] = fl_2mu2e
    filelists['4mu'] = fl_4mu

    def decompose_paramtag(paramtag):
        # paramtag  mXX-1000_mA-0p8_lxy-300 => (1000, 0.8, 300)
        paramtags = paramtag.split('_')
        assert (len(paramtags) == 3)

        res = []
        for t in paramtags:
            v = t.split('-')[1]
            if 'p' in v:
                res.append(float(v.replace('p', '.')))
            else:
                res.append(int(v))

        return tuple(res)

    scale_2mu2e = {}
    print("\t> 2mu2e")
    for i, paramtag in enumerate(filelists['2mu2e'], start=1):
        print("({}/{})".format(i, len(filelists['2mu2e'])), paramtag)
        # paramtag like : mXX-1000_mA-0p8_lxy-300
        parameters = decompose_paramtag(paramtag)
        if parameters not in genfiltereff['2mu2e']:
            # didn't run those samples
            scale_2mu2e[paramtag] = 0
            continue

        filtereff = genfiltereff['2mu2e'][parameters]
        xsec = genxsec[parameters[0]]
        brs = darkphotonbr['ee'][parameters[1]] * darkphotonbr['mumu'][parameters[1]] * 2
        nevents = total_event_number(filelists['2mu2e'][paramtag])

        scale_2mu2e[paramtag] = xsec * brs * filtereff / nevents


    scale_4mu = {}
    print("\t> 4mu")
    for i, paramtag in enumerate(filelists['4mu'], start=1):
        print("({}/{})".format(i, len(filelists['4mu'])), paramtag)
        # paramtag like : mXX-1000_mA-0p8_lxy-300
        parameters = decompose_paramtag(paramtag)
        if parameters not in genfiltereff['4mu']:
            # didn't run those samples
            scale_4mu[paramtag] = 0
            continue

        filtereff = genfiltereff['4mu'][parameters]
        xsec = genxsec[parameters[0]]
        brs = darkphotonbr['mumu'][parameters[1]] * darkphotonbr['mumu'][parameters[1]]
        nevents = total_event_number(filelists['4mu'][paramtag])

        scale_4mu[paramtag] = xsec * brs * filtereff / nevents

    return scale_4mu, scale_2mu2e


def stage_out_json(outfn, datasets, shortcutdir, shortcutfn):
    with open(outfn, "w") as outf:
        outf.write(json.dumps(datasets, indent=4))
    os.chdir(shortcutdir)
    if os.path.islink(shortcutfn): os.remove(shortcutfn)
    os.symlink(relpath(outfn, shortcutdir), basename(shortcutfn))



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="produce data ntuple files")
    parser.add_argument("datatype", type=str, nargs=1, choices=["sigmc", "bkgmc", "data"], help="Type of dataset",)
    parser.add_argument("--skim", action='store_true', default=False, help="make ntuple files from skimmed samples. Only valid when datatype is data/bkgmc")
    parser.add_argument("--eventregion", "-r", default='all', type=str, choices=['all', 'proxy', 'muonType'])
    args = parser.parse_args()


    outdir = join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/samples/store')
    shortcutdir = join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/samples/latest')
    if not os.path.isdir(outdir): os.makedirs(outdir)
    if not os.path.isdir(shortcutdir): os.makedirs(shortcutdir)

    if args.datatype[0] == "data":
        if args.skim:
            datasets = generate_data_files(filedict=EOSPATHS_DATA_SKIM)
            outfn = join(outdir, "skimmed_control_data2018_{}.json".format(datetime.now().strftime('%y%m%d')))
            shortcutfn = join(shortcutdir, 'skimmed_control_data2018.json')
        else:
            if args.eventregion=='all':
                datasets = generate_data_files()
                outfn = join(outdir, "control_data2018_{}.json".format(datetime.now().strftime('%y%m%d')))
                shortcutfn = join(shortcutdir, 'control_data2018.json')
            if args.eventregion=='proxy':
                datasets = generate_data_files(filedict=EOSPATHS_DATA_PROXY)
                outfn = join(outdir, "proxy_data2018_{}.json".format(datetime.now().strftime('%y%m%d')))
                shortcutfn = join(shortcutdir, 'proxy_data2018.json')

        stage_out_json(outfn, datasets, shortcutdir, shortcutfn)

    if args.datatype[0] == "bkgmc":
        if args.skim:
            datasets = generate_background_files(eospathdict=EOSPATHS_BKGSKIM)
            outfn = join(outdir, "skimmed_backgrounds_{}.json".format(datetime.now().strftime('%y%m%d')))
            shortcutfn = join(shortcutdir, 'skimmed_backgrounds.json')
            stage_out_json(outfn, datasets, shortcutdir, shortcutfn)

            datasetsForscale = generate_background_files(eospathdict=EOSPATHS_BKGSKIM, forscale=True)
            scales = generate_background_scale(datasetsForscale)
            outfn = join(outdir, "skimmed_backgrounds_scale_{}.json".format(datetime.now().strftime('%y%m%d')))
            shortcutfn = join(shortcutdir, 'skimmed_backgrounds_scale.json')
            stage_out_json(outfn, scales, shortcutdir, shortcutfn)
        else:
            if args.eventregion=='muonType':
                datasets = generate_background_files(eospathdict=EOSPATHS_BKGS_MUONTYPE)
                outfn = join(outdir, "muontype_backgrounds_{}.json".format(datetime.now().strftime('%y%m%d')))
                shortcutfn = join(shortcutdir, 'muontype_backgrounds.json')
                stage_out_json(outfn, datasets, shortcutdir, shortcutfn)

                scales = generate_background_scale(datasets)
                outfn = join(outdir, "muontype_backgrounds_scale_{}.json".format(datetime.now().strftime('%y%m%d')))
                shortcutfn = join(shortcutdir, 'muontype_backgrounds_scale.json')
                stage_out_json(outfn, scales, shortcutdir, shortcutfn)

            if args.eventregion=='proxy':
                datasets = generate_background_files(eospathdict=EOSPATHS_BKGS_PROXY)
                outfn = join(outdir, "proxy_backgrounds_{}.json".format(datetime.now().strftime('%y%m%d')))
                shortcutfn = join(shortcutdir, 'proxy_backgrounds.json')
                stage_out_json(outfn, datasets, shortcutdir, shortcutfn)

                scales = generate_background_scale(datasets)
                outfn = join(outdir, "proxy_backgrounds_scale_{}.json".format(datetime.now().strftime('%y%m%d')))
                shortcutfn = join(shortcutdir, 'proxy_backgrounds_scale.json')
                stage_out_json(outfn, scales, shortcutdir, shortcutfn)

            if args.eventregion=='all':
                datasets_ = generate_background_files()

                scales = generate_background_scale(datasets_)
                outfn = join(outdir, "backgrounds_scale_{}.json".format(datetime.now().strftime('%y%m%d')))
                shortcutfn = join(shortcutdir, 'backgrounds_scale.json')
                stage_out_json(outfn, datasets, shortcutdir, shortcutfn)

                datasets = clean_background_files(datasets_)
                outfn = join(outdir, "backgrounds_{}.json".format(datetime.now().strftime('%y%m%d')))
                shortcutfn = join(shortcutdir, 'backgrounds.json')
                stage_out_json(outfn, datasets, shortcutdir, shortcutfn)


    if args.datatype[0] == "sigmc":
        if args.eventregion == 'all':
            ds_4mu, ds_2mu2e = generate_signal_files( (EOSPATH_SIG, EOSPATH_SIG2) )

            outfn = join(outdir, "signal_4mu_{}.json".format(datetime.now().strftime('%y%m%d')))
            shortcutfn = join(shortcutdir, 'signal_4mu.json')
            stage_out_json(outfn, ds_4mu, shortcutdir, shortcutfn)

            outfn = join(outdir, "signal_2mu2e_{}.json".format(datetime.now().strftime('%y%m%d')))
            shortcutfn = join(shortcutdir, 'signal_2mu2e.json')
            stage_out_json(outfn, ds_2mu2e, shortcutdir, shortcutfn)

            ## signal scales
            scale_4mu, scale_2mu2e = generate_signal_scale(ds_4mu, ds_2mu2e)

            outfn = join(outdir, "signal_4mu_scale_{}.json".format(datetime.now().strftime('%y%m%d')))
            shortcutfn = join(shortcutdir, 'signal_4mu_scale.json')
            stage_out_json(outfn, scale_4mu, shortcutdir, shortcutfn)

            outfn = join(outdir, "signal_2mu2e_scale_{}.json".format(datetime.now().strftime('%y%m%d')))
            shortcutfn = join(shortcutdir, 'signal_2mu2e_scale.json')
            stage_out_json(outfn, scale_2mu2e, shortcutdir, shortcutfn)

        if args.eventregion == 'proxy':
            ds_4mu, ds_2mu2e = generate_signal_files( (EOSPATH_SIG_PROXY, EOSPATH_SIG2_PROXY) )

            outfn = join(outdir, "proxy_signal_4mu_{}.json".format(datetime.now().strftime('%y%m%d')))
            shortcutfn = join(shortcutdir, 'proxy_signal_4mu.json')
            stage_out_json(outfn, ds_4mu, shortcutdir, shortcutfn)

            outfn = join(outdir, "proxy_signal_2mu2e_{}.json".format(datetime.now().strftime('%y%m%d')))
            shortcutfn = join(shortcutdir, 'proxy_signal_2mu2e.json')
            stage_out_json(outfn, ds_2mu2e, shortcutdir, shortcutfn)

            ## signal scales
            scale_4mu, scale_2mu2e = generate_signal_scale(ds_4mu, ds_2mu2e)

            outfn = join(outdir, "proxy_signal_4mu_scale_{}.json".format(datetime.now().strftime('%y%m%d')))
            shortcutfn = join(shortcutdir, 'proxy_signal_4mu_scale.json')
            stage_out_json(outfn, scale_4mu, shortcutdir, shortcutfn)

            outfn = join(outdir, "proxy_signal_2mu2e_scale_{}.json".format(datetime.now().strftime('%y%m%d')))
            shortcutfn = join(shortcutdir, 'proxy_signal_2mu2e_scale.json')
            stage_out_json(outfn, scale_2mu2e, shortcutdir, shortcutfn)
