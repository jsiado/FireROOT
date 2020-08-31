from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *

from rootpy.tree import Tree
from rootpy.io import root_open

class MyEvents(SignalEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)

        # _outname = self.OutName.replace('.root','')
        # _outname += '__'+self.Dtag+'.root'
        self._outf = root_open(self.OutName, 'recreate')
        self._outele = Tree("electron")
        self._outele.create_branches({
            "lxy" : "F",
            "genpt" : "F",
            "dr" : "F",
            "pt" : "F",
            "ptreso" : "F",
            "idbit" : "I",
            'grade': "I",
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
                # match with PFElectrons
                for e in event.electrons:
                    if e.p4.pt()<10 or abs(e.p4.eta())>2.4: continue
                    distance = DeltaR(dp.p4, e.p4)
                    if distance > DR_THRESHOLD: continue
                    else:
                        mindr = distance
                        matched = e
                if matched is not None:
                    self._outele.lxy   = lxy
                    self._outele.genpt = dp.p4.pt()
                    self._outele.dr    = mindr
                    self._outele.pt    = matched.p4.pt()
                    self._outele.ptreso= (matched.p4.pt()-dp.p4.pt())/dp.p4.pt()
                    self._outele.idbit = matched.idbit
                    self._outele.grade = matched.idResults
                    self._outele.fill()

    def postProcess(self):
        super(MyEvents, self).postProcess()

        self._outele.write()
        self._outf.close()
