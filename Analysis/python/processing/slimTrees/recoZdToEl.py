from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *

from rootpy.tree import Tree
from rootpy.io import root_open

class MyEvents(SignalEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)

        self._outf = root_open(self.OutName, 'recreate')
        self._outt = Tree("egmlj")
        self._outt.create_branches({
            's_MXX': 'F',
            's_MA': 'F',
            's_LXY': 'F',

            'dp_lxy': 'F',
            'dp_lz': 'F',
            'dp_pt': 'F',
            'dp_eta': 'F',
            'dp_daudr': 'F',

            'rho': 'F',

            'lj_pt': 'F',
            'lj_gendr': 'F',
            'lj_nele': 'I',
            'lj_npho': 'I',
            'lj_ndau': 'I',
            'lj_area': 'F',

            'j_pt': 'F',
            'j_rawpt': 'F',
            'j_gendr': 'F',
            'j_hadfrac': 'F',
            'j_emfrac': 'F',
            'j_neuhadfrac': 'F',
            'j_neuemfrac': 'F',
            'j_id': 'I',
            'j_ncands': 'I',

            'ele_gendr': 'F',
            'ele_pt': 'F',
            'ele_idbit': 'I',
            'ele_grade': 'I',

            'pho_gendr': 'F',
            'pho_pt': 'F',
            'pho_isconv': 'I',
            'pho_haspix': 'I',
            'pho_idbit': 'I',
            'pho_grade': 'I',
        })


    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']

        dp_toMu = [p for p in aux['dp'] if p.daupid==13]
        dp_toEl = [p for p in aux['dp'] if p.daupid==11]

        DR_THRESHOLD = 0.4 # maximum dR limit between (gen darkphoton, lepton-jets) matching

        # dp->el, el
        for dp in dp_toEl:
            if dp.p4.pt()<30 or abs(dp.p4.eta())>2.4: continue

            lxy = (dp.dauvtx - dp.vtx).Rho()
            lz  = (dp.dauvtx - dp.vtx).Z()
            # if abs(lz)>250: continue

            self._outt.s_MXX = self.SignalParam['MXX']
            self._outt.s_MA = self.SignalParam['MA']
            self._outt.s_LXY = self.SignalParam['LXY']
            self._outt.dp_lxy  = lxy
            self._outt.dp_lz = lz
            self._outt.dp_pt = dp.p4.pt()
            self._outt.dp_eta = dp.p4.eta()
            self._outt.dp_daudr= dp.daudr
            self._outt.rho = event.fixedGridRho


            # match with lepton-jets
            mindr, matched = 999., None
            for lj in event.leptonjets:
                if not lj.isEgmType(): continue
                if not lj.passSelection(event): continue
                distance = DeltaR(dp.p4, lj.p4)
                if distance > DR_THRESHOLD: continue
                if distance<mindr:
                    mindr = distance
                    matched = lj

            if matched:
                ## matching with lepton-jets
                # pt_resolution = (matched.p4.pt()-dp.p4.pt())/dp.p4.pt() # (reco-gen)/gen

                self._outt.lj_pt = matched.p4.pt()
                self._outt.lj_gendr = mindr
                self._outt.lj_nele = matched.nPFElectron()
                self._outt.lj_npho = matched.nPFPhoton()
                self._outt.lj_ndau = matched.nDaughters()
                self._outt.lj_area = matched.area

            else:

                self._outt.lj_pt = -999.
                self._outt.lj_gendr = -999.
                self._outt.lj_nele = -999
                self._outt.lj_npho = -999
                self._outt.lj_ndau = -999
                self._outt.lj_area = -999



            # matching with PFAK4Jets
            mindr, matched = 999., None
            for j in event.ak4jets:
                if j.p4.pt()<30 or abs(j.p4.eta())>2.4: continue
                distance = DeltaR(dp.p4, j.p4)
                if distance > DR_THRESHOLD: continue
                if distance<mindr:
                    mindr = distance
                    matched = j

            if matched:
                # pt_resolution = (matched.p4.pt()-dp.p4.pt())/dp.p4.pt() # (reco-gen)/gen
                # rawpt_resolution = (matched.rawP4.pt()-dp.p4.pt())/dp.p4.pt() # (reco-gen)/gen
                neu_had_fraction = matched.hadronEnergyFraction - matched.chaHadEnergyFraction
                neu_em_fraction = matched.emEnergyFraction - matched.chaEmEnergyFraction
                jetid = bool(matched.jetid)

                self._outt.j_pt         = matched.p4.pt()
                self._outt.j_rawpt      = matched.rawP4.pt()
                self._outt.j_gendr      = mindr
                self._outt.j_hadfrac    = matched.hadronEnergyFraction
                self._outt.j_emfrac     = matched.emEnergyFraction
                self._outt.j_neuhadfrac = neu_had_fraction
                self._outt.j_neuemfrac  = neu_em_fraction
                self._outt.j_id         = int(jetid)
                self._outt.j_ncands     = matched.pfcands_n


            else:

                self._outt.j_pt         = -999.
                self._outt.j_rawpt      = -999.
                self._outt.j_gendr      = -999.
                self._outt.j_hadfrac    = -999.
                self._outt.j_emfrac     = -999.
                self._outt.j_neuhadfrac = -999.
                self._outt.j_neuemfrac  = -999.
                self._outt.j_id         = -999
                self._outt.j_ncands     = -999


            # matching with Electrons
            mindr, matched = 999., None
            for e in event.electrons:
                if e.p4.pt()<10 or abs(e.p4.eta())>2.4: continue
                distance = DeltaR(dp.p4, e.p4)
                if distance > DR_THRESHOLD: continue
                else:
                    mindr = distance
                    matched = e

            if matched:
                self._outt.ele_gendr = mindr
                self._outt.ele_pt = matched.p4.pt()
                self._outt.ele_idbit = matched.idbit
                self._outt.ele_grade = matched.idResults
            else:
                self._outt.ele_gendr = -999.
                self._outt.ele_pt = -999.
                self._outt.ele_idbit = -999
                self._outt.ele_grade = -999


            # matching with Photons
            mindr, matched = 999., None
            for g in event.photons:
                if g.p4.pt()<10 or abs(g.p4.eta())>2.4: continue
                distance = DeltaR(dp.p4, g.p4)
                if distance > DR_THRESHOLD: continue
                else:
                    mindr = distance
                    matched = g

            if matched:
                self._outt.pho_gendr = mindr
                self._outt.pho_pt    = matched.p4.pt()
                self._outt.pho_isconv= matched.isConversion
                self._outt.pho_haspix= matched.hasPixelSeed
                self._outt.pho_idbit = matched.idBit
                self._outt.pho_grade = matched.idResults
            else:
                self._outt.pho_gendr = -999.
                self._outt.pho_pt    = -999.
                self._outt.pho_isconv= -999
                self._outt.pho_haspix= -999
                self._outt.pho_idbit = -999
                self._outt.pho_grade = -999


            self._outt.fill()



    def postProcess(self):
        super(MyEvents, self).postProcess()

        self._outt.write()
        self._outf.close()
