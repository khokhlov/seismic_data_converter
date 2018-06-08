#!/usr/bin/env python

# Script to txt data to binary file.
# (C) Nikolay Khokhlov <k_h@inbox.ru> 2017

import argparse
import sys
import numpy as np
from binjson import load_bin, save_bin
from segypy import read_segy


def six_floats(value):
    values = value.split()
    if len(values) != 6:
        raise argparse.ArgumentError
    values = map(float, values)
    return values


def main():
    parser = argparse.ArgumentParser(description = 'Convert txt data to binary file.')
    parser.add_argument('input', help='input txt file')
    parser.add_argument('output', help='output json bin file')
    parser.add_argument('-b', '--bounds', help='bounding box', type=six_floats, metavar='"xmin xmax ymin ymax zmin zmax"', required = False)
    parser.add_argument('-s', '--shape', help='shape', type=int, metavar='x y z', nargs=3, required = True)
    
    args = parser.parse_args()

    data = np.loadtxt(args.input)
    
    s = args.shape
    bounds = [0.0, s[0]]
    if s[1] > 1:
        bounds += [0.0, s[1]]
        if s[2] > 1:
            bounds += [0.0, s[2]]
    
    if args.bounds:
        bounds = args.bounds
    
    s1 = [s[0],]
    if s[1] > 1:
        s1 = [s[1],]+s1
    if s[2] > 1:
        s1 = [s[2],]+s1
    
    data = data.reshape(s1)
    
    save_bin(args.output, data, bounds)
    
if __name__ == "__main__":
    main()
