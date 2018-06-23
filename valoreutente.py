#!/usr/bin/python

import pymongo
from pymongo import MongoClient
import pprint
import json

#Connessione a MongoDB

client = MongoClient('localhost',27017)
db = client.YelpDB

#Caricamento utenti

users = db.user.find()

#Calcolo valore utente

jsonlist = []
for element in users:
	subel = {}
	subel['user_id']= element['user_id']    #id utente
	numAnniElite = len(element['elite'])
	numAmici = len(element['friends'])
	sCompl = element['compliment_hot'] + element['compliment_more'] + element['compliment_profile'] + element['compliment_cute'] + element['compliment_list'] + element['compliment_note'] + element['compliment_plain'] + element['compliment_cool'] + element['compliment_funny'] + element['compliment_writer'] + element['compliment_photos'] 
	if '2017' in element['elite']:
		Elite17 = 1
	else:
		Elite17 = 0
	subel['valore'] = 0.27*Elite17+ 0.05*numAnniElite+0.13*element['fans']+0.08*element['review_count']+0.08*numAmici+0.1*sCompl+0.19*element['useful']+0.03*element['funny']+0.05*element['cool']
	jsonlist.append(subel)
	
with open('sintesiuser.json','w') as outfile:
    json.dump(jsonlist,outfile)
	
collection = db.sintesiuser
clear = collection.remove()
result = collection.insert_many(jsonlist)
	
client.close()