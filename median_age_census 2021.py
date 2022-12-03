# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 2022
Calculating median age for England and Wales census small areas 2021
Python3 script
@author: Gaynor Astbury
"""

import numpy as np
import pandas as pd
 
age_df = pd.read_csv('TS007_age_by_single_year_2022.csv', header = 5, skiprows = [6], skipfooter = 7, index_col='mnemonic')  # Raw data download: Census 2021 table 'TS007 - Age by Single Year' from source: https://www.nomisweb.co.uk/ at Nov 2022
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
print(df_m)