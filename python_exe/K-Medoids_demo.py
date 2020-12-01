# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 11:06:26 2018

@author: 565637
"""

import pandas as pd
from pyclustering.cluster import kmedoids
#from pyclustering.cluster.kmedoids import kmedoids;
import time
import math

import pickle

start = time.time()

fileName = "/home/ubuntu/cummins/sampleData/Dataextract2_Updated.csv"
data = pd.read_csv(fileName,encoding = "ISO-8859-1")

number_of_records = data.shape[0]
print (number_of_records) 

square_root = math.sqrt(number_of_records)
log = math.log(number_of_records,2)

  #log = log2(square_root)
  
total = square_root * log
n_clusters = int(total)
print ("# of clusters :",n_clusters )

import random
random.seed(8000)
start_medoids = random.sample(range(0, (number_of_records-1)), n_clusters)
pickle.dump(start_medoids, open('start_medoids.p', 'wb'))


cluster_algo = kmedoids.kmedoids(data.as_matrix(),start_medoids)

cluster_algo.process();
clusters = cluster_algo.get_clusters();

# Only 2 clusters were extracted in version without fix (now 3)
print("Number of clusters:", len(clusters));
end = time.time()

print ((cluster_algo.get_medoids()))
pickle.dump(cluster_algo.get_medoids(), open('medoids.p', 'wb'))
print("!!! Execution Time : ", round((end - start),3), "sec")

df2= data.ix[cluster_algo.get_medoids()]
outFileName = fileName.rsplit("/",1)[0]+"/"+fileName.split("/")[-1].split(".csv")[0]+ "_KMedoidSampled.csv"
print ("!! outFileName >>",outFileName)
df2.to_csv(outFileName)
print ("File written !!")
