#!/usr/bin/python

from textblob import  TextBlob
import math
import pymongo
from pymongo import MongoClient
import nltk
nltk.download('vader_lexicon')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
import csv
import sys

def tf(word, blob):
    parola = TextBlob(word)
    if (len(word) < 4) or (parola.tags[0][1] in ("MD","WDT","WRB","VB", "VBD", "VBG", "VBN", "VBP", "VBZ","DT","RB","RBR","RBS","IN","PRP","TO","WP","PRP$")) :
        return 0
    else:
        return (float)(blob.words.count(word))
def tfidf(word, blob, bloblist):
        return tf(word, blob)



client = MongoClient('localhost',27017)
db = client.YelpDB

reviews = []

tempReview = db.review.find({"business_id": str(sys.argv[1])})
r = ''
for review in tempReview:
    r = r + review['text']
reviews.append(TextBlob(r).lower())


bloblist = reviews
print len(bloblist)
for i, blob in enumerate(bloblist):
   print("Top words in business {}".format(i+1))
   scores = {word: tfidf(word,blob,bloblist) for word in blob.words}
   sorted_words = sorted(scores.items(), key=lambda x: x[1],reverse=True)
   myData = [["Parola","Score"]]
   for word,score in sorted_words[:20]:
       myData.append([word,round(score,5)])
       print("\tWord: {}, Score: {}".format(word,round(score,5)))

myFile = open('wf'+str(sys.argv[1])+'.csv','w')
with myFile:
    writer = csv.writer(myFile)
    writer.writerows(myData)

client.close()
