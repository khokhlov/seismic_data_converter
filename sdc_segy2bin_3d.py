#!/usr/bin/env python

# Script to convert 3d segy data to binary file.
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
    parser = argparse.ArgumentParser(description = 'Convert 3d segy data to binary file.')
    parser.add_argument('input', help='input segy file')
    parser.add_argument('output', help='output json bin file')
    parser.add_argument('-b', '--bounds', help='bounding box', type=six_floats, metavar='"xmin xmax ymin ymax zmin zmax"', required = True)
    parser.add_argument('-s', '--size', help='num nodes at x y direction', type=int, nargs=2, required = True)
    
    args = parser.parse_args()

    data, header, trace_header = read_segy(file(args.input, 'rb'))
    
    save_bin(args.output, data.reshape([data.shape[0],] + args.size[::-1]), args.bounds)
    
if __name__ == "__main__":
    main()
