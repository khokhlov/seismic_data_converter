#!/usr/bin/env python

# (C) Nikolay Khokhlov <k_h@inbox.ru> 2017

import argparse
import sys
import numpy as np
import imp
import os

from binjson import load_bin

SDC_SEGY_2_BIN = 'sdc_segy2bin_2d.py -v%s -c%s %s %s'
SDC_RESHAPE = 'sdc_reshape_2d.py -s %s %s %s %s'
SDC_CLIP = 'sdc_clip.py -b"1.0 1000000" %s %s'

TEMPLATE = """

verbose = true

dt = %DT%

steps = %STEPS%


[grids]
	[grid]
		id = segy_task
		[node]
			name = ElasticMetaNode2D
		[/node]
		[material_node]
            name = ElasticMaterialMetaNode
		[/material_node]
		[material]
			c1 = 3000
			c2 = 2000
			rho = 2500
		[/material]
		[factory]
			name = RectGridFactory
			size = %SIZEX%, %SIZEY%
			origin = %OX%, %OY%
			spacing = %HX%, %HY%
		[/factory]
		[schema]
			name = ElasticMatRectSchema2DRusanov3
		[/schema]
		[fillers]
            [filler]
				name = RectNoReflectFiller
				axis = 0
				side = 0
			[/filler]
			[filler]
				name = RectNoReflectFiller
				axis = 0
				side = 1
			[/filler]
			[filler]
				name = RectNoReflectFiller
				axis = 1
				side = 0
			[/filler]
			[filler]
				name = RectNoReflectFiller
				axis = 1
				side = 1
			[/filler]
        [/fillers]
        [correctors]
            [corrector]
                   name = ForceRectElasticBoundary2D
                        axis = 1
                          side = 0
               [/corrector]

            [corrector]
                name = PointSourceCorrector2D
                coords = %SX%, %SY%, 0.0
                compression = 1.0
                axis = 1
                eps = %SEPS%
                #source_axis = 1
                save = source.vtk
                [impulse]
                    name = FileInterpolationImpulse
                    [interpolator]
                        name = PiceWiceInterpolator1D
                        file = source.txt
                    [/interpolator]
                [/impulse]
               [/corrector]
		[/correctors]

	[/grid]
[/grids]

[contacts]
[/contacts]

[initials]
    [initial]
        name = StructuredFileLoader
        path = p_model.bin
        value = c1
        binary = true
        order = 1
    [/initial]
    [initial]
        name = StructuredFileLoader
        path = s_model.bin
        value = c2
        binary = true
        order = 2
    [/initial]
    [initial]
        name = StructuredFileLoader
        path = rho_model.bin
        value = rho
        binary = true
        order = 3
    [/initial]
[/initials]

[savers]
	[saver]
		name = StructuredVTKSaver
		path = vtk/%g_%s.vtk
		order = 1
		save = %VTK_SAVE%
		params = v
		norms = 1
	[/saver]
    [saver]
		name = StructuredVTKSaver
		path = model.vtk
		order = 1
		save = 1000000
		params = c1, c2, rho
		norms = 0, 0, 0
	[/saver]

    [saver]
        name = RectGridPointSaver
        path = seismogramm.txt
        params = vx, vy
        order = 1
		save = %SEGY_SAVE%

		norms = 0, 0
		save_receivers_vtk = receivers_rect.vtk
		save_receivers_txt = receivers_rect.txt
		
		points_file = receivers.txt
    [/saver]
[/savers]


"""

def create_path(p):
    try:
        os.makedirs(p)
    except:
        pass


