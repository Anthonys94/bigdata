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

reviews1 = db.sintesireviewopt.find({"business_id" : negozi[0]})
#reviews2 = db.sintesireviewopt.find({"business_id" : negozi[1]})
#reviews3 = db.sintesireviewopt.find({"business_id" : negozi[2]})

review1=[]
#review1 = [["business_id","valoreOP1","valoreOP2","valoreOP3","user_id","vlutente","valoretext","date","stars","valorelib"]]
for e in reviews1:
    review1.append([e['business_id'],e['valoreOP1'],e['valoreOP2'],e['valoreOP3'],e['user_id'],e['vlutente'],e['valoretext'],e['date'],e['stars'],e['valorelib']])
	
#ordina review1 per data
review1=sorted(review1, key=itemgetter(7))
somma=0
somma2=0
somma3=0
indice=1
for e in review1:
	somma=somma+e['valoreOP1']
	somma2=somma2+e['valoreOP2']
	somma3=somma3+e['valoreOP3']
	e.append(somma/i)
	e.append(somma2/i)
	e.append(somma3/i)
	i=i+1
finale=["business_id","valoreOP1","valoreOP2","valoreOP3","user_id","vlutente","valoretext","date","stars","valorelib","cumop1","cumop2","cumop3"]+review1
myFile1 = open('business1.csv', 'w')  
with myFile1:  
   writer = csv.writer(myFile1, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
   writer.writerows(finale)

client.close()
