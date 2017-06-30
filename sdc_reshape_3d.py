#!/usr/bin/env python

# (C) Nikolay Khokhlov <k_h@inbox.ru> 2017

import argparse
import sys
import numpy as np
from scipy.interpolate import RegularGridInterpolator
from binjson import load_bin, save_bin


def main():
    parser = argparse.ArgumentParser(description = 'Reshape 3D data.')
    parser.add_argument('input', help='input file')
    parser.add_argument('output', help='output file')
    parser.add_argument('-s', '--size', help='number of nodes at x, y, z-direction', type=int, nargs=3, required = True)
    
    args = parser.parse_args()

    jd, d = load_bin(args.input)
    b = jd['bbox']
    s = jd['size']
    n = args.size
    x = np.linspace(b[0], b[1], s[0])
    y = np.linspace(b[2], b[3], s[1])
    z = np.linspace(b[4], b[5], s[2])
    
    newx = np.linspace(b[0], b[1], n[0])
    newy = np.linspace(b[2], b[3], n[1])
    newz = np.linspace(b[4], b[5], n[2])
    f = RegularGridInterpolator(points = (z, y, x), values = d, fill_value = None)
    z, y, x = np.meshgrid(newz, newy, newx, indexing='ij')
    data = f((z.ravel(), y.ravel(), x.ravel()))
    save_bin(args.output, data.reshape(n[::-1]), jd['bbox'])

if __name__ == "__main__":
    main()
