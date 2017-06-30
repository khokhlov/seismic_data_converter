import json
import os.path
import sys
import numpy as np

def gen_bin_filename(json_path):
    f = os.path.splitext(os.path.basename(json_path))[0]
    return f + '.bin'

def get_bin_path(json_path, fname = None):
    d = os.path.dirname(json_path)
    if fname is None:
        fname = gen_bin_filename(json_path)
    return os.path.join(d, fname)

def save_bin(json_path, data, bbox, size = None, comment = None, command = " ".join(sys.argv[:]), dtype = 'f', verbose = False):
    if size is None:
        size = data.shape
    bin_path = get_bin_path(json_path)
    data.astype(dtype).tofile(bin_path)
    jdata = {
        'bin_data': gen_bin_filename(json_path),
        'bbox': bbox,
        'comment': comment,
        'command': command,
        'dtype': dtype,
        'size': size[::-1]
        }
    v = json.dumps(jdata, sort_keys = True, indent = 4, separators=(',', ': '))
    with open(json_path, 'w') as f:
        f.write(v)
        
    if verbose:
        print 'Array size:', jdata['size']
        print 'Bounding box:', jdata['bbox']
        print 'Saving binary data to "%s"' % bin_path
        print 'Min/max value:', data.min(), data.max()
        print 'Spacing:', (bbox[1]-bbox[0]) / jdata['size'][0], (bbox[3]-bbox[2]) / jdata['size'][1]

    return jdata

def load_bin(json_path):
    jdata = json.loads(file(json_path, 'r').read())
    bin_path = get_bin_path(json_path, jdata['bin_data'])
    data = np.fromfile(bin_path, dtype=jdata['dtype'])
    #print data.shape
    return jdata, data.reshape(jdata['size'][::-1])
