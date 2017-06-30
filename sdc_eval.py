#!/usr/bin/env python

# (C) Nikolay Khokhlov <k_h@inbox.ru> 2017

import argparse
import sys
import numpy as np
from binjson import load_bin, save_bin


def main():
    parser = argparse.ArgumentParser(description = 'Evaluate any expression.')
    parser.add_argument('expr', help='expression', type=str)
    parser.add_argument('output', help='output file')
    parser.add_argument('-a', help='a-parameter', type=str, required = True)
    parser.add_argument('-b', help='b-parameter', type=str)
    parser.add_argument('-c', help='c-parameter', type=str)
    parser.add_argument('-d', help='d-parameter', type=str)
    
    args = parser.parse_args()

    a = b = c = d = None
    jd, a = load_bin(args.a)
    if args.b:
        jd, b = load_bin(args.b)
    if args.c:
        jd, c = load_bin(args.c)
    if args.d:
        jd, d = load_bin(args.d)
    
    data = eval(args.expr)
    
    save_bin(args.output, data, jd['bbox'])

if __name__ == "__main__":
    main()
