#pySPARROW's Network Class

## Initialize ##
Network(HDF file path, 

&lt;version&gt;

)

### Examples ###
net = Network(r'C:\mydatabase.hdf')
net = Network(r'C:\mydatabase.hdf', '2')

## Reach ##

## Waterbody ##

## DB ##

```
from pySPARROW import *
net = Network(r'C:\mydatabase.hdf')
print len(net.get_upstream_reaches)
```