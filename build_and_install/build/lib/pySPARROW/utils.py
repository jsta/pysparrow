from numpy import array, dot
from math import exp
import sys, pyodbc, os
from tables import *

# SPARROW coefficients
#beta must match with the s array defined below
#Forestland, Grassland, Shrubland, Transitional, Urban, PntSrc_Kg, AtmNO3_Kg, Fertil_Kg, LvskWst_Kg
#_beta = array([2.82,1.42,1.02,75.10,64.60,0.1340,1.406,0.1882,0.2136])
_beta = array([440.3653033, 0 , 0, 0, 0, 0.460155723, 1.648010351,	0.300483097,	0.274057989])

#alpha array must match with z array defined below
#SoilPerm, DrainDnst, Temp_F
#_alpha = array([-0.1177,1.575,-0.0331])
_alpha = array([-0.095887767, 1.766827208, -0.024549489])

#k array gives flow decay rates
#_k =  array([0.3758, 0.1233, 0.0406]) 
_k = array([0.533902977,	0.133292406,	0.000369142,	8.258529056])

def get_reservoir_decay(hload):
    return 1 / (1 + _k[3] / hload)
    
def get_reach_decay(tt_days, flow_CFS):
    if flow_CFS > 0 and flow_CFS < 500:
        return exp( -1 * _k[0] * tt_days)
    elif flow_CFS >= 500 and flow_CFS <10000:
        return exp( -1 * _k[1] * tt_days)
    elif flow_CFS >= 10000:
        return exp( -1 * _k[2] * tt_days)
    else:
        #TODO: Flow of 0 should yeild a travel time of infinity. But this  
        #assumes that any reach with zero flow is a mistake and I'm ignoring 
        #any reduction that might occur in these reaches (because I don't believe
        #any reaches will have zero flow). JLG
        return 1.0

def get_new_reach_runoff(NLCD, PntSrc_Kg, AtmNO3_Kg, Fertil_rate, \
                          LvskWst_rate, SoilPerm, DrainDnst, Temp_F):
    """Returns the runoff load for a reach (i.e. loading from the
    reach's catchment that reaches the stream)."""
    Fertil_Kg = Fertil_rate * NLCD['82']
    LvskWst_Kg = LvskWst_rate * NLCD['81']
    Forestland = NLCD['41'] + NLCD['42'] + NLCD['43']
    Grassland = NLCD['21'] + NLCD['71']
    Shrubland = NLCD['52']
    Transitional = NLCD['31']
    Urban = NLCD['22'] + NLCD['23'] + NLCD['24']
    s = array([Forestland, Grassland, Shrubland, Transitional, Urban, \
               PntSrc_Kg, AtmNO3_Kg, Fertil_Kg, LvskWst_Kg])
    z = array([SoilPerm, DrainDnst, Temp_F])
    return dot(_beta, s) * exp(dot(_alpha, z))

