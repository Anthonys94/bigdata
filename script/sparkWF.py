#!/usr/bin/python

from textblob import  TextBlob  
import math
import pymongo
from pymongo import MongoClient
import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('vader_lexicon')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
import csv
import sys
from pyspark import SparkConf, SparkContext
import string
import re
reload(sys)
sys.setdefaultencoding('utf8')
conf = SparkConf()
conf.setMaster("local[*]")
conf.setAppName("wfrequency")
conf.set("spark.executor.memory", "10g")
sc = SparkContext(conf = conf)


client = MongoClient('localhost',27017)
db = client.YelpDB

reviews = []

tempReview = db.review.find({"business_id": str(sys.argv[1])})


reviews = []
for review in tempReview:
    reviews.append(TextBlob(review['text']).lower())

def count_score(word):
    if len(word)<4:
        return (word,0)
    else:
        parola = TextBlob(word)
        if parola.tags is not None:
            if (parola.tags[0][1]  in  ("MD","WDT","WRB","VB", "VBD", "VBG", "VBN", "VBP", "VBZ","DT","RB","RBR","RBS","IN","PRP","TO","WP","PRP$")):
                return (word,0)
            else:
                return (word,1)
        else:
            return (word,0)

lines = sc.parallelize(reviews)

counts = lines.flatMap(lambda line: line.words).map(count_score).reduceByKey(lambda x, y: x + y)
print '************************************************ result *************************************************************** '
#print counts.top(20,lambda t:t[1])


myData = [["Parola","Score"]]
for el in counts.top(30,lambda t:t[1]):
    word = str(el).replace("u'","").replace("'","")
    word = re.sub(r'[^-{,}\w]', ' ', word)
    myData.append([word])
myFile = open('wf'+str(sys.argv[1])+'.csv','w')
with myFile:
    writer = csv.writer(myFile)
    writer.writerows(myData)


client.close()
