import numpy as np
from os.path import exists
from urllib.request import urlretrieve

from timeit import default_timer as timer
from datetime import timedelta

import swmf_file_reader as swmf

urlbase = 'http://mag.gmu.edu/git-data/swmf_file_reader/demodata/'
tmpdir = '/tmp/'
filebase = '3d__var_2_e20190902-041000-000'

for ext in ['.tree', '.info', '.out']:
    filename = filebase + ext
    if not exists(tmpdir + filename):
        print("Downloading " + urlbase + filename)
        print("to")
        print(tmpdir + filename)
        urlretrieve(urlbase + filename, tmpdir + filename)

start = timer()
print("Reading " + tmpdir + filebase + ".{tree, info, out}")
batsclass = swmf.read_batsrus(tmpdir + filebase)
end = timer()
print("Read time: {}".format(timedelta(seconds=end-start)))

assert batsclass.data_arr.shape == (5896192, 19)

# Get a 513th value of x, y, z, and rho
var_dict = dict(batsclass.varidx)
rho = batsclass.data_arr[:, var_dict['rho']][513]
x = batsclass.data_arr[:,var_dict['x']][513]
y = batsclass.data_arr[:,var_dict['y']][513]
z = batsclass.data_arr[:,var_dict['z']][513]
print(x, y, z, rho)
# -71.25 -15.75 -7.75 4.22874

start = timer()
rhoi = batsclass.interpolate(np.array([x, y, z]), 'rho')
assert rho == rhoi
end = timer()
print("Interpolation time: {}".format(timedelta(seconds=end-start)))
assert rho == rhoi

# Compute a derived quantity
print( batsclass.get_native_partial_derivatives(123456, 'rho') )
# [0.25239944 0.41480255 0.7658005 ]