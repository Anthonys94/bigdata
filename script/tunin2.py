#!/usr/bin/python
import pymongo
from pymongo import MongoClient
import numpy as np
from sklearn.metrics import mean_squared_error
from math import sqrt
import itertools
import operator
from collections import Counter

#Connessione a MongoDB

client = MongoClient('localhost',27017)
db = client.YelpDB

cursor=db.sintesireviewidea.find()
print cursor.count()
val=[(0,0.1,0.9),(0,0.2,0.8),(0,0.3,0.7),(0,0.4,0.6),(0,0.5,0.5),(0,0.6,0.4),(0,0.7,0.3),(0,0.8,0.2),(0,0.9,0.1),(0.1,0,0.9),(0.1,0.1,0.8),(0.1,0.2,0.7),(0.1,0.3,0.6),(0.1,0.4,0.5),(0.1,0.5,0.4),(0.1,0.6,0.3),(0.1,0.7,0.2),(0.1,0.8,0.1),(0.1,0.9,0),(0.2,0,0.8),(0.2,0.1,0.7),(0.2,0.2,0.6),(0.2,0.3,0.5),(0.2,0.4,0.4),(0.2,0.5,0.3),(0.2,0.6,0.2),(0.2,0.7,0.1),(0.2,0.8,0),(0.3,0,0.7),(0.3,0.1,0.6),(0.3,0.2,0.5),(0.3,0.3,0.4),(0.3,0.4,0.3),(0.3,0.5,0.2),(0.3,0.6,0.1),(0.3,0.7,0),(0.4,0,0.6),(0.4,0.1,0.5),(0.4,0.2,0.4),(0.4,0.3,0.3),(0.4,0.4,0.2),(0.4,0.5,0.1),(0.4,0.6,0),(0.5,0,0.5),(0.5,0.1,0.4),(0.5,0.2,0.3),(0.5,0.3,0.2),(0.5,0.4,0.1),(0.5,0.5,0),(0.6,0,0.4),(0.6,0.1,0.3),(0.6,0.2,0.2),(0.6,0.3,0.1),(0.6,0.4,0),(0.7,0,0.3),(0.7,0.1,0.2),(0.7,0.3,0),(0.8,0,0.2),(0.8,0.1,0.1),(0.8,0.2,0),(0.9,0,0.1),(0.9,0.1,0)]

#val=np.array([(0.2,0.1,0.7),(0.2,0.2,0.6),(0.2,0.3,0.5),(0.2,0.4,0.4)])

valori=[] 
tupleese=[]

i=1
for e in cursor:
    for t in val:
    	valori.append(abs(e['valoretext']*(1+t[0]*e['useful']+t[1]*e['cool']+t[2]*e['funny'])*(1+e['vlutente'])))
	tupleese.append(t)
    print i
    i=i+1

massimo=max(valori)
#massimo tra tutte le review
tuplamax=tupleese[valori.index(massimo)]
alp=tuplamax[0]
valori1=[]

k=1
tupleese1=[]
valori1=[]
cursor.rewind()
for e in cursor:
    for t in val:
	if t[0]==alp:
            valori1.append(abs(e['valoretext']*(1+t[0]*e['useful']+t[1]*e['cool']+t[2]*e['funny'])*(1+e['vlutente'])))
	    tupleese1.append(t)
    print k
    k=k+1
	
massimo1=max(valori1)
#massimo tra tutte le review
tuplamax1=tupleese1[valori1.index(massimo1)]
beta=tuplamax1[1]

gamma=1-alp-beta
print "Alpha : "
print alp
print "Beta : "
print beta
print "Gamma : "
print gamma
#cnt = Counter(tuplemax)      
#print cnt.most_common(3)
#f=open("tuning.txt", "a+")
#f.write("Tupla: %5.1f %5.1f %5.1f  \n" %(tup[0],tup[1],tup[2]))
#f.close()                        
                                    
client.close()
