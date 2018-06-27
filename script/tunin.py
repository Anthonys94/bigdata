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
tuplemax=[]
calcolomax=[]
i=1
for e in cursor:
    for t in val:
    	valori.append(abs(e['valoretext']*(1+t[0]*e['useful']+t[1]*e['cool']+t[2]*e['funny'])*(1+e['vlutente'])))
	
    print i
    i=i+1
    tupla=val[valori.index(max(valori))]
    tuplemax.append(tupla)
    f=open("tuning.txt", "a+")
    f.write("Tupla: %5.1f %5.1f %5.1f \n" %(tupla[0],tupla[1],tupla[2]))
    f.close()
    del valori[:]
	
cnt = Counter(tuplemax)      
print cnt.most_common(3)
#f=open("tuning.txt", "a+")
#f.write("Tupla: %5.1f %5.1f %5.1f  \n" %(tup[0],tup[1],tup[2]))
#f.close()                        
                                    
client.close()
