#!/usr/bin/env python

# (C) Nikolay Khokhlov <k_h@inbox.ru> 2017

import argparse
import sys
import numpy as np
from scipy.interpolate import RegularGridInterpolator
from binjson import load_bin, save_bin

def main():
    parser = argparse.ArgumentParser(description = 'Place 3D data (input1) inside other 3D data (input2).')
    parser.add_argument('input1', help='input1 file')
    parser.add_argument('input2', help='input2 file')
    parser.add_argument('output', help='output file')
    parser.add_argument('-i', '--index', help='index', type=int, nargs=3, required = True)
    
    args = parser.parse_args()

    jd1, d1 = load_bin(args.input1)
    jd2, d2 = load_bin(args.input2)
    bb = jd1['bbox']
    i = args.index
    d2[i[2]:i[2]+d1.shape[0], i[1]:i[1]+d1.shape[1], i[0]:i[0]+d1.shape[2]] = d1
    
    
    save_bin(args.output, d2, jd2['bbox'])

if __name__ == "__main__":
    main()
