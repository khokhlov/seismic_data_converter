#!/usr/bin/env python

# (C) Nikolay Khokhlov <k_h@inbox.ru> 2017

import argparse
import sys
import numpy as np
from scipy.interpolate import RectBivariateSpline
from binjson import load_bin, save_bin
from segypy import write_segy


def main():
    parser = argparse.ArgumentParser(description = 'Convert bin to segy.')
    parser.add_argument('input', help='input file')
    parser.add_argument('output', help='output file')
    
    args = parser.parse_args()

    jd, d = load_bin(args.input)
    b = jd['bbox']
    s = jd['size']
    
    spacing = (b[5] - b[4]) / d.shape[0]
    
    x = np.linspace(b[0], b[1], d.shape[2])
    y = np.linspace(b[2], b[3], d.shape[1])
    xv, yv = np.meshgrid(x, y, sparse=False, indexing='ij')
    
    header = {}
    header['GroupX'] = xv.ravel()
    header['GroupY'] = yv.ravel()
    

    write_segy(args.output, d.reshape((d.shape[0], d.shape[1]*d.shape[2])), dt = spacing, trace_header_in = header)


if __name__ == "__main__":
    main()
