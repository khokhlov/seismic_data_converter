#!/usr/bin/env python

# (C) Nikolay Khokhlov <k_h@inbox.ru> 2017

import argparse
import sys
import numpy as np
from scipy.interpolate import RectBivariateSpline
from binjson import load_bin, save_bin


def main():
    parser = argparse.ArgumentParser(description = 'Interpolate points 2d.')
    parser.add_argument('coords', help='coords file (x, y)')
    parser.add_argument('input', help='input files', nargs="+")

    
    args = parser.parse_args()
    
    c = np.loadtxt(args.coords)

    for i in args.input:
        jd, d = load_bin(i)
        b = jd['bbox']
        s = jd['size']
    
        x = np.linspace(b[0], b[1], s[0])
        y = np.linspace(b[2], b[3], s[1])
        d = d.reshape((s[1], s[0]))
    
        f = RectBivariateSpline(y, x, d, kx = 1, ky = 1)
        
        data = []
        if len(c.shape) == 1:
            data = f(c[1], c[0])
        else:
            data = [[]]
            for j in range(c.shape[0]):
                data[0].append(f(c[j,1], c[j,0])[0][0])
        
        s = ''
        for j in data[0]:
            s = '%s %s' % (s, j)
        print s

if __name__ == "__main__":
    main()
