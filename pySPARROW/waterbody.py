from pySPARROW import reach # import Reach
from pySPARROW import database #.DB as DB
from pySPARROW import utils
from math import exp, sqrt
import time

class Waterbody:
    """A river segment that receives pollution from upstream reaches."""
    def __init__(self, Network, ComID):       
        # set attribute values
        self._network = Network
        self._comID = ComID
        
    def get_atm_load(self, verbose=0):
        #get upstream reaches 
        r = self._network.get_reach(self._comID)
        d = {}
        if r._IsMonitored != '1':
            d = self._network.get_upstream_reaches(r)
        else:
            r = self._network.get_reach(self._comID)
 #           #get upstream reaches
 #           up_stream_reaches = self._network._g_unbroken.predecessors(r)
 #           predicted_load_for_source = 0.0
 #           #sum source and total loads from upstream reaches
 #           for i in up_stream_reaches:
 #               wb = self._network.get_waterbody(i._ComID)
 #               predicted_load_for_source += wb.get_atm_load()
 #           #transport upstream loads to this reach
 #           predicted_load_for_source *= r._ReachDecay * r._ReservoirDecay
 #           #add incremental load from reach
 #           predicted_load_for_source += r.get_atm_runoff() * \
 #                   sqrt(r._ReachDecay) * r._ReservoirDecay
 #           return predicted_load_for_source
        
        #get upstream reaches
            downstream_reach = self._network._g.successors(r)[0]
            wb = self._network.get_waterbody(downstream_reach._ComID)
            downstream_loading = wb.get_atm_load()
            incremental_loading = downstream_reach.get_atm_runoff() * \
                    sqrt(downstream_reach._ReachDecay) * downstream_reach._ReservoirDecay
            load = (downstream_loading - incremental_loading) \
                    / (downstream_reach._ReachDecay * downstream_reach._ReservoirDecay) 
                   
            #predicted_load_for_source = 0.0
            #predicted_load_total = 0.0
            ##sum source and total loads from upstream reaches
            #for i in up_stream_reaches:
            #    wb = self._network.get_waterbody(i._ComID)
            #    predicted_load_for_source += wb.get_atm_load()
            #    predicted_load_total += wb.get_tot_load()
            ##transport upstream loads to this reach
            #predicted_load_for_source *= r._ReachDecay * r._ReservoirDecay
            #predicted_load_total *= r._ReachDecay * r._ReservoirDecay
            #load = (predicted_load_for_source / predicted_load_total) * \
            #       r._MeasuredLoad
            ##add incremental load from reach
            #predicted_load_for_source += r.get_atm_runoff() * \
            #        sqrt(r._ReachDecay) * r._ReservoirDecay
            #predicted_load_total += r.get_tot_runoff() * \
            #        sqrt(r._ReachDecay) * r._ReservoirDecay
            ##recale load 
            #load = (predicted_load_for_source / predicted_load_total) * \
            #       r._MeasuredLoad
            return load
        
        tot = 0.0
        for i in d.keys():          
            #calculate instream loss
            instream_decay = 1.0
            for j in d[i]:
                if j._IsMonitored == '1': #monitored reach has no decay
                    pass
                elif j._ComID == i._ComID: #reach has partial decay
                    instream_decay *= sqrt(j._ReachDecay) * j._ReservoirDecay
                else: #all other reaches have full decay
                    instream_decay *= j._ReachDecay * j._ReservoirDecay
            #adjust runoff due to monitoring station (if necessary)
            p_unbroken = self._network._g_unbroken.predecessors(i)
            p_broken = self._network._g.predecessors(i)
            runoff = 0.0
            if (len(p_broken)) == 0:
                if (len(p_unbroken)) == 0:
                    #head water
                    runoff = i.get_atm_runoff() 
                else:
                    #monitored
                    runoff = i.get_atm_runoff(adjust_for_monitoring=True)
            else:
                runoff = i.get_atm_runoff() 
            #calculate load 
            tot += runoff * instream_decay 
        return tot
    
    def get_pnt_load(self, verbose = 0):
        """Returns the point source loading from all upstream reaches to the waterbody."""
        r = self._network.get_reach(self._comID)
        d = {}
        if r._IsMonitored != '1':
            d = self._network.get_upstream_reaches(r)
        else:
            d = self._network.get_upstream_reaches(r, broken_at_gages=False)
        
        tot = 0.0
        for i in d.keys():
            #calculate instream loss
            instream_decay = 1.0
            for j in d[i]:
                if j._IsMonitored == '1': #monitored reach has no decay
                    pass
                elif j._ComID == i._ComID: #head water reach has partial decay
                    instream_decay *= sqrt(j._ReachDecay) * j._ReservoirDecay
                else: #all other reaches have full decay
                    instream_decay *= j._ReachDecay * j._ReservoirDecay
            #adjust runoff due to monitoring station (if necessary)
            p_unbroken = self._network._g_unbroken.predecessors(i)
            p_broken = self._network._g.predecessors(i)
            runoff = 0.0
            if (len(p_broken)) == 0:
                if (len(p_unbroken)) == 0:
                    #head water
                    runoff = i.get_pnt_runoff() 
                else:
                    #monitored
                    runoff = i.get_pnt_runoff(adjust_for_monitoring=True)
            else:
                runoff = i.get_pnt_runoff() 
            #calculate load 
            tot += runoff * instream_decay 
        return tot
    
    def get_waste_load(self, verbose = 0):
        """Returns the waste source loading from all upstream reaches to the waterbody."""
        r = self._network.get_reach(self._comID)
        d = {}
        if r._IsMonitored != '1':
            d = self._network.get_upstream_reaches(r)
        else:
            d = self._network.get_upstream_reaches(r, broken_at_gages=False)
        
        tot = 0.0
        for i in d.keys():
            #calculate instream loss
            instream_decay = 1.0
            for j in d[i]:
                if j._IsMonitored == '1': #monitored reach has no decay
                    pass
                elif j._ComID == i._ComID: #head water reach has partial decay
                    instream_decay *= sqrt(j._ReachDecay) * j._ReservoirDecay
                else: #all other reaches have full decay
                    instream_decay *= j._ReachDecay * j._ReservoirDecay
            #adjust runoff due to monitoring station (if necessary)
            p_unbroken = self._network._g_unbroken.predecessors(i)
            p_broken = self._network._g.predecessors(i)
            runoff = 0.0
            if (len(p_broken)) == 0:
                if (len(p_unbroken)) == 0:
                    #head water
                    runoff = i.get_waste_runoff() 
                else:
                    #monitored
                    runoff = i.get_waste_runoff(adjust_for_monitoring=True)
            else:
                runoff = i.get_waste_runoff() 
            #calculate load 
            tot += runoff * instream_decay 
        return tot
    
    def get_fert_load(self, verbose = 0):
        """Returns the fertilizer loading from all upstream reaches to the waterbody."""
        r = self._network.get_reach(self._comID)
        d = {}
        if r._IsMonitored != '1':
            d = self._network.get_upstream_reaches(r)
        else:
            d = self._network.get_upstream_reaches(r, broken_at_gages=False)
        
        tot = 0.0
        for i in d.keys():
            #calculate instream loss
            instream_decay = 1.0
            for j in d[i]:
                if j._IsMonitored == '1': #monitored reach has no decay
                    pass
                elif j._ComID == i._ComID: #head water reach has partial decay
                    instream_decay *= sqrt(j._ReachDecay) * j._ReservoirDecay
                else: #all other reaches have full decay
                    instream_decay *= j._ReachDecay * j._ReservoirDecay
            #adjust runoff due to monitoring station (if necessary)
            p_unbroken = self._network._g_unbroken.predecessors(i)
            p_broken = self._network._g.predecessors(i)
            runoff = 0.0
            if (len(p_broken)) == 0:
                if (len(p_unbroken)) == 0:
                    #head water
                    runoff = i.get_fert_runoff() 
                else:
                    #monitored
                    runoff = i.get_fert_runoff(adjust_for_monitoring=True)
            else:
                runoff = i.get_fert_runoff() 
            #calculate load 
            tot += runoff * instream_decay 
        return tot

    def get_forest_load(self, verbose = 0):
        """Returns the forest land loading from all upstream reaches to the waterbody."""
        r = self._network.get_reach(self._comID)
        d = {}
        if r._IsMonitored != '1':
            d = self._network.get_upstream_reaches(r)
        else:
            d = self._network.get_upstream_reaches(r, broken_at_gages=False)
        
        tot = 0.0
        for i in d.keys():
            #calculate instream loss
            instream_decay = 1.0
            for j in d[i]:
                if j._IsMonitored == '1': #monitored reach has no decay
                    pass
                elif j._ComID == i._ComID: #head water reach has partial decay
                    instream_decay *= sqrt(j._ReachDecay) * j._ReservoirDecay
                else: #all other reaches have full decay
                    instream_decay *= j._ReachDecay * j._ReservoirDecay
            #adjust runoff due to monitoring station (if necessary)
            p_unbroken = self._network._g_unbroken.predecessors(i)
            p_broken = self._network._g.predecessors(i)
            runoff = 0.0
            if (len(p_broken)) == 0:
                if (len(p_unbroken)) == 0:
                    #head water
                    runoff = i.get_forest_runoff() 
                else:
                    #monitored
                    runoff = i.get_forest_runoff(adjust_for_monitoring=True)
            else:
                runoff = i.get_forest_runoff() 
            #calculate load 
            tot += runoff * instream_decay 
        return tot

    def get_grass_load(self, verbose = 0):
        """Returns the grass land loading from all upstream reaches to the waterbody."""
        r = self._network.get_reach(self._comID)
        d = {}
        if r._IsMonitored != '1':
            d = self._network.get_upstream_reaches(r)
        else:
            d = self._network.get_upstream_reaches(r, broken_at_gages=False)
        
        tot = 0.0
        for i in d.keys():
            #calculate instream loss
            instream_decay = 1.0
            for j in d[i]:
                if j._IsMonitored == '1': #monitored reach has no decay
                    pass
                elif j._ComID == i._ComID: #head water reach has partial decay
                    instream_decay *= sqrt(j._ReachDecay) * j._ReservoirDecay
                else: #all other reaches have full decay
                    instream_decay *= j._ReachDecay * j._ReservoirDecay
            #adjust runoff due to monitoring station (if necessary)
            p_unbroken = self._network._g_unbroken.predecessors(i)
            p_broken = self._network._g.predecessors(i)
            runoff = 0.0
            if (len(p_broken)) == 0:
                if (len(p_unbroken)) == 0:
                    #head water
                    runoff = i.get_grass_runoff() 
                else:
                    #monitored
                    runoff = i.get_grass_runoff(adjust_for_monitoring=True)
            else:
                runoff = i.get_grass_runoff() 
            #calculate load 
            tot += runoff * instream_decay 
        return tot

    def get_shrub_load(self, verbose = 0):
        """Returns the shrub land loading from all upstream reaches to the waterbody."""
        r = self._network.get_reach(self._comID)
        d = {}
        if r._IsMonitored != '1':
            d = self._network.get_upstream_reaches(r)
        else:
            d = self._network.get_upstream_reaches(r, broken_at_gages=False)
        
        tot = 0.0
        for i in d.keys():
            #calculate instream loss
            instream_decay = 1.0
            for j in d[i]:
                if j._IsMonitored == '1': #monitored reach has no decay
                    pass
                elif j._ComID == i._ComID: #head water reach has partial decay
                    instream_decay *= sqrt(j._ReachDecay) * j._ReservoirDecay
                else: #all other reaches have full decay
                    instream_decay *= j._ReachDecay * j._ReservoirDecay
            #adjust runoff due to monitoring station (if necessary)
            p_unbroken = self._network._g_unbroken.predecessors(i)
            p_broken = self._network._g.predecessors(i)
            runoff = 0.0
            if (len(p_broken)) == 0:
                if (len(p_unbroken)) == 0:
                    #head water
                    runoff = i.get_shrub_runoff() 
                else:
                    #monitored
                    runoff = i.get_shrub_runoff(adjust_for_monitoring=True)
            else:
                runoff = i.get_shrub_runoff() 
            #calculate load 
            tot += runoff * instream_decay 
        return tot

    def get_trans_load(self, verbose = 0):
        """Returns the transitional land loading from all upstream reaches to the waterbody."""
        r = self._network.get_reach(self._comID)
        d = {}
        if r._IsMonitored != '1':
            d = self._network.get_upstream_reaches(r)
        else:
            d = self._network.get_upstream_reaches(r, broken_at_gages=False)
        
        tot = 0.0 
        for i in d.keys():
            #calculate instream loss
            instream_decay = 1.0
            for j in d[i]:
                if j._IsMonitored == '1': #monitored reach has no decay
                    pass
                elif j._ComID == i._ComID: #head water reach has partial decay
                    instream_decay *= sqrt(j._ReachDecay) * j._ReservoirDecay
                else: #all other reaches have full decay
                    instream_decay *= j._ReachDecay * j._ReservoirDecay
            #adjust runoff due to monitoring station (if necessary)
            p_unbroken = self._network._g_unbroken.predecessors(i)
            p_broken = self._network._g.predecessors(i)
            runoff = 0.0
            if (len(p_broken)) == 0:
                if (len(p_unbroken)) == 0:
                    #head water
                    runoff = i.get_trans_runoff() 
                else:
                    #monitored
                    runoff = i.get_trans_runoff(adjust_for_monitoring=True)
            else:
                runoff = i.get_trans_runoff() 
            #calculate load 
            tot += runoff * instream_decay 
        return tot
    
    def get_urban_load(self, verbose = 0):
        """Returns the urban land loading from all upstream reaches to the waterbody."""
        r = self._network.get_reach(self._comID)
        d = {}
        if r._IsMonitored != '1':
            d = self._network.get_upstream_reaches(r)
        else:
            d = self._network.get_upstream_reaches(r, broken_at_gages=False)
        
        tot = 0.0
        for i in d.keys():
            #calculate instream loss
            instream_decay = 1.0
            for j in d[i]:
                if j._IsMonitored == '1': #monitored reach has no decay
                    pass
                elif j._ComID == i._ComID: #head water reach has partial decay
                    instream_decay *= sqrt(j._ReachDecay) * j._ReservoirDecay
                else: #all other reaches have full decay
                    instream_decay *= j._ReachDecay * j._ReservoirDecay
            #adjust runoff due to monitoring station (if necessary)
            p_unbroken = self._network._g_unbroken.predecessors(i)
            p_broken = self._network._g.predecessors(i)
            runoff = 0.0
            if (len(p_broken)) == 0:
                if (len(p_unbroken)) == 0:
                    #head water
                    runoff = i.get_urban_runoff() 
                else:
                    #monitored
                    runoff = i.get_urban_runoff(adjust_for_monitoring=True)
            else:
                runoff = i.get_urban_runoff() 
            #calculate load 
            tot += runoff * instream_decay 
        return tot
    
    def get_tot_load(self, verbose = 0):
        """Returns the total loading from all upstream reaches to the waterbody."""
        r = self._network.get_reach(self._comID)
        d = {}
        if r._IsMonitored != '1':
            d = self._network.get_upstream_reaches(r)
        else:
            d = self._network.get_upstream_reaches(r, broken_at_gages=False)
        
        tot = 0.0
        for i in d.keys():
            #calculate instream loss
            instream_decay = 1.0
            for j in d[i]:
                if j._IsMonitored == '1': #monitored reach has no decay
                    pass
                elif j._ComID == i._ComID: #head water reach has partial decay
                    instream_decay *= sqrt(j._ReachDecay) * j._ReservoirDecay
                else: #all other reaches have full decay
                    instream_decay *= j._ReachDecay * j._ReservoirDecay
            #adjust runoff due to monitoring station (if necessary)
            p_unbroken = self._network._g_unbroken.predecessors(i)
            p_broken = self._network._g.predecessors(i)
            runoff = 0.0
            if (len(p_broken)) == 0:
                if (len(p_unbroken)) == 0:
                    #head water
                    runoff = i.get_tot_runoff() 
                else:
                    #monitored
                    runoff = i.get_tot_runoff(adjust_for_monitoring=True)
            else:
                runoff = i.get_tot_runoff() 
            #calculate load 
            tot += runoff * instream_decay 
        return tot

## HAVE NOT TESTED THIS   
#    def get_tot_loading_from_reach(self, comID):
#        """Returns the loading from a reach to the waterbody.  This number \
#        includes any instream losses that occur from the reach to the \
#        waterbody."""
#        r = self._network.get_reach(comID)
#        return r.get_tot_runoff() * \
#            self._network.get_percent_loss(comID, self._comID) 

## HAVE NOT TESTED THIS
#    def get_concentration(self): 
#        """Returns the long term average concentration (mg/L) of nitrogen in the streamflow entering the waterbody."""
#        loading = self.get_total_loading() # in kg/yr
#        r = Reach(self._comID)
#        flow = r._Flow  #in cfs
#        #Oct 9, fixed equation to reflect sec/year (31557600), not sec/day (86400)
#        concentration = loading / flow / 31557600 / 28.3168466 * 1000000 # in mg/L
#        return concentration  
