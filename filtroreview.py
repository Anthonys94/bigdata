#!/usr/bin/python

#Tale script serve per determinare il valore di opinione per le varie review.
#In particolare, sono prese in considerazione solo le review relative ad un business che ha un numero di review maggiore di 500.


from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
import pymongo
from pymongo import MongoClient
import pprint
import json
import csv


client=MongoClient('localhost',27017)
db=client.YelpDB
mostreviewed = db.business.find().sort({"review_count" : -1}).limit(3)
negozi=[]
for element in mostreviewed:
    negozi.append(element['business_id'])
print "--- Lettura delle review"
reviews1 = db.sintesireviewopt.find({"business_id" : negozi[0]})
reviews2 = db.sintesireviewopt.find({"business_id" : negozi[1]})
reviews3 = db.sintesireviewopt.find({"business_id" : negozi[2]})

review1 = []
subel1 = {}
for e in reviews1:
	subel1['business_id']=e['business_id]
	subel1['valore1']=e['valoreOP1']
	subel1['valore2']=e['valoreOP2']
	subel1['valore3']=e['valoreOP3']
	subel1['user_id']=e['user_id']
	subel1['vlutente']=e['vlutente']
	review1.append(subel)
	
review2 = []
subel2 = {}
for e in reviews2:
	subel2['business_id']=e['business_id]
	subel2['valore1']=e['valoreOP1']
	subel2['valore2']=e['valoreOP2']
	subel2['valore3']=e['valoreOP3']
	subel2['user_id']=e['user_id']
	subel2['vlutente']=e['vlutente']
	review2.append(subel)

review3 = []
subel3 = {}
for e in reviews3:
	subel3['business_id']=e['business_id]
	subel3['valore1']=e['valoreOP1']
	subel3['valore2']=e['valoreOP2']
	subel3['valore3']=e['valoreOP3']
	subel3['user_id']=e['user_id']
	subel3['vlutente']=e['vlutente']
	review3.append(subel)
	  
myFile1 = open('business1.csv', 'w')  
with myFile1:  
   writer = csv.writer(myFile1, delimiter=', ', quotechar='|', quoting=csv.QUOTE_MINIMAL))
   writer.writerows(review1)
	

client.close()