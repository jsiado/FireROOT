from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *

from rootpy.tree import Tree
from rootpy.io import root_open

class MyEvents(SignalEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)

        self._outf = root_open(self.OutName, 'recreate')
        self._outt = Tree("trig")
        _branches = {t: 'B' for t in self.Triggers}
        _branches.update({
            'dsa1_pt': 'F',
            'dsa1_eta': 'F',
        })
        self._outt.create_branches(_branches)

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']

        _dsamu = []
        for mu in event.dsamuons:
            if abs(mu.p4.eta()) > 2: continue
            if mu.DTStations + mu.CSCStations < 2: continue
            _dsamu.append(mu)

        if len(_dsamu) < 2: return

        _dsamu.sort(key=lambda mu: mu.p4.pt(), reverse=True)
        subleadMu = _dsamu[1]
        self._outt.dsa1_pt = subleadMu.p4.pt()
        self._outt.dsa1_eta = subleadMu.p4.eta()

        for t in self.Triggers:
            setattr(self._outt, t, getattr(event.hlt, t) )

        self._outt.fill()


    def postProcess(self):
        super(MyEvents, self).postProcess()

        self._outt.write()
        self._outf.close()
