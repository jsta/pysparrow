import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from networkx import graphviz_layout
from pySPARROW import Network, Reach

path = "test.h5"
workspace = "/home/user/pysparrow-read-only/examples/testing_on_sample_sparrow_dataset/"
test_reach = '5012'

net = Network(workspace + 'test.h5')
G=net._g.subgraph(net.get_upstream_reaches(net.get_reach(test_reach)))
wb = net.get_waterbody(test_reach)
l_old = wb.get_fert_load()

wbs =['5092', '5014', '5087', '5041', '5054', '5068', '5061']
l_new = []
for j in wbs:
        wb = net.get_waterbody(j)
        l_new.append(wb.get_tot_load() / 10**5)

N = 7
ind = np.arange(N)     
plt.subplot(1,1,1)
plt.bar(ind, l_new, width = 0.3, color="black")

increase = [1]
l_new2 = []
for i in increase:
    
    # update 
    for r in G:
        r._Temp_F += 2.0
    
    for j in wbs:
        wb = net.get_waterbody(j)
        l_new2.append(wb.get_tot_load()/ 10**5)

#l_error1 = []
#for i in range(0, len(l_new)):
#    l_error1.append((l_new[i] - l_new[0]) / l_new[0] * 100.0)
#    print l_error1[i]
N = 7
ind = np.arange(N)     
plt.subplot(1,1,1)
plt.bar(ind + 0.3, l_new2, width = 0.3, color="gray")

net = Network(workspace + 'test.h5')
G=net._g.subgraph(net.get_upstream_reaches(net.get_reach(test_reach)))
l_new = []
for i in increase:

    # update 
    for r in G:
        r._NLCD['42'] += 1.0
    
    wb = net.get_waterbody(test_reach)
    l_new.append(wb.get_tot_load())

#l_error2 = []
#for i in range(0, len(l_new)):
#    l_error2.append((l_new[i] - l_new[0]) / l_new[0] * 100.0)
#    print l_error2[i]
    
#plt.subplot(2,1,2)
#plt.plot(increase, l_error2, color="black")
plt.legend( (l_new[0], l_new2[0]), ('Prior', 'Post') )
plt.xticks(ind+0.35, ('5092', '5014', '5087', '5041', '5054', '5068', '5061') )
plt.ylabel(r'loading $(kg/yr\times10^5)$')
plt.xlabel('Outlet Reaches')
plt.savefig('network_viz_04.png')


