#!/usr/bin/env python

import argparse
import numpy as np
from binjson import save_bin

def ricker(t, f):
    w = 2 * np.pi * f
    v = w ** 2  * t ** 2
    return (1.0 - 0.5 * v) * np.exp(-0.25 * v)

def main():
    parser = argparse.ArgumentParser(description="Generate Ricker impulse samples.")

    parser.add_argument("start", type=float, help="samples start time, s")
    parser.add_argument("end", type=float, help="samples end time, s")
    parser.add_argument("num", type=int, help="num samples")
    parser.add_argument("freq", type=float, help="impulse frequency, Hz")
    parser.add_argument("out", type=str, help="OUT binary samples")
    parser.add_argument('-d', '--display', help='print data to screen', action = 'store_true')
    parser.add_argument('-z', '--zero', help='start data from zero time', action = 'store_true')

    args = parser.parse_args()

    time_samples = np.linspace(args.start, args.end, args.num)

    data = ricker(time_samples, args.freq)
    bbox = [args.start, args.end]
    if args.zero:
        bbox = [0.0, args.end - args.start]
    save_bin(args.out, data, bbox)
    
    if args.display:
        for i in range(args.num):
            t = time_samples[i]
            if args.zero:
                t -= args.start
            print t, data[i]

if __name__ == "__main__":
    main()
