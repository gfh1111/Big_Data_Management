from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import types as T
import sys

def step1(partId, rows):
    if partId==0:
       next(rows)
    import csv
    reader = csv.reader(rows)
    for row in reader:
        (year,product,company) = (row[0][0:4],row[1].lower(),row[7].lower())
        yield (year,product,company)

if __name__=="__main__":
    #sc = SparkContext()
    sc = pyspark.SparkContext.getOrCreate()
    spark = SparkSession.builder.getOrCreate()
    
    complains = sc.textFile(sys.argv[1], use_unicode=True).cache()  
    A = complains.mapPartitionsWithIndex(step1).saveAsTextFile(sys.argv[2])

#     #total number of complains
#     B = A.map(lambda x: ((x[1],x[0]),1))\
#          .reduceByKey(lambda x,y: x+y)

#     #total number of companies
#     C = A.map(lambda x: ((x[1],x[0],x[2]),1))\
#          .reduceByKey(lambda x,y: x+y)\
#          .map(lambda x: ((x[0][0],x[0][1]),1))\
#          .reduceByKey(lambda x,y: x+y)

#     #highest number of complains received by a company   
#     D = A.map(lambda x: ((x[1],x[0],x[2]),1))\
#          .reduceByKey(lambda x,y: x+y)\
#          .map(lambda x: ((x[0][0],x[0][1]),x[1]))\
#          .reduceByKey(lambda x,y: max(x,y))
#          .saveAsTextFile(sys.argv[2])
    
#     #expected output
#     E = B.join(C).join(D)\
#          .map(lambda x: (x[0],(x[1][0][0],x[1][0][1],x[1][1])))\
#          .map(lambda x: ((x[0][0],x[0][1]),(str(x[1][0]),str(x[1][1]),str(round(x[1][2]/x[1][0]*100)))))\
#          .sortByKey(ascending=True, numPartitions=None)\
#          .map(lambda x: x[0]+x[1])
 
#     E.map(lambda x: ','.join(str(item) for item in x))\
#      .saveAsTextFile(sys.argv[2])
