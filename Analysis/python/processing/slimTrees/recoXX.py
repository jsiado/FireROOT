from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *

from rootpy.tree import Tree
from rootpy.io import root_open

class MyEvents(SignalEvents):
    def __init__(self, files=None, type='MC', maxevents=-1, channel=['2mu2e', '4mu'], **kwargs):
        super(MyEvents, self).__init__(files=files, type=type, maxevents=maxevents, channel=channel, **kwargs)

        self._outf = root_open(self.OutName, 'recreate')
        self._outt = Tree("XX")
        self._outt.create_branches({
            's_MXX': 'F',
            's_MA': 'F',
            's_LXY': 'F',

            'xx_mass': 'F',
        })

    def processEvent(self, event, aux):
        if aux['channel'] not in self.Channel: return
        chan = aux['channel']

        _leptonjets = []
        for lj in event.leptonjets:
            if not lj.passSelection(event): continue
            _leptonjets.append(lj)

        if len(_leptonjets)<2: return

        self._outt.s_MXX = self.SignalParam['MXX']
        self._outt.s_MA = self.SignalParam['MA']
        self._outt.s_LXY = self.SignalParam['LXY']

        self._outt.xx_mass = (_leptonjets[0].p4 + _leptonjets[1].p4).M()

        self._outt.fill()

    def postProcess(self):
        super(MyEvents, self).postProcess()

        self._outt.write()
        self._outf.close()
