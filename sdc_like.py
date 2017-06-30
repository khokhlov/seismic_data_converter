#!/usr/bin/env python

# (C) Nikolay Khokhlov <k_h@inbox.ru> 2017

import argparse
import numpy as np
import sys
from binjson import load_bin, save_bin


def main():
    parser = argparse.ArgumentParser(description = 'Create data with constant value like existing array.')
    parser.add_argument('input', help='input file')
    parser.add_argument('output', help='output file')
    parser.add_argument('-a', '--value', help='value', type=float, required = True)
    
    args = parser.parse_args()
    jd, data = load_bin(args.input)
    
    save_bin(args.output, np.full_like(data, args.value), jd['bbox'])

if __name__ == "__main__":
    main()