def main():
    parser = argparse.ArgumentParser(description = 'Generate config to rect from segy models.')
    parser.add_argument('config', help='config file')
    args = parser.parse_args()

    cfg = imp.load_source('cfg', args.config)
    
    # create working dir
    create_path(cfg.work_dir)
    create_path(os.path.join(cfg.work_dir, 'vtk'))
    
    path_t   = os.path.join(cfg.work_dir, 't.json')
    path_p   = os.path.join(cfg.work_dir, 'p.json')
    path_s   = os.path.join(cfg.work_dir, 's.json')
    path_rho = os.path.join(cfg.work_dir, 'rho.json')
    
    # convert to bin data
    command = SDC_SEGY_2_BIN % (cfg.segy_scale_value, cfg.segy_scale_coords, cfg.segy_p_wave, path_t)
    print command
    os.system(command)
    command = SDC_CLIP % (path_t, path_p)
    print command
    os.system(command)
    
    command = SDC_SEGY_2_BIN % (cfg.segy_scale_value, cfg.segy_scale_coords, cfg.segy_s_wave, path_t)
    print command
    os.system(command)
    command = SDC_CLIP % (path_t, path_s)
    print command
    os.system(command)
    
    command = SDC_SEGY_2_BIN % (cfg.segy_scale_value, cfg.segy_scale_coords, cfg.segy_rho, path_t)
    print command
    os.system(command)
    command = SDC_CLIP % (path_t, path_rho)
    print command
    os.system(command)
    
    
    # getting max p-wave
    jp, data = load_bin(path_p)
    max_p = data.max()
    min_p = data.min()
    print 'Mix/max p-wave velocity:', min_p, max_p
    wl = min_p / cfg.source_frequency
    print 'Min wave length:', wl
    h = wl / cfg.cells_per_wave
    print 'Evaluate spacing:', h
    
    bb = jp['bbox']
    print 'Model bounding:', bb
    nx = int((bb[1]-bb[0]) / h) + 1
    ny = int((bb[3]-bb[2]) / h) + 1
    
    print 'Evaluating model size:', nx, ny
    
    hx = (bb[1]-bb[0]) / nx
    hy = (bb[3]-bb[2]) / ny
    h = max(hx, hy)
    
    
    path_p_model   = os.path.join(cfg.work_dir, 'p_model.json')
    path_s_model   = os.path.join(cfg.work_dir, 's_model.json')
    path_rho_model = os.path.join(cfg.work_dir, 'rho_model.json')

    command = SDC_RESHAPE % (nx, ny, path_p, path_p_model)
    print command
    os.system(command)
    command = SDC_RESHAPE % (nx, ny, path_s, path_s_model)
    print command
    os.system(command)
    command = SDC_RESHAPE % (nx, ny, path_rho, path_rho_model)
    print command
    os.system(command)
    
    # time step
    max_dt = h / max_p
    print 'Maximum time step:', max_dt
    
    dt = cfg.dt
    save_segy = 1
    
    if max_dt < dt:
        n = int(dt / max_dt) + 1
        dt = dt / n
        save_segy = n
    
    print 'Evaluate dt:', dt
    print 'Save segy every %s step.' % save_segy
    save_vtk = int(cfg.dt_vtk / dt)
    print 'Save vtk every %s step' % save_vtk
    
    steps = int(cfg.t_max / dt) + 1
    print 'Number of time steps:', steps
    
    # geterating source
    path_source     = os.path.join(cfg.work_dir, 'source.json')
    path_source_txt = os.path.join(cfg.work_dir, 'source.txt')
    delay = 1.5 / cfg.source_frequency
    command = 'sdc_ricker.py -z -d -%s %s %s %s %s > %s' % (delay, cfg.t_max - delay, steps * 2, cfg.source_frequency, path_source, path_source_txt)
    print command
    os.system(command)
    
    # generating receivers
    path_rec = os.path.join(cfg.work_dir, 'receivers.txt')
    f = file(path_rec, 'w')
    for i in file(cfg.receivers_coords, 'r'):
        f.write('%s 0\n' % i.strip())
    f.close()
    
    config = TEMPLATE.replace('%DT%', '%s' % dt)
    config = config.replace('%STEPS%', '%s' % steps)

    config = config.replace('%SIZEX%', '%s' % nx)
    config = config.replace('%SIZEY%', '%s' % ny)
    
    config = config.replace('%OX%', '%s' % bb[0])
    config = config.replace('%OY%', '%s' % bb[2])

    config = config.replace('%HX%', '%s' % hx)
    config = config.replace('%HY%', '%s' % hy)
    
    config = config.replace('%SX%', '%s' % cfg.source_coords[0])
    config = config.replace('%SY%', '%s' % cfg.source_coords[1])
    config = config.replace('%SEPS%', '%s' % (h * 0.6))
    
    config = config.replace('%VTK_SAVE%', '%s' % save_vtk)
    config = config.replace('%SEGY_SAVE%', '%s' % save_segy)
    
    path_config = os.path.join(cfg.work_dir, 'config.cfg')
    file(path_config, 'w').write(config)
    
    
    # run
    
    os.system('cd %s && pwd && %s config.cfg' % (cfg.work_dir, cfg.rect_path))
    
    
    # convert to segy
    path_rect_receivers = os.path.join(cfg.work_dir, 'receivers_rect.txt')
    path_rect_seismogramm = os.path.join(cfg.work_dir, 'seismogramm.txt')
    os.system('sdc_txt2segy_2d.py -n2 -c0 -r %s %s %s/vx.segy' % (path_rect_receivers, path_rect_seismogramm, cfg.work_dir))
    os.system('sdc_txt2segy_2d.py -n2 -c1 -r %s %s %s/vz.segy' % (path_rect_receivers, path_rect_seismogramm, cfg.work_dir))


if __name__ == "__main__":
    main()
