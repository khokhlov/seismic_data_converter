#!/usr/bin/env python

# Script to convert Irap classic grid (ASCII) data to binary file.
# (C) Nikolay Khokhlov <k_h@inbox.ru> 2017

import argparse
import numpy as np
import sys

from binjson import save_bin

def irap_parser(path, crop = None):
    with open(path, 'r') as f:
        t = f.readline().split()
        hx, hy = float(t[2]), float(t[3])
        xmin, xmax, ymin, ymax = (float(i) for i in f.readline().split())
        nx = int(f.readline().split()[0])
        f.readline()
        data = np.fromfile(f, sep = " ")
        s = data.shape[0]
        
        # TODO: fix
        data = data.reshape((s/nx, nx))
        if crop:
            data = data[crop[2]:crop[3], crop[0]:crop[1]]
        return (hx, hy), (xmin, xmax, ymin, ymax), data

def four_ints(value):
    values = value.split()
    if len(values) != 4:
        raise argparse.ArgumentError
    values = map(int, values)
    return values

def main():
    parser = argparse.ArgumentParser(description = 'Convert Irap Classical Grid (ASCII) to binary data.')
    parser.add_argument('irap_file', help='irap file to parse')
    parser.add_argument('json_file', help='save to file')
    parser.add_argument('-c', '--comment', help='add comment to file', type=str)
    parser.add_argument('-p', '--crop', help='crop data, "xmin, xmax, ymin, ymax", you can use numpy notation i.e. negative indexes', type=four_ints, metavar='"xmin xmax ymin ymax"')
    parser.add_argument('-v', '--verbose', help='verbose output', action = 'store_true')

    args = parser.parse_args()
    
    if args.verbose:
        print 'Reading file "%s"' % args.irap_file
    (hx, hy), (xmin, xmax, ymin, ymax), data = irap_parser(args.irap_file, args.crop)
    if args.verbose:
        print 'Saving to "%s"' % args.json_file
    jd = save_bin(args.json_file, data, (xmin, xmax, ymin, ymax), comment = args.comment, command = " ".join(sys.argv[:]), verbose = args.verbose)
    
if __name__ == "__main__":
    main()
