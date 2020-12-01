# -*- coding: utf-8 -*-
import pandas as pd
import os
from sksos import SOS

input_str=input("Enter file path for input file: ");
xpath=input_str #r'C:\Users\thath\Downloads\Anomaly Data Sets\Data Set Laplacian\mdlon.csv'
#xpath = "C:/Users/565637/Desktop/Cummins/irisdata.csv"
iris = pd.read_csv(xpath)
numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
df_Numeric = iris.select_dtypes(include=numerics)

X = df_Numeric.values


#X = iris.drop("class", axis=1).values
#X = iris.drop("Name", axis=1).values
detector = SOS()
print (type(X))
iris["score"] = detector.predict(X)
y=iris.sort_values("score", ascending=False)#.head(200)
###print (y)


#newpath = r'C:\SOS_Prediction' 
#if not os.path.exists(newpath):
#  os.makedirs(newpath)  
  
writer = pd.ExcelWriter('./SOS_PRDCTN_output_file_K-MedoidSampled_24Oct.xlsx')


 #writer = pd.ExcelWriter(r'C:\PurushTemp\output1.xlsx')
y.to_excel(writer,'Sheet1')
writer.save()

print("!!! Output file is created in the path: SOS_PRDCTN_output_file_K-MedoidSampled_24Oct.xlsx");
print("Prediction score is added to the last column of the input file and saved in the above output file");

