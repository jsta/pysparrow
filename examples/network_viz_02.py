import networkx as nx
import matplotlib.pyplot as plt
from networkx import graphviz_layout
from pySPARROW import Network, Reach

path = "test.h5"
workspace = "/home/user/pysparrow-read-only/examples/testing_on_sample_sparrow_dataset/"
test_reach = '5012'

net = Network(workspace + 'test.h5')
G=net._g.subgraph(net.get_upstream_reaches(net.get_reach(test_reach)))

lab = {}
node_size =[]
node_color = []
i = 1
for r in G:
    lab[r] = r._ComID
    #print r._AreaHa
    #if r._AreaHa >= 1000.0: 
    node_size.append((net.get_instream_loss(r._ComID, test_reach)*500.0) ** 1.0 )
    node_color.append((net.get_instream_loss(r._ComID, test_reach)*500.0) ** 1.0 )
    #else:
    #    node_size.append(1.0)
    #    node_color.append(1.0)
    i+=1
    
pos=nx.graphviz_layout(G,prog='neato',args='')
plt.figure(figsize=(8,8))
nx.draw(G,pos, \
    node_size=node_size, \
    alpha=0.5, \
    node_color=node_color, \
    font_size = 8,
    style='dashed',
    labels=lab)
    #with_labels=False)
plt.axis('equal')
plt.savefig('network_viz_02.png')
plt.close()
#plt.show()
