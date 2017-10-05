#!/usr/bin/env python

# (C) Nikolay Khokhlov <k_h@inbox.ru> 2017

import argparse
import sys
import numpy as np
from scipy.interpolate import RegularGridInterpolator
from binjson import load_bin, save_bin


def main():
    parser = argparse.ArgumentParser(description = 'Interpolate 3D data to points.')
    parser.add_argument('input', help='input file')
    parser.add_argument('coords', help='coords file (x y z format)')
    
    args = parser.parse_args()

    jd, d = load_bin(args.input)
    b = jd['bbox']
    s = jd['size']
    x = np.linspace(b[0], b[1], s[0])
    y = np.linspace(b[2], b[3], s[1])
    z = np.linspace(b[4], b[5], s[2])
    
    f = RegularGridInterpolator(points = (z, y, x), values = d, fill_value = None)

    c = np.loadtxt(args.coords)
    
    data = f((c[:,2], c[:,1], c[:,0]))
    
    for i in data:
        print i

if __name__ == "__main__":
    main()
