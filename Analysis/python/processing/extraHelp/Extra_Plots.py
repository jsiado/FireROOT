#!/usr/bin/env python
#from __future__ import print_function

import matplotlib.pylab as plt
import numpy as np

myTRGm = {"L2Mu23NoVtx_2Cha":15963,
          "L2Mu23NoVtx_2Cha_NoL2Matched":16257,
          "L2Mu23NoVtx_2Cha_CosmicSeed":11994,
          "L2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched":12087,
          #"DoubleL2Mu25NoVtx_2Cha":15685,
          #"DoubleL2Mu25NoVtx_2Cha_NoL2Matched":15974,
          #"DoubleL2Mu25NoVtx_2Cha_CosmicSeed":11602,
          #"DoubleL2Mu25NoVtx_2Cha_CosmicSeed_NoL2Matched":11693,
          "L2Mu25NoVtx_2Cha_Eta2p4":16433,
          "L2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4":11929}

myTRGe = {"L2Mu23NoVtx_2Cha":4457,
          "L2Mu23NoVtx_2Cha_NoL2Matched":4875,
          "L2Mu23NoVtx_2Cha_CosmicSeed":3332,
          "L2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched":3367,
          #"DoubleL2Mu25NoVtx_2Cha":4227,
          #"DoubleL2Mu25NoVtx_2Cha_NoL2Matched":4635,
          #"DoubleL2Mu25NoVtx_2Cha_CosmicSeed":3114,
          #"DoubleL2Mu25NoVtx_2Cha_CosmicSeed_NoL2Matched":3147,
          "L2Mu25NoVtx_2Cha_Eta2p4":4271,
          "L2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4":3146,}


x = [i for i in range(0,6)]

listm = sorted(myTRGm.items()) # sorted by key, return a list of tuples
liste = sorted(myTRGe.items())
xTicks, y = zip(*listm) # unpack a list of pairs into two tuples
xTicks, z = zip(*liste)
plt.figure(facecolor="white")
plt.xticks(x,xTicks)
plt.xticks(range(6),xTicks,rotation = 90)
plt.plot(x,y,'b*-', label = '4mu')
plt.plot(x,z,'r*-',label = '2mu2e')
plt.title('Double Mu triggers')
plt.gca().set_xlabel('Trigger path')
plt.gca().set_ylabel('# events')
plt.grid(True)
legend = plt.gca().legend(loc='upper left', fontsize='large')
plt.savefig('dmutrigger.png')
plt.show()
