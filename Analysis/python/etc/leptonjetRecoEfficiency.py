#!/usr/bin/env python
import os
from rootpy.io import root_open

from FireROOT.Analysis.Utils import *


fn = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/outputs/rootfiles/modules/signalLjEfficiency__mXX-500_lxy-30.root')
outdir = os.path.join(os.getenv('CMSSW_BASE'), 'src/FireROOT/Analysis/python/etc/plots/leptonjetRecoEfficiency')
if not os.path.isdir(outdir): os.makedirs(outdir)

if __name__ == '__main__':

    from rootpy.plotting.style import set_style
    from rootpy.plotting import Canvas, Efficiency, Legend


    def get_efficiency(parentDirectory, denomHistName, numerHistName, binsToMerge=None, numerAdd=None):
        sampleNames = [k.name for k in parentDirectory.keys()]
        if len(sampleNames)==0: raise ValueError('No sample directory found!')

        hDenom = getattr(getattr(parentDirectory, sampleNames[0]), denomHistName).clone()
        hNumer = getattr(getattr(parentDirectory, sampleNames[0]), numerHistName).clone()
        if numerAdd:
            hNumer.Add( getattr(getattr(parentDirectory, sampleNames[0]), numerHistName+numerAdd).clone() )

        for s in sampleNames[1:]:
            hDenom.Add( getattr(getattr(parentDirectory, s), denomHistName).clone() )
            hNumer.Add( getattr(getattr(parentDirectory, s), numerHistName).clone() )
            if numerAdd:
                hNumer.Add( getattr(getattr(parentDirectory, s), numerHistName+numerAdd).clone() )

        if binsToMerge:
            hDenom = hDenom.merge_bins(binsToMerge)
            hNumer = hNumer.merge_bins(binsToMerge)
        return Efficiency(hNumer, hDenom)


    def make_plot(parentDirectory, efficiencyName, titleText, outfn, legendText=None,
                  drawHist=False, binsToMerge=None, numerAdd=None):

        _efficiency = get_efficiency(parentDirectory,
                                     efficiencyName+'__total',
                                     efficiencyName+'__match',
                                     binsToMerge=binsToMerge,
                                     numerAdd=numerAdd)
        _graph = _efficiency.graph
        _graph.drawstyle='AP'
        draw(_graph, xtitle='Lxy [cm]', ytitle='Efficiency')

        title = TitleAsLatex(titleText)
        title.Draw()

        if legendText:
            leg=Legend(1, margin=0.25, leftmargin=0.45, topmargin=0.02, entrysep=0.01, entryheight=0.02, textsize=12)
            leg.AddEntry(_graph, legendText, style='LEP')
            leg.Draw()

        canvas.SaveAs(outfn)
        canvas.clear()

        if drawHist:
            _total, _passed = _efficiency.total, _efficiency.passed
            _passed.markercolor = 'red'

            draw([_total, _passed], logy=True)
            title.Draw()
            leg = Legend(2, margin=0.25, leftmargin=0.45, topmargin=0.02, entrysep=0.01, entryheight=0.02, textsize=12)
            leg.AddEntry(_total,  label='total',  style='LEP')
            leg.AddEntry(_passed, label='passed', style='LEP')
            leg.Draw()
            canvas.SaveAs(outfn.replace('.pdf', '__HIST.pdf'))
            canvas.clear()


    def compare_efficiency(parentDirectory, efficiencyName, titleText, outfn, baseLegendText=None,
                           binsToMerge=None, numerAdds=[], additionalLegendTexts=[]):
        base_efficiency = get_efficiency(parentDirectory,
                                     efficiencyName+'__total',
                                     efficiencyName+'__match',
                                     binsToMerge=binsToMerge,
                                     numerAdd=None).graph
        base_efficiency.drawstyle='AP'
        base_efficiency.markercolor=sigCOLORS[6]
        base_efficiency.linecolor  =sigCOLORS[6]

        comp_efficiencies = []
        for numerAdd in numerAdds:
            g = get_efficiency(parentDirectory,
                                efficiencyName+'__total',
                                efficiencyName+'__match',
                                binsToMerge=binsToMerge,
                                numerAdd=numerAdd).graph
            comp_efficiencies.append( g )
        for i, g in enumerate(comp_efficiencies):
            g.drawstyle = 'P'
            g.markercolor = sigCOLORS[i+7]
            g.linecolor   = sigCOLORS[i+7]
        draw([base_efficiency]+[g for g in comp_efficiencies], xtitle='Lxy [cm]', ytitle='Efficiency')

        title = TitleAsLatex(titleText)
        title.Draw()

        if baseLegendText:
            leg=Legend(1+len(numerAdds), margin=0.25, leftmargin=0.45, topmargin=0.02, entrysep=0.01, entryheight=0.03, textsize=14)
            leg.AddEntry(base_efficiency, baseLegendText, style='LEP')
            for g, t in zip(comp_efficiencies, additionalLegendTexts):
                leg.AddEntry(g, t, style='LEP')
            leg.Draw()

        canvas.SaveAs(outfn)
        canvas.clear()


    def make_composition(parentDirectory, denomHistName, outfn,
                         numerHistNames={}, titleText=None, binsToMerge=None):
        sampleNames = [k.name for k in parentDirectory.keys()]
        if len(sampleNames)==0: raise ValueError('No sample directory found!')

        hDenom = getattr(getattr(parentDirectory, sampleNames[0]), denomHistName).clone()
        if binsToMerge: hDenom = hDenom.merge_bins(binsToMerge)
        hNumerS = {
            label : getattr(getattr(parentDirectory, sampleNames[0]), hName).clone() \
            for label, hName in numerHistNames.items()
            }

        for s in sampleNames[1:]:
            hDenom.Add( getattr(getattr(parentDirectory, s), denomHistName).clone() )
            for label, hName in numerHistNames.items():
                hNumerS[label].Add( getattr(getattr(parentDirectory, s), hName).clone() )

        # stack up
        _stack = HistStack()
        for i, (label, h) in enumerate(hNumerS.items()):
            if binsToMerge: h = h.merge_bins(binsToMerge)
            h.title = label
            h.fillcolor=sigCOLORS[i+6]
            h.drawstyle='hist'
            h.fillstyle='solid'
            h.linewidth=0
            h.legendstyle='F'
            _stack.Add(h)

        draw([_stack, hDenom],logy=False)

        if titleText:
            title = TitleAsLatex(titleText)
            title.Draw()

        leg=Legend([hDenom, _stack], margin=0.25, leftmargin=0.45, topmargin=0.02, entrysep=0.01, entryheight=0.02, textsize=12)
        leg.Draw()

        canvas.SaveAs(outfn)
        canvas.clear()




    f = root_open(fn)
    d = f.ch2mu2e.sig

    set_style(MyStyle())
    canvas = Canvas()


    # mergedBins = [(17,18), (19,20), (21,25), (26,30), (31,35), (36,40), (41,50), (51,60), (61,80), (81,100),]
    make_plot(d, 'lxyDpToMu',
              titleText='Z_{d}#rightarrow#mu^{+}#mu^{-} lepton-jet efficiency',
              outfn='%s/lxyDpToMu_muonType_efficiency.pdf' % outdir,
              legendText='lepton-jet',
              drawHist=False, binsToMerge=None,)

    make_composition(d, 'lxyDpToMu__total',
                     outfn='%s/lxyDpToMu_muonType_composition_addjet.pdf' % outdir,
                     numerHistNames={'lepton-jets': 'lxyDpToMu__match', 'PFAK4Jets': 'lxyDpToMu__matchAk4'},
                     titleText='Z_{d}#rightarrow#mu^{+}#mu^{-} reco matching')

    compare_efficiency(d, 'lxyDpToMu',
              titleText='Z_{d}#rightarrow#mu^{+}#mu^{-} lepton-jet efficiency',
              outfn='%s/lxyDpToEl_muonType_efficiency_addjet_overlap.pdf' % outdir,
              baseLegendText='lepton-jet',
              additionalLegendTexts=['lepton-jet + AK4 Jet',],
              numerAdds=['Ak4'],
              )


    overflow_mergedbins = [(-2, -1),]
    make_composition(d, 'lxyDpToEl__total',
                     outfn='%s/lxyDpToEl_egmType_composition.pdf' % outdir,
                     numerHistNames={'lepton-jets': 'lxyDpToEl__match',},
                     titleText='Z_{d}#rightarrowe^{+}e^{-} reco matching',
                     binsToMerge=None)

    make_composition(d, 'lxyDpToEl__total',
                     outfn='%s/lxyDpToEl_egmType_composition_addjet.pdf' % outdir,
                     numerHistNames={'lepton-jets': 'lxyDpToEl__match', 'PFAK4Jets': 'lxyDpToEl__matchAk4'},
                     titleText='Z_{d}#rightarrowe^{+}e^{-} reco matching',
                     binsToMerge=None)

    make_composition(d, 'lxyDpToEl__total',
                     outfn='%s/lxyDpToEl_egmType_composition_addpho.pdf' % outdir,
                     numerHistNames={'lepton-jets': 'lxyDpToEl__match', 'PFPhoton': 'lxyDpToEl__matchPho', },
                     titleText='Z_{d}#rightarrowe^{+}e^{-} reco matching',
                     binsToMerge=None)

    make_composition(d, 'lxyDpToEl__total',
                     outfn='%s/lxyDpToEl_egmType_composition_addele.pdf' % outdir,
                     numerHistNames={'lepton-jets': 'lxyDpToEl__match', 'PFElectron': 'lxyDpToEl__matchEle', },
                     titleText='Z_{d}#rightarrowe^{+}e^{-} reco matching',
                     binsToMerge=None)


    make_plot(d, 'lxyDpToEl',
              titleText='Z_{d}#rightarrowe^{+}e^{-} lepton-jet efficiency',
              outfn='%s/lxyDpToEl_egmType_efficiency.pdf' % outdir,
              legendText='lepton-jet',
              drawHist=False)

    make_plot(d, 'lxyDpToEl',
              titleText='Z_{d}#rightarrowe^{+}e^{-} lepton-jet efficiency',
              outfn='%s/lxyDpToEl_egmType_efficiency_addjet.pdf' % outdir,
              legendText='lepton-jet + AK4 Jet',
              drawHist=False,
              numerAdd='Ak4')

    make_plot(d, 'lxyDpToEl',
              titleText='Z_{d}#rightarrowe^{+}e^{-} lepton-jet efficiency',
              outfn='%s/lxyDpToEl_egmType_efficiency_addpho.pdf' % outdir,
              legendText='lepton-jet + Photon',
              drawHist=False,
              numerAdd='Pho')

    make_plot(d, 'lxyDpToEl',
              titleText='Z_{d}#rightarrowe^{+}e^{-} lepton-jet efficiency',
              outfn='%s/lxyDpToEl_egmType_efficiency_addele.pdf' % outdir,
              legendText='lepton-jet + Electron',
              drawHist=False,
              numerAdd='Ele')


    compare_efficiency(d, 'lxyDpToEl',
              titleText='Z_{d}#rightarrowe^{+}e^{-} lepton-jet efficiency',
              outfn='%s/lxyDpToEl_egmType_efficiency_addjet_overlap.pdf' % outdir,
              baseLegendText='lepton-jet',
              additionalLegendTexts=['lepton-jet + AK4 Jet',],
              numerAdds=['Ak4'],
              )

    compare_efficiency(d, 'lxyDpToEl',
              titleText='Z_{d}#rightarrowe^{+}e^{-} lepton-jet efficiency',
              outfn='%s/lxyDpToEl_egmType_efficiency_addele_overlap.pdf' % outdir,
              baseLegendText='lepton-jet',
              additionalLegendTexts=['lepton-jet + Electron',],
              numerAdds=['Ele'],
              )

    f.close()
