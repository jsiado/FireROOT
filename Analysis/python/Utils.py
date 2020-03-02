#!/usr/bin/env python
import operator
from math import log

import rootpy.ROOT as ROOT
from rootpy.plotting.utils import *
from rootpy.context import preserve_current_canvas, do_nothing
from rootpy.plotting.hist import _Hist, Hist, HistStack
from rootpy.plotting.graph import _Graph1DBase, Graph
from rootpy.plotting.style import get_style

bkgCOLORS ={'QCD': 'powderblue', 'DYJetsToLL': 'wheat', 'TTJets': 'darkcyan', 'DiBoson': 'salmon'}
multiadd = lambda a, b: map(operator.add, a, b)
multisub = lambda a, b: map(operator.sub, a, b)


M_PI = ROOT.Math.Pi()
DeltaPhi = ROOT.Math.VectorUtil.DeltaPhi
DeltaR = ROOT.Math.VectorUtil.DeltaR

def mergeHistsFromMapping(hists, mapping, fillcolors=None):
    """
    merge histograms from mappping.
    e.g.
    - hists {'a_1': Hist(), 'a_2': Hist(), ... , 'b_1': Hist(),  'b_2': Hist()}
    - mapping {'a': ['a_1', 'a_2',], 'b': ['b_1', 'b_2']}
    - fillcolors [optional] {'a': 'green', 'b': 'red'}
    - returns OrderedDict('a': Hist(), 'b': Hist()) sorted by Integral()
    """

    from collections import OrderedDict
    CatHists = {}
    for cat, ds in mapping.items():
        output = None
        for d in ds:
            if output is None:
                output = hists[d].Clone()
                ROOT.SetOwnership(output, False)
            else:
                output.Add(hists[d])
        if fillcolors:
            output.fillcolor = fillcolors[cat]
        output.SetTitle(cat)
        CatHists[cat] = output
    return OrderedDict(sorted(CatHists.items(), key=lambda x: x[1].Integral()))


def ErrorBandFromHistStack(hstack, **kwargs):
    """
    possion error band (TGraphAsymmError) from sum of `hstack`
    kwargs are forwarded for TGraphAsymmError property setting
    """
    _sumStack = None
    for h in hstack.GetHists():
        if _sumStack is None: _sumStack = h.Clone()
        else: _sumStack.Add(h)

    stackError = _sumStack.poisson_errors()
    ROOT.SetOwnership(stackError, False)
    kwDefaults = {
        'fillstyle': 3244,
        'fillcolor': 'gray',
        'drawstyle': '2',
        'legendstyle': 'F',
        'title': 'stat. unc',
    }
    kwDefaults.update(kwargs)
    for k, v in kwDefaults.items():
        setattr(stackError, k, v)

    return stackError


def sumHistStack(hstack):
    """
    sum of hstack hists
    """
    _sumStack = None
    for h in hstack.GetHists():
        if _sumStack is None: _sumStack = h.Clone()
        else: _sumStack.Add(h)
    return _sumStack


def TitleAsLatex(s):
    """Add a title as TLatex on top left"""

    label = ROOT.TLatex(ROOT.gStyle.GetPadLeftMargin(), 0.9+ROOT.gStyle.GetPadTopMargin()+0.01, s)
    label.SetTextFont(43)
    label.SetTextAlign(11)
    label.SetTextSize(22)
    label.SetNDC()
    return label


def extractHistByName(histdict, name):
    """
    histdict is dictionary of dictionary,
    first level datasetName, second level hist name
    return: dictionary with dataset as name, selected hist as value
    """
    return {k: v[name] for k, v in histdict.items()}



def MyStyle():
    """customize ROOT style based on *CMSTDR* style"""

    style = get_style('CMSTDR')
    style.SetTitleSize(0.03, "XYZ")
    style.SetLabelSize(0.03, "XYZ")
    style.SetLegendBorderSize(0)
    style.SetLegendFillColor(0)
    font = 43 # Helvetica
    style.SetTextFont(font)
    style.SetLegendFont(font)
    style.SetPalette(112) # ROOT.kViridis
    style.SetErrorX()
    return style



