#!/usr/bin/env python

# (C) Nikolay Khokhlov <k_h@inbox.ru> 2017

import argparse
import sys
import numpy as np
from scipy.interpolate import RegularGridInterpolator
from tvtk.api import tvtk, write_data
from binjson import load_bin, save_bin


def main():
    parser = argparse.ArgumentParser(description = 'Convert 3D data to VTK.')
    parser.add_argument('input', help='input file')
    parser.add_argument('output', help='output file')
    
    args = parser.parse_args()

    jd, d = load_bin(args.input)
    b = jd['bbox']
    s = jd['size']

    x = np.linspace(b[0], b[1], s[0])
    y = np.linspace(b[2], b[3], s[1])
    z = np.linspace(b[4], b[5], s[2])
    
    hx = x[1] - x[0]
    hy = y[1] - y[0]
    hz = z[1] - z[0]
    
    n = [s[0]-1, s[1]-1, s[2]-1]
    
    newx = np.linspace(b[0] + hx / 2, b[1] - hx / 2, n[0])
    newy = np.linspace(b[2] + hy / 2, b[3] - hy / 2, n[1])
    newz = np.linspace(b[4] + hz / 2, b[5] - hz / 2, n[2])
    f = RegularGridInterpolator(points = (z, y, x), values = d, fill_value = None)
    zv, yv, xv = np.meshgrid(newz, newy, newx, indexing='ij')
    data = f((zv.ravel(), yv.ravel(), xv.ravel()))
    
    #grid = tvtk.ImageData(spacing=(hx, hy, hz), origin=(b[0], b[2], b[4]), dimensions=s)
    grid = tvtk.RectilinearGrid(dimensions=s)
    grid.x_coordinates = x
    grid.y_coordinates = y
    grid.z_coordinates = z
    grid.cell_data.scalars = np.ravel(data, order='F')
    grid.cell_data.scalars.name = 'data'

    # Writes legacy ".vtk" format if filename ends with "vtk", otherwise
    # this will write data using the newer xml-based format.
    write_data(grid, args.output)


if __name__ == "__main__":
    main()
