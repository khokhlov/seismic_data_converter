#!/usr/bin/env python

# (C) Nikolay Khokhlov <k_h@inbox.ru> 2017

import argparse
import sys
import numpy as np
from segypy import read_segy, write_segy

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
    a, h, th = read_segy(file(args.a, 'rb'))
    if args.b:
        b, h, th = read_segy(file(args.b, 'rb'))
    if args.c:
        c, h, th = read_segy(file(args.c, 'rb'))
    if args.d:
        d, h, th = read_segy(file(args.d, 'rb'))
    
    data = eval(args.expr)
    
    write_segy(args.output, data, dt = th['dt'][0], trace_header_in = th)

if __name__ == "__main__":
    main()