def _limits_helper(x1, x2, a, b, snap=False):
    """
    Given x1, x2, a, b, where:
        x1 - x0         x3 - x2
    a = ------- ,   b = -------
        x3 - x0         x3 - x0
    determine the points x0 and x3:
    x0         x1                x2       x3
    |----------|-----------------|--------|
    """
    if x2 < x1:
        raise ValueError("x2 < x1")
    if a + b >= 1:
        raise ValueError("a + b >= 1")
    if a < 0:
        raise ValueError("a < 0")
    if b < 0:
        raise ValueError("b < 0")
    if snap:
        if x1 >= 0:
            x1 = 0
            a = 0
        elif x2 <= 0:
            x2 = 0
            b = 0
        if x1 == x2 == 0:
            # garbage in garbage out
            return 0., 1.
    elif x1 == x2:
        # garbage in garbage out
        return x1 - 1., x1 + 1.
    if a == 0 and b == 0:
        return x1, x2
    elif a == 0:
        return x1, (x2 - b * x1) / (1 - b)
    elif b == 0:
        return (x1 - a * x2) / (1 - a), x2
    x0 = ((b / a) * x1 + x2 - (x2 - x1) / (1 - a - b)) / (1 + b / a)
    x3 = (x2 - x1) / (1 - a - b) + x0
    return x0, x3


def get_limits(plottables,
               xpadding=0,
               ypadding=0.1,
               xerror_in_padding=True,
               yerror_in_padding=True,
               snap=True,
               logx=False,
               logy=False,
               logx_crop_value=1E-5,
               logy_crop_value=1E-5,
               logx_base=10,
               logy_base=10):
    """
    Get the axes limits that should be used for a 1D histogram, graph, or stack
    of histograms.
    Parameters
    ----------
    plottables : Hist, Graph, HistStack, or list of such objects
        The object(s) for which visually pleasing plot boundaries are
        requested.
    xpadding : float or 2-tuple, optional (default=0)
        The horizontal padding as a fraction of the final plot width.
    ypadding : float or 2-tuple, optional (default=0.1)
        The vertical padding as a fraction of the final plot height.
    xerror_in_padding : bool, optional (default=True)
        If False then exclude the x error bars from the calculation of the plot
        width.
    yerror_in_padding : bool, optional (default=True)
        If False then exclude the y error bars from the calculation of the plot
        height.
    snap : bool, optional (default=True)
        Make the minimum or maximum of the vertical range the x-axis depending
        on if the plot maximum and minimum are above or below the x-axis. If
        the plot maximum is above the x-axis while the minimum is below the
        x-axis, then this option will have no effect.
    logx : bool, optional (default=False)
        If True, then the x-axis is log scale.
    logy : bool, optional (default=False)
        If True, then the y-axis is log scale.
    logx_crop_value : float, optional (default=1E-5)
        If an x-axis is using a logarithmic scale then crop all non-positive
        values with this value.
    logy_crop_value : float, optional (default=1E-5)
        If the y-axis is using a logarithmic scale then crop all non-positive
        values with this value.
    logx_base : float, optional (default=10)
        The base used for the logarithmic scale of the x-axis.
    logy_base : float, optional (default=10)
        The base used for the logarithmic scale of the y-axis.
    Returns
    -------
    xmin, xmax, ymin, ymax : tuple of plot boundaries
        The computed x and y-axis ranges.
    """
    try:
        import numpy as np
        use_numpy = True
    except ImportError:
        use_numpy = False


    if not isinstance(plottables, (list, tuple)):
        plottables = [plottables]

    xmin = float('+inf')
    xmax = float('-inf')
    ymin = float('+inf')
    ymax = float('-inf')

    for h in plottables:

        if isinstance(h, HistStack):
            h = h.sum

        if not isinstance(h, (_Hist, _Graph1DBase)):
            raise TypeError(
                "unable to determine plot axes ranges "
                "from object of type `{0}`".format(
                    type(h)))

        if use_numpy:
            y_array_min = y_array_max = np.array(list(h.y()))
            if yerror_in_padding:
                y_array_min = y_array_min - np.array(list(h.yerrl()))
                y_array_max = y_array_max + np.array(list(h.yerrh()))
            _ymin = y_array_min.min() if y_array_min.size else float('+inf')
            _ymax = y_array_max.max() if y_array_max.size else float('-inf')
        else:
            y_array_min = y_array_max = list(h.y())
            if yerror_in_padding:
                y_array_min = multisub(y_array_min, list(h.yerrl()))
                y_array_max = multiadd(y_array_max, list(h.yerrh()))
            _ymin = min(y_array_min) if y_array_min else float('+inf')
            _ymax = max(y_array_max) if y_array_max else float('-inf')

        if isinstance(h, _Graph1DBase):
            if use_numpy:
                x_array_min = x_array_max = np.array(list(h.x()))
                if xerror_in_padding:
                    x_array_min = x_array_min - np.array(list(h.xerrl()))
                    x_array_max = x_array_max + np.array(list(h.xerrh()))
                _xmin = x_array_min.min() if x_array_min.size else float('+inf')
                _xmax = x_array_max.max() if x_array_max.size else float('-inf')
            else:
                x_array_min = x_array_max = list(h.x())
                if xerror_in_padding:
                    x_array_min = multisub(x_array_min, list(h.xerrl()))
                    x_array_max = multiadd(x_array_max, list(h.xerrh()))
                _xmin = min(x_array_min)
                _xmax = max(x_array_max)
        else:
            _xmin = h.xedgesl(1)
            _xmax = h.xedgesh(h.nbins(0))

        if logy:
            _ymin = max(logy_crop_value, _ymin)
            _ymax = max(logy_crop_value, _ymax)
        if logx:
            _xmin = max(logx_crop_value, _xmin)
            _xmax = max(logx_crop_value, _xmax)

        if _xmin < xmin:
            xmin = _xmin
        if _xmax > xmax:
            xmax = _xmax
        if _ymin < ymin:
            ymin = _ymin
        if _ymax > ymax:
            ymax = _ymax

    if isinstance(xpadding, (list, tuple)):
        if len(xpadding) != 2:
            raise ValueError("xpadding must be of length 2")
        xpadding_left = xpadding[0]
        xpadding_right = xpadding[1]
    else:
        xpadding_left = xpadding_right = xpadding

    if isinstance(ypadding, (list, tuple)):
        if len(ypadding) != 2:
            raise ValueError("ypadding must be of length 2")
        ypadding_top = ypadding[0]
        ypadding_bottom = ypadding[1]
    else:
        ypadding_top = ypadding_bottom = ypadding

    if logx:
        x0, x3 = _limits_helper(
            log(xmin, logx_base), log(xmax, logx_base),
            xpadding_left, xpadding_right)
        xmin = logx_base ** x0
        xmax = logx_base ** x3
    else:
        xmin, xmax = _limits_helper(
            xmin, xmax, xpadding_left, xpadding_right)

    if logy:
        y0, y3 = _limits_helper(
            log(ymin, logy_base), log(ymax, logy_base),
            ypadding_bottom, ypadding_top, snap=False)
        ymin = logy_base ** y0
        ymax = logy_base ** y3
    else:
        ymin, ymax = _limits_helper(
            ymin, ymax, ypadding_bottom, ypadding_top, snap=snap)

    return xmin, xmax, ymin, ymax


