#!/usr/bin/env python
from __future__ import print_function
from FireROOT.Analysis.Events import *
from FireROOT.Analysis.Utils import *
from FireROOT.Analysis.DatasetMapLoader import DatasetMapLoader, SigDatasetMapLoader

from rootpy.logger import log
log = log[__name__]

dml = DatasetMapLoader()
dataDS, dataMAP = dml.fetch('data')
bkgDS, bkgMAP, bkgSCALE = dml.fetch('bkg')

sdml = SigDatasetMapLoader()
sigDS_2mu2e, sigSCALE_2mu2e = sdml.fetch('2mu2e')
sigDS_4mu, sigSCALE_4mu = sdml.fetch('4mu')


class MyEvents(Events):
    def __init__(self, files=None, type='MC'):
        super(MyEvents, self).__init__(files=files, type=type)

    def processEvent(self, event, aux):
        LJ0, LJ1 = aux['lj0'], aux['lj1']
        passCosmic = all(map(lambda lj: lj.passCosmicVeto(event), [LJ0, LJ1]))
        passIso = all(map(lambda lj: not (lj.pfiso()>=0.12), [LJ0, LJ1]))
        passFake = all(map(lambda lj: not (lj.maxTrackNormChi2()>=2), [LJ0, LJ1]))
        passMuD0 = all(map(lambda lj: not (lj.isMuonType() and lj.minTkD0()>0 and lj.minTkD0()<=0.01), [LJ0, LJ1]))

        notPassCosmic = all(map(lambda lj: not lj.passCosmicVeto(event), [lj for lj in [LJ0, LJ1] if lj.isMuonType()]))
        notPassIso = all(map(lambda lj: lj.pfiso()>=0.12, [LJ0, LJ1]))
        notPassFake = all(map(lambda lj: lj.maxTrackNormChi2()>=2, [LJ0, LJ1]))

        # if not passMuD0: return

        for chan in ['2mu2e', '4mu']:
            if aux['channel'] == chan:
                if notPassCosmic and passIso and passFake:
                    histToFill = 'dphi-CosmicCR-{}'.format(chan)
                    if histToFill in self.Histos:
                        self.Histos[histToFill].Fill(abs(DeltaPhi(LJ0.p4, LJ1.p4)), aux['wgt'])
                if passCosmic and notPassIso and passFake:
                    histToFill = 'dphi-IsoCR-{}'.format(chan)
                    if histToFill in self.Histos:
                        self.Histos[histToFill].Fill(abs(DeltaPhi(LJ0.p4, LJ1.p4)), aux['wgt'])
                if passCosmic and passIso and notPassFake:
                    histToFill = 'dphi-FakeCR-{}'.format(chan)
                    if histToFill in self.Histos:
                        self.Histos[histToFill].Fill(abs(DeltaPhi(LJ0.p4, LJ1.p4)), aux['wgt'])



### backgrounds
BkgHists = {}
for ds, files in bkgDS.items():
    events_ = MyEvents(files=files, type='MC')
    events_.setScale(bkgSCALE[ds])
    for chan in ['2mu2e', '4mu']:
        for cr in ['CosmicCR', 'IsoCR', 'FakeCR']:
            events_.bookHisto('dphi-{}-{}'.format(cr, chan), ROOT.Hist(20,0, ROOT.Math.Pi(),
                                                title='Lepton-jet pair #Delta#phi;#Delta#phi_{lj0, lj1};counts/20',
                                                drawstyle='hist', legendstyle='F', fillstyle='solid', linewidth=0))

    events_.process()
    BkgHists[ds] = events_.histos
log.info('background MC done')

# ________________________________________________________
sampleSig = 'mXX-150_mA-0p25_lxy-300|mXX-500_mA-1p2_lxy-300|mXX-800_mA-5_lxy-300'.split('|')
# sampleSig = 'mXX-100_mA-5_lxy-0p3|mXX-1000_mA-0p25_lxy-0p3'.split('|')

### signal 4mu
SigHists4mu = {}
for ds in sampleSig:
    events_ = MyEvents(files=sigDS_4mu[ds], type='MC')
    events_.setScale(sigSCALE_4mu[ds])
    for cr in ['CosmicCR', 'IsoCR', 'FakeCR']:
        events_.bookHisto('dphi-{}-4mu'.format(cr), ROOT.Hist(20,0, ROOT.Math.Pi(),
                                            title=ds, drawstyle='hist pmc plc', legendstyle='L', linewidth=2))
    events_.process()
    SigHists4mu[ds] = events_.histos

### signal 2mu2e
SigHists2mu2e = {}
for ds in sampleSig:
    events_ = MyEvents(files=sigDS_2mu2e[ds], type='MC')
    events_.setScale(sigSCALE_2mu2e[ds])
    for cr in ['CosmicCR', 'IsoCR', 'FakeCR']:
        events_.bookHisto('dphi-{}-2mu2e'.format(cr), ROOT.Hist(20,0, ROOT.Math.Pi(),
                                            title=ds, drawstyle='hist pmc plc', legendstyle='L', linewidth=2))
    events_.process()
    SigHists2mu2e[ds] = events_.histos
log.info('signal MC done')


# ________________________________________________________
### data
DataHists = {}
_files = []
for ds in dataDS: _files.extend(dataDS[ds])
events_ = MyEvents(files=_files, type='DATA')
for chan in ['2mu2e', '4mu']:
    for cr in ['CosmicCR', 'IsoCR', 'FakeCR']:
        events_.bookHisto('dphi-{}-{}'.format(cr, chan), ROOT.Hist(20,0, ROOT.Math.Pi(),
                                            title='data {}'.format(cr),
                                            drawstyle='e1', legendstyle='LEP', linewidth=2, markercolor='black'))
events_.process()
DataHists = events_.histos
log.info('data done')


from rootpy.plotting.style import set_style
set_style(MyStyle())

c = ROOT.Canvas()
c.SetLogy()

for chan in ['2mu2e', '4mu']:
    for cr in ['CosmicCR', 'IsoCR', 'FakeCR']:
        histName = 'dphi-{}-{}'.format(cr, chan)
        toDraw = []
        legs = []

        CatHists = mergeHistsFromMapping(extractHistByName(BkgHists, histName), bkgMAP, bkgCOLORS)
        hstack = ROOT.HistStack(list(CatHists.values()), title='a title', drawstyle='HIST')
        stackError = ErrorBandFromHistStack(hstack)

        toDraw.append(hstack)
        toDraw.append(stackError)

        legs.extend(hstack.GetHists())
        legs.append(stackError)

        if chan == '4mu':
            SigHists = SigHists4mu
            channelLatex = '4#mu'
        if chan == '2mu2e':
            SigHists = SigHists2mu2e
            channelLatex = '2#mu2e'

        sigHistList = list(extractHistByName(SigHists, histName).values())
        toDraw.extend(sigHistList)
        legs.extend(sigHistList)

        # toDraw.append(DataHists[histName])
        # legs.append(DataHists[histName])

        draw(toDraw, pad=c, xtitle='#Delta#phi_{lj0, lj1}', ytitle='counts/20', logy=True, )
        legend = ROOT.Legend(legs, pad=c, leftmargin=0.05, margin=0.1, entryheight=0.02, textsize=12)
        # legend.SetNColumns(2)
        legend.Draw()

        title = TitleAsLatex("[{},{}] lepton-jet pair #Delta#phi".format(channelLatex, cr))
        title.Draw()

        c.Print('ljpairDphi-{}-{}.pdf'.format(cr, chan))

        c.clear()

