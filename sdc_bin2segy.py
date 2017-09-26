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

    write_segy(args.output, d.reshape((d.shape[0], d.shape[1]*d.shape[2])), dt = 1000000.0 * spacing)


if __name__ == "__main__":
    main()
