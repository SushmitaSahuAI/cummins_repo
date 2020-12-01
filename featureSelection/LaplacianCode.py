# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 09:55:00 2018

@author: SAimCognitiveSP
"""

import numpy as np
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale
from scipy import stats
import getGowarDistance as ggd
import itertools
import time,math

def pca_summary(pca, standardised_data):
    names = ["PC"+str(i) for i in range(1, len(pca.explained_variance_ratio_)+1)]
    a = list(np.std(pca.transform(standardised_data), axis=0))
    b = list(pca.explained_variance_ratio_)
    c = [np.sum(pca.explained_variance_ratio_[:i]) for i in range(1, len(pca.explained_variance_ratio_)+1)]
    columns = pd.MultiIndex.from_tuples([("sdev", "Standard deviation"), ("varprop", "Proportion of Variance"), ("cumprop", "Cumulative Proportion")])
    summary = pd.DataFrame(list(zip(a, b, c)), index=names, columns=columns)
    return summary

# ***** Code for LapScore of R
def LapScore(data,t,k,nf):
    one= [1]*len(data)
    print (len(data))
    s=[]
    lr =[]
    dataFrame_index = 0
    for key,value in data.iteritems():
    #fr = data[data.columns[0]]
        fr= value
        b = np.reshape(fr,(len(data),1))
    
        dm = ggd.gower_distances(b)
        
        
        for i in range(0,len(dm)):
            
            z= np.argwhere(np.argsort(dm[i])<k)
            z = z.tolist()
            z = list(itertools.chain(*z))
            # print(z)
            temp = [0]*len(dm)
            for j in z:
                temp[j]= np.exp(-dm[i][j]/t)
            #print(temp)
            s.append(temp)
            
        s_mat = np.matrix(s)
        s1 = np.matmul(s_mat, one)
        diag_s1 = np.diag(s1.A1)
        l = diag_s1 -s_mat
        
        
        imd = np.matmul((np.matmul(fr,diag_s1)),one)/np.matmul((np.matmul(one,diag_s1)),one) # imd<-(t(fr)%*%d%*%one)/(t(one)%*%d%*%one)
        one = np.array(one)
        frbar =fr - imd*one
        
        
        #lr[dataFrame_index] = np.matmul((np.matmul(frbar,l)),frbar)/np.matmul((np.matmul(frbar,diag_s1)),frbar) #lllll = (t(frbar)%*%l%*%frbar)/(t(frbar)%*%d%*%frbar)
        #print (((np.matmul((np.matmul(frbar,l)),frbar)/np.matmul((np.matmul(frbar,diag_s1)),frbar)))[0,0])
        lr.append(((np.matmul((np.matmul(frbar,l)),frbar)/np.matmul((np.matmul(frbar,diag_s1)),frbar)))[0,0])
        
        #dataFrame_index = dataFrame_index +1
        s = []
    print ("lr >>" , lr)
    z2 = np.argwhere(np.argsort(lr)<nf)
    ls_z2 = z2
    ls_flr = lr
    return ls_z2, ls_flr


def runLaplace(fName):
    start = time.time()
    #Load data set
    
    data = pd.read_csv(fName,encoding = "ISO-8859-1")
    #convert it to numpy arrays
    #data = data[["ITEM_KEY","Line.Net.Sales...Local","Line.Net.Sales","map_transactional","line_total_cost_functional","line_total_cost_corp","Line.Prime.Cost...Local","Line.Prime.Cost","Line.Gross.Sales...Local","Line.Gross.Sales","Line.Total.Discount...Local","Line.Total.Discount","dsn","CUSTOMER_KEY","invoice_number","ORDER_NUMBER","ORDER_TYPE_ID","Serial_Number","Operational_Revenue","Operational_Revenue_Corp","Operational_Prime_Cost","Operational_Prime_Cost_corp","Operational_standard_cost","Operational_standard_cost_Corp","BMS.Project.Number","Item.Number","Item.Description","User.Item.Type","BRAND_FRANCHISE_PRODUCT","ECC","Print.Part.Number","Long.Part.Number","PVC.Code","ECC.Code.Major","ECC.Code.Minor","SPC.Code.Major","VENDOR_ITEM.","PRICE_GROUP","CUSTOMER_NAME","CUSTOMER_NUMBER","CUSTOMER_TYPE","POSTAL_CODE","STATE"]]
    data = data[0:100]
    X=data[0:100].values
    
    #Scaling the values
    X = scale(X)
    
    pca = PCA().fit(X)
    
    
        
    #The amount of variance that each PC explains
    var= pca.explained_variance_ratio_
    X1=pca.fit_transform(X)
    #
    ##Cumulative Variance explains
    #var1=np.cumsum(np.round(pca.explained_variance_ratio_, decimals=4)*100)
    summary = pca_summary(pca, X)
    xev = summary["sdev"]**2
    xev.reset_index(drop=True, inplace=True)
    xev = xev/xev.sum()
    xev_list =  xev['Standard deviation'].tolist()
    pc,sumValue = 1,0
    thresh = 0.9
    for i,r in enumerate(xev_list):
        sumValue = sumValue + r
        if(sumValue>thresh):
            pc = i+1
            break
        
    print ("pc >> ", pc)
    X1_pc = X1[:, [i for i in range(0,pc)]]
    #corpc = stats.pearsonr(X, X1_pc)
    corpc = np.corrcoef(X, X1_pc, rowvar=False)
    
    n1= range(11,len(corpc))
    n2=range (0,pc)
    b = corpc[:,n1]
    c= b[n2,:]
    
    n1= range((len(corpc)-pc),len(corpc))
    n2 = range(0,len(X[0]))
    b = corpc[:,n1]
    final_corpc= b[n2,:]
    abscorpc = np.absolute(final_corpc)
    evpc = xev_list[0:pc]
    mat_mul = np.matmul(abscorpc, evpc)
    
    ls_z2, ls_flr = LapScore(data,0.5,5,pc);
    
    import itertools
    selected_Columns = list(itertools.chain(*(ls_z2.tolist())))
    print ("Columns after Laplacian: ", selected_Columns)
    newData = data.iloc[:,selected_Columns]
    outputFileName = fName.split(".")[0] + "_featureSelected.csv"
    newData.to_csv(outputFileName,index = False)
    end = time.time()
    print("!!! Execution Time : ", round((end - start),3), "sec")
    
fileName = "Dataextract2_Updated.csv"
runLaplace(fileName)

        
            