def csv_2_hdf(csv_file, h5_file):
    """Creates an hdf5 file from a csv table using ODBC"""

    class Reach(IsDescription):
        ComID = StringCol(16)       # Catchment COMID
        ToComID = StringCol(16)     # COMID of catchment immediately downstream
        Direction = StringCol(16)   # 709=connected; 712=net start; 713=net end; 714=coastal
        NLCD_21 = FloatCol()        # ha Developed, open space
        NLCD_22 = FloatCol()        # ha Developed, low-intensity
        NLCD_23 = FloatCol()        # ha Developed, med-intensity
        NLCD_24 = FloatCol()        # ha Developed, high-intensity
        NLCD_31 = FloatCol()        # ha Barren/Transitional
        NLCD_41 = FloatCol()        # ha Forest, deciduous
        NLCD_42 = FloatCol()        # ha Forest, evergreen forest
        NLCD_43 = FloatCol()        # ha Forest, mixed
        NLCD_52 = FloatCol()        # ha Shrubland
        NLCD_71 = FloatCol()        # ha Grassland
        NLCD_81 = FloatCol()        # ha Pasture
        NLCD_82 = FloatCol()        # ha Row Crop
        AreaHa = FloatCol()         # total area of catchment (ha)
        PntSrc_Kg = FloatCol()      # kg N from point sources
        AtmNO3_Kg = FloatCol()      # kg N from atmospheric deposition
        Fertil_rate = FloatCol()    # kg N/ha row crops in catchment
        LvskWst_rate = FloatCol()   # kg N/ha pasture in catchment
        SoilPerm = FloatCol()       # avg soil permeability (cm/hr)
        DrainDnst = FloatCol()      # km stream/sq km catchment area
        AREAWTMAT = FloatCol()      # area wtd mean temperature (°F)
        MAFlowU = FloatCol()        # mean annual flow (cfs)
        MAVelU = FloatCol()         # mean annual velocity (ft/s)
        LengthKm = FloatCol()       # total stream length in catchment
        Runoff = FloatCol()         # total runoff from catchment
        InstreamLossExponent = FloatCol()    # percent loss exponent due to instream transport
        IsReservoir = StringCol(16)
    
    # required files (assumes this csv file is in current working directory)
    conn_string = 'DRIVER={Microsoft Text Driver (*.txt; *.csv)};;DBQ=' + os.getcwd()
       
    conn = odbc.odbc(conn_string)
    cur = conn.cursor()
   
    # cursor is ordered in desc order by version to ensure latest version
    # of reach (up to the specified version) is returned
    cur.execute('SELECT COMID, TOCOMID, DIRECTION,  \
        NLCD01_21, NLCD01_22, NLCD01_23, NLCD01_24, NLCD01_31, \
        NLCD01_41, NLCD01_42,  NLCD01_43,  NLCD01_52, NLCD01_71, NLCD01_81,  NLCD01_82, \
        TotArea_HA, IndPtSrc_rate, MunPtSrc_rate, AtmN_kg, Fert_rate, LvStk_rate, SoilPerm_cmhr, \
        Length_km, Temp_F, Discharge_cfs, Velocity_fps FROM ' + csv_file)
   
    rec = cur.fetchone()

    # Open a file in "w"rite mode
    h5file = openFile(h5_file, mode = "w", title = "data for pySPARROW")

    # Create a new group under "/" (root)
    group = h5file.createGroup("/", "networks", "networks")

    # Create a new table under the Networks group
    table = h5file.createTable(group, "network0", Reach)
    i = 1
    while rec:
        print str(int(rec[0])) + " " + str(i)
        i = i + 1
        
        #Calculate PtSrc values from: indust. rt * indus. area (NLCD-24) + mun rt * mun area (NLCD 22-24)
        PtSrc = (float(rec[17]*float(rec[6]))) + (float(rec[18])*(float(rec[4])+float(rec[5])+float(rec[6])))
        #Calculate drainage density:
        drainage_density = float(rec[22])/float(rec[15])
        reach = table.row
        reach['ComID'] = str(int(rec[0]))
        reach['ToComID'] = str(int(rec[1]))
        reach['Direction'] = str(int(rec[2]))
        reach['NLCD_21'] = float(rec[3])
        reach['NLCD_22'] = float(rec[4])
        reach['NLCD_23'] = float(rec[5])
        reach['NLCD_24'] = float(rec[6])
        reach['NLCD_31'] = float(rec[7])
        reach['NLCD_41'] = float(rec[8])
        reach['NLCD_42'] = float(rec[9])
        reach['NLCD_43'] = float(rec[10])
        reach['NLCD_52'] = float(rec[11])
        reach['NLCD_71'] = float(rec[12])
        reach['NLCD_81'] = float(rec[13])
        reach['NLCD_81'] = float(rec[13])
        reach['NLCD_82'] = float(rec[14])
        reach['AreaHa'] = float(rec[15])
        reach['PntSrc_Kg'] = PtSrc # value calculated above
        reach['AtmNO3_Kg'] = float(rec[18])
        reach['Fertil_rate'] = float(rec[19])
        reach['LvskWst_rate'] = float(rec[20])
        reach['SoilPerm'] = float(rec[21])
        reach['DrainDnst'] = drainage_density
        reach['AREAWTMAT'] =float(rec[23])
        reach['MAFlowU'] = float(rec[24])
        reach['MAVelU'] = float(rec[25])
        reach['LengthKm'] = float(rec[22])
        NLCD = {'21': float(rec[3]), \
                '22': float(rec[4]), \
                '23': float(rec[5]), \
                '24': float(rec[6]), \
                '31': float(rec[7]), \
                '41': float(rec[8]), \
                '42': float(rec[9]), \
                '43': float(rec[10]), \
                '52': float(rec[11]), \
                '71': float(rec[12]), \
                '81': float(rec[13]), \
                '82': float(rec[14])}
        reach['Runoff'] = get_new_reach_runoff(NLCD, PtSrc, \
            float(rec[18]), float(rec[19]), float(rec[20]), float(rec[21]), \
            drainage_density, float(rec[23]))
        reach['IsReservoir'] = rec['ReservoirFlag']
        #Skip reach (don't even append it) if flow velocity <= 0)
        if float(rec['MAVelU']) > 0:
            reach['InstreamLossExponent'] = get_new_reach_instream_loss_exponent( \
                rec['LengthKm'] / rec['MAVelU'] / 26.33472, float(rec[24]), rec['ReservoirFlag'])
            reach.append()
        rec = cur.fetchone()    
    h5file.close()
