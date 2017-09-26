#!/usr/bin/env python

# Script to vtk files to bin files.
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

def read_vtk(path):
    with open(path, 'r') as f:
        f.readline()
        f.readline()
        t = f.readline().strip()
        assert(t == 'BINARY')
        t = f.readline().strip()
        assert(t == 'DATASET STRUCTURED_POINTS')
        
        t = f.readline().strip().split()
        size = [int(t[1]), int(t[2]), int(t[3])]
        
        t = f.readline().strip().split()
        spacing = [float(t[1]), float(t[2]), float(t[3])]
        
        t = f.readline().strip().split()
        origin = [float(t[1]), float(t[2]), float(t[3])]
        f.readline()
        
        
        d = {}
        t = [0,]
        while len(t) > 0:
            t = f.readline().strip().split()
            if len(t) == 0:
                continue
            assert(t[0] == 'SCALARS')
            assert(t[2] == 'float')
            name = t[1]
            f.readline()
            data = np.fromfile(f, dtype = np.dtype('>f4'), count = size[0]*size[1]*size[2]).reshape(size[2], size[1], size[0])
            f.readline()
            d[name] = data
        return d, spacing, origin, size


def main():
    parser = argparse.ArgumentParser(description = 'Convert legacy vtk file to bin file.')
    parser.add_argument('input', help='input vtk file')
    parser.add_argument('output', help='output json bin file')
    parser.add_argument('-c', '--component', help='component to save', type=str, required = True)
    
    args = parser.parse_args()

    data, h, o, s = read_vtk(args.input)
    bbox = [o[0], o[0]+h[0]*s[0], o[1], o[1]+h[1]*s[1], o[2], o[2]+h[2]*s[2]]
    
    if data.has_key(args.component):
        save_bin(args.output, data[args.component], bbox = bbox)
    else:
        print 'Unknown component "%s", components: %s' %(args.component, data.keys())
    
if __name__ == "__main__":
    main()
