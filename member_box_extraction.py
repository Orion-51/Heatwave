"""
I3D Project
Daniel Brener, s1704203
08/11/2020
"""
# Import modules
print("LOADING MODULES")
import numpy as np
import iris
import iris.coord_categorisation
import itertools

###########
# EXTRACT DOMAIN
# This process uses lazy data,
# except for the final line which 
# requires full loading.

filename = "xmxmpa.pal9jul.nc"

# Define domain
# See this for the box definition on a map:
# http://bboxfinder.com/#42.488302,-5.053711,50.064192,9.931641

min_lat = 42.488302
max_lat = 50.064192
min_lon = -5.053711
max_lon = 9.931641

# Create domain constraint iris object
domain = iris.Constraint(latitude = lambda c: c>= min_lat and c<= max_lat , longitude = lambda d: d>= min_lon and d<= max_lon)

# Define variables to extract from NetCDF
vars = ['air_temperature']

##########
# LOADING AND PROCESSING ENSEMBLE
months = ['mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov']
ensemble_id = "xowea"
months_extract = [".nc"]*9
for i in range(9):
	months_extract[i] = ensemble_id+".pal9"+months[i]+months_extract[i]

filenames = months_extract

# Load single ensemble temperatures
member = iris.load(filenames, vars)[0]

# Select domain defined above
member_boxed = member.extract(domain)

# Save data
#np.save(,member_boxed.data)
print(member_boxed.data)