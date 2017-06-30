#!/usr/bin/env python

# (C) Nikolay Khokhlov <k_h@inbox.ru> 2017

import argparse
import sys
import numpy as np
from scipy.interpolate import RectBivariateSpline
from binjson import load_bin, save_bin


def main():
    parser = argparse.ArgumentParser(description = 'Reshape 2D data.')
    parser.add_argument('input', help='input file')
    parser.add_argument('output', help='output file')
    parser.add_argument('-s', '--size', help='number of nodes at x, y-direction', type=int, nargs=2, required = True)
    
    args = parser.parse_args()

    jd, d = load_bin(args.input)
    b = jd['bbox']
    s = jd['size']
    n = args.size
    x = np.linspace(b[0], b[1], s[0])
    y = np.linspace(b[2], b[3], s[1])
    
    newx = np.linspace(b[0], b[1], n[0])
    newy = np.linspace(b[2], b[3], n[1])
    
    f = RectBivariateSpline(y, x, d)
    
    data = f(newy, newx)
    
    save_bin(args.output, data, jd['bbox'])

if __name__ == "__main__":
    main()
