from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *

from rootpy.tree import Tree
from rootpy.io import root_open

class MyEvents(SignalEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)

        self._outf = root_open(self.OutName, 'recreate')
        self._outpho = Tree("photon")
        self._outpho.create_branches({
            "lxy" : "F",
            "genpt" : "F",
            "dr" : "F",
            "pt" : "F",
            "ptreso" : "F",
            "isconv" : "I",
            "haspix" : "I",
            "idbit" : "I",
            "grade": "I",
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

            lxy = (p.dauvtx - p.vtx).Rho()
            lz  = (p.dauvtx - p.vtx).Z()
            if abs(lz)>250: continue


            mindr, matched = 999., None
            for lj in event.leptonjets:
                if not lj.isEgmType(): continue
                if not lj.passSelection(event): continue
                distance = DeltaR(dp.p4, lj.p4)
                if distance > DR_THRESHOLD: continue
                if distance<mindr:
                    mindr = distance
                    matched = lj

            if matched is None:
                # match with PFPhotons
                for g in event.photons:
                    if g.p4.pt()<10 or abs(g.p4.eta())>2.4: continue
                    distance = DeltaR(dp.p4, g.p4)
                    if distance > DR_THRESHOLD: continue
                    else:
                        mindr = distance
                        matched = g
                if matched is not None:
                    self._outpho.lxy   = lxy
                    self._outpho.genpt = dp.p4.pt()
                    self._outpho.dr    = mindr
                    self._outpho.pt    = matched.p4.pt()
                    self._outpho.ptreso= (matched.p4.pt()-dp.p4.pt())/dp.p4.pt()
                    self._outpho.isconv= matched.isConversion
                    self._outpho.haspix= matched.hasPixelSeed
                    self._outpho.idbit = matched.idBit
                    self._outpho.grade = matched.idResults
                    self._outpho.fill()

    def postProcess(self):
        super(MyEvents, self).postProcess()

        self._outpho.write()
        self._outf.close()
