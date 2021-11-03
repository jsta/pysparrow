# pySPARROW

An object-oriented Python package for calculating water quality loadings using the SPARROW model

## Installation

```shell
conda env create -f environment.yml
conda activate pysparrow

pip install --upgrade -e .
```

## Usage

### Data

| Column name                       | Definition                                               |
|-----------------------------------|----------------------------------------------------------|
| ToComID = StringCol(16)           | # COMID of catchment immediately downstream              |
| Direction = StringCol(16)         | # 709=connected; 712=net start; 713=net end; 714=coastal |
| NLCD_21 = FloatCol()              | # ha Developed, open space                               |
| NLCD_22 = FloatCol()              | # ha Developed, low-intensity                            |
| NLCD_23 = FloatCol()              | # ha Developed, med-intensity                            |
| NLCD_24 = FloatCol()              | # ha Developed, high-intensity                           |
| NLCD_31 = FloatCol()              | # ha Barren/Transitional                                 |
| NLCD_41 = FloatCol()              | # ha Forest, deciduous                                   |
| NLCD_42 = FloatCol()              | # ha Forest, evergreen forest                            |
| NLCD_43 = FloatCol()              | # ha Forest, mixed                                       |
| NLCD_52 = FloatCol()              | # ha Shrubland                                           |
| NLCD_71 = FloatCol()              | # ha Grassland                                           |
| NLCD_81 = FloatCol()              | # ha Pasture                                             |
| NLCD_82 = FloatCol()              | # ha Row Crop                                            |
| AreaHa = FloatCol()               | # total area of catchment (ha)                           |
| PntSrc_Kg = FloatCol()            | # kg N from point sources                                |
| AtmNO3_Kg = FloatCol()            | # kg N from atmospheric deposition                       |
| Fertil_rate = FloatCol()          | # kg N/ha row crops in catchment                         |
| LvskWst_rate = FloatCol()         | # kg N/ha pasture in catchment                           |
| SoilPerm = FloatCol()             | # avg soil permeability (cm/hr)                          |
| DrainDnst = FloatCol()            | # km stream/sq km catchment area                         |
| AREAWTMAT = FloatCol()            | # area wtd mean temperature (�F)                         |
| MAFlowU = FloatCol()              | # mean annual flow (cfs)                                 |
| MAVelU = FloatCol()               | # mean annual velocity (ft/s)                            |
| LengthKm = FloatCol()             | # total stream length in catchment                       |
| Runoff = FloatCol()               | # total runoff from catchment                            |
| InstreamLossExponent = FloatCol() | # percent loss exponent due to instream transport        |

### Execution

```python

```

## Acknowledgements

Original Authors: J. Goodall, D. Bollinger, Jr., J. Fay

Original Release Date: May 23, 2010

See [https://doi.org/10.1016/j.envsoft.2010.04.007](10.1016/j.envsoft.2010.04.007
)
