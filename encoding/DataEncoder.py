# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 14:52:01 2018

@author: 565637
"""

import pandas as pd
import numpy as np

filepath = "C:/Users/565637/Desktop/Cummins/Enocding-Decoding/Dataextract2.csv"
data = pd.read_csv(filepath)

data = data[:800].fillna("")
#data = data[6300:7044]
print(type(""))
#print(data.dtypes)

#numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
#df_nonNumeric = data.select_dtypes(exclude=numerics)
#df_Numeric = data.select_dtypes(include=numerics)

#df_nonNumeric = df_nonNumeric.applymap(lambda x : int.from_bytes(x.encode('utf-8'), 'little'))