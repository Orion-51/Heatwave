"""
A.Tully
I3D
Maps Max Temperature in Europe
Maps EOBS data for a single time step
Maps Historical ensemble data for single time step

"""

import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import pandas as pd
import cartopy.crs as ccrs
from datetime import date
import nc_time_axis

#so that dates work
pd.plotting.register_matplotlib_converters()

#open dataset from nc file
ds = xr.open_dataset("tx_ens_mean_0.25deg_reg_2011-2019_v21.0e.nc")
#get max temperature
tx = ds.tx
#specify date range of date
da = tx.loc["2018-12-1"]

#get data for select location
tx_Paris = da.sel(latitude=49, longitude=2., method="nearest")
#open dataset for historical ensemble
dsHist = xr.open_dataset("xmxmoa.pal8dec.nc")


#get max T (is this the right variable?)
txHist = dsHist.air_temperature_2 -273.15


#data for slect location
tx_ParisHist = txHist.sel(latitude=49, longitude=2, method="nearest")


#code to plot map

sap = da.isel()

# Draw coastlines of the Earth
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()

sap.plot()
plt.savefig('EOBSMap.png')
plt.close()

sap2 = txHist.isel(time=0)

ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_ylim(25.38,75.38)
ax.set_xlim(-40.38,75.38)
ax.coastlines()

sap2.plot()
plt.savefig('HistMap.png')
plt.close()
