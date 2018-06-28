#!/usr/bin/python

import pymongo
from pymongo import MongoClient
import csv
from operator import itemgetter

client=MongoClient('localhost',27017)
db=client.YelpDB

negLasVegas = db.business.find({'city': "Las Vegas",'review_count' : {'$gte': 500 },'categories': {"$in": ["Bars"]}}).limit(20)
negozi=[]
for e in negLasVegas:
    negozi.append([e['business_id'],e['name'],e['latitude'],e['longitude']])
reviews =[]
for id in negozi:
	reviews.append(db.sintesireviewoptidea.find({"business_id" : id[0]}))

review =[]
i = 0
for cursore in reviews:
	reviewTemp = []
        for e in cursore:
		reviewTemp.append([e['business_id'],e['valoreOP2'],e['date'],negozi[i][2],negozi[i][3],negozi[i][1]])

	reviewTemp=sorted(reviewTemp, key=itemgetter(2))
	somma=0
	for t in reviewTemp:
		somma=(somma/2)+t[1]
		t.append(somma)
	review.append(reviewTemp[len(reviewTemp)-1])
	i=i+1
finale=[["business_id","valoreOP","date","latitude","longitude","name","cum"]]+review
myFile1 = open('bcGeo.csv', 'w')
with myFile1:
   writer = csv.writer(myFile1, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
   writer.writerows(finale)



client.close()
