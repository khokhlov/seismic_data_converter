#!/usr/bin/env python

# (C) Nikolay Khokhlov <k_h@inbox.ru> 2019

import argparse
import sys
import numpy as np
from scipy.interpolate import RegularGridInterpolator
from binjson import load_bin, save_bin


def main():
    parser = argparse.ArgumentParser(description = 'Slice 3D data by one coordinate.')
    parser.add_argument('input', help='input file')
    parser.add_argument('-a', '--value', help='coordinate value', type=float, required = True)
    parser.add_argument('-c', '--coord', help='coordinate index -- 0, 1, or 2', type=int, required = True)
    parser.add_argument('output', help='output file')
    
    args = parser.parse_args()

    jd, d = load_bin(args.input)
    b = jd['bbox']
    s = jd['size']
    x = np.linspace(b[0], b[1], s[0])
    y = np.linspace(b[2], b[3], s[1])
    z = np.linspace(b[4], b[5], s[2])
    """
    f = RegularGridInterpolator(points = (z, y, x), values = d, fill_value = None)

    c = np.loadtxt(args.coords)
    
    data = f((c[:,2], c[:,1], c[:,0]))
    
    for i in data:
        print i
    """
    if args.coord == 1:
        if args.value >= b[2] and args.value <= b[3]:
            h = (b[3] - b[2]) / s[1]
            print "Y spacing", h
            ind = int((args.value - b[2]) / h)
            print "Y index", ind
            ind2 = ind + 1
            y1 = y[ind]
            y2 = y[ind2]
            print "Interpolate between", y1, y2
            c1 = (y2 - args.value) / (y2 - y1)
            c2 = 1.0 - c1
            newd = d[:, ind, :] * c1 + d[:, ind2, :] * c2
            save_bin(args.output, newd, [b[0], b[1], b[4], b[5]])
    else:
        print "Invalid coord value:", args.coord
if __name__ == "__main__":
    main()
