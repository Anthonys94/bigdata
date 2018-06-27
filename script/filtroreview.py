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
mostreviewed = db.business.find().sort("review_count",-1).limit(3)
negozi=[]
for element in mostreviewed:
    negozi.append(element['business_id'])
print "--- Lettura delle review"
reviews1 = db.sintesireviewoptidea.find({"business_id" : negozi[0]})
reviews2 = db.sintesireviewoptidea.find({"business_id" : negozi[1]})
reviews3 = db.sintesireviewoptidea.find({"business_id" : negozi[2]})

print reviews1.count()
print reviews2.count()
print reviews3.count()
#reviews1 = db.sintesireviewoptidea.find({"business_id" :"u4sTiCzVeIHZY8OlaL346Q"})

review1 = [["business_id","valoreOP1","valoreOP2","valoreOP3","user_id","vlutente","valoretext","date","stars","valorelib"]]
for e in reviews1:
    review1.append([e['business_id'],e['valoreOP1'],e['valoreOP2'],e['valoreOP3'],e['user_id'],e['vlutente'],e['valoretext'],e['date'],e['stars'],e['valorelib']])

myFile1 = open('business1.csv', 'w')  
with myFile1:  
   writer = csv.writer(myFile1, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
   writer.writerows(review1)

review2 =[["business_id","valoreOP1","valoreOP2","valoreOP3","user_id","vlutente","valoretext","date","stars","valorelib"]]
for e in reviews2:
    review2.append([e['business_id'],e['valoreOP1'],e['valoreOP2'],e['valoreOP3'],e['user_id'],e['vlutente'],e['valoretext'],e['date'],e['stars'],e['valorelib']])

myFile2 = open('business2.csv', 'w')
with myFile2:
    writer = csv.writer(myFile2, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
    writer.writerows(review2)

review3 = [["business_id","valoreOP1","valoreOP2","valoreOP3","user_id","vlutente","valoretext","date","stars","valorelib"]]
for e in reviews3:
    review3.append([e['business_id'],e['valoreOP1'],e['valoreOP2'],e['valoreOP3'],e['user_id'],e['vlutente'],e['valoretext'],e['date'],e['stars'],e['valorelib']])

myFile3 = open('business3.csv', 'w')
with myFile3:
    writer = csv.writer(myFile3, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
    writer.writerows(review3)




client.close()
