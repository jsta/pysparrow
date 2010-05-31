import networkx as nx
import matplotlib.pyplot as plt
from networkx import graphviz_layout
from pySPARROW import Network, Reach

workspace = "/home/user/pysparrow-read-only/examples/testing_on_sample_sparrow_dataset/"
test_reach = '5012'

net = Network(workspace + 'test.h5')
max2= 0
id2 = 0

#for i in net._g:
#    if len(net.get_upstream_reaches(i)) > 1000: 
#        print str(len(net.get_upstream_reaches(i))) + " " + str(i._ComID)

    
G=net._g.subgraph(net.get_upstream_reaches(net.get_reach(test_reach)))
pos=nx.graphviz_layout(G,prog='neato',args='')
plt.figure(figsize=(8,8))
lab = {}
node_size = []
node_color = []
for r in G:
    lab[r] = r._ComID
    #print r._AreaHa
    if r._AreaHa >= 1000.0: 
        node_size.append((r.get_tot_runoff() / r._AreaHa ) ** 2.0 )
        node_color.append((r.get_tot_runoff() / r._AreaHa ) ** 2.0 )
    else:
        node_size.append(1.0)
        node_color.append(1.0)
        
plt.subplot(2,3,1)
plt.title('Total')
nx.draw(G,pos, \
    node_size=node_size, \
    alpha=0.5, \
    node_color=node_color, \
    font_size = 8,
    style='dashed',
    with_labels=False)

lab = {}
node_size = []
node_color = []
for r in G:
    lab[r] = r._ComID
    #print r._AreaHa
    if r._AreaHa >= 1000.0: 
        node_size.append((r.get_atm_runoff() / r._AreaHa ) ** 2.0 )
        node_color.append((r.get_atm_runoff() / r._AreaHa ) ** 2.0 )
    else:
        node_size.append(1.0)
        node_color.append(1.0)
        
plt.subplot(2,3,2)
plt.title('Atmosphere')
nx.draw(G,pos, \
    node_size=node_size, \
    alpha=0.5, \
    node_color=node_color, \
    font_size = 8,
    style='dashed',
    with_labels=False)    
    
lab = {}
node_size = []
node_color = []
for r in G:
    lab[r] = r._ComID
    #print r._AreaHa
    if r._AreaHa >= 1000.0: 
        node_size.append((r.get_forest_runoff() / r._AreaHa ) ** 2.0 )
        node_color.append((r.get_forest_runoff() / r._AreaHa ) ** 2.0 )
    else:
        node_size.append(1.0)
        node_color.append(1.0)
        
plt.subplot(2,3,3)
plt.title('Nonag')
nx.draw(G,pos, \
    node_size=node_size, \
    alpha=0.5, \
    node_color=node_color, \
    font_size = 8,
    style='dashed',
    with_labels=False)
    
lab = {}
node_size = []
node_color = []
for r in G:
    lab[r] = r._ComID
    #print r._AreaHa
    if r._AreaHa >= 1000.0: 
        node_size.append((r.get_fert_runoff() / r._AreaHa ) ** 2.0 )
        node_color.append((r.get_fert_runoff() / r._AreaHa ) ** 2.0 )
    else:
        node_size.append(1.0)
        node_color.append(1.0)
        
plt.subplot(2,3,4)
plt.title('Fertilizer')
nx.draw(G,pos, \
    node_size=node_size, \
    alpha=0.5, \
    node_color=node_color, \
    font_size = 8,
    style='dashed',
    with_labels=False)

lab = {}
node_size = []
node_color = []
for r in G:
    lab[r] = r._ComID
    #print r._AreaHa
    if r._AreaHa >= 1000.0: 
        node_size.append((r.get_waste_runoff() / r._AreaHa ) ** 2.0 )
        node_color.append((r.get_waste_runoff() / r._AreaHa ) ** 2.0 )
    else:
        node_size.append(1.0)
        node_color.append(1.0)
        
plt.subplot(2,3,5)
plt.title('Waste')
nx.draw(G,pos, \
    node_size=node_size, \
    alpha=0.5, \
    node_color=node_color, \
    font_size = 8,
    style='dashed',
    with_labels=False)

lab = {}
node_size = []
node_color = []
for r in G:
    lab[r] = r._ComID
    #print r._AreaHa
    if r._AreaHa >= 1000.0: 
        node_size.append((r.get_pnt_runoff() / r._AreaHa ) ** 2.0 )
        node_color.append((r.get_pnt_runoff() / r._AreaHa ) ** 2.0 )
    else:
        node_size.append(1.0)
        node_color.append(1.0)
        
plt.subplot(2,3,6)
plt.title('Point')
nx.draw(G,pos, \
    node_size=node_size, \
    alpha=0.5, \
    node_color=node_color, \
    font_size = 8,
    style='dashed',
    with_labels=False)
    
plt.axis('equal')
plt.savefig('network_viz_03.png')
plt.close()
#plt.show()

