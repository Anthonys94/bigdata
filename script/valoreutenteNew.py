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

#Calcolo max
maxfan = db.user.find().sort("fans", -1).limit(1) 
fan = maxfan.next()["fans"]
print "fan"
print fan

maxReviewCount = db.user.find().sort("review_count",-1).limit(1)
revCount = maxReviewCount.next()["review_count"]
print "review count"
print revCount

numAm = []
numElite = []
for e in users:
    numAm.append(len(e["friends"]))
maxNumAm = max(numAm)
print "num amici"
print maxNumAm

maxUseful = db.user.find().sort("useful",-1).limit(1)
useful = maxUseful.next()["useful"]
print "useful"
print useful

maxFunny = db.user.find().sort("funny",-1).limit(1)
funny = maxFunny.next()["funny"]
print "funny"
print funny

maxCool = db.user.find().sort("cool",-1).limit(1)
cool = maxCool.next()["cool"]
print "cool"
print cool

com=db.user.find().sort("compliment_hot",-1).limit(1)
maxcomhot=com.next()["compliment_hot"]
print "com hot"
print maxcomhot

com=db.user.find().sort("compliment_more",-1).limit(1)
maxmore=com.next()["compliment_more"]
print "com more"
print maxmore

com=db.user.find().sort("compliment_profile",-1).limit(1)
maxprofile=com.next()["compliment_profile"]
print "com profile"
print maxprofile

com=db.user.find().sort("compliment_cute",-1).limit(1)
maxcute=com.next()["compliment_cute"]
print "com cute"
print maxcute

com=db.user.find().sort("compliment_list",-1).limit(1)
maxlist=com.next()["compliment_list"]
print "com list"
print maxlist

com=db.user.find().sort("compliment_note",-1).limit(1)
maxnote=com.next()["compliment_note"]
print "com note"
print maxnote

com=db.user.find().sort("compliment_plain",-1).limit(1)
maxplain=com.next()["compliment_plain"]
print "com plain"
print maxplain

com=db.user.find().sort("compliment_cool",-1).limit(1)
maxcool=com.next()["compliment_cool"]
print "com cool"
print maxcool

com=db.user.find().sort("compliment_funny",-1).limit(1)
maxfunny=com.next()["compliment_funny"]
print "com funny"
print maxfunny

com=db.user.find().sort("compliment_writer",-1).limit(1)
maxwriter=com.next()["compliment_writer"]
print "com writer"
print maxwriter

com=db.user.find().sort("compliment_photos",-1).limit(1)
maxphotos=com.next()["compliment_photos"]
print "com photos"
print maxphotos

#Calcolo parametri
par=[1.0/maxphotos, 1.0/maxwriter, 1.0/maxfunny, 1.0/maxcool, 1.0/maxplain, 1.0/maxnote, 1.0/maxlist, 1.0/maxcute, 1.0/maxprofile, 1.0/maxmore, 1.0/maxcomhot, 1.0/fan, 1.0/maxNumAm, 1.0/revCount, 1.0/funny, 1.0/cool, 1.0/useful]
massimo = max(par)
minimo = min(par)
somma=0;
for i in range(0,len(par)):
    somma=somma+par[i]
print somma
for i in range(0,len(par)):
    par[i]=par[i]*0.8/somma
print par
somma1=0;
for i in range(0,len(par)):
    somma1=somma1+par[i]
print somma1


