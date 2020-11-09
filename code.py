import numpy as np # pkg for high level maths
import xarray as xr # for handling NetCDF files

import matplotlib.pyplot as plt # for plotting
import scipy.stats as st
from scipy.integrate import quad
from scipy.stats._continuous_distns import _distn_names

import warnings
import pandas as pd
import statsmodels as sm
from distfit import distfit

#Directory_hist = \pathtohistoricalensemble
#Directory_nat = \pathtonaturalensemble

EVENT = 31
no_runs = 20
loc_list = np.linspace(0,100,num=100)
weights = np.ones_like(loc_list)
temp_list_hist = np.zeros_like(loc_list)
temp_list_nat = np.zeros_like(loc_list)

temp_list_hist_arr = np.zeros((no_runs,len(loc_list))) #to hold historical data
temp_list_nat_arr = np.zeros((no_runs,len(loc_list))) #to hold natural data

"""
#this bit opens the historical data and gets 3day avg maxes and their indices
counter = 0
for filename_hist, filename_nat in zip(os.listdir(Directory_hist),os.listdir(Directory_nat)): #iterate thru folders
    if filename_hist.endswith(".nc") and filename_nat.endswith(".nc"): #make sure it is the right format
        full_path_hist = os.path.join(Directory_hist, filename_hist) #get path to HIST file
        full_path_nat = os.path.join(Directory_nat, filename_nat) #get path to Nat file
        if os.path.isfile(full_path_hist) and os.path.isfile(full_path_nat): #if its a file:
            DS_hist = xr.open_dataset(full_path_hist) #open run for Hist
            airtemp_hist = DS_hist.air_temperature #get temp data for Hist
            DS_nat = xr.open_dataset(full_path_nat) #open run for Nat
            airtemp_nat = DS_nat.air_temperature #get temp data for Nat

            for loc in loc_list
                airtemp_hist_loc = airtemp_hist.sel(latitude = loc[0], longitude = loc[1], method = 'nearest') #iterate through locations, get time-temp data for each
                airtemp_nat_loc = airtemp_nat.sel(latitude = loc[0], longitude = loc[1], method = 'nearest')
                avgs_hist = [] #make lists to hold 3 day avgs
                avgs_nat = []

                for j in range(airtemp_hist_loc-2): #find all 3 day avgs
                    avgs_hist.append(np.average(airtemp_hist_loc[j:j+2]))
                    avgs_nat.append(np.average(airtemp_nat_loc[j:j+2]))

                ind = np.argmax(avgs_hist) #get the max 3 day avg and its first index
                threeday_avgmax_hist = avgs_hist[ind]
                threeday_avgmax_nat = avgs_nat[ind] #get temp at same point in natural

                temp_list_hist[i] = threeday_avgmax_hist # apppend temperature into hist list
                temp_list_nat[i] = threeday_avgmax_nat # apppend  temperature into nat list

    temp_list_hist_arr[counter,:] = temp_list_hist #append lists into array
    temp_list_nat_arr[counter,:] = temp_list_nat
    counter += 1
"""
temp_list_hist_arr = np.random.normal(loc=31,scale = 10,size=(no_runs,len(loc_list))) #to hold historical data
temp_list_nat_arr = np.random.normal(loc=30,scale = 10,size=(no_runs,len(loc_list))) #to hold natural data

summed_hist = np.average(temp_list_hist_arr,weights = weights, axis=1) #sum together contributions of each location to get a "heat value" for each run
summed_nat = np.average(temp_list_nat_arr, weights = weights, axis=1)

#TESTING FOR NORMALITY
NormTests = [st.normaltest,st.shapiro,st.jarque_bera,st.anderson]
print("Testing for normality, HIST then NAT")
for i in NormTests:
    print(i.__name__)
    print(i(summed_hist))
    print(i(summed_nat))

print("KS TEST")
print(st.kstest((summed_hist),"norm",args=(np.mean(summed_hist),np.std(summed_hist))))
print(st.kstest((summed_nat),"norm",args=(np.mean(summed_nat),np.std(summed_nat))))
def chi(INPUT):
    rang=np.arange(-200,200,10)
    dist = np.random.normal(np.mean(INPUT),np.std(INPUT),100000000)
    binned = (np.array(np.histogram(dist,bins=rang,density=True)) * len(INPUT) *10)[0]
    a = np.array(np.histogram(INPUT,bins=rang))[0]
    aa = []
    binnd = []
    for i in zip(binned,a):
        if i[0] == 0.:
            pass
        else:
            binnd.append(i[0])
            aa.append(i[1])
    print("CHISQ TEST")
    print(st.chisquare(aa,binnd))
chi(summed_hist)
chi(summed_nat)

#TESING IF DISTRIBUTIONS ARE "THE SAME"
Tests = [st.mannwhitneyu,st.f_oneway,st.ks_2samp,st.chisquare]
print("Testing for same parent distribution")
for i in Tests:
    print(i.__name__)
    print(i(summed_hist,summed_nat))
print("T TEST")
print(st.ttest_ind(summed_hist,summed_nat,equal_var=False))

#FIND UNDERLYING PDF
def get_prob(data):
    # Create models from data
    dist = distfit(distr='norm', bins=50,smooth=20)
    dist.fit_transform(data)
    dist.plot()

    # All scores of the tested distributions
    #print(dist.summary)

    # get probabilities
    norm_fac = quad(dist.model["distr"].pdf, -np.inf, np.inf, args=(dist.model["params"]))[0]
    print(norm_fac)
    prob = quad(dist.model["distr"].pdf, EVENT, np.inf, args=(dist.model["params"]))[0]
    normed_prob = prob/norm_fac
    return normed_prob

#GET RISK RATIO
hist_prob = get_prob(summed_hist)
nat_prob = get_prob(summed_nat)
RR = hist_prob/nat_prob
print(RR)