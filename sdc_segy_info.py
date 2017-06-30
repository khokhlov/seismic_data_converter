#!/usr/bin/env python

# (C) Nikolay Khokhlov <k_h@inbox.ru> 2017

import argparse
import sys
import numpy as np
from segypy import read_reel_header

def main():
    parser = argparse.ArgumentParser(description = 'Print header for segy file.')
    parser.add_argument('input', help='input segy file')
    args = parser.parse_args()

    h = read_reel_header(file(args.input, 'rb'))
    for k in h.keys():
        print k, h[k]
    
if __name__ == "__main__":
    main()
