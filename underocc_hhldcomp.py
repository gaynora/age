# -*- coding: utf-8 -*-
"""
Calculating 2021 small area bedroom occupation averages against age-related household composition
and visualising the results spatially
"""

import pandas
import geopandas
import numpy
import geoplot
import geoplot.crs as gcrs
import mapclassify

#import raw data with new column names to convert the occupancy rating into a continuous variable ; Census 2021 table RM098 - Occupancy rating (bedrooms) by household composition in England and Wales by Output Areas
allhhlds_df = pandas.read_csv('rm098_nomis_allhhlds.csv', usecols=[1, 2, 3, 4, 5], names=['mnemonic', 2, 1, 0, -1], header = None, index_col='mnemonic', skiprows = [0,1,2,3,4,5,6,7,8,9]) # Data source: https://www.nomisweb.co.uk/
oneper_66plus_df = pandas.read_csv('rm098_1pershhld_66over.csv', usecols=[1, 2, 3, 4, 5], names=['mnemonic', 'a2', 'a1', 'a0', 'a-1'], header = None, index_col='mnemonic', skiprows = [0,1,2,3,4,5,6,7,8,9]) # Data source: https://www.nomisweb.co.uk/
singlefam_66over_df = pandas.read_csv('rm098_singlefamhhld_66over.csv', usecols=[1, 2, 3, 4, 5], names=['mnemonic', 'b2', 'b1', 'b0', 'b-1'], header = None, index_col='mnemonic', skiprows = [0,1,2,3,4,5,6,7,8,9]) # Data source: https://www.nomisweb.co.uk/
oas_gdf = geopandas.read_file('Output_Areas_Dec_2021_Boundaries_Generalised_Clipped_EW_BGC_2022.gpkg') # Data source: https://geoportal.statistics.gov.uk/datasets/ons::output-areas-dec-2021-boundaries-generalised-clipped-ew-bgc/explore?location=52.800500%2C-2.489483%2C7.76


#rejig census file
#join over 66 dataframes into one and delete old columns
joined = pandas.concat([oneper_66plus_df, singlefam_66over_df], axis=1, join="inner")
joined['sum2'] = joined['a2'] + joined['b2']
joined['sum1'] = joined['a1'] + joined['b1']
joined['sum0'] = joined['a0'] + joined['b0']
joined['sum-1'] = joined['a-1'] + joined['b-1']
joined.rename(columns = {'sum2':2, 'sum1':1, 'sum0':0, 'sum-1':-1}, inplace = True)
joined.drop(['a2', 'a0', 'a1', 'a-1', 'b2', 'b1', 'b0', 'b-1'], inplace=True, axis=1)
print(joined)

#calculate median occupancy rating for all households
def calcmedian(x_df):
  x_df[[2,1,0,-1]].astype(numpy.float).astype("Int32")

  m = list() # median list
  for index, row in x_df.iterrows():
      v = list() # value list
      z = zip(row.index, row.values)
      for item in z:
          for f in range(item[1]):
              v.append(item[0])
      m.append(numpy.median(v))
  x_df_m = pandas.DataFrame({'mnemonic': x_df.index, 'Medianocc': m})
  return(x_df_m)

medianallh = calcmedian(allhhlds_df)
medianoldh = calcmedian(joined)
medianoldh.rename(columns = {'Medianocc':'Medoccold'}, inplace = True)
medianallh.rename(columns = {'Medianocc':'Medoccall'}, inplace = True)

# join table to polyons
oas_gdf.rename(columns = {'OA21CD':'mnemonic'}, inplace = True)
spatial_join = oas_gdf.merge(medianallh, on='mnemonic')
spatial_join2 = spatial_join.merge(medianoldh, on='mnemonic')


# map visualisations with geoplot
scheme = mapclassify.UserDefined(spatial_join2['Medoccall'], bins=[-1, 0, 1, 2])
mapall = geoplot.choropleth(spatial_join2, projection=gcrs.OSGB(), hue='Medoccall', scheme=scheme, cmap='Greens', legend=True)
scheme = mapclassify.UserDefined(spatial_join2['Medoccold'], bins=[-1, 0, 1, 2])
mapall = geoplot.choropleth(spatial_join2, projection=gcrs.OSGB(), hue='Medoccold', scheme=scheme, cmap='Greens', legend=True)

spatial_join2.to_csv('result.csv')
spatial_join2.to_file('result.gpkg', driver='GPKG') # to export the spatial vector file if needed
