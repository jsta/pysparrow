import sys
from networkx import DiGraph, shortest_path, single_source_shortest_path, \
    dijkstra_path_length, single_source_dijkstra_path_length
from math import exp, sqrt
from tables import *

sys.path.append(".")
from pySPARROW import database #.DB as DB
from pySPARROW import reach #.Reach as Reach
from pySPARROW import waterbody # import Waterbody
from pySPARROW import utils
Reach = reach.Reach


class Network:
    """A set of reaches composed into a graph."""
    def __init__(self, path, version = '0'):
        g = DiGraph()
        gaged_reaches = []
        db = open_file(path, "r")        
        table = db.get_node('/', 'networks/network' + str(version))
        reaches = {}
        #read data out of file
        for row in table:            
            if row['ComID'].decode('UTF-8') != '-1':
                reaches[row['ComID'].decode('UTF-8')] = Reach(self, row)
            else:
                reaches[row['ComID'].decode('UTF-8')]  = '-1'
                g.add_edge(Reach(self, row), '-1')
            # example data seems to be missing this field...
            # if row['MonitoredFlag'] == '1' : 
            #     gaged_reaches.append(row['ComID'])
        db.close()
        #make network
        for comid in reaches.keys():
            to_comID = reaches[comid]._ToComID
            if to_comID.decode('UTF-8') != '-1':
                g.add_edge(reaches[comid], reaches[to_comID])
            else:
                g.add_edge(reaches[comid], -1)
        self._g_unbroken = g.copy()
        self._g_unbroken_reverse = self._g_unbroken.reverse()
        
        #break upstream of monitored reaches
        for i in gaged_reaches:
            if i != '-1':
                up = g.predecessors(reaches[i])
                for j in up:
                    if j != '-1':
                        g.delete_edge(j, reaches[i])
                    else:
                        g.delete_edge(j, '-1')
        self._g = g
        self._g_rev = g.reverse()
        self._version = str(version)
        self._path = str(path)
        # breakpoint()
        self._reaches = reaches
        db.close()

    def get_reach(self, comID):
        """Returns a reach in the network"""
        # breakpoint()
        return self._reaches[comID]
    
    def get_waterbody(self, comID):
        """Returns a waterbody in the network."""
        return waterbody.Waterbody(self, comID)
    
    def get_upstream_reaches(self, outlet_reach, broken_at_gages=True):
        """Returns the comIDs of the upstream reaches for a given reach.  
        If no comID is specified, then all reaches in the network are 
        returned."""
        if broken_at_gages == True:
            return single_source_shortest_path(self._g_rev, outlet_reach)
        else:
            return single_source_shortest_path(self._g_unbroken_reverse, outlet_reach)
                
    def get_next_upstream_reaches(self, comID):
        """Returns the next upstream reach(es) for a given reach."""
        return self._g.predecessors(str(comID))

    def get_next_downstream_reaches(self, comID):
        """Returns the next downstream reach(es) for a given reach."""
        return self._g.successors(str(comID))
           
    def get_instream_loss(self, from_comID, to_comID):
        #"""Returns the percent loss due to transport from a given reach to a
        #given downstream reach."""
        if from_comID == to_comID: return 1.0
        
        d = shortest_path(self._g, self.get_reach(from_comID), \
                          self.get_reach(to_comID))
         
        instream_loss = 1.0
        for j in d:
            if j._IsMonitored == '1': #monitored reach has no decay
                pass
            elif j._ComID == from_comID: #head water reach has partial decay
                instream_loss *= sqrt(j._ReachDecay) * j._ReservoirDecay
            else: #all other reaches have full decay
                instream_loss *= j._ReachDecay * j._ReservoirDecay
        return instream_loss
    
#    def get_NX_XDiGraph(self):
#        """Returns a networkx XDiGraph object representing the Network."""
#        return self._g
