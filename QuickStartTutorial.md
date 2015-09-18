#Quick Start Tutorial

**Find the number of reaches within a basin database**

```
from pySPARROW import *
net = Network(r'C:\mydatabase.hdf')
print len(net.get_upstream_reaches)
```