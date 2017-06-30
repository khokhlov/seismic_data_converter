#!/usr/bin/env python

# Show 2D binary data.
# (C) Nikolay Khokhlov <k_h@inbox.ru> 2017

import argparse
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from binjson import load_bin


def main():
    parser = argparse.ArgumentParser(description = 'Show 3D binary data.')
    parser.add_argument('json_file', help='json data file')
    args = parser.parse_args()
    
    jdata, data = load_bin(args.json_file)

    fig = plt.figure()
    ims = []
    for k in range(data.shape[0]):
        im = plt.imshow(data[k], cmap='jet', animated=True, aspect='auto')
        ims.append([im])

    ani = animation.ArtistAnimation(fig, ims, interval=100, blit=True, repeat_delay=1000)

    plt.show()
    
if __name__ == "__main__":
    main()
