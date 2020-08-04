#!/usr/bin/env python
from rootpy import log
log = log['/SIDM.Limit']

def optimized_boundary(channel, params):
    assert(channel in ['2mu2e', '4mu'])
    mxx, ma, lxy = params

    if channel == '4mu':
        category1 = [
            (100, 0.25, 0.3),
            (100, 1.2,  0.3),
        ]
        category2 = [
            (100, 0.25, 30 ),
            (100, 0.25, 150),
            (100, 0.25, 300),
            (100, 1.2 , 150),
            (100, 1.2 , 300),
            (100, 5   , 150),
            (100, 5   , 300),
        ]

        # if   params in category1: return (19, 12) # (0.95pi/0.05pi, 0.3/0.025)
        # elif params in category2: return (19, 10) # (0.95pi/0.05pi, 0.25/0.025)
        # else:                     return (19, 8 ) # (0.95pi/0.05pi, 0.2/0.025)

        if   params in category1: return (18, 12) # (0.9pi/0.05pi, 0.3/0.025)
        elif params in category2: return (18, 10) # (0.9pi/0.05pi, 0.25/0.025)
        else:                     return (18, 8 ) # (0.9pi/0.05pi, 0.2/0.025)

    elif channel == '2mu2e':
        emptyones = [
            ( 100, 0.25, 0.3),
            ( 100, 1.2 , 0.3),
            ( 150, 1.2 , 0.3),
            ( 500, 5   , 0.3),
            ( 800, 5   , 0.3),
            (1000, 5   , 0.3),
        ]

        if params in emptyones: return (None, None)
        elif mxx<=200:          return (18, 4) # (0.9pi/0.05pi, 0.1/0.025)
        else:                   return (18, 2) # (0.9pi/0.05pi, 0.05/0.025)

    return (None, None)


def closure_uncertainty(channel, boundary):
    assert(channel in ['2mu2e', '4mu'])

    if channel == '4mu':
        unc_map = {
            (19, 12) : 0.13,
            (19, 10) : 0.1225,
            (19, 8 ) : 0.1675,

            (18, 12) : 0.156,
            (18, 10) : 0.272,
            (18, 8 ) : 0.192,
        }
        return unc_map[boundary]

    if channel == '2mu2e':
        unc_map = {
            (18, 4) : 0.436,
            (18, 2) : 0.252,
        }
        return unc_map[boundary]

    return None

def abcd_bin_value(h, boundary):
    xbin, ybin = boundary
    res = [
        h.integral(     1,       xbin, ybin+1, h.nbins(1)), # A
        h.integral(xbin+1, h.nbins(0), ybin+1, h.nbins(1)), # B
        h.integral(     1,       xbin,      1,       ybin), # C
        h.integral(xbin+1, h.nbins(0),      1,       ybin), # D
    ]

    return res


genxsec = {
    100: 1.24451,
    150: 3.28918,
    200: 7.96058,
    500: 929.772,
    800: 10.6244,
    1000: 3.14398,
}