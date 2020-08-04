#!/usr/bin/env python

REDIRECTOR = "root://cmseos.fnal.gov/"

# This is control region events.
EOSPATHS_DATA = dict(
    A="/store/group/lpcmetx/SIDM/ffNtupleV2/2018/DoubleMuon/Run2018A-17Sep2018-v2",
    B="/store/group/lpcmetx/SIDM/ffNtupleV2/2018/DoubleMuon/Run2018B-17Sep2018-v1",
    C="/store/group/lpcmetx/SIDM/ffNtupleV2/2018/DoubleMuon/Run2018C-17Sep2018-v1",
    D="/store/group/lpcmetx/SIDM/ffNtupleV2/2018/DoubleMuon/Run2018D-PromptReco-v2",
)

# This is skimmed control region events.
EOSPATHS_DATA_SKIM = dict(
    A="/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/DoubleMuon/Run2018A-17Sep2018-v2",
    B="/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/DoubleMuon/Run2018B-17Sep2018-v1",
    C="/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/DoubleMuon/Run2018C-17Sep2018-v1",
    D="/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/DoubleMuon/Run2018D-PromptReco-v2",
)


# background sample path
EOSPATHS_BKG = dict(
    QCD={
        "QCD_Pt-15to20": ["/store/group/lpcmetx/SIDM/ffNtupleV2/2018/QCD_Pt-15to20_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v3",],
        "QCD_Pt-20to30": ["/store/group/lpcmetx/SIDM/ffNtupleV2/2018/QCD_Pt-20to30_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v4",],
        "QCD_Pt-30to50": ["/store/group/lpcmetx/SIDM/ffNtupleV2/2018/QCD_Pt-30to50_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v3",],
        "QCD_Pt-50to80": ["/store/group/lpcmetx/SIDM/ffNtupleV2/2018/QCD_Pt-50to80_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v3",],
        "QCD_Pt-80to120": [
            "/store/group/lpcmetx/SIDM/ffNtupleV2/2018/QCD_Pt-80to120_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",
            "/store/group/lpcmetx/SIDM/ffNtupleV2/2018/QCD_Pt-80to120_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v2",
        ],
        "QCD_Pt-120to170": [
            "/store/group/lpcmetx/SIDM/ffNtupleV2/2018/QCD_Pt-120to170_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",
            "/store/group/lpcmetx/SIDM/ffNtupleV2/2018/QCD_Pt-120to170_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v2",
        ],
        "QCD_Pt-170to300": ["/store/group/lpcmetx/SIDM/ffNtupleV2/2018/QCD_Pt-170to300_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v3",],
        "QCD_Pt-300to470": [
            "/store/group/lpcmetx/SIDM/ffNtupleV2/2018/QCD_Pt-300to470_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v3",
            "/store/group/lpcmetx/SIDM/ffNtupleV2/2018/QCD_Pt-300to470_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext3-v1",
        ],
        "QCD_Pt-470to600": [
            "/store/group/lpcmetx/SIDM/ffNtupleV2/2018/QCD_Pt-470to600_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",
            "/store/group/lpcmetx/SIDM/ffNtupleV2/2018/QCD_Pt-470to600_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v2",
        ],
        "QCD_Pt-600to800": ["/store/group/lpcmetx/SIDM/ffNtupleV2/2018/QCD_Pt-600to800_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",],
        "QCD_Pt-800to1000": ["/store/group/lpcmetx/SIDM/ffNtupleV2/2018/QCD_Pt-800to1000_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext3-v2",],
        "QCD_Pt-1000toInf": ["/store/group/lpcmetx/SIDM/ffNtupleV2/2018/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",],
    },
    DYJetsToLL={
        "DYJetsToLL-M-10to50": ["/store/group/lpcmetx/SIDM/ffNtupleV2/2018/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v2"],
        "DYJetsToLL_M-50": ["/store/group/lpcmetx/SIDM/ffNtupleV2/2018/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1"],
    },
    Top={
        "TTJets": ["/store/group/lpcmetx/SIDM/ffNtupleV2/2018/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",],
    },
)

# background skim sample path
EOSPATHS_BKGSKIM = dict(
    QCD={
        "QCD_Pt-50to80": ["/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/QCD_Pt-50to80_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v3",],
        "QCD_Pt-80to120": ["/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/QCD_Pt-80to120_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v2",],
        "QCD_Pt-120to170": [
            "/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/QCD_Pt-120to170_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",
            "/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/QCD_Pt-120to170_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v2",
            ],
        "QCD_Pt-170to300": ["/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/QCD_Pt-170to300_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v3",],
        "QCD_Pt-300to470": [
            "/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/QCD_Pt-300to470_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v3",
            "/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/QCD_Pt-300to470_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext3-v1",
        ],
        "QCD_Pt-470to600": [
            "/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/QCD_Pt-470to600_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",
            "/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/QCD_Pt-470to600_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v2",
        ],
        "QCD_Pt-600to800": ["/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/QCD_Pt-600to800_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",],
        "QCD_Pt-800to1000": ["/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/QCD_Pt-800to1000_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext3-v2",],
        "QCD_Pt-1000toInf": ["/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",],
    },
    DYJetsToLL={
        "DYJetsToLL-M-10to50": ["/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v2",],
        "DYJetsToLL_M-50": ["/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",],
    },
    Top={
        "TTJets": ["/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",],
    },
    DiBoson={
        "WW": ["/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/WW_TuneCP5_13TeV-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v2",],
        "WZ": ["/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/WZ_TuneCP5_13TeV-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v3",],
        "ZZ": ["/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/ZZ_TuneCP5_13TeV-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v2",],
    }
)

