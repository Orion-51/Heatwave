import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import pandas as pd
import cartopy.crs as import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import pandas as pd
import cartopy.crs as ccrs
import datetime
import nc_time_axis
import cftime
#so that dates work
pd.plotting.register_matplotlib_converters()
#latitude and longitude lists define domain
latitude = [ 41.375,  41.625,  41.875,  42.125,  42.375,  42.625,  42.875, 43.125,  43.375,  43.625,  43.875,  44.125,  44.375,  44.625, 44.875,  45.125,  45.375,  45.625,  45.875,  46.125,  46.375,
        46.625,  46.875,  47.125,  47.375,  47.625,  47.875,  48.125,
        48.375,  48.625,  48.875,  49.125,  49.375,  49.625,  49.875,
        50.125,  50.375,  50.625,  50.875,  51.125,  51.375,  51.625,
        51.875,  52.125,  52.375,  52.625,  52.875]

longitude = [ -5.125,  -4.875,  -4.625,  -4.375,  -4.125,  -3.875,  -3.625,
        -3.375,  -3.125,  -2.875,  -2.625,  -2.375,  -2.125,  -1.875,
        -1.625,  -1.375,  -1.125,  -0.875,  -0.625,  -0.375,  -0.125,
         0.125,   0.375,   0.625,   0.875,   1.125,   1.375,   1.625,
         1.875,   2.125,   2.375,   2.625,   2.875,   3.125,   3.375,
         3.625,   3.875,   4.125,   4.375,   4.625,   4.875,   5.125,
         5.375,   5.625,   5.875,   6.125,   6.375,   6.625,   6.875,
         7.125,   7.375,   7.625,   7.875,   8.125,   8.375,   8.625,
         8.875,   9.125,   9.375,   9.625,   9.875,  10.125,  10.375,
        10.625,  10.875,  11.125,  11.375,  11.625,  11.875,  12.125,
        12.375,  12.625,  12.875,  13.125,  13.375,  13.625,  13.875,
        14.125,  14.375,  14.625,  14.875,  15.125,  15.375,  15.625,
        15.875,  16.125,  16.375,  16.625,  16.875,  17.125,  17.375,
        17.625,  17.875,  18.125,  18.375,  18.625,  18.875,  19.125]


#List of locations created using lat and lon lists
loc_list = []
for lat in latitude:
    for lon in longitude:
        loc_list.append(tuple((lat,lon)))

#open EOBS file
dsObs = xr.open_dataset("/exports/csce/eddie/geos/groups/I3D/data/EOBS/tg_ens_mean_0.25deg_reg_v21.0e.nc")
#Get data for relevant time frame
tx = dsObs.tg.loc["2000-1-1":"2010-12-30"]
ccrs
import datetime
import nc_time_axis
import cftime
#so that dates work
pd.plotting.register_matplotlib_converters()
#latitude and longitude lists define domain
latitude = [ 41.375,  41.625,  41.875,  42.125,  42.375,  42.625,  42.875, 43.125,  43.375,  43.625,  43.875,  44.125,  44.375,  44.625, 44.875,  45.125,  45.375,  45.625,  45.875,  46.125,  46.375,
        46.625,  46.875,  47.125,  47.375,  47.625,  47.875,  48.125,
        48.375,  48.625,  48.875,  49.125,  49.375,  49.625,  49.875,
        50.125,  50.375,  50.625,  50.875,  51.125,  51.375,  51.625,
        51.875,  52.125,  52.375,  52.625,  52.875]

longitude = [ -5.125,  -4.875,  -4.625,  -4.375,  -4.125,  -3.875,  -3.625,
        -3.375,  -3.125,  -2.875,  -2.625,  -2.375,  -2.125,  -1.875,
        -1.625,  -1.375,  -1.125,  -0.875,  -0.625,  -0.375,  -0.125,
         0.125,   0.375,   0.625,   0.875,   1.125,   1.375,   1.625,
         1.875,   2.125,   2.375,   2.625,   2.875,   3.125,   3.375,
         3.625,   3.875,   4.125,   4.375,   4.625,   4.875,   5.125,
         5.375,   5.625,   5.875,   6.125,   6.375,   6.625,   6.875,
         7.125,   7.375,   7.625,   7.875,   8.125,   8.375,   8.625,
         8.875,   9.125,   9.375,   9.625,   9.875,  10.125,  10.375,
        10.625,  10.875,  11.125,  11.375,  11.625,  11.875,  12.125,
        12.375,  12.625,  12.875,  13.125,  13.375,  13.625,  13.875,
        14.125,  14.375,  14.625,  14.875,  15.125,  15.375,  15.625,
        15.875,  16.125,  16.375,  16.625,  16.875,  17.125,  17.375,
        17.625,  17.875,  18.125,  18.375,  18.625,  18.875,  19.125]




#List of locations created using lat and lon lists
loc_list = []
for lat in latitude:
    for lon in longitude:
        loc_list.append(tuple((lat,lon)))

#open EOBS file
dsObs = xr.open_dataset("/exports/csce/eddie/geos/groups/I3D/data/EOBS/tg_ens_mean_0.25deg_reg_v21.0e.nc")

#Open lists to hold arrays for each lat-lon point average
ObsAvg = []


#Concate EOBS data
ObsAll= xr.concat(ObsAvg,dim="time")
#find mean, median, max and min for EOBS
npObsAll=ObsAll.values
median=np.median(npObsAll)
mean=np.mean(npObsAll)
max=np.amax(npObsAll)
min=np.amin(npObsAll)
#Plot histogram and values
plt.hist(ObsAll,bins=40)
plt.suptitle("EOBS (every point)")
plt.title("\n mean = "+str(mean)+" median = "+str(median)+"\n min = "+str(min)+" max = "+str(max))
plt.savefig("/exports/csce/eddie/geos/groups/I3D/top/s1606013/Europe/EOBSep10Y.png") #save
plt.show()
plt.close()
#Get data for relevant time frame
tx = dsObs.tg.loc["2000-1-1":"2010-12-30"]
