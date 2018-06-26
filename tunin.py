#!/usr/bin/python
import pymongo
from pymongo import MongoClient
import numpy as np
from sklearn.metrics import mean_squared_error
from math import sqrt


#Connessione a MongoDB

client = MongoClient('localhost',27017)
db = client.YelpDB

cursor=db.sintesireview.find()
print cursor.count()
val=np.array([(0.2,0.1,0.7),(0.2,0.2,0.6),(0.2,0.3,0.5),(0.2,0.4,0.4),(0.2,0.5,0.3),(0.2,0.6,0.2),(0.2,0.7,0.1),(0.2,0.8,0),(0.3,0,0.7),(0.3,0.1,0.6),(0.3,0.2,0.5),(0.3,0.3,0.4),(0.3,0.4,0.3),(0.3,0.5,0.2),(0.3,0.6,0.1),(0.3,0.7,0),(0.4,0,0.6),(0.4,0.1,0.5),(0.4,0.2,0.4),(0.4,0.3,0.3),(0.4,0.4,0.2)])

#val=np.array([(0.2,0.1,0.7),(0.2,0.2,0.6),(0.2,0.3,0.5),(0.2,0.4,0.4)])

valori=[] 
stelle=[]
rms=[]
valorinorm=[]

for t in val:
    print "stampa la tripla"
    print t[0],t[1],t[2]
    i=0
    for e in cursor:
       print i
       i=i+1
       valori.append(e['valoretext']*(1+t[0]*e['useful']+t[1]*e['cool']+t[2]*e['funny'])*(1+e['vlutente']))
       stelle.append(0.5*e['stars']-1.5)
    
    cursor.rewind()
    #normalizzazione valori
   # print valori
    valorinorm = (2/(max(valori)-min(valori)))*(valori - max(valori)) + 1
   # print valorinorm
    err=np.sqrt(((valorinorm-stelle)**2).mean())
    #err=sqrt(mean_squared_error(stelle, valorinorm))
   # print err
   # f=open("rmsMichela.txt", "a+")
   # f.write("Tupla: %5.1f %5.1f %5.1f , Errore: %5.8f \n" %(t[0],t[1],t[2],err))
   # f.close()
    rms.append(err)
    del valori[:]
    del stelle[:]

                                    
                                    
print "Minimo : "
print min(rms)
print "Corrispondente a: "
print val[rms.index(min(rms))]
client.close()
