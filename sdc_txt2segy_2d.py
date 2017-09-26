#!/usr/bin/env python

# (C) Nikolay Khokhlov <k_h@inbox.ru> 2017

import argparse
import sys
import numpy as np
from binjson import load_bin, save_bin
from segypy import write_segy


def main():
    parser = argparse.ArgumentParser(description = 'Convert text data to segy file.')
    parser.add_argument('input', help='input txt file')
    parser.add_argument('output', help='output segy file')
    parser.add_argument('-n', '--num-components', help='number of components at txt file', type=int, required = True)
    parser.add_argument('-c', '--component', help='component to save', type=int, required = True)
    parser.add_argument('-r', '--receivers', help='file with receivers, format x,y,z', type=str)
    
    args = parser.parse_args()

    header = {}
    if args.receivers:
        c = np.loadtxt(args.receivers)
        header['GroupX'] = c[:, 0]
        header['GroupY'] = c[:, 1]
    
    data = np.loadtxt(args.input)
    #print 'Data size', data.shape
    t = data[:,0]
    v = data[:,1+args.component::args.num_components]
    #print 'Selected data size', v.shape
    write_segy(args.output, v, dt = (t[1]-t[0])*1000000.0, trace_header_in = header)


if __name__ == "__main__":
    main()
