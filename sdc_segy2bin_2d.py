#!/usr/bin/env python

# Script to convert 2d segy data to binary file.
# (C) Nikolay Khokhlov <k_h@inbox.ru> 2017

import argparse
import sys
import numpy as np
from binjson import load_bin, save_bin
from segypy import read_segy


def four_floats(value):
    values = value.split()
    if len(values) != 4:
        raise argparse.ArgumentError
    values = map(float, values)
    return values


def main():
    parser = argparse.ArgumentParser(description = 'Convert 2d segy data to binary file.')
    parser.add_argument('input', help='input segy file')
    parser.add_argument('output', help='output json bin file')
    parser.add_argument('-b', '--bounds', help='bounding box', type=four_floats, metavar='"xmin xmax ymin ymax"', required = False)
    parser.add_argument('-c', '--scale-coords', help='scale coords', type=float, default=1.0, metavar='SCALE', required = False)
    parser.add_argument('-v', '--scale-values', help='scale values', type=float, default=1.0, metavar='SCALE', required = False)
    
    args = parser.parse_args()

    data, header, trace_header = read_segy(file(args.input, 'rb'))
    
    # get dy
    dy = header['dt'] * args.scale_coords
    by = dy * header['ns']
    
    # get dx
    dx1 = trace_header['GroupX'][1] - trace_header['GroupX'][0]
    dx2 = trace_header['GroupY'][1] - trace_header['GroupY'][0]
    dx = (dx1**2 + dx2**2)**0.5 * args.scale_coords
    bx = dx * header['ntraces']
    
    bounds = [0.0, bx, 0.0, by]
    
    if args.bounds:
        bounds = args.bounds
    
    save_bin(args.output, data * args.scale_values, bounds)
    
if __name__ == "__main__":
    main()
