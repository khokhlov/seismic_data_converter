#!/usr/bin/env python

# Show 2D binary data.
# (C) Nikolay Khokhlov <k_h@inbox.ru> 2017

import argparse
import numpy as np
import sys
import matplotlib.pyplot as plt

from binjson import load_bin


def main():
    parser = argparse.ArgumentParser(description = 'Show 2D binary data.')
    parser.add_argument('json_file', help='json data file')
    args = parser.parse_args()
    
    jdata, data = load_bin(args.json_file)
    plt.imshow(data, cmap='jet', aspect='auto')
    plt.colorbar()
    plt.show()
    
if __name__ == "__main__":
    main()
