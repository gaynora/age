# -*- coding: utf-8 -*-
"""
Created on Sat Dec  21 2022
Calculating median age for UK census output areas / small areas 2011
Python3 script
@author: Gaynor Astbury
"""

import numpy as np
import pandas as pd
import geopandas as gpd
 
# Raw data download: Census 2011 table QS103UK Age By Single Year https://www.nomisweb.co.uk/ download record limits are in place, so individual tables by country and region are downloaded and appended here
ni_df = pd.read_csv('ni_sa_qs103UK_age_by_single_year_2011.csv', header = 5, skiprows = [6], skipfooter = 7, index_col='mnemonic') 
ee_em_df = pd.read_csv('oa_ee_em_qs103UK_age_by_single_year_2011.csv', header = 5, skiprows = [6], skipfooter = 7, index_col='mnemonic')
lon_df = pd.read_csv('oa_lon_qs103UK_age_by_single_year_2011.csv', header = 5, skiprows = [6], skipfooter = 7, index_col='mnemonic')                  
ne_nw_df = pd.read_csv('oa_ne_nw_qs103UK_age_by_single_year_2011.csv', header = 5, skiprows = [6], skipfooter = 7, index_col='mnemonic')                    
scot_df = pd.read_csv('oa_scot_qs103UK_age_by_single_year_2011.csv', header = 5, skiprows = [6], skipfooter = 7, index_col='mnemonic')
se_sw_df = pd.read_csv('oa_se_sw_qs103UK_age_by_single_year_2011.csv', header = 5, skiprows = [6], skipfooter = 7, index_col='mnemonic')                       
wales_df = pd.read_csv('oa_wales_qs103UK_age_by_single_year_2011.csv', header = 5, skiprows = [6], skipfooter = 7, index_col='mnemonic')
wm_yh_df = pd.read_csv('oa_wm_yh_qs103UK_age_by_single_year_2011.csv', header = 5, skiprows = [6], skipfooter = 7, index_col='mnemonic')                      
age_df = pd.concat([ni_df, ee_em_df, lon_df, ne_nw_df, scot_df, se_sw_df, wales_df, wm_yh_df], axis=0)                   
       
del age_df['All categories: Age']
del age_df['2011 NI small area']
del age_df['2011 output area']
age_df.rename(columns = {'Age under 1':0, 'Age 1':1, 'Age 2':2, 'Age 3':3, 'Age 4':4, 'Age 5':5, 'Age 6':6, 'Age 7':7, 'Age 8':8, 'Age 9':9, 'Age 10':10, 'Age 11':11, 'Age 12':12, 'Age 13':13, 'Age 14':14, 'Age 15':15, 'Age 16':16, 'Age 17':17, 'Age 18':18, 'Age 19':19, 'Age 20':20, 'Age 21':21, 'Age 22':22, 'Age 23':23, 'Age 24':24, 'Age 25':25, 'Age 26':26, 'Age 27':27, 'Age 28':28, 'Age 29':29, 'Age 30':30, 'Age 31':31, 'Age 32':32, 'Age 33':33, 'Age 34':34, 'Age 35':35, 'Age 36':36, 'Age 37':37, 'Age 38':38, 'Age 39':39, 'Age 40':40, 'Age 41':41, 'Age 42':42, 'Age 43':43, 'Age 44':44, 'Age 45':45, 'Age 46':46, 'Age 47':47, 'Age 48':48, 'Age 49':49, 'Age 50':50, 'Age 51':51, 'Age 52':52, 'Age 53':53, 'Age 54':54, 'Age 55':55, 'Age 56':56, 'Age 57':57, 'Age 58':58, 'Age 59':59, 'Age 60':60, 'Age 61':61, 'Age 62':62, 'Age 63':63, 'Age 64':64, 'Age 65':65, 'Age 66':66, 'Age 67':67, 'Age 68':68, 'Age 69':69, 'Age 70':70, 'Age 71':71, 'Age 72':72, 'Age 73':73, 'Age 74':74, 'Age 75':75, 'Age 76':76, 'Age 77':77, 'Age 78':78, 'Age 79':79, 'Age 80':80, 'Age 81':81, 'Age 82':82, 'Age 83':83, 'Age 84':84, 'Age 85':85, 'Age 86':86, 'Age 87':87, 'Age 88':88, 'Age 89':89, 'Age 90':90, 'Age 91':91, 'Age 92':92, 'Age 93':93, 'Age 94':94, 'Age 95':95, 'Age 96':96, 'Age 97':97, 'Age 98':98, 'Age 99':99, 'Age 100 and over':100}, inplace = True)
age_df[[0,1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84,85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]].astype(np.float).astype("Int32")


