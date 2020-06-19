#!/usr/bin/env python

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
    parser = argparse.ArgumentParser(description = 'Merge binary files by y-axis.')
    parser.add_argument('output', help='output json bin file')
    parser.add_argument('files', help='files to merge', nargs="+")
    parser.add_argument('-y', '--yspacing', help='spacing at y direction', type=float, required = True)
    
    args = parser.parse_args()
    
    ny = len(args.files)
    data = None
    bbox = None
    cnt = 0
    for i in args.files:
        jd, d = load_bin(i)
        if cnt == 0:
            data = np.zeros([d.shape[0], ny, d.shape[1]], dtype = np.float)
        data[:, cnt, :] = d
        cnt += 1
        bbox = jd['bbox']
    
    bb = [bbox[0], bbox[1], 0.0, ny * args.yspacing, bbox[2], bbox[3]]
    save_bin(args.output, data, bbox = bb)
    
if __name__ == "__main__":
    main()
