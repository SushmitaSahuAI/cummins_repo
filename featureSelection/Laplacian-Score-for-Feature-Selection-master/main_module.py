from lp_score import *
import argparse as aP
import numpy as np
import time
import pandas as pd


if __name__=='__main__':
    start_time=time.time()
    input_str=input("Enter file path for input file: ");
    fileName =input_str 
    X = pd.read_csv(fileName,encoding = "ISO-8859-1")
    print ("X.shape >>",X.shape)
    n_samples,n_feature=X.shape
    data=X[0:10000]
    print ("!!!! data.shape >>",data.shape)
    L=LaplacianScore(data,neighbour_size=16,t_param=2)
    print ("L : ", L)
    print ("feature_ranking(L) >> ",feature_ranking(L))
    print ("len feature_ranking(L) >> ",len(feature_ranking(L)))
    print("--- %s seconds ---" % (time.time() - start_time))

