#!/usr/bin/env python

# (C) Nikolay Khokhlov <k_h@inbox.ru> 2017

import argparse
import numpy as np
import sys
from scipy import interpolate
from binjson import load_bin, save_bin


def main():
    parser = argparse.ArgumentParser(description = 'Set values between fault.')
    parser.add_argument('input', help='input file')
    parser.add_argument('f1', help='fault bottom')
    parser.add_argument('f2', help='fault top')
    parser.add_argument('output', help='output file')
    parser.add_argument('-v', '--value', help='fault value', type=float, required = True)
    
    args = parser.parse_args()
    jd, data = load_bin(args.input)
    
    bb = jd['bbox']
    xl = np.linspace(bb[0], bb[1], data.shape[1])
    yl = np.linspace(bb[2], bb[3], data.shape[0])
    
    print bb

    
    f1 = np.loadtxt(args.f1)
    ff1 = interpolate.interp1d(f1[:,0], f1[:,1] + 150.0, bounds_error = False, fill_value = 'extrapolate')
    f2 = np.loadtxt(args.f2)
    ff2 = interpolate.interp1d(f2[:,0], f2[:,1] + 150.0, bounds_error = False, fill_value = 'extrapolate')
    
    rmin = min(f1[:,0].min(), f2[:,0].min())
    rmax = max(f1[:,0].max(), f2[:,0].max())
    
    
    for i in range(data.shape[1]):
        if xl[i] < rmin or xl[i] > rmax:
            continue
        y1 = ff1(xl[i])
        y2 = ff2(xl[i])
        for j in range(data.shape[0]):
            if yl[j] >= y1 and yl[j] <= y2:
                data[j, i] = args.value
    
    save_bin(args.output, data, jd['bbox'])

if __name__ == "__main__":
    main()
