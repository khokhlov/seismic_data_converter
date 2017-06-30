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
    parser.add_argument('-b', '--bounds', help='bounding box', type=four_floats, metavar='"xmin xmax ymin ymax"', required = True)
    
    args = parser.parse_args()

    data, header, trace_header = read_segy(file(args.input, 'rb'))
    
    save_bin(args.output, data, args.bounds)
    
if __name__ == "__main__":
    main()
