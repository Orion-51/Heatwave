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

#List of locations
loc_list = [(49,2), (50,3), (60,10)]
#open dataset from nc file
dsObs = xr.open_dataset("/exports/csce/eddie/geos/groups/I3D/data/EOBS/tg_ens_mean_0.25deg_reg_v21.0e.nc")
#open dataset for historical ensemble
dsHist = xr.open_dataset("/exports/csce/eddie/geos/groups/I3D/data/HadAM3P/xisda/daily_tas8192.nc")
#get max temperature
tx = dsObs.tg.loc["2000-1-1":"2010-12-30"]
#Inorder to get arrays to work need to convert Hist time to format of EOBS, easiest way to do is to set Hist times as EOBS times
#This is clunky and is likely to not work great

d1=(2000-1959)*360
d2=(2010-1959)*360
dsHist_time=dsHist.air_temperature.loc[]
#get max T
dsHist_noalt=dsHist_time.sel(altitude=1.5) #select altitude to stop problems later

txHist = dsHist_noalt.air_temperature #convert to
#Open lists to hold arrays for each lat-lon point average
ObsAvg = []
HistAvg = []
time = []
#get data for each location
#go through location list and get lat and lon
for loc in loc_list:
    print(loc)
    txObs_loc = tx.sel(latitude = loc[0], longitude = loc[1], method="nearest") #EOBS data for location
    txHist_loc = txHist.sel(latitude= loc[0], longitude= loc[1], method="nearest") #Hist data for each location

    a=txObs_loc.rolling(time=3).mean().dropna("time") #3 day average for Obs data (average of day before, current day and day after)
    ObsAvg.append(a) #add to Obs list
    b=txHist_loc.rolling(time=3).mean().dropna("time") #3 day average for Hist data
    HistAvg.append(b) #add to Hist

#Print statements to check numbers


ObsAll= xr.concat(ObsAvg,dim="time")
HistAll=xr.concat(HistAvg,dim="time")

plt.hist(ObsAll)
plt.title("EOBS (every point)")
plt.savefig("/exports/csce/eddie/geos/groups/I3D/top/s1606013/Europe/EOBSep.png")
plt.close()
plt.hist(HistAll)
plt.title("Hist (every point)")
plt.savefig("/exports/csce/eddie/geos/groups/I3D/top/s1606013/Europe/Histep.png")
plt.close()
SumObs=ObsAvg[0] #initial array to give shape
#iterate through arrays in differnce list to get sum
for i in range(1,len(ObsAvg)):
    SumObs = SumObs+ObsAvg[i]
#divide through to give mean
AveObs=SumObs/len(ObsAvg)
print("averages")
print(AveObs)
plt.hist(AveObs)
plt.title("EOBS (domain average)")
plt.savefig("/exports/csce/eddie/geos/groups/I3D/top/s1606013/Europe/EOBSda.png")
plt.close()
SumHist=HistAvg[0] #initial array to give shape
for i in range(1,len(HistAvg)):
    SumHist = SumHist+HistAvg[i]
#divide through to give mean
AveHist=SumHist/len(HistAvg)
print(AveHist)
plt.hist(AveHist)
plt.title("Hist (domain average)")
plt.savefig("/exports/csce/eddie/geos/groups/I3D/top/s1606013/Europe/Histda.png")
plt.close()
