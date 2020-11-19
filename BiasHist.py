"""
A.Tully
I3D Project
Program finds differnce between EOBS data and Historical ensemble data for 3 day average of Max Temperature
"""

import numpy as np
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



#open EOBS file
dsObs = xr.open_dataset("/exports/csce/eddie/geos/groups/I3D/data/EOBS/tg_ens_mean_0.25deg_reg_v21.0e.nc")
#Get data for relevant time frame
tx = dsObs.tg.loc["2000-1-1":"2010-12-30"]

#each historical ensemble member name
xisda="xisda"
xisdb="xisdb"
xisdc="xisdc"
xisdd="xisdd"
xisde="xisde"

#Open lists to hold arrays for each lat-lon point average
ObsAvg = []

#get data for each location
#go through location list and get lat and lon
for lat in latitude:
    current_lat=[]
    for lon in longitude:
        txObs_loc = tx.sel(latitude = lat, longitude = lon, method="nearest") #EOBS data for location
        a=txObs_loc.rolling(time=3).mean().dropna("time")
        b=a.values +273.15 #3 day average for EOBS data (average of day before, current day and day after)
        current_lat.append(b) #add to Obs list
    current_lat_np=np.array(current_lat)
    ObsAvg.append(current_lat_np)
dsObs.close() #close EOBS
ObsAvgnp=np.array(ObsAvg)


#Lists to hold 3 day averages for Hist
xisda_loc_ave=[]
xisdb_loc_ave=[]
xisdc_loc_ave=[]
xisdd_loc_ave=[]
xisde_loc_ave=[]
#function to give 3 day averages
#goes through each time step for a latitude, gives averages for each longitude in array
#input is Hist member to be used and list to append averages to (see above)

def get_3day_ave(xisd,list):
    x=np.load("/exports/csce/eddie/geos/groups/I3D/top/europe/files_for_alex/"+str(xisd)+"_member.npy")
    for k in range(15000,18600-2):
        current_time=[]
        for i in range(0,47):
            l=[]
            arr=x[k,i]
            arr1=x[k+2,i]
            arr2=x[k+2,i]
            l.append(arr)
            l.append(arr1)
            l.append(arr2)
            n=np.mean(l,axis=0)
            current_time.append(n)
        current_time_np=np.array(current_time)
        list.append(current_time_np)
#run functions for each member
get_3day_ave(xisda,xisda_loc_ave)
get_3day_ave(xisdb,xisdb_loc_ave)
get_3day_ave(xisdc,xisdc_loc_ave)
get_3day_ave(xisdd,xisdd_loc_ave)
get_3day_ave(xisde,xisde_loc_ave)
#list for average of Hist ensemble members

ensemble_list=[xisda_loc_ave,xisdb_loc_ave,xisdc_loc_ave,xisdd_loc_ave,xisde_loc_ave]
ensemble=np.array(ensemble_list)

xAve=np.mean(ensemble,axis=0)

np.save("/exports/csce/eddie/geos/groups/I3D/top/europe/bias_files/Obs10Y.npy",ObsAvgnp)
np.save("/exports/csce/eddie/geos/groups/I3D/top/europe/bias_files/Hist10Y.npy",xAve)
