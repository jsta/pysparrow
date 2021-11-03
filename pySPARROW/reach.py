from pySPARROW import database #.DB as DB
from numpy import array, dot
from math import exp, sqrt
from pySPARROW import utils

class Reach:
    def __init__(self, Network, Record):
        """A river segment and associated catchment that contribute pollution to downstream waterbodies."""
        rec = Record
        
        # set attribute values
        self._Network = Network
        self._ComID = rec['ComID']
        self._NLCD = {}
        self._NLCD['21'] = rec['NLCD_21'] # Developed, open space
        self._NLCD['22'] = rec['NLCD_22'] # Developed, low-intensity
        self._NLCD['23'] = rec['NLCD_23'] # Developed, med-intensity
        self._NLCD['24'] = rec['NLCD_24'] # Developed, high-intensity
        self._NLCD['31'] = rec['NLCD_31'] # Barren/Transitional
        self._NLCD['41'] = rec['NLCD_41'] # Forested, deciduous
        self._NLCD['42'] = rec['NLCD_42'] # Forested, evergreen
        self._NLCD['43'] = rec['NLCD_43'] # Forested, mixed
        self._NLCD['52'] = rec['NLCD_52'] # Shrubland
        self._NLCD['71'] = rec['NLCD_71'] # Grassland
        self._NLCD['81'] = rec['NLCD_81'] # Pasture
        self._NLCD['82'] = rec['NLCD_82'] # Row Crop
        self._AreaHa = rec['AreaHa']
        self._PntSrc_Kg = rec['PntSrc_Kg']
        self._AtmNO3_Kg = rec['AtmNO3_Kg']
        self._Fertil_rate = rec['Fertil_rate']
        self._LvskWst_rate = rec['LvskWst_rate']
        self._SoilPerm = rec['SoilPerm']
        self._DrainDnst = rec['DrainDnst']
        self._Temp_F = rec['AREAWTMAT']
        self._Flow = rec['MAFlowU']
        self._Velocity = rec['MAVelU']
        self._Length = rec['LengthKm']
        self._Runoff = rec['Runoff'] #todo delete this attribute and use only method to generate runoff
        # example data rows seem to be missing these columns...
        # rec.table
        # self._ReachDecay = rec['ReachDecay']
        # self._ReservoirDecay = rec['ReservoirDecay']
        # self._IsReservoir = rec['ReservoirFlag']
        # self._IsMonitored = rec['MonitoredFlag']
        # self._MeasuredLoad = rec['MeasuredLoad']
        self._ToComID = rec['ToComID']
    
    def get_LULC(self):
        """Returns the reach's current land use/land cover values as a dictionary."""
        return self._NLCD
    
    def get_atm_source(self):
        return self._AtmNO3_Kg * utils._beta[6]
    
    def get_pnt_source(self):
        return self._PntSrc_Kg * utils._beta[5]
    
    def get_waste_source(self):
        return self._LvskWst_rate * self._NLCD['81'] * utils._beta[8]
    
    def get_fert_source(self):
        return self._Fertil_rate * self._NLCD['82'] * utils._beta[7]
    
    def get_forest_source(self):
        return (self._NLCD['41'] + self._NLCD['42'] + self._NLCD['43']) * utils._beta[0] 

    def get_grass_source(self):
        return (self._NLCD['21'] + self._NLCD['71']) * utils._beta[1]
    
    def get_shrub_source(self):
        return self._NLCD['52'] * utils._beta[2]
    
    def get_trans_source(self):
        return self._NLCD['31'] * utils._beta[3] 
    
    def get_urban_source(self):
        return (self._NLCD['22'] + self._NLCD['23'] + self._NLCD['24']) * utils._beta[4]
    
    def get_tot_source(self):
        """Returns the total amount of pollution source for the reach"""
        return get_atm_source() + get_pnt_source() + get_waste_source() + \
            get_fert_source() + get_forest_source() + get_grass_source() + \
            get_shrub_source() + get_trans_source() + get_urban_source()  
    
    def get_atm_runoff(self, adjust_for_monitoring=False):
        if adjust_for_monitoring == False:
            z = array([self._SoilPerm, self._DrainDnst, self._Temp_F])
            return self.get_atm_source() * exp(dot(utils._alpha, z))
        else: #use measured load to rescale predicted load
            #get upstream reaches
            up_stream_reaches = self._Network._g_unbroken.predecessors(self)
            predicted_load_for_source = 0.0
            predicted_load_total = 0.0
            #sum source and total loads from upstream reaches
            for i in up_stream_reaches:
                wb = self._Network.get_waterbody(i._ComID)
                predicted_load_for_source += wb.get_atm_load()
                predicted_load_total += wb.get_tot_load()
            #transport upstream loads to this reach
            predicted_load_for_source *= self._ReachDecay * self._ReservoirDecay
            predicted_load_total *= self._ReachDecay * self._ReservoirDecay
            #add incremental load from reach
            predicted_load_for_source += self.get_atm_runoff() * \
                    sqrt(self._ReachDecay) * self._ReservoirDecay
            predicted_load_total += self.get_tot_runoff() * \
                    sqrt(self._ReachDecay) * self._ReservoirDecay
            #recale load 
            load = (predicted_load_for_source / predicted_load_total) * \
                   self._MeasuredLoad
            return load

    def get_pnt_runoff(self, adjust_for_monitoring=False):
        if adjust_for_monitoring == False:
            return self.get_pnt_source()
        else:
            #get upstream reaches
            up_stream_reaches = self._Network._g_unbroken.predecessors(self)
            predicted_load_for_source = 0.0
            predicted_load_total = 0.0
            #sum source and total loads from upstream reaches
            for i in up_stream_reaches:
                wb = self._Network.get_waterbody(i._ComID)
                predicted_load_for_source += wb.get_pnt_load()
                predicted_load_total += wb.get_tot_load()
            #transport upstream loads to this reach
            predicted_load_for_source *= self._ReachDecay * self._ReservoirDecay
            predicted_load_total *= self._ReachDecay * self._ReservoirDecay
            #add incremental load from reach
            predicted_load_for_source += self.get_pnt_runoff() * \
                    sqrt(self._ReachDecay) * self._ReservoirDecay
            predicted_load_total += self.get_tot_runoff() * \
                    sqrt(self._ReachDecay) * self._ReservoirDecay
            #recale load 
            load = (predicted_load_for_source / predicted_load_total) * \
                   self._MeasuredLoad
            return load
    
    def get_waste_runoff(self, adjust_for_monitoring=False):
        if adjust_for_monitoring == False:
            z = array([self._SoilPerm, self._DrainDnst, self._Temp_F])
            return self.get_waste_source() * exp(dot(utils._alpha, z))
        else:
            #get upstream reaches
            up_stream_reaches = self._Network._g_unbroken.predecessors(self)
            predicted_load_for_source = 0.0
            predicted_load_total = 0.0
            #sum source and total loads from upstream reaches
            for i in up_stream_reaches:
                wb = self._Network.get_waterbody(i._ComID)
                predicted_load_for_source += wb.get_waste_load()
                predicted_load_total += wb.get_tot_load()
            #transport upstream loads to this reach
            predicted_load_for_source *= self._ReachDecay * self._ReservoirDecay
            predicted_load_total *= self._ReachDecay * self._ReservoirDecay
            #add incremental load from reach
            predicted_load_for_source += self.get_waste_runoff() * \
                    sqrt(self._ReachDecay) * self._ReservoirDecay
            predicted_load_total += self.get_tot_runoff() * \
                    sqrt(self._ReachDecay) * self._ReservoirDecay
            #recale load 
            load = (predicted_load_for_source / predicted_load_total) * \
                   self._MeasuredLoad
            return load
    
    def get_fert_runoff(self, adjust_for_monitoring=False):
        if adjust_for_monitoring == False:
            z = array([self._SoilPerm, self._DrainDnst, self._Temp_F])
            return self.get_fert_source() * exp(dot(utils._alpha, z))
        else:
            #use measured load to rescale predicted load
            #get upstream reaches
            up_stream_reaches = self._Network._g_unbroken.predecessors(self)
            predicted_load_for_source = 0.0
            predicted_load_total = 0.0
            #sum source and total loads from upstream reaches
            for i in up_stream_reaches:
                wb = self._Network.get_waterbody(i._ComID)
                predicted_load_for_source += wb.get_fert_load()
                predicted_load_total += wb.get_tot_load()
            #transport upstream loads to this reach
            predicted_load_for_source *= self._ReachDecay * self._ReservoirDecay
            predicted_load_total *= self._ReachDecay * self._ReservoirDecay
            #add incremental load from reach
            predicted_load_for_source += self.get_fert_runoff() * \
                    sqrt(self._ReachDecay) * self._ReservoirDecay
            predicted_load_total += self.get_tot_runoff() * \
                    sqrt(self._ReachDecay) * self._ReservoirDecay
            #recale load 
            load = (predicted_load_for_source / predicted_load_total) * \
                   self._MeasuredLoad
            return load
    
    def get_forest_runoff(self, adjust_for_monitoring=False):
        if adjust_for_monitoring == False:
            z = array([self._SoilPerm, self._DrainDnst, self._Temp_F])
            return self.get_forest_source() * exp(dot(utils._alpha, z))
        else:
            #use measured load to rescale predicted load
            #get upstream reaches
            up_stream_reaches = self._Network._g_unbroken.predecessors(self)
            predicted_load_for_source = 0.0
            predicted_load_total = 0.0
            #sum source and total loads from upstream reaches
            for i in up_stream_reaches:
                wb = self._Network.get_waterbody(i._ComID)
                predicted_load_for_source += wb.get_forest_load()
                predicted_load_total += wb.get_tot_load()
            #transport upstream loads to this reach
            predicted_load_for_source *= self._ReachDecay * self._ReservoirDecay
            predicted_load_total *= self._ReachDecay * self._ReservoirDecay
            #add incremental load from reach
            predicted_load_for_source += self.get_forest_runoff() * \
                    sqrt(self._ReachDecay) * self._ReservoirDecay
            predicted_load_total += self.get_tot_runoff() * \
                    sqrt(self._ReachDecay) * self._ReservoirDecay
            #recale load 
            load = (predicted_load_for_source / predicted_load_total) * \
                   self._MeasuredLoad
            return load
        
    def get_grass_runoff(self, adjust_for_monitoring=False):
        if adjust_for_monitoring == False:
            z = array([self._SoilPerm, self._DrainDnst, self._Temp_F])
            return self.get_grass_source() * exp(dot(utils._alpha, z))
        else:
            #use measured load to rescale predicted load
            #get upstream reaches
            up_stream_reaches = self._Network._g_unbroken.predecessors(self)
            predicted_load_for_source = 0.0
            predicted_load_total = 0.0
            #sum source and total loads from upstream reaches
            for i in up_stream_reaches:
                wb = self._Network.get_waterbody(i._ComID)
                predicted_load_for_source += wb.get_grass_load()
                predicted_load_total += wb.get_tot_load()
            #transport upstream loads to this reach
            predicted_load_for_source *= self._ReachDecay * self._ReservoirDecay
            predicted_load_total *= self._ReachDecay * self._ReservoirDecay
            #add incremental load from reach
            predicted_load_for_source += self.get_grass_runoff() * \
                    sqrt(self._ReachDecay) * self._ReservoirDecay
            predicted_load_total += self.get_tot_runoff() * \
                    sqrt(self._ReachDecay) * self._ReservoirDecay
            #recale load 
            load = (predicted_load_for_source / predicted_load_total) * \
                   self._MeasuredLoad
            return load
    
    def get_shrub_runoff(self, adjust_for_monitoring=False):
        if adjust_for_monitoring == False:
            z = array([self._SoilPerm, self._DrainDnst, self._Temp_F])
            return self.get_shrub_source() * exp(dot(utils._alpha, z))
        else:
            #use measured load to rescale predicted load
            #get upstream reaches
            up_stream_reaches = self._Network._g_unbroken.predecessors(self)
            predicted_load_for_source = 0.0
            predicted_load_total = 0.0
            #sum source and total loads from upstream reaches
            for i in up_stream_reaches:
                wb = self._Network.get_waterbody(i._ComID)
                predicted_load_for_source += wb.get_shrub_load()
                predicted_load_total += wb.get_tot_load()
            #transport upstream loads to this reach
            predicted_load_for_source *= self._ReachDecay * self._ReservoirDecay
            predicted_load_total *= self._ReachDecay * self._ReservoirDecay
            #add incremental load from reach
            predicted_load_for_source += self.get_shrub_runoff() * \
                    sqrt(self._ReachDecay) * self._ReservoirDecay
            predicted_load_total += self.get_tot_runoff() * \
                    sqrt(self._ReachDecay) * self._ReservoirDecay
            #recale load 
            load = (predicted_load_for_source / predicted_load_total) * \
                   self._MeasuredLoad
            return load
    
    def get_trans_runoff(self, adjust_for_monitoring=False):
        if adjust_for_monitoring == False:
            z = array([self._SoilPerm, self._DrainDnst, self._Temp_F])
            return self.get_trans_source() * exp(dot(utils._alpha, z))
        else:
            #use measured load to rescale predicted load
            #get upstream reaches
            up_stream_reaches = self._Network._g_unbroken.predecessors(self)
            predicted_load_for_source = 0.0
            predicted_load_total = 0.0
            #sum source and total loads from upstream reaches
            for i in up_stream_reaches:
                wb = self._Network.get_waterbody(i._ComID)
                predicted_load_for_source += wb.get_trans_load()
                predicted_load_total += wb.get_tot_load()
            #transport upstream loads to this reach
            predicted_load_for_source *= self._ReachDecay * self._ReservoirDecay
            predicted_load_total *= self._ReachDecay * self._ReservoirDecay
            #add incremental load from reach
            predicted_load_for_source += self.get_trans_runoff() * \
                    sqrt(self._ReachDecay) * self._ReservoirDecay
            predicted_load_total += self.get_tot_runoff() * \
                    sqrt(self._ReachDecay) * self._ReservoirDecay
            #recale load 
            load = (predicted_load_for_source / predicted_load_total) * \
                   self._MeasuredLoad
            return load
    
    def get_urban_runoff(self, adjust_for_monitoring=False):
        if adjust_for_monitoring == False:
            z = array([self._SoilPerm, self._DrainDnst, self._Temp_F])
            return self.get_urban_source() * exp(dot(utils._alpha, z))
        else:
            #use measured load to rescale predicted load
            #get upstream reaches
            up_stream_reaches = self._Network._g_unbroken.predecessors(self)
            predicted_load_for_source = 0.0
            predicted_load_total = 0.0
            #sum source and total loads from upstream reaches
            for i in up_stream_reaches:
                wb = self._Network.get_waterbody(i._ComID)
                predicted_load_for_source += wb.get_urban_load()
                predicted_load_total += wb.get_tot_load()
            #transport upstream loads to this reach
            predicted_load_for_source *= self._ReachDecay * self._ReservoirDecay
            predicted_load_total *= self._ReachDecay * self._ReservoirDecay
            #add incremental load from reach
            predicted_load_for_source += self.get_urban_runoff() * \
                    sqrt(self._ReachDecay) * self._ReservoirDecay
            predicted_load_total += self.get_tot_runoff() * \
                    sqrt(self._ReachDecay) * self._ReservoirDecay
            #recale load 
            load = (predicted_load_for_source / predicted_load_total) * \
                   self._MeasuredLoad
            return load
    
    def get_tot_runoff(self, adjust_for_monitoring=False):
        """Returns the runoff load for the reach (i.e. loading from the 
        reach's catchment (non-point source) that reaches the stream)."""
        if adjust_for_monitoring == False:
            return self.get_atm_runoff() + self.get_pnt_runoff() + self.get_waste_runoff() + \
                self.get_fert_runoff() + self.get_forest_runoff() + self.get_grass_runoff() + \
                self.get_shrub_runoff() + self.get_trans_runoff() + self.get_urban_runoff()  
        else:
            return self.get_atm_runoff(adjust_for_monitoring=True) \
                    + self.get_pnt_runoff(adjust_for_monitoring=True) \
                    + self.get_waste_runoff(adjust_for_monitoring=True) \
                    + self.get_fert_runoff(adjust_for_monitoring=True) \
                    + self.get_forest_runoff(adjust_for_monitoring=True) \
                    + self.get_grass_runoff(adjust_for_monitoring=True) \
                    + self.get_shrub_runoff(adjust_for_monitoring=True) \
                    + self.get_trans_runoff(adjust_for_monitoring=True) \
                    + self.get_urban_runoff(adjust_for_monitoring=True) 


