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

#Seleziona le review relative ai business con review_count maggiore di 500

curnegozi = db.business.find({"review_count": {"$gte": 500 }})
#tutti i negozi con review_cout magg o uguale a 500
negozi=[]

for element in curnegozi:
    negozi.append(element['business_id'])
#usa la lista per ricavare le review relative ai negozi

reviews= db.review.find({"business_id":{"$in":negozi}})

#dobbiamo scorrere la lista delle review per effettuare il calcolo dei valori.


jsonlist= []
sid = SentimentIntensityAnalyzer()
for element in reviews:
    subel = {}
    subel['review_id']= element['review_id']         #reviewid
    subel['business_id']= element['business_id']     #id negozio
    subel['user_id']= element['user_id']             #id utente
    subel['date'] = element['date']                  #data

    #adesso dobbiamo calcolare il valore, dato dalla seguente espressione
    #(lib+sterlinenormalizzato)*(useful0.7+funny0.1+cool0.2 ) * valoreUtente
    #ci serve quindi il valoreutente prima di terminare lo script!!!
    #divido la review in fasi.
    lines_list = tokenize.sent_tokenize(element['text'])
    #per ogni frase viene calcolata lo score di polarità
    #I vari score si sommano tra loro
    #Infine viene effettuata una media
    app=0
    for sentence in lines_list:
        ss = sid.polarity_scores(sentence)
        app=ss['compound']+app
    
    lib = app/lines_list.count()  #media
    #normalizzazion stelle:
    # 1 stella --> -1
    # 2 stelle --> -0.5
    # 3 stelle --> 0        ==> punteggio= 0.5*Stella-1.5
    # 4 stelle --> 0.5
    # 5 stelle --> 1 
	user = db.sintesiuser.find({"user_id": subel['user_id']}) 
	valoreUtente = user['valore'] 
	subel['valore']= (lib+0.5*element['stars']-1.5)*(0.7*element['useful']+0.1*element['funny']+0.2*element['cool'])*valoreUtente
	jsonlist.append(subel)

#mettere l'output su un file json che si chiama sintesireview.json
#inserire il file nel database. 

#jsonobj=json.dumps(jsonlist)
with open('sintesireview.json','w') as outfile:
    json.dump(jsonlist,outfile)

#vedere come salvare sul db!

collection = db.sintesireview 
clear = collection.remove()            #pulisco la collection da eventuali scritture precedenti 
result = collection.insert_many(jsonlist)    #inserisco gli elementi calcolati 
 
client.close()

