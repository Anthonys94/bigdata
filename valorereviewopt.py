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

################################

#Connessione a MongoDB

client=MongoClient('localhost',27017)
db=client.YelpDB

#Prendo tutte le review sintetizzate
print "--- Lettura Sintesireview"
reviews= db.sintesireview.find()

jsonlist= []
valore1=[]
valore2=[]
valore3=[]
sid = SentimentIntensityAnalyzer()

indice=0
for element in reviews:
    print indice      #per tener conto delle elaborazioni
    indice=indice+1
	#oggetto da creare ha i seguenti capi:
	# review_id -
	# user_id -
	# date-
	# star-
	# business_id -
	# valore_text (lib+stelline)-
	# valore lib-
	# valoreop   (andamento opinione)
	# valoreutente-
	
    subel = {}
    subel['review_id']= element['review_id']         #reviewid
    subel['business_id']= element['business_id']     #id negozio
    subel['user_id']= element['user_id']             #id utente
    subel['date'] = element['date']                  #data
    subel['stars']= 0.5*element['stars']-1.5         #stelle normalizzate
	subel['valoretext']= element['valoretext']		 #prendo valore testo (lib+stelle)
	subel['valorelib']= element['valorelib']		 #solo val lib
	subel['vlutente']=element['vlutente']			 #valore utente
	subel['valoreOP1']=0
	subel['valoreOP2']=0
	subel['valoreOP3']=0
	#(lib+sterlinenormalizzato)*(1+useful*alpha+cool*beta+funny*gamma )*(1+valoreUtente)  
	#val migliore: a=0.1 b=0 g=0.9
	#val2: a=0.2 b=0 g=0.8
	#val3: a=0.3 b=0 g=0.7
	valore1.append(element['valoretext']*(1+0.1*element['useful']+0.9*element['funny'])*(1+element['vlutente']))
	valore2.append(element['valoretext']*(1+0.2*element['useful']+0.8*element['funny'])*(1+element['vlutente']))
	valore3.append(element['valoretext']*(1+0.3*element['useful']+0.7*element['funny'])*(1+element['vlutente']))
	jsonlist.append(subel)
	
	
valnorm1=(2/(max(valore1)-min(valore1)))*(valore1 - max(valore1)) + 1
valnorm2=(2/(max(valore2)-min(valore2)))*(valore2 - max(valore2)) + 1
valnorm3=(2/(max(valore2)-min(valore2)))*(valore2 - max(valore2)) + 1
i=0
for e in jsonlist:
	subel['valoreOP1']=valnorm1[i]
	subel['valoreOP2']=valnorm2[i]
	subel['valoreOP3']=valnorm3[i]
	i=i+1
	
with open('sintesireviewopt.json','w') as outfile:
    json.dump(jsonlist,outfile)

collection = db.sintesireviewopt
clear = collection.remove()            
result = collection.insert_many(jsonlist)    

client.close()

