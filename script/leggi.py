#!/usr/bin/python

from collections import Counter

linee=[]
filem=open('tuning.txt','r')
for line in filem:
    linee.append(line)

cnt = Counter(linee)
print (cnt.most_common(3))

filem.close()
