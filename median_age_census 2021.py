# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 2022
Calculating median age for England and Wales census small areas 2021
Python3 script
@author: Gaynor Astbury
"""

import numpy as np
import pandas as pd
import geopandas as gpd
import plotly.express as px
import numpy
#from urllib.request import urlopen
 
age_df = pd.read_csv('TS007_age_by_single_year_2022.csv', index_col='mnemonic')  # Raw data download: Census 2021 table 'TS007 - Age by Single Year' from source: https://www.nomisweb.co.uk/ at Nov 2022
del age_df['Total']
del age_df['2021 super output area - middle layer']
age_df.rename(columns = {'Aged under 1 year':0, 'Aged 1 year':1, 'Aged 2 years':2, 'Aged 3 years':3, 'Aged 4 years':4, 'Aged 5 years':5, 'Aged 6 years':6, 'Aged 7 years':7, 'Aged 8 years':8, 'Aged 9 years':9, 'Aged 10 years':10, 'Aged 11 years':11, 'Aged 12 years':12, 'Aged 13 years':13, 'Aged 14 years':14, 'Aged 15 years':15, 'Aged 16 years':16, 'Aged 17 years':17, 'Aged 18 years':18, 'Aged 19 years':19, 'Aged 20 years':20, 'Aged 21 years':21, 'Aged 22 years':22, 'Aged 23 years':23, 'Aged 24 years':24, 'Aged 25 years':25, 'Aged 26 years':26, 'Aged 27 years':27, 'Aged 28 years':28, 'Aged 29 years':29, 'Aged 30 years':30, 'Aged 31 years':31, 'Aged 32 years':32, 'Aged 33 years':33, 'Aged 34 years':34, 'Aged 35 years':35, 'Aged 36 years':36, 'Aged 37 years':37, 'Aged 38 years':38, 'Aged 39 years':39, 'Aged 40 years':40, 'Aged 41 years':41, 'Aged 42 years':42, 'Aged 43 years':43, 'Aged 44 years':44, 'Aged 45 years':45, 'Aged 46 years':46, 'Aged 47 years':47, 'Aged 48 years':48, 'Aged 49 years':49, 'Aged 50 years':50, 'Aged 51 years':51, 'Aged 52 years':52, 'Aged 53 years':53, 'Aged 54 years':54, 'Aged 55 years':55, 'Aged 56 years':56, 'Aged 57 years':57, 'Aged 58 years':58, 'Aged 59 years':59, 'Aged 60 years':60, 'Aged 61 years':61, 'Aged 62 years':62, 'Aged 63 years':63, 'Aged 64 years':64, 'Aged 65 years':65, 'Aged 66 years':66, 'Aged 67 years':67, 'Aged 68 years':68, 'Aged 69 years':69, 'Aged 70 years':70, 'Aged 71 years':71, 'Aged 72 years':72, 'Aged 73 years':73, 'Aged 74 years':74, 'Aged 75 years':75, 'Aged 76 years':76, 'Aged 77 years':77, 'Aged 78 years':78, 'Aged 79 years':79, 'Aged 80 years':80, 'Aged 81 years':81, 'Aged 82 years':82, 'Aged 83 years':83, 'Aged 84 years':84, 'Aged 85 years':85, 'Aged 86 years':86, 'Aged 87 years':87, 'Aged 88 years':88, 'Aged 89 years':89, 'Aged 90 years':90, 'Aged 91 years':91, 'Aged 92 years':92, 'Aged 93 years':93, 'Aged 94 years':94, 'Aged 95 years':95, 'Aged 96 years':96, 'Aged 97 years':97, 'Aged 98 years':98, 'Aged 99 years':99, 'Aged 100 years and over':100}, inplace = True)


# calculate median for freq table contained in the above dataframe
m = list() # median list
for index, row in age_df.iterrows():
    v = list() # value list
    z = zip(row.index, row.values)
    for item in z:
        for f in range(item[1]):
            v.append(item[0])
    m.append(np.median(v))
df_m = pd.DataFrame({'mnemonic': age_df.index, 'Medianage': m})
df_m.rename(columns = {'mnemonic':'MSOA21CD'}, inplace = True)
#print(df_m)
df_m.to_csv('ew_msoa_median_age_2021.csv', index=False)

# CREATE A SPATIAL VECTOR FILE FOR MAPPING
#import MSOA boundaries into geodataframe
msoa_2021_boundaries = gpd.read_file('Middle_layer_Super_Output_Areas_December_2021_Boundaries_EW_BGC_V3.gpkg') #data source: https://geoportal.statistics.gov.uk/datasets/ons::msoa-dec-2021-boundaries-generalised-clipped-ew-bgc/explore?location=52.808224%2C-2.489483%2C7.76
#join median age results
spatial_join = msoa_2021_boundaries.merge(df_m, on='MSOA21CD')
#export to gjson
spatial_join.to_file('ew_msoa_median_age_2021.gpkg')

# OR JUST PLOT A MAP IN A BROWSER USING PLOTLY

'''
# Alternatively load the spatial vector data from the ONS API - this currently has a record limit on the return request so best to download and save the flat file
with urlopen('https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Middle_layer_Super_Output_Areas_December_2021_Boundaries_EW_BGC_V3/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson') as response:
    gdf = json.load(response)
'''

spatial_join = spatial_join.to_crs(4326) # plotly needs data input in geographic coordinates: convert the ONS data from EPSG 27700

# for a point map using centroids:
'''
gdf['lon'] = numpy.nan # create new fields with coordinates rather than the geometry field for the plotly scatter_geo method
gdf['lat'] = numpy.nan
gdf['lon'] = gdf.centroid.x  
gdf['lat'] = gdf.centroid.y

# then run scatter_geo on df fields
fig_map = px.scatter_geo(gdf,
                         lat=gdf['lat'],
                         lon=gdf['lon'],
                         hover_name='Medianage',
                         center=dict(lat=53.059293, lon=-1.693406), #sets the centre point of the map
                         fitbounds='locations',
                         color='Medianage'
                         )

fig_map.update_geos(resolution=50) # to retrieve larger-scale country outline from the Natural Earth server
fig_map.update_layout(title = 'Median age by MSOA 2021')
fig_map.write_html('age_2021_scatter.html')
'''

# or run a chropleth map - pass df and gdf geojson as seperate and join field then the join is done on the fly

fig = px.choropleth_mapbox(df_m, geojson=spatial_join, 
                           locations='MSOA21CD', # codes in dataframe to match to 'featureidkey' in gdf
                           featureidkey="properties.MSOA21CD", # codes in geodataframe to match to 'locations' in df                
                           color='Medianage', # column for attribute values to colour by
                           title='Median age by MSOA, Census 2021 England and Wales',
                           color_continuous_scale="Viridis",
                           mapbox_style="carto-positron",
                           range_color=(df_m['Medianage'].min(),df_m['Medianage'].max()),
                           center=dict(lat=53.059293, lon=-1.693406), #sets the centre point of the map  
                           opacity=0.8,
                           zoom=5.2,
                           labels={'Medianage':'Median Age 2021 in MSOA', }
                           )
fig.update_layout(margin={"r":0,"t":25,"l":0,"b":0})

fig.write_html('median_age_2021_choropleth.html')
