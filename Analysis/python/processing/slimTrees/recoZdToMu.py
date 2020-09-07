from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *

from rootpy.tree import Tree
from rootpy.io import root_open

class MyEvents(SignalEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)

        self._outf = root_open(self.OutName, 'recreate')
        self._outt = Tree("mulj")
        self._outt.create_branches({
            's_MXX': 'F',
            's_MA': 'F',
            's_LXY': 'F',

            'dp_lxy': 'F',
            'dp_lz': 'F',
            'dp_pt': 'F',
            'dp_eta': 'F',
            'dp_daudr': 'F',

            'genmu_p_pt': 'F',
            'genmu_p_eta': 'F',
            'genmu_m_pt': 'F',
            'genmu_m_eta': 'F',

            'lj_pt': 'F',
            'lj_gendr': 'F',
            'lj_type': 'I',  # 1: PFMuType, 2: DSAType
            'lj_ndsa': 'I',

            'mu_p_pt': 'F',
            'mu_p_gendr': 'F',
            'mu_p_type': 'I',
            'mu_p_samesign': 'I',
            'mu_p_selector': 'I',
            'mu_m_pt': 'F',
            'mu_m_gendr': 'F',
            'mu_m_type': 'I',
            'mu_m_samesign': 'I',
            'mu_m_selector': 'I',
            'mu_pm_same': 'I',
            'mu_pm_pt': 'F',

            'dsa_p_pt': 'F',
            'dsa_p_gendr': 'F',
            'dsa_p_samesign': 'I',
            'dsa_p_nsta': 'I',
            'dsa_p_ndthits': 'I',
            'dsa_p_ncschits': 'I',
            'dsa_p_normchi2': 'F',
            'dsa_p_pterrptinv': 'F',
            'dsa_p_extrpdr': 'F',
            'dsa_m_pt': 'F',
            'dsa_m_gendr': 'F',
            'dsa_m_samesign': 'I',
            'dsa_m_nsta': 'I',
            'dsa_m_ndthits': 'I',
            'dsa_m_ncschits': 'I',
            'dsa_m_normchi2': 'F',
            'dsa_m_pterrptinv': 'F',
            'dsa_m_extrpdr': 'F',
            'dsa_pm_same': 'I',
            'dsa_pm_pt': 'F',


            'ljsrc_p_pt': 'F',
            'ljsrc_p_gendr': 'F',
            'ljsrc_p_type': 'I', # 3: PFMu, 8: DSAMu
            'ljsrc_p_samesign': 'I',
            'ljsrc_m_pt': 'F',
            'ljsrc_m_gendr': 'F',
            'ljsrc_m_type': 'I',
            'ljsrc_m_samesign': 'I',
            'ljsrc_pm_same': 'I',

        })


    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']

        dp_toMu = [p for p in aux['dp'] if p.daupid == 13]
        genmu_p = [p for p in event.gens if p.pid==13]
        genmu_m = [p for p in event.gens if p.pid == -13]


        DR_THRESHOLD = 0.4  # maximum dR limit between (gen darkphoton, lepton-jets) matching
        DR_THRESHOLD_MU = 0.2  # maximum dR limit between (gen mu, reco mu) matching

        for dp in dp_toMu:
            if dp.p4.pt() < 30 or abs(dp.p4.eta()) > 2.4: continue

            lxy = (dp.dauvtx - dp.vtx).Rho()
            lz = (dp.dauvtx - dp.vtx).Z()
            # if abs(lz) > 800: continue

            mup = [p for p in genmu_p if (p.vtx - dp.dauvtx).R() < 1e-5]
            mum = [p for p in genmu_m if (p.vtx - dp.dauvtx).R() < 1e-5]
            if len(mup) != 1 or len(mum) != 1: continue
            _mup, _mum = mup[0], mum[0]

            self._outt.s_MXX = self.SignalParam['MXX']
            self._outt.s_MA = self.SignalParam['MA']
            self._outt.s_LXY = self.SignalParam['LXY']
            self._outt.dp_lxy = lxy
            self._outt.dp_lz = lz
            self._outt.dp_pt = dp.p4.pt()
            self._outt.dp_eta = dp.p4.eta()
            self._outt.dp_daudr = dp.daudr
            self._outt.genmu_p_pt = _mup.p4.pt()
            self._outt.genmu_p_eta = _mup.p4.eta()
            self._outt.genmu_m_pt = _mum.p4.pt()
            self._outt.genmu_m_eta = _mum.p4.eta()



            ##################
            ### LEPTON-JET ###
            ##################

            mindr, matched = 999., None
            for lj in event.leptonjets:
                if not lj.isMuonType(): continue
                if not lj.passSelection(event): continue
                distance = DeltaR(dp.p4, lj.p4)
                if distance > DR_THRESHOLD: continue
                if distance<mindr:
                    mindr = distance
                    matched = lj

            if matched:
                self._outt.lj_pt = matched.p4.pt()
                self._outt.lj_gendr = mindr
                self._outt.lj_type = matched.type()
                self._outt.lj_ndsa = matched.nDSA()
            else:
                self._outt.lj_pt = -999.
                self._outt.lj_gendr = -999.
                self._outt.lj_type = -999
                self._outt.lj_ndsa = -999


            #################
            ### RECO MUON ###
            #################

            # match with gen mu+
            mindr, matched_p, matchedIdx_p = 999., None, -1
            for i, mu in enumerate(event.muons):
                if mu.p4.pt() < 5 or abs(mu.p4.eta()) > 2.4: continue
                distance = DeltaR(_mup.p4, mu.p4)
                if distance > DR_THRESHOLD_MU: continue
                if distance < mindr:
                    mindr = distance
                    matched_p = mu
                    matchedIdx_p = i

            if matched_p:
                self._outt.mu_p_pt = matched_p.p4.pt()
                self._outt.mu_p_gendr = mindr
                self._outt.mu_p_type = matched_p.type
                self._outt.mu_p_samesign = int(matched_p.charge > 0)
                self._outt.mu_p_selector = matched_p.selectors
            else:
                self._outt.mu_p_pt = -999.
                self._outt.mu_p_gendr = -999.
                self._outt.mu_p_type = -999
                self._outt.mu_p_samesign = -999
                self._outt.mu_p_selector = -999


            # match with gen mu-
            mindr, matched_m, matchedIdx_m = 999., None, -1
            for i, mu in enumerate(event.muons):
                if mu.p4.pt() < 5 or abs(mu.p4.eta()) > 2.4: continue
                distance = DeltaR(_mum.p4, mu.p4)
                if distance > DR_THRESHOLD_MU: continue
                if distance < mindr:
                    mindr = distance
                    matched_m = mu
                    matchedIdx_m = i

            if matched_m:
                self._outt.mu_m_pt = matched_m.p4.pt()
                self._outt.mu_m_gendr = mindr
                self._outt.mu_m_type = matched_m.type
                self._outt.mu_m_samesign = int(matched_m.charge < 0)
                self._outt.mu_m_selector = matched_m.selectors
            else:
                self._outt.mu_m_pt = -999.
                self._outt.mu_m_gendr = -999.
                self._outt.mu_m_type = -999
                self._outt.mu_m_samesign = -999
                self._outt.mu_m_selector = -999


            # is _mup and _mum matched with the same reco mu?
            if matchedIdx_p == -1 and matchedIdx_m == -1:
                self._outt.mu_pm_same = -999
            elif matchedIdx_p == matchedIdx_m:
                self._outt.mu_pm_same = 1
            else:
                self._outt.mu_pm_same = 0

            if matched_p and matched_m:
                self._outt.mu_pm_pt = (matched_p.p4+matched_m.p4).pt()
            else:
                self._outt.mu_pm_pt = -999.



            ################
            ### DSA MUON ###
            ################

            # match with gen mu+
            mindr, matched_p, matchedIdx_p = 999., None, -1
            for i, mu in enumerate(event.dsamuons):
                if mu.p4.pt() < 10 or abs(mu.p4.eta()) > 2.4: continue
                distance = DeltaR(_mup.p4, mu.p4)
                if distance > DR_THRESHOLD_MU: continue
                if distance < mindr:
                    mindr = distance
                    matched_p = mu
                    matchedIdx_p = i

            if matched_p:
                self._outt.dsa_p_pt = matched_p.p4.pt()
                self._outt.dsa_p_gendr = mindr
                self._outt.dsa_p_samesign = int(matched_p.charge > 0)
                self._outt.dsa_p_nsta = matched_p.DTStations + matched_p.CSCStations
                self._outt.dsa_p_ndthits = matched_p.DTHits
                self._outt.dsa_p_ncschits = matched_p.CSCHits
                self._outt.dsa_p_normchi2 = matched_p.normChi2
                self._outt.dsa_p_pterrptinv = matched_p.ptErrorOverPt
                self._outt.dsa_p_extrpdr = matched_p.extrapolatedDr

            else:
                self._outt.dsa_p_pt = -999.
                self._outt.dsa_p_gendr = -999.
                self._outt.dsa_p_samesign = -999
                self._outt.dsa_p_nsta = -999
                self._outt.dsa_p_ndthits = -999
                self._outt.dsa_p_ncschits = -999
                self._outt.dsa_p_normchi2 = -999.
                self._outt.dsa_p_pterrptinv = -999.
                self._outt.dsa_p_extrpdr = -999.


            # match with gen mu-
            mindr, matched_m, matchedIdx_m = 999., None, -1
            for i, mu in enumerate(event.dsamuons):
                if mu.p4.pt() < 10 or abs(mu.p4.eta()) > 2.4: continue
                distance = DeltaR(_mum.p4, mu.p4)
                if distance > DR_THRESHOLD_MU: continue
                if distance < mindr:
                    mindr = distance
                    matched_m = mu
                    matchedIdx_m = i

            if matched_m:
                self._outt.dsa_m_pt = matched_m.p4.pt()
                self._outt.dsa_m_gendr = mindr
                self._outt.dsa_m_samesign = int(matched_m.charge > 0)
                self._outt.dsa_m_nsta = matched_m.DTStations + matched_m.CSCStations
                self._outt.dsa_m_ndthits = matched_m.DTHits
                self._outt.dsa_m_ncschits = matched_m.CSCHits
                self._outt.dsa_m_normchi2 = matched_m.normChi2
                self._outt.dsa_m_pterrptinv = matched_m.ptErrorOverPt
                self._outt.dsa_m_extrpdr = matched_m.extrapolatedDr

            else:
                self._outt.dsa_m_pt = -999.
                self._outt.dsa_m_gendr = -999.
                self._outt.dsa_m_samesign = -999
                self._outt.dsa_m_nsta = -999
                self._outt.dsa_m_ndthits = -999
                self._outt.dsa_m_ncschits = -999
                self._outt.dsa_m_normchi2 = -999.
                self._outt.dsa_m_pterrptinv = -999.
                self._outt.dsa_m_extrpdr = -999.


            # is _mup and _mum matched with the same dsa mu?
            if matchedIdx_p == -1 and matchedIdx_m == -1:
                self._outt.dsa_pm_same = -999
            elif matchedIdx_p == matchedIdx_m:
                self._outt.dsa_pm_same = 1
            else:
                self._outt.dsa_pm_same = 0

            if matched_p and matched_m:
                self._outt.dsa_pm_pt = (matched_p.p4+matched_m.p4).pt()
            else:
                self._outt.dsa_pm_pt = -999.


            #########################
            ### LEPTONJETS SOURCE ###
            #########################

            # match with gen mu+
            mindr, matched_p, matchedIdx_p = 999., None, -1
            for i, mu in enumerate(event.ljsources):
                if mu.type not in [3,8]: continue
                # if mu.p4.pt() < 5 or abs(mu.p4.eta()) > 2.4: continue
                distance = DeltaR(_mup.p4, mu.p4)
                if distance > DR_THRESHOLD_MU: continue
                if distance < mindr:
                    mindr = distance
                    matched_p = mu
                    matchedIdx_p = i

            if matched_p:
                self._outt.ljsrc_p_pt = matched_p.p4.pt()
                self._outt.ljsrc_p_gendr = mindr
                self._outt.ljsrc_p_type = matched_p.type
                self._outt.ljsrc_p_samesign = int(matched_p.charge > 0)
            else:
                self._outt.ljsrc_p_pt = -999.
                self._outt.ljsrc_p_gendr = -999.
                self._outt.ljsrc_p_type = -999
                self._outt.ljsrc_p_samesign = -999


            # match with gen mu-
            mindr, matched_m, matchedIdx_m = 999., None, -1
            for i, mu in enumerate(event.ljsources):
                if mu.type not in [3,8]: continue
                # if mu.p4.pt() < 5 or abs(mu.p4.eta()) > 2.4: continue
                distance = DeltaR(_mum.p4, mu.p4)
                if distance > DR_THRESHOLD_MU: continue
                if distance < mindr:
                    mindr = distance
                    matched_m = mu
                    matchedIdx_m = i

            if matched_m:
                self._outt.ljsrc_m_pt = matched_m.p4.pt()
                self._outt.ljsrc_m_gendr = mindr
                self._outt.ljsrc_m_type = matched_m.type
                self._outt.ljsrc_m_samesign = int(matched_m.charge < 0)
            else:
                self._outt.ljsrc_m_pt = -999.
                self._outt.ljsrc_m_gendr = -999.
                self._outt.ljsrc_m_type = -999
                self._outt.ljsrc_m_samesign = -999

            # is _mup and _mum matched with the same reco mu?
            if matchedIdx_p == -1 and matchedIdx_m == -1:
                self._outt.ljsrc_pm_same = -999
            elif matchedIdx_p == matchedIdx_m:
                self._outt.ljsrc_pm_same = 1
            else:
                self._outt.ljsrc_pm_same = 0


            self._outt.fill()


    def postProcess(self):
        super(MyEvents, self).postProcess()

        self._outt.write()
        self._outf.close()
