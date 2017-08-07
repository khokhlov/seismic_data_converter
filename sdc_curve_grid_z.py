#!/usr/bin/env python

# (C) Nikolay Khokhlov <k_h@inbox.ru> 2017

import argparse
import numpy as np
import sys
from binjson import load_bin, save_bin

def load_layer(path):
    jd, data = load_bin(path)
    return jd, data

def two_floats(value):
    values = value.split()
    if len(values) != 2:
        raise argparse.ArgumentError
    values = map(float, values)
    return values


def main():
    parser = argparse.ArgumentParser(description = 'Create 3D curve grid from 2 heighmaps.')
    parser.add_argument('l1', help='input file for layer1')
    parser.add_argument('l2', help='inout file for layer2')
    parser.add_argument('outx', help='output file for x coordinate')
    parser.add_argument('outy', help='output file for y coordinate')
    parser.add_argument('outz', help='output file for z coordinate')
    parser.add_argument('-n', '--nodes', help='number of nodes at z-direction', type=int, required = True)
    
    args = parser.parse_args()
    
    jd1, d1 = load_layer(args.l1)
    jd2, d2 = load_layer(args.l2)
    
    bb = jd1['bbox']
    
    assert d1.shape == d2.shape
    
    nz, ny, nx = args.nodes, d1.shape[0], d1.shape[1]
    
    x = np.zeros([nz, ny, nx])
    y = np.zeros([nz, ny, nx])
    z = np.zeros([nz, ny, nx])
    
    xl = np.linspace(bb[0], bb[1], d1.shape[1])
    yl = np.linspace(bb[2], bb[3], d1.shape[0])
    
    h = (bb[1] - bb[0]) / (nx - 1)
    for i in range(nx):
        x[:,:,i] = h * i + bb[0]
        
    h = (bb[3] - bb[2]) / (ny - 1)
    for j in range(ny):
        y[:,j,:] = h * j + bb[2]

    h = (d2 - d1) / (nz - 1)
    for k in range(nz):
        z[k, :, :] = h * k + d1
    
    save_bin(args.outx, x)
    save_bin(args.outy, y)
    save_bin(args.outz, z)
    
if __name__ == "__main__":
    main()
