#!/usr/bin/env python

# (C) Nikolay Khokhlov <k_h@inbox.ru> 2017

import argparse
import numpy as np
import sys
from binjson import load_bin, save_bin

def two_floats(value):
    values = value.split()
    if len(values) != 2:
        raise argparse.ArgumentError
    values = map(float, values)
    return values


def main():
    parser = argparse.ArgumentParser(description = 'Clip (limit) the values in an array.')
    parser.add_argument('input', help='input file')
    parser.add_argument('output', help='output file')
    parser.add_argument('-b', '--bounds', help='bounds for values', type=two_floats, metavar='"min max"', required = True)
    
    args = parser.parse_args()
    jd, data = load_bin(args.input)
    
    save_bin(args.output, np.clip(data, args.bounds[0], args.bounds[1]), jd['bbox'])

if __name__ == "__main__":
    main()