def draw(plottables, pad=None, same=False,
         xaxis=None, yaxis=None,
         xtitle=None, ytitle=None,
         xlimits=None, ylimits=None,
         xdivisions=None, ydivisions=None,
         logx=False, logy=False,
         **kwargs):
    """
    Draw a list of histograms, stacks, and/or graphs.
    Parameters
    ----------
    plottables : Hist, Graph, HistStack, or list of such objects
        List of objects to draw.
    pad : Pad or Canvas, optional (default=None)
        The pad to draw onto. If None then use the current global pad.
    same : bool, optional (default=False)
        If True then use 'SAME' draw option for all objects instead of
        all but the first. Use this option if you are drawing onto a pad
        that already holds drawn objects.
    xaxis : TAxis, optional (default=None)
        Use this x-axis or use the x-axis of the first plottable if None.
    yaxis : TAxis, optional (default=None)
        Use this y-axis or use the y-axis of the first plottable if None.
    xtitle : str, optional (default=None)
        Set the x-axis title.
    ytitle : str, optional (default=None)
        Set the y-axis title.
    xlimits : tuple, optional (default=None)
        Set the x-axis limits with a 2-tuple of (min, max)
    ylimits : tuple, optional (default=None)
        Set the y-axis limits with a 2-tuple of (min, max)
    xdivisions : int, optional (default=None)
        Set the number of divisions for the x-axis
    ydivisions : int, optional (default=None)
        Set the number of divisions for the y-axis
    logx : bool, optional (default=False)
        If True, then set the x-axis to log scale.
    logy : bool, optional (default=False)
        If True, then set the y-axis to log scale.
    kwargs : dict
        All extra arguments are passed to get_limits when determining the axis
        limits.
    Returns
    -------
    (xaxis, yaxis), (xmin, xmax, ymin, ymax) : tuple
        The axes and axes bounds.
    See Also
    --------
    get_limits
    """
    import ROOT
    context = preserve_current_canvas if pad else do_nothing
    if not isinstance(plottables, (tuple, list)):
        plottables = [plottables]
    elif not plottables:
        raise ValueError("plottables is empty")
    with context():
        if pad is not None:
            pad.cd()
        # get the axes limits
        xmin, xmax, ymin, ymax = get_limits(plottables,
                                            logx=logx, logy=logy,
                                            **kwargs)
        if xlimits is not None:
            xmin, xmax = xlimits
        if ylimits is not None:
            ymin, ymax = ylimits
        if not same:
            obj = plottables.pop(0)
            if isinstance(obj, ROOT.THStack):
                obj.SetMinimum(ymin)
                obj.SetMaximum(ymax)
            obj.Draw()
            xaxis = obj.xaxis
            yaxis = obj.yaxis
        # draw the plottables
        for i, obj in enumerate(plottables):
            if i == 0 and isinstance(obj, ROOT.THStack):
                # use SetMin/Max for y-axis
                obj.SetMinimum(ymin)
                obj.SetMaximum(ymax)
                # ROOT: please fix this...
            obj.Draw('SAME')
        # set the axes limits and titles
        if xaxis is not None:
            xaxis.SetLimits(xmin, xmax)
            xaxis.SetRangeUser(xmin, xmax)
            if xtitle is not None:
                xaxis.SetTitle(xtitle)
            if xdivisions is not None:
                xaxis.SetNdivisions(xdivisions)
        if yaxis is not None:
            yaxis.SetLimits(ymin, ymax)
            yaxis.SetRangeUser(ymin, ymax)
            if ytitle is not None:
                yaxis.SetTitle(ytitle)
            if ydivisions is not None:
                yaxis.SetNdivisions(ydivisions)
        if pad is None:
            pad = ROOT.gPad
        pad.SetLogx(bool(logx))
        pad.SetLogy(bool(logy))
        # redraw axes on top
        # axes ticks sometimes get hidden by filled histograms
        pad.RedrawAxis()
    return (xaxis, yaxis), (xmin, xmax, ymin, ymax)