# calculate median for freq table contained in the above dataframe (age_df)
m = list() # median list
for index, row in age_df.iterrows():
    v = list() # value list
    z = zip(row.index, row.values)
    for item in z:
        for f in range(item[1]):
            v.append(item[0])
    m.append(np.median(v))
df_m = pd.DataFrame({'mnemonic': age_df.index, 'Medianage': m})
df_m.rename(columns = {'mnemonic':'geo_code'}, inplace = True)
#export tabular results to csv
df_m.to_csv('uk_oasa_median_age_2011.csv', index=False)

#import Output Area Classification (OAC) data
oac_2011 = pd.read_csv('2011 OAC Clusters and Names csv v2.csv') # Data source: https://www.ons.gov.uk/methodology/geography/geographicalproducts/areaclassifications/2011areaclassifications/datasets
oac_2011.rename(columns = {'Output Area Code':'geo_code'}, inplace = True)

#import relevant geography files
oa_2011_boundaries = gpd.read_file('infuse_oa_lyr_2011.shp') #data source:  InFuse Output Areas and Small Areas, 2011 from https://borders.ukdataservice.ac.uk/
oa_ew_2011_centroids = gpd.read_file('Output_Areas_(Dec_2011)_PWC.geojson') #Data source:  https://geoportal.statistics.gov.uk/datasets/ons::output-areas-dec-2011-pwc/about
oa_scot_2011_centroids = gpd.read_file('OutputArea2011_PWC.shp') #Data source: https://www.nrscotland.gov.uk/statistics-and-data/geography/our-products/census-datasets/2011-census/2011-boundaries
# NI did not produce population-weighted centroids, but the polygon file contains coordinates for the geographic centroid of each area - create point geodataframe using the coords from the NI polygon attribute table (in geodataframe above)
sa_ni_2011 = gpd.read_file('SA2011.shp') #Data source: https://www.nisra.gov.uk/support/geography/northern-ireland-small-areas
sa_ni_2011_centroids = gpd.GeoDataFrame(sa_ni_2011, geometry=gpd.points_from_xy(sa_ni_2011.X_COORD,sa_ni_2011.Y_COORD)) 
sa_ni_2011_centroids = sa_ni_2011_centroids.set_crs(29902, allow_override=True)
#rename code fields to 'geo_code' in each geodataframes to align 
oa_ew_2011_centroids.rename(columns = {'OA11CD':'geo_code'}, inplace = True)
oa_scot_2011_centroids.rename(columns = {'code':'geo_code'}, inplace = True)
sa_ni_2011_centroids.rename(columns = {'SA2011':'geo_code'}, inplace = True)
#reproject into wgs84 so all gdf share same coordinate reference system
oa_scot_2011_centroids_wgs84  = oa_scot_2011_centroids.to_crs({'init': 'epsg:4326'})
sa_ni_2011_centroids_wgs84  = sa_ni_2011_centroids.to_crs({'init': 'epsg:4326'})
#append centroids geodataframes into one
append_gdf = pd.concat([oa_ew_2011_centroids, oa_scot_2011_centroids_wgs84, sa_ni_2011_centroids_wgs84])

#join median age and OAC results and export to file
spatial_join = oa_2011_boundaries.merge(df_m, on='geo_code')
spatial_join2 = append_gdf.merge(df_m, on='geo_code')
spatial_join3 = oa_2011_boundaries.merge(oac_2011, on='geo_code')
spatial_join4 = append_gdf.merge(oac_2011, on='geo_code')
spatial_join3.to_file("uk_oasa_median_age_2011_.shp")
spatial_join4.to_file("uk_oasa_median_age_2011.shp")
