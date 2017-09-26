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
    parser = argparse.ArgumentParser(description = 'Merge binary files by z-axis.')
    parser.add_argument('output', help='output json bin file')
    parser.add_argument('files', help='files to merge', nargs="+")
    parser.add_argument('-z', '--zspacing', help='spacing at z direction', type=float, required = True)
    
    args = parser.parse_args()
    
    nz = len(args.files)
    data = None
    bbox = None
    cnt = 0
    for i in args.files:
        jd, d = load_bin(i)
        if cnt == 0:
            data = np.zeros([nz, d.shape[1], d.shape[2]], dtype = np.float)
        data[cnt, :, :] = d[0, :, :]
        cnt += 1
        bbox = jd['bbox']
    
    bb = [bbox[0], bbox[1], bbox[2], bbox[3], 0.0, nz * args.zspacing]
    save_bin(args.output, data, bbox = bb)
    
if __name__ == "__main__":
    main()
