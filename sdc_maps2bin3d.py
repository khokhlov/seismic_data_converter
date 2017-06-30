#!/usr/bin/env python

# (C) Nikolay Khokhlov <k_h@inbox.ru> 2017

import argparse
import numpy as np
import sys
from binjson import load_bin, save_bin

def load_layer(path):
    jd, data = load_bin(path)
    #print 'Layer %s min max %s %s' % (path, data.min(), data.max())
    #return data.reshape(size)
    return jd, data

def two_floats(value):
    values = value.split()
    if len(values) != 2:
        raise argparse.ArgumentError
    values = map(float, values)
    return values


def main():
    parser = argparse.ArgumentParser(description = 'Create 3D model from 2D maps.')
    parser.add_argument('output', help='output file')
    parser.add_argument('layers', help='layers files', nargs="+")
    parser.add_argument('-b', '--bounds', help='bounds at Z-direction', type=two_floats, metavar='"zmin zmax"', required = True)
    parser.add_argument('-n', '--nodes', help='number of nodes at z-direction', type=int, required = True)
    parser.add_argument('-l', '--values', help='values for layers', type=file, required = True)
    
    args = parser.parse_args()
    
    
    layers = []
    jd = []
    for i in args.layers:
        j, d = load_layer(i)
        layers.append(d)
        jd.append(j)
    layers = [np.full_like(layers[0], args.bounds[0]+1.0)] + layers
    layers = layers + [np.full_like(layers[0], args.bounds[1]-1.0)]
    
    v = np.loadtxt(args.values)
    if len(v) != len(layers)-1:
        raise argparse.ArgumentError("number of layers and values should be the same")
    
    n = layers[0].shape
    
    z = np.linspace(args.bounds[0], args.bounds[1], args.nodes)
    #print z
    data = np.zeros((args.nodes, n[0], n[1]))
    for j in range(n[0]):
        print 'Procession %s of %s' % (j, n[0])
        for i in range(n[1]):
            #for k in range(n[2]):
                for m in range(len(layers)-1):
                    l1 = layers[m][j][i]
                    l2 = layers[m+1][j][i]
                    #print l1,l2, z[k]
                    #if z[k] <= l1 and z[k] >= l2:
                        #print 'AAA'
                    #    data[k][j][i] = v[m]
                    #    break
                    data[:,j,i] += (data[:,j,i] <= 0.0) * ((z < l1) & (z > l2)) * v[m]
    
    print 'Min max data %s %s' % (data.min(), data.max())
    save_bin(args.output, data, jd[0]['bbox'] + args.bounds, command = " ".join(sys.argv[:]))

if __name__ == "__main__":
    main()
