#!/usr/bin/env python

# (C) Nikolay Khokhlov <k_h@inbox.ru> 2017

import argparse
import numpy as np
import sys

from binjson import load_bin


def main():
    parser = argparse.ArgumentParser(description = 'Show some info about binary file.')
    parser.add_argument('json_file', help='json data file')
    args = parser.parse_args()
    
    jdata, data = load_bin(args.json_file)
    bbox = jdata['bbox']
    
    print 'Array size:', jdata['size']
    print 'Bounding box:', jdata['bbox']
    print 'Saving binary data to "%s"' % jdata['bin_data']
    print 'Min/max value:', data.min(), data.max()
    print 'Spacing:', (bbox[1]-bbox[0]) / jdata['size'][0], (bbox[3]-bbox[2]) / jdata['size'][1]
    print 'Comment:', jdata['comment']
    print 'Command:', jdata['command']

    
if __name__ == "__main__":
    main()
