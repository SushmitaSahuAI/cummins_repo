library(imputeMissings)

file_location = "C:/Users/565637/Desktop/Cummins/Enocding-Decoding/"
file_lists = list.files(file_location,pattern = "*.csv",full.names = T)

data_summary <- function(input_dataset)
{
  df1 <- data.frame(character(),character(),integer(),integer(),numeric(),integer(),numeric(),integer(),numeric(),logical())
  
  for (name in colnames(input_dataset)) {
    
    df1 <- rbind(df1,data.frame(ColName=name,DataType=class(input_dataset[,name]),
                                TotalRecords=nrow(input_dataset),
                                UniqueCounts=length(unique(input_dataset[,name])),
                                UniquePercent=round(length(unique(input_dataset[,name]))/nrow(input_dataset)*100,2),
                                NACounts=sum(is.na(input_dataset[,name])),
                                NAPercent=round(sum(is.na(input_dataset[,name]))/nrow(input_dataset)*100,2) ))
    
  }
  
  return(df1)
}

# Iterating each file and normalize the same
for(file_name in file_lists)
{
  print(paste("Normalizing",file_name))
  
  #read data
  data <- read.csv(file_name, header = T, stringsAsFactors = T,na.strings = c("NA","na","NULL","null",""," "))
  #Remove the first column since it's an index column
  #data = data[,-1]
  #reducing the rows to 200 because of RAM restriction. If we have high RAM, then comment the below line
  data = data[6300:7044,]
  #append all the columns one more time to the dataframe
  final_data <- cbind(data,data)
  
  summary_output = data_summary(final_data)
  
  #Filter columns which are significant (each row contains unique value & 
  #                                      columns having more than 50% NA values &
  #                                      columns having only one value in rows)
  significant_columns = summary_output$ColName[summary_output$UniquePercent!=100 & 
                                                 summary_output$NAPercent<50 &
                                                 summary_output$UniqueCounts!=1]
  final_data <- final_data[,significant_columns]
  
  #Impute the missing value using mean/mode method
  Imputed_data = impute(final_data)
  
  #convert non-numeric columns into numeric (method of creating dummy variables)
  numeric_data = as.data.frame(sapply(Imputed_data,as.numeric))
  
  #write the revised input file which can feed into Laplacian functions
  write.csv(numeric_data,
            file=paste(sub(".csv","",file_name),"_Updated.csv",sep=""),
            row.names = FALSE)
  print("CSV written !!")
}