class LabelTextAlignmentError(Exception):
    pass


class LabelPositionError(Exception):
    pass


class LabelBase(ROOT.TLatex):
    """The base label class."""

    # Tuples of horizontal and vertical text alignment names and
    # their corresponding ROOT text alignment integer values.
    TEXT_ALIGNMENT = {
        ('left', 'bottom'): 11,
        ('left', 'center'): 12,
        ('left', 'top'): 13,
        ('center', 'bottom'): 21,
        ('center', 'center'): 22,
        ('center', 'top'): 23,
        ('right', 'bottom'): 31,
        ('right', 'center'): 32,
        ('right', 'top'): 33,
    }

    def __init__(self):
        super(LabelBase, self).__init__()

    @property
    def align(self):
        return self.GetTextAlign()

    @align.setter
    def align(self, value):
        if value in self.TEXT_ALIGNMENT:
            self.SetTextAlign(self.TEXT_ALIGNMENT[value])
        elif value in self.TEXT_ALIGNMENT.values():
            self.SetTextAlign(value)
        else:
            raise LabelTextAlignmentError('Unrecognized value: {0!s}'.format(value))

    @property
    def font(self):
        return self.GetTextFont()

    @font.setter
    def font(self, value):
        self.SetTextFont(value)

    @property
    def size(self):
        return self.GetTextSize()

    @size.setter
    def size(self, value):
        self.SetTextSize(value)

    @staticmethod
    def get_canvas_margins():
        """Return the top, right, bottom, and left margins of the active canvas.
        Figure labels are often oriented relative to these margins.
        """
        return ROOT.gPad.GetTopMargin(), ROOT.gPad.GetRightMargin(), ROOT.gPad.GetBottomMargin(), ROOT.gPad.GetLeftMargin()


