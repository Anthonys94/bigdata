#!/usr/bin/python

import pymongo
from pymongo import MongoClient
import pprint
import json
from pyspark import SparkConf, SparkContext
import string
import csv
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')
conf = SparkConf()
conf.setMaster("local[*]")
conf.setAppName("val utente")
conf.set("spark.executor.memory", "16g")
sc = SparkContext(conf = conf)
#Connessione a MongoDB

client = MongoClient('localhost',27017)
db = client.YelpDB

#Caricamento utenti

users= db.user.find().limit(50000)

#Calcolo valore utente

jsonlist = []
#for element in users:
def worker(element):	
	#subel['user_id']= element['user_id']    #id utente
	numAnniElite = len(element['elite'])
	numAmici = len(element['friends'])
	sCompl = element['compliment_hot'] + element['compliment_more'] + element['compliment_profile'] + element['compliment_cute'] + element['compliment_list'] + element['compliment_note'] + element['compliment_plain'] + element['compliment_cool'] + element['compliment_funny'] + element['compliment_writer'] + element['compliment_photos'] 
	if '2017' in element['elite']:
		Elite17 = 1
	else:
		Elite17 = 0
	valore = 0.27*Elite17+ 0.05*numAnniElite+0.13*element['fans']+0.06*element['review_count']+0.1*numAmici+0.1*sCompl+0.19*element['useful']+0.03*element['funny']+0.05*element['cool']
        subel=[element['user_id'],numAnniElite, numAmici, sCompl,element['fans'],element['review_count'],element['useful'], element['funny'], element['cool'],valore]
        return subel
#	jsonlist.append(subel)


user = sc.parallelize(users)
results = user.map(worker)
print ' ********************************* RESULT *************************'
csvf= [["user_id","numAnniElite","numAmici","sCompl","fans","review_count","useful","funny","cool","valore"]]

csvf= csvf+ results.take(results.count())
#print json.dumps(results.take(1))

fileu=open("AnalisiUt.csv",'w')
with fileu:
    writer = csv.writer(fileu, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
    writer.writerows(csvf)

	
client.close()
