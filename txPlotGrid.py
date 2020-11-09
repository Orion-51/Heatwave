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

#so that dates work
pd.plotting.register_matplotlib_converters()

#List of locations
loc_list = [(49,2), (50,3), (60,10)]
#open dataset from nc file
dsObs = xr.open_dataset("tx_ens_mean_0.25deg_reg_2011-2019_v21.0e.nc")
#open dataset for historical ensemble
dsHist = xr.open_dataset("xmxmoa.pal8dec.nc")
#get max temperature
tx = dsObs.tx.loc["2018-12-1":"2018-12-30"]
#Inorder to get arrays to work need to convert Hist time to format of EOBS, easiest way to do is to set Hist times as EOBS times
#This is clunky and is likely to not work great
dsHist["time"]=tx.indexes["time"]
#get max T
dsHist_noalt=dsHist.sel(altitude=1.5) #select altitude to stop problems later

txHist = dsHist_noalt.air_temperature_2 -273.15  #convert to celcius

#Open lists to hold arrays for each lat-lon point average
ObsAvg = []
HistAvg = []
time = []
Diff = []
label = []
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
    diff=a-b #find the differnce between the two average values
    Diff.append(diff) #add to difference list
    label.append(loc) #Add location to list for plotting later

#Print statements to check numbers
print("Obs")
print(ObsAvg)
print("Hist")
print(HistAvg)
print("diff")
print(Diff)
print(len(Diff))

#Find average differnce across all locations
SumDiff=Diff[0] #initial array to give shape
#iterate through arrays in differnce list to get sum
for i in range(1,len(Diff)):
    SumDiff = SumDiff+Diff[i]
#divide through to give mean
AveDiff=SumDiff/len(Diff)

#Plot each location
for k in range(0,len(Diff)):
    latlon= label[k]
    Diff[k].plot(label= "lat: "+str(latlon[0])+" lon: "+str(latlon[1]))
#Plot average
AveDiff.plot(label="AveDiff")
#Titles and labels
plt.xlabel("Date")
plt.ylabel("Differnce in 3 Day Average Max Temperature (C)")
plt.legend()
plt.savefig("GridBoxPlot.png")
