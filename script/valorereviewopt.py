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

reviews=db.sintesireviewidea.find()

jsonlist= []
somma=[]
somma1=[]
somma2=[]
indice=0
for element in reviews:
    #print indice      #per tener conto delle elaborazioni
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
  
    somma.append(0*element['useful']+0.1*element['cool']+0.9*element['funny'])
    somma1.append(0.9*element['useful']+0*element['cool']+0.1*element['funny'])
    somma2.append(0.1*element['useful']+0.9*element['cool']+0*element['funny'])


    jsonlist.append(subel)
	

massimo1=max(somma)
minimo1=min(somma)
massimo2=max(somma1)
minimo2=min(somma1)
massimo3=max(somma2)
minimo3=min(somma2)

i=0
for e in jsonlist:
    #print i
    e['valoreOP1']=e['valoretext']*(1+(10/(massimo1-minimo1))*(somma[i]-massimo1)+10)*(1+e['vlutente'])
    e['valoreOP2']=e['valoretext']*(1+(10/(massimo2-minimo2))*(somma1[i]-massimo2)+10)*(1+e['vlutente'])
    e['valoreOP3']=e['valoretext']*(1+(10/(massimo3-minimo3))*(somma2[i]-massimo3)+10)*(1+e['vlutente'])
    #print "valoretesto" 
    #print e['valoretext']
    #print "valore utente"
    #print e['vlutente']
    #print "valore opinione"
    #print e['valoreOP1']
    #print "valore u f c"
    #print somma[i]
    i=i+1

with open('prova.json','w') as outfile:
    json.dump(jsonlist,outfile)

collection = db.sintesireviewoptidea
clear = collection.remove()            
result = collection.insert_many(jsonlist)    

client.close()