class CMSLabel(LabelBase):
    """A label displaying the CMS name.
    Credits to Gautier Hamel de Monchenault (Saclay), Joshua Hardenbrook (Princeton),
    and Dinko Ferencek (Rutgers) for the initial Python implementation.
    The label's text and style properties, which are set to default values from the
    CMS Publication Committee, are exposed as instance attributes for customization:
    text : string
        The CMS label text. The default is "CMS".
    position : string
        One of the following label positions on the active canvas:
            :left: The top left corner inside the frame (default)
            :center: The top center inside the frame
            :right: The top right corner inside the frame
            :outside: The top left corner outside the frame
    font : int
        The text font code. The default is 61 (Helvetica Bold).
    scale : float
        The text size scale relative to the size of the top margin
        of the active canvas. The default is 0.75.
    padding_left : float
        The amount of padding to the left of the text when positioned
        inside the frame, relative to the frame width of the active canvas.
        The default is 0.045.
    padding_right : float
        The amount of padding to the right of the text when positioned
        inside the frame, relative to the frame width of the active canvas.
        The default is 0.045.
    padding_top : float
        The amount of padding above the text. When positioned inside of
        the frame, it is relative to the frame height of the active canvas
        and the default is 0.035. When positioned outside of the frame, it
        is relative to the size of the top margin of the active canvas and
        the default is 0.8.
    sublabel.text : string
        The sublabel text positioned below the main text inside of the frame
        or to the right of the main text outside of the frame. Common examples
        are "Preliminary", "Simulation", or "Unpublished". The default is an
        empty string for no sublabel.
    sublabel.font : string
        The sublabel text font code. The default is 52 (Helvetica Italic).
    sublabel.scale : float
        The sublabel text size scale relative to the size of the main text.
        The default is 0.76.
    sublabel.padding_left : float
        The amount of padding to the left of the sublabel text relative to the
        frame width of the active canvas. This only applies if the main text is
        positioned outside the frame of the active canvas. The default is 0.12.
    sublabel.padding_top : float
        The amount of padding above the sublabel text relative to the size of
        the main text. This only applies if the main text is positioned inside
        the frame of the active canvas. The default is 1.2.
    """
    def __init__(self):
        super(CMSLabel, self).__init__()
        self.text = 'CMS'
        self.position = 'left'
        self.font = 61
        self.scale = 0.75
        self.padding_left = 0.045
        self.padding_right = 0.045
        self.padding_top = None
        self.sublabel = LabelBase()
        self.sublabel.text = ''
        self.sublabel.font = 52
        self.sublabel.scale = 0.76
        self.sublabel.padding_left = 0.12
        self.sublabel.padding_top = 1.2

    def draw(self):
        """Draw the CMS label and sublabel on the active canvas."""
        # Draw the label.
        if self.position == 'left':
            label_coordinates = self._draw_label_left()
        elif self.position == 'center':
            label_coordinates = self._draw_label_center()
        elif self.position == 'right':
            label_coordinates = self._draw_label_right()
        elif self.position == 'outside':
            label_coordinates = self._draw_label_outside()
        else:
            raise LabelPositionError('Unrecognized value: {0}'.format(self.position))
        # Draw the sublabel.
        if self.sublabel.text:
            if self.position == 'outside':
                self._draw_sublabel_outside(*label_coordinates)
            else:
                self._draw_sublabel_inside(*label_coordinates)

    def _draw_label_left(self):
        """Draw the label on the top left corner inside the frame and return its coordinates."""
        top_margin, right_margin, bottom_margin, left_margin = self.get_canvas_margins()
        self.size = self.scale * top_margin
        self.align = ('left', 'top')
        x = left_margin + self.padding_left * (1 - left_margin - right_margin)
        y = 1 - top_margin - (self.padding_top or 0.035) * (1 - top_margin - bottom_margin)
        self.DrawLatexNDC(x, y, self.text)
        return x, y

    def _draw_label_center(self):
        """Draw the label on the top center inside the frame and return its coordinates."""
        top_margin, right_margin, bottom_margin, left_margin = self.get_canvas_margins()
        self.size = self.scale * top_margin
        self.align = ('center', 'top')
        x = left_margin + 0.5 * (1 - left_margin - right_margin)
        y = 1 - top_margin - (self.padding_top or 0.035) * (1 - top_margin - bottom_margin)
        self.DrawLatexNDC(x, y, self.text)
        return x, y

    def _draw_label_right(self):
        """Draw the label on the top right corner inside the frame and return its coordinates."""
        top_margin, right_margin, bottom_margin, left_margin = self.get_canvas_margins()
        self.size = self.scale * top_margin
        self.align = ('right', 'top')
        x = 1 - right_margin - self.padding_right * (1 - left_margin - right_margin)
        y = 1 - top_margin - (self.padding_top or 0.035) * (1 - top_margin - bottom_margin)
        self.DrawLatexNDC(x, y, self.text)
        return x, y

    def _draw_label_outside(self):
        """Draw the label on the top left corner outside the frame and return its coordinates."""
        top_margin, _, _, left_margin = self.get_canvas_margins()
        self.size = self.scale * top_margin
        self.align = ('left', 'bottom')
        x = left_margin
        y = 1 - (self.padding_top or 0.8) * top_margin
        self.DrawLatexNDC(x, y, self.text)
        return x, y

    def _draw_sublabel_inside(self, x_label, y_label):
        """Draw the sublabel below the label inside the frame."""
        self.sublabel.size = self.sublabel.scale * self.size
        self.sublabel.align = self.align
        x_sublabel = x_label
        y_sublabel = y_label - self.sublabel.padding_top * self.size
        self.sublabel.DrawLatexNDC(x_sublabel, y_sublabel, self.sublabel.text)

    def _draw_sublabel_outside(self, x_label, y_label):
        """Draw the sublabel to the right of the label outside the frame."""
        _, right_margin, _, left_margin = self.get_canvas_margins()
        self.sublabel.size = self.sublabel.scale * self.size
        self.sublabel.align = self.align
        x_sublabel = left_margin + self.sublabel.padding_left * (1 - left_margin - right_margin)
        y_sublabel = y_label
        self.sublabel.DrawLatexNDC(x_sublabel, y_sublabel, self.sublabel.text)


