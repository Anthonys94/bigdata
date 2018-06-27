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
import sys

client=MongoClient('localhost',27017)
db=client.YelpDB
mostreviewed = db.business.find().sort("review_count",-1).limit(3)
negozi=[]
for element in mostreviewed:
    negozi.append(element['business_id'])
print "--- Lettura delle review"

print str(sys.argv[1])
reviews1 = db.sintesireviewoptidea.find({"business_id" : str(sys.argv)[1]})

review1=[]
for e in reviews1:
    review1.append([e['business_id'],e['valoreOP1'],e['valoreOP2'],e['valoreOP3'],e['user_id'],e['vlutente'],e['valoretext'],e['date'],e['stars'],e['valorelib']])
	
#ordina review1 per data
review1=sorted(review1, key=itemgetter(7))
somma=0
somma1=0
somma2=0
i=1
for e in review1:
    e.append(i)
    somma=(somma/2)+e[1]
    somma1=(somma1/2)+e[2]
    somma2=(somma2/2)+e[3]
    e.append(somma)
    e.append(somma1)
    e.append(somma2)
    i=i+1
	
finale=[["business_id","valoreOP1","valoreOP2","valoreOP3","user_id","vlutente","valoretext","date","stars","valorelib","indice","cum","cum2","cum3"]]+review1
myFile1 = open('bc'+str(sys.argv[1])+'.csv', 'w')  
with myFile1:  
   writer = csv.writer(myFile1, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
   writer.writerows(finale)


client.close()
