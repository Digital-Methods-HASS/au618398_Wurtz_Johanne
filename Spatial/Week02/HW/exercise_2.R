##-----------------------------------------------##
##    Author: Adela Sobotkova                    ##
##    Institute of Culture and Society           ##
##    Aarhus University, Aarhus, Denmark         ##
##    adela@cas.au.dk                             ##
##-----------------------------------------------##

#### Goals ####

# - Understand the provided datasets
# - Learn how to reproject spatial data
# - Limit your data into an area of interest
# - Create a new map

# We highlighted all parts of the R script in which you are supposed to add your
# own code with: 

# /Start Code/ #

print("Hello World") # This would be your code contribution

# /End Code/ #

#### Required R libraries ####

# We will use the sf, raster, and tmap packages.
# Additionally, we will use the spData and spDataLarge packages that provide new datasets. 
# These packages have been preloaded to the worker2 workspace.

library(sf)
library(raster)
library(tmap)
library(spData)
library(spDataLarge)

#### Data sets #### 

# We will use two data sets: `srtm` and `zion`.
# The first one is an elevation raster object for the Zion National Park area, and the second one is an sf object with polygons representing borders of the Zion National Park.

srtm <- raster(system.file("raster/srtm.tif", package = "spDataLarge"))
zion <- read_sf(system.file("vector/zion.gpkg", package = "spDataLarge"))

# Additionally, the last exercise (IV) will used the masked version of the `lc_data` dataset.

study_area <- read_sf("data/study_area.gpkg")
lc_data <- raster("data/example_landscape.tif")
lc_data_masked <- mask(crop(lc_data, study_area), study_area)

#### Exercise I ####

# 1. Display the `zion` object and view its structure.

# What can you say about the content of this file?
# What type of data does it store? 
# What is the coordinate system used?
# How many attributes does it contain?
# What is its geometry?

# 2. Display the `srtm` object and view its structure.
# What can you say about the content of this file? 
# What type of data does it store?
# What is the coordinate system used? 
# How many attributes does it contain?
# How many dimensions does it have? 
# What is the data resolution?

# Your solution (type answer to the questions as code comments and the code used)

# /Start Code/ #

##1. zion
#I use head() to view the 'zion' object
head(zion)
# The zion file contains information about the Zion National park. 
# It contains spatial information about the national park along with geometry and metadata.

# It stores polygon data
# I find the used coordinate system by using crs() as we are dealing with a raster
crs(zion)
# The coordinates are GRS80

##2. srtm
#I use head() to view the 'srtm' object
head(srtm)
# The file contains raster data for divided into rows and columns. The attributes are a list. 

# I find the used coordinate system by using crs() as we are dealing with a raster
crs(srtm)
# The coordinates are WGS84

# I use dim() to find the dimensions
dim(srtm)
# I get the information, 457, 465 and 1. 457 and 465 are the numbers of rows and columns.
# That is, 1 must be the dimension.

# I use res() to find the data resolution
res(srtm)
# 0.0008333333 0.0008333333


# /End Code/ #

#### Exercise II ####

# 1. Reproject the `srtm` dataset into the coordinate reference system used in the `zion` object. 
# Create a new object `srtm2`
# Vizualize the results using the `plot()` function.

# 2. Reproject the `zion` dataset into the coordinate reference system used in the `srtm` object.
# Create a new object `zion2`
# Vizualize the results using the `plot()` function.


# Your solution

# /Start Code/ #

# 1.
# Check the CRS
crs(zion)
crs(srtm)

# Assign the CRS from zion to srtm
crs_zion <- "+proj=utm +zone=12 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
srtm2 <- srtm
crs(srtm2) <- crs_zion 

# Check the CRS again
crs(zion)
crs(srtm)
crs(srtm2)

# plot the data
plot(srtm)
plot(zion, max.plot = 11) #make sure all 11 attributes are used
plot(srtm2)

# 2.
# Assign the CRS from srtm to zion
crs_srtm <- "+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0"
zion2 <- st_transform(zion, crs = crs_srtm)

# Check the CRS again
crs(srtm)
crs(zion)
crs(zion2)

# plot the data
plot(srtm)
plot(zion, max.plot = 11) #make sure all 11 attributes are used
plot(zion2, max.plot = 11) #make sure all 11 attributes are used

# /End Code/ #


