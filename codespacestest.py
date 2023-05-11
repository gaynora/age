# -*- coding: utf-8 -*-
"""
python 3 script
"""

import pandas
import geopandas
import geoplot
import mapclassify

#create dataframe with coordinates
points = {
  "coordinates": [[291427,92458],[291441,92504],[291531,92442],[291487,92375],[291582,92420],[291433,92406],[291494,92533],[291483,92473],[291460,92554]],
  "value":[5,5,1,0,7,2,3,8,9]
}
df = pandas.DataFrame(points)

# create geodataframe from dataframe
gdf = geopandas.GeoDataFrame(df, crs="EPSG:267700")

#plot points using geoplot, mapclassify
geoplot.pointplot(points)