class LuminosityLabel(LabelBase):
    """A label displaying the integrated luminosity and center-of-mass energy.
    Credits to Gautier Hamel de Monchenault (Saclay), Joshua Hardenbrook (Princeton),
    and Dinko Ferencek (Rutgers) for the initial Python implementation.
    The label's text and style properties, which are set to default values from the
    CMS Publication Committee, are exposed as instance attributes for customization:
    font : int
        The text font code. The default is 42 (Helvetica).
    scale : float
        The text size scale relative to the size of the top margin
        of the active canvas. The default is 0.6.
    align : int or 2-tuple of strings
        The text alignment relative to the drawing coordinates of the text as
        either an integer code or tuple of horizontal and vertical alignment
        names, respectively. The default is 31, or ("right", "bottom").
    padding_top : float
        The amount of padding above the text relative to the size
        of the top margin of the active canvas. The default is 0.8.
    Parameters
    ----------
    text : string
        The luminosity label text. Data taking periods must be separated by
        the "+" symbol, e.g. "19.7 fb^{-1} (8 TeV) + 4.9 fb^{-1} (7 TeV)".
    """
    def __init__(self, text):
        super(LuminosityLabel, self).__init__()
        self.text = text
        self.font = 42
        self.scale = 0.6
        self.align = 31
        self.padding_top = 0.8

    def draw(self):
        """Draw the luminosity label on the active canvas."""
        top_margin, right_margin, _, _ = self.get_canvas_margins()
        self.size = self.scale * top_margin
        x = 1 - right_margin
        y = 1 - self.padding_top * top_margin
        self.DrawLatexNDC(x, y, self.text)



def draw_labels(lumi_text, cms_position='left', extra_text=''):
    """Draw the CMS Publication Committee figure labels on the active canvas.
    Parameters
    ----------
    lumi_text : string
        The luminosity label text. Data taking periods must be separated by
        the "+" symbol, e.g. "19.7 fb^{-1} (8 TeV) + 4.9 fb^{-1} (7 TeV)".
    cms_position : string, optional
        The CMS label position on the active canvas:
            :left: The top left corner inside the frame (default)
            :center: The top center inside the frame
            :right: The top right corner inside the frame
            :outside: The top left corner outside the frame
    extra_text : string, optional
        The sublabel text positioned below the CMS label inside of the frame
        or to the right of the CMS label outside of the frame. Common examples
        are "Preliminary", "Simulation", or "Unpublished". The default is an
        empty string for no sublabel.
    """
    cms_label = CMSLabel()
    cms_label.position = cms_position
    cms_label.sublabel.text = extra_text
    cms_label.draw()
    lumi_label = LuminosityLabel(lumi_text)
    lumi_label.draw()
    ROOT.gPad.Update()
