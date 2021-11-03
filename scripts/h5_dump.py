# h5dump -d /networks/network0 examples/test.h5

import h5py
import pandas as pd

paths = []
with h5py.File('examples/test.h5','r') as hf:
    hf.visit(paths.append)
dt = pd.HDFStore('examples/test.h5').get(paths[1])
dt.to_csv('examples/test.csv')