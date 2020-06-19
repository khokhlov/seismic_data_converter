#!/usr/bin/env python

# (C) Nikolay Khokhlov <k_h@inbox.ru> 2019

import sys

def main():
    data = sys.stdin.readlines()
    print "# vtk DataFile Version 3.0"
    print "Created by %s" % sys.argv[0]
    print "ASCII"
    print "DATASET UNSTRUCTURED_GRID"
    print "POINTS %s float" % len(data)
    for i in data:
        print i.strip()
    print "CELLS %s %s" % (len(data), len(data) * 2)
    for i in range(len(data)):
        print "1 %s" % i
    print "CELL_TYPES %s" % len(data)
    for i in data:
        print "1"

    
if __name__ == "__main__":
    main()
