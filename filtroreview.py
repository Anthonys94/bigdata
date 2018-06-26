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
subel = []
for e in reviews1:
	subel['business_id']=e['business_id]
	subel['valore1']=e['valoreOP1']
	subel['valore2']=e['valoreOP2']
	subel['valore3']=e['valoreOP3']
	review1.append(subel)
	


bloblist=reviews1
print len(bloblist)
for i,blob in enumerate(bloblist):
	print("Review value for top business {}.format(i+1))
	

client.close()