EOSPATHS_BKGAOD = dict(
    QCD={
        "QCD_Pt-15to20": ["/store/group/lpcmetx/SIDM/Skim/2018/QCD_Pt-15to20_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v3",],
        "QCD_Pt-20to30": ["/store/group/lpcmetx/SIDM/Skim/2018/QCD_Pt-20to30_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v4",],
        "QCD_Pt-30to50": ["/store/group/lpcmetx/SIDM/Skim/2018/QCD_Pt-30to50_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v3",],
        "QCD_Pt-50to80": ["/store/group/lpcmetx/SIDM/Skim/2018/QCD_Pt-50to80_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v3",],
        "QCD_Pt-80to120": [
            "/store/group/lpcmetx/SIDM/Skim/2018/QCD_Pt-80to120_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",
            "/store/group/lpcmetx/SIDM/Skim/2018/QCD_Pt-80to120_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v2",
        ],
        "QCD_Pt-120to170": [
            "/store/group/lpcmetx/SIDM/Skim/2018/QCD_Pt-120to170_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",
            "/store/group/lpcmetx/SIDM/Skim/2018/QCD_Pt-120to170_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v2",
        ],
        "QCD_Pt-170to300": ["/store/group/lpcmetx/SIDM/Skim/2018/QCD_Pt-170to300_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v3",],
        "QCD_Pt-300to470": [
            "/store/group/lpcmetx/SIDM/Skim/2018/QCD_Pt-300to470_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v3",
            "/store/group/lpcmetx/SIDM/Skim/2018/QCD_Pt-300to470_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext3-v1",
        ],
        "QCD_Pt-470to600": [
            "/store/group/lpcmetx/SIDM/Skim/2018/QCD_Pt-470to600_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",
            "/store/group/lpcmetx/SIDM/Skim/2018/QCD_Pt-470to600_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v2",
        ],
        "QCD_Pt-600to800": ["/store/group/lpcmetx/SIDM/Skim/2018/QCD_Pt-600to800_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",],
        "QCD_Pt-800to1000": ["/store/group/lpcmetx/SIDM/Skim/2018/QCD_Pt-800to1000_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext3-v2",],
        "QCD_Pt-1000toInf": ["/store/group/lpcmetx/SIDM/Skim/2018/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",],
    },
    DYJetsToLL={
        "DYJetsToLL-M-10to50": ["/store/group/lpcmetx/SIDM/Skim/2018/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v2"],
        "DYJetsToLL_M-50": ["/store/group/lpcmetx/SIDM/Skim/2018/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1"],
    },
    Top={
        "TTJets": ["/store/group/lpcmetx/SIDM/Skim/2018/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",],
    },
    DiBoson={
        "WW": ["/store/group/lpcmetx/SIDM/Skim/2018/WW_TuneCP5_13TeV-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v2",],
        "WZ": ["/store/group/lpcmetx/SIDM/Skim/2018/WZ_TuneCP5_13TeV-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v3",],
        "ZZ": ["/store/group/lpcmetx/SIDM/Skim/2018/ZZ_TuneCP5_13TeV-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v2",],
    }
)



# private signal MC
EOSPATH_SIG = '/store/group/lpcmetx/SIDM/ffNtupleV2/2018/CRAB_PrivateMC/'
EOSPATH_SIG2 = {
    "4mu": "/store/group/lpcmetx/SIDM/ffNtupleV2/2018/SIDM_XXTo2ATo4Mu",
    "2mu2e": "/store/group/lpcmetx/SIDM/ffNtupleV2/2018/SIDM_XXTo2ATo2Mu2E",
}





###################################################################

