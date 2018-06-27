#!/usr/bin/python
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
from operator import itemgetter

client=MongoClient('localhost',27017)
db=client.YelpDB
mostreviewed = db.business.find().sort("review_count",-1).limit(3)
negozi=[]
for element in mostreviewed:
    negozi.append(element['business_id'])
print "--- Lettura delle review"

reviews1 = db.sintesireviewoptidea.find({"business_id" : negozi[0]})


review1=[]
for e in reviews1:
    review1.append([e['business_id'],e['valoreOP1'],e['user_id'],e['vlutente'],e['valoretext'],e['date'],e['stars'],e['valorelib']])
	
#ordina review1 per data
review1=sorted(review1, key=itemgetter(5))
somma=0

indice=1
for e in review1:
	e.append(i)
	somma=(somma/2)+e['valoreOP1']
	e.append(somma)
	i=i+1
	
finale=["business_id","valoreOP1","user_id","vlutente","valoretext","date","stars","valorelib","indice","cum"]+review1
myFile1 = open('business1cumulativo.csv', 'w')  
with myFile1:  
   writer = csv.writer(myFile1, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
   writer.writerows(finale)

client.close()
