#!/usr/bin/env python

# (C) Nikolay Khokhlov <k_h@inbox.ru> 2017

import argparse
import sys
import numpy as np
from scipy.interpolate import RegularGridInterpolator
from binjson import load_bin, save_bin

def three_floats(value):
    values = value.split()
    if len(values) != 3:
        raise argparse.ArgumentError
    values = map(float, values)
    return values

def main():
    parser = argparse.ArgumentParser(description = 'Translate 3D data.')
    parser.add_argument('input', help='input file')
    parser.add_argument('output', help='output file')
    parser.add_argument('-t', '--translate', help='vector', type=three_floats, metavar='"x y z"', required = True)
    
    args = parser.parse_args()

    jd, d = load_bin(args.input)
    bb = jd['bbox']
    bb[0] += args.translate[0]
    bb[1] += args.translate[0]
    
    bb[2] += args.translate[1]
    bb[3] += args.translate[1]
    
    bb[4] += args.translate[2]
    bb[5] += args.translate[2]
    save_bin(args.output, d, bb)

if __name__ == "__main__":
    main()