# background sample path: ffNtuple, muon-type
EOSPATHS_BKGS_MUONTYPE = dict(
    # QCD={
    #     "QCD_Pt-50to80": ["/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/QCD_Pt-50to80_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v3",],
    #     "QCD_Pt-80to120": ["/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/QCD_Pt-80to120_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v2",],
    #     "QCD_Pt-120to170": [
    #         "/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/QCD_Pt-120to170_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",
    #         "/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/QCD_Pt-120to170_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v2",
    #         ],
    #     "QCD_Pt-170to300": ["/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/QCD_Pt-170to300_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v3",],
    #     "QCD_Pt-300to470": [
    #         "/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/QCD_Pt-300to470_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v3",
    #         "/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/QCD_Pt-300to470_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext3-v1",
    #     ],
    #     "QCD_Pt-470to600": [
    #         "/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/QCD_Pt-470to600_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",
    #         "/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/QCD_Pt-470to600_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v2",
    #     ],
    #     "QCD_Pt-600to800": ["/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/QCD_Pt-600to800_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",],
    #     "QCD_Pt-800to1000": ["/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/QCD_Pt-800to1000_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext3-v2",],
    #     "QCD_Pt-1000toInf": ["/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",],
    # },
    DYJetsToLL={
        # "DYJetsToLL-M-10to50": ["/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v2",],
        "DYJetsToLL_M-50": ["/store/group/lpcmetx/SIDM/ffNtupleV2/MuonTypeLJ/2018/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",],
    },
    # TTJets={
    #     "TTJets": ["/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",],
    # },
    # DiBoson={
    #     "WW": ["/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/WW_TuneCP5_13TeV-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v2",],
    #     "WZ": ["/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/WZ_TuneCP5_13TeV-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v3",],
    #     "ZZ": ["/store/group/lpcmetx/SIDM/ffNtupleV2/Skim/2018/ZZ_TuneCP5_13TeV-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v2",],
    # }
)




###################################################################

# background sample path: ffNtuple, proxy events
EOSPATHS_BKGS_PROXY = dict(
    QCD={
        "QCD_Pt-15to20": ["/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/QCD_Pt-15to20_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v3",],
        "QCD_Pt-20to30": ["/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/QCD_Pt-20to30_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v4",],
        "QCD_Pt-30to50": ["/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/QCD_Pt-30to50_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v3",],
        "QCD_Pt-50to80": ["/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/QCD_Pt-50to80_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v3",],
        "QCD_Pt-80to120": ["/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/QCD_Pt-80to120_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v2",],
        "QCD_Pt-120to170": [
            "/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/QCD_Pt-120to170_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",
            "/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/QCD_Pt-120to170_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v2",
            ],
        "QCD_Pt-170to300": ["/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/QCD_Pt-170to300_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v3",],
        "QCD_Pt-300to470": [
            "/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/QCD_Pt-300to470_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v3",
            "/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/QCD_Pt-300to470_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext3-v1",
        ],
        "QCD_Pt-470to600": [
            "/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/QCD_Pt-470to600_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",
            "/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/QCD_Pt-470to600_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v2",
        ],
        "QCD_Pt-600to800": ["/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/QCD_Pt-600to800_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",],
        "QCD_Pt-800to1000": ["/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/QCD_Pt-800to1000_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext3-v2",],
        "QCD_Pt-1000toInf": ["/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",],
    },
    DYJetsToLL={
        "DYJetsToLL-M-10to50": ["/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v2",],
        "DYJetsToLL_M-50": ["/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",],
        #"DYJetsToLL_M-50_NLO": [
        #    "/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",
        #    "/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext2-v1",
        #],
    },
    Top={
        "TTJets": ["/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",],
        "ST_t-channel_antitop": ["/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/ST_t-channel_antitop_5f_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",],
        "ST_t-channel_top": ["/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/ST_t-channel_top_5f_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",],
        "ST_tW_antitop": ["/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v1",],
    },
    WJets={
        "WJets_HT-100To200": ["/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",],
        "WJets_HT-400To600": ["/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",],
        "WJets_HT-600To800": ["/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",],
        "WJets_HT-800To1200": ["/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",],
        "WJets_HT-1200To2500": ["/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",],
        "WJets_HT-2500ToInf": ["/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1",],
    },
    DiBoson={
        "WW": ["/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/WW_TuneCP5_13TeV-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v2",],
        "WZ": ["/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/WZ_TuneCP5_13TeV-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v3",],
        "ZZ": ["/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/ZZ_TuneCP5_13TeV-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v2",],
    }
)


# private signal sample path: ffNtuple, proxy events
EOSPATH_SIG_PROXY = '/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/CRAB_PrivateMC/'
EOSPATH_SIG2_PROXY = {
    "4mu": "/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/SIDM_XXTo2ATo4Mu",
    "2mu2e": "/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/SIDM_XXTo2ATo2Mu2E",
}

EOSPATHS_DATA_PROXY = dict(
    A="/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/DoubleMuon/Run2018A-17Sep2018-v2",
    B="/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/DoubleMuon/Run2018B-17Sep2018-v1",
    C="/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/DoubleMuon/Run2018C-17Sep2018-v1",
    D="/store/group/lpcmetx/SIDM/ffNtupleV2/proxy/2018/DoubleMuon/Run2018D-PromptReco-v2",
)
