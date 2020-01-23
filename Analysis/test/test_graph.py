# create a graph
from rootpy.plotting import Graph
from rootpy.plotting.style import set_style
from FireROOT.Analysis.Utils import *
from math import sin

set_style(MyStyle())

c = ROOT.Canvas()
objects = []
graph = Graph(10, drawstyle='AP')
for i in range(10):
    x = -2 + i * 4 / 10.
    graph.SetPoint(i, x, 40 + 10 * sin(x))
objects.append(graph)

draw(objects, xtitle='Some Variable [Units]', ytitle='Events', ypadding=0.05)
graph.GetHistogram().SetMaximum(100)
print(graph.GetCorrelationFactor())

c.SaveAs('test_graph.pdf')