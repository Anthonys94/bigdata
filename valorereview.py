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

print "--- Lettura negozi"
curnegozi = db.business.find({"review_count": {"$gte": 500 }})
#tutti i negozi con review_cout magg o uguale a 500
negozi=[]
for element in curnegozi:
    negozi.append(element['business_id'])

#usa la lista per ricavare le review relative ai negozi
print "--- Lettura review"
reviews= db.review.find({"business_id":{"$in":negozi}})

#lista degli utenti che hanno scritto le review relative ai business
print "--- Lista utenti"
listaid=db.review.distinct("user_id", {"business_id":{"$in":negozi}})
#prendo gli utenti con l'id ritornato sopra.

utenti= db.sintesiuser.find({"user_id": {"$in": listaid}})
#dobbiamo scorrere la lista delle review per effettuare il calcolo dei valori

utentidict=[]
print "--- Creazione dizionario degli utenti"
for element in utenti:
    utentidict.append([element['user_id'],element['valore']])
utentidict=dict(utentidict)


print "--- Analisi review e calcolo valore"

#Quindi abbiamo selezionato le review relative a tutti i negozi con 
#review count > 500 e inoltre abbiamo preso tutti gli utenti 
#che hanno scritto quelle review

jsonlist= []
sid = SentimentIntensityAnalyzer()

indice=0
for element in reviews:
    print indice      #per tener conto delle elaborazioni
    indice=indice+1
    subel = {}
    subel['review_id']= element['review_id']         #reviewid
    subel['business_id']= element['business_id']     #id negozio
    subel['user_id']= element['user_id']             #id utente
    subel['date'] = element['date']                  #data
    subel['stars']= element['stars']                 #stelle per elaborazione
    #adesso dobbiamo calcolare il valore, dato dalla seguente espressione
   
   #(lib+sterlinenormalizzato)*(1 + useful0.7+funny0.1+cool0.2 )*(1+ valoreUtente)
    
    lines_list = tokenize.sent_tokenize(element['text'])
    #per ogni frase viene calcolata lo score di polarita
    #I vari score si sommano tra loro
    #Infine viene effettuata una media
   
    app=0
    for sentence in lines_list:
        ss = sid.polarity_scores(sentence)
        app=ss['compound']+app
    
    lib = app/len(lines_list)  #media
    #normalizzazion stelle:
    # 1 stella --> -1
    # 2 stelle --> -0.5
    # 3 stelle --> 0        ==> punteggio= 0.5*Stella-1.5
    # 4 stelle --> 0.5
    # 5 stelle --> 1       
    
    valoreUtente = utentidict[subel['user_id']]
    
    subel['valorelib']= lib                     #valorelib
    subel['valoretext']=lib+0.5*element['stars']-1.5 #valore solo testo
    #valore opinione
    subel['valoreOp']= (lib+0.5*element['stars']-1.5)*(1 + 0.7*element['useful']+0.1*element['funny']+0.2*element['cool'])*(1 + valoreUtente)
    
    jsonlist.append(subel)

#mettere l'output su un file json che si chiama sintesireview.json
#inserire il file nel database. 

#jsonobj=json.dumps(jsonlist)
with open('sintesireview.json','w') as outfile:
    json.dump(jsonlist,outfile)

#vedere come salvare sul db!

collection = db.sintesireview 
clear = collection.remove()            #pulisco la collection da eventuali scritture precedenti 
result = collection.insert_many(jsonlist)    #inserisco gli elementi calcolati '

client.close()

