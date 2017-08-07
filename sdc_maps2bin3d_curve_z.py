#!/usr/bin/env python

# (C) Nikolay Khokhlov <k_h@inbox.ru> 2017

import argparse
import numpy as np
import sys
from binjson import load_bin, save_bin

def load_layer(path):
    jd, data = load_bin(path)
    return jd, data

def load_values(path, shape):
    v = []
    for i in path:
        d = None
        try:
            print i
            jd, d = load_bin(i.strip())
            print 'Loading layer', i
        except:
            d = np.ones(shape) * float(i)
            print 'Creating layer', i
        v.append(d)
    return v

def main():
    parser = argparse.ArgumentParser(description = 'Create 3D model from 2D maps.')
    parser.add_argument('output', help='output file')
    parser.add_argument('layers', help='layers files', nargs="+")
    parser.add_argument('-l', '--values', help='values for layers', type=file, required = True)
    parser.add_argument('-z', '--zcoords', help='values for z coordinates', type=str, required = True)
    
    args = parser.parse_args()
    
    
    layers = []
    jd = []
    for i in args.layers:
        j, d = load_layer(i)
        layers.append(d)
        jd.append(j)
    
    layers[0] += 1.0
    layers[-1] -= 1.0
    
    v = load_values(args.values, layers[0].shape)
    
    if len(v) != len(layers)-1:
        raise argparse.ArgumentError("number of layers and values should be the same")
    
    n = layers[0].shape
    
    t, z = load_bin(args.zcoords)

    data = np.zeros((z.shape[0], n[0], n[1]))
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
                    data[:,j,i] += (data[:,j,i] <= 0.0) * ((z[:, j, i] <= l1) & (z[:, j, i] >= l2)) * v[m][j,i]
    
    print 'Min max data %s %s' % (data.min(), data.max())
    
    save_bin(args.output, data, jd[0]['bbox'] + [float(z.min()), float(z.max())])

if __name__ == "__main__":
    main()
