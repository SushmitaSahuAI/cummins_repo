require(cluster)
LapScore<-function (data,t,k,nf)
{
  on<-rep(1,nrow(data))
  one<-t(t(on))
  lr<-c()
  s<-c()
  ls<-c()
  for(i in 1 :ncol(data))
  {
    fr<-data[i]
    dm<-as.matrix(daisy(fr, metric = "euclidean",stand = TRUE))
    for (j in 1:ncol(dm))
    {
      col<-dm[j,]
      z<-which(order(col)<=k)
      temp<-rep(0,ncol(dm))
      temp[z]<-exp(1)^(-col[z]/t)
      s<-rbind(s,temp)
    }
    s1<-s%*%one
    s1<-as.vector(s1)
    d<-diag(s1)
    l<-d - s
    imd<-(t(fr)%*%d%*%one)/(t(one)%*%d%*%one)
    imd<-c(imd)
    frbar<-fr - imd*as.matrix(one)
    frbar<-as.matrix(frbar)
    lr[i]<-(t(frbar)%*%l%*%frbar)/(t(frbar)%*%d%*%frbar)
    s<-c()
  }
  z<-which(order(lr)<=nf)
  ls$lr<-lr[z]
  ls$z<-z
  ls$flr<-lr
  ls
}

fselect<-function(data,thresh)
{
  # Initialization
  fscore<-c()
  # Normalization of data and then applying PCA 
  x<-scale(data)
  xpca<-prcomp(x)
  #  Find the no. of components based on % of variance explained
  xev<-xpca$sdev^2
  xevm<-as.matrix(xev)
  xevm<-xevm/sum(xevm[,1])
  pc<-1
  sum<-0
  for (i in 1:nrow(xevm))
  {
    print(i)
    sum<-sum + xevm[i,]
 
    if(sum>thresh)
    {
      pc<-i

      break
    }
  }
  #  Select features and score them on correlation with the main principal components
  corpc<-cor(x,xpca$x[,1:pc])
  abscorpc<-abs(corpc)
  evpc<-as.matrix(xevm[1:pc,])
  fscore$x<-abscorpc %*% evpc
  fscore$pc<-pc
  return(fscore)
}

purity <- function(data,nc,nvr)
{
  purity<- c()
  sumpure<-0
  #removing the class
  datac<-data[-nvr]
  datac<-scale(datac)
  #performing K means on the data
  
  for ( l in 1 : 100)
  {
  x1<-sample(1:10000,1)
  
  set.seed(x1)
  kmdata<-kmeans(datac,nc,iter.max = 25, nstart = 10)
  # comparing the class and the cluster information
  
  pure<-as.matrix(table(kmdata$cluster,t(data[nvr])))
  
  
  # Looping to find out maximum of each class
  
  for(i in 1 : ncol(pure))
  {
  sumpure<-sumpure+max(pure[i,])
  
  }
  
  purity<-c(purity,sumpure/nrow(data))
  sumpure<-0
  }
  return(mean(purity))

}

# getSWunique <- function(subsetdata, maxclus)
# {
#   x <- as.data.frame(subsetdata)
# 
#   id <- as.integer(x[1,1])
#   people <- length(as.vector(x[,1]))
#   
#   if (people == 1){
#     p = 0
#   } 
#   else {
#     diss <- daisy(x, metric="gower")
#     asw <- numeric(maxclus)
# 
#     for (k in 2:maxclus) {
#       asw[[k]] <- pam(diss, k, diss=T)$silinfo$avg.width
#     }
#     k.best <- which.max(asw)
#     swg <- asw[k.best]
#   }  
#   swg  
# }

runLaplacian <- function(data)
{
  class <- data[ncol(data)]
  data <- data[-ncol(data)]
  print(class)
  print("*****")
  
  fs<-fselect(data,.9)
  print (fs)
 # *** commented by Sushmita for testing
  # k<-LapScore(data,0.5,5,fs$pc)
  # print("Laplacian : ")
  # print(length(k$z))
  # print(k$z)
  # data2<-cbind(data[k$z],class)
  
  #l<-purity(data2,length(table(class)),ncol(data2))
  
  #maxclus <- nrow(unique(class))
  #l <- getSWunique(data2[-ncol(data2)], maxclus)  

  #return(l)
}
fileName = "C:/Users/565637/Desktop/Cummins/sampleData/Data1/Dataextract2_Updated.csv"
print (fileName)
mydata <- read.csv(fileName, header = T, stringsAsFactors = T)
mydata <- mydata[0:100,c("ITEM_KEY","Line.Net.Sales...Local","Line.Net.Sales","map_transactional","line_total_cost_functional","line_total_cost_corp","Line.Prime.Cost...Local","Line.Prime.Cost","Line.Gross.Sales...Local","Line.Gross.Sales","Line.Total.Discount...Local","Line.Total.Discount","dsn","CUSTOMER_KEY","invoice_number","ORDER_NUMBER","ORDER_TYPE_ID","Serial_Number","Operational_Revenue","Operational_Revenue_Corp","Operational_Prime_Cost","Operational_Prime_Cost_corp","Operational_standard_cost","Operational_standard_cost_Corp","BMS.Project.Number","Item.Number","Item.Description","User.Item.Type","BRAND_FRANCHISE_PRODUCT","ECC","Print.Part.Number","Long.Part.Number","PVC.Code","ECC.Code.Major","ECC.Code.Minor","SPC.Code.Major","VENDOR_ITEM.","PRICE_GROUP","CUSTOMER_NAME","CUSTOMER_NUMBER","CUSTOMER_TYPE","POSTAL_CODE","STATE")]
#fs<-fselect(data,.9)

runLaplacian(mydata)
