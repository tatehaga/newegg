#!/usr/bin/python3

import json

with open('cases_graphics_data.json') as json_file:
    data = json.load(json_file)
count = 0
newcount = 0
authorcount = 0
reviewcount = 0
anon = 0
authors = []
#print(len(data['Desktop Graphics Cards']))
for p in (data['Desktop Graphics Cards']):
    count +=1
    try: 
        data['Desktop Graphics Cards'][p][0]
        newcount += 1
        for i in range(len(data['Desktop Graphics Cards'][p])):
            reviewcount += 1
            if data['Desktop Graphics Cards'][p][i]['AuthorID'] not in authors:
                authors.append(data['Desktop Graphics Cards'][p][i]['AuthorID'])
            if data['Desktop Graphics Cards'][p][i]['AuthorID'] == "Anonymous":
                anon +=1
    except:
        continue

for p in (data['Computer Cases']):
    count +=1
    try: 
        data['Computer Cases'][p][0]
        newcount += 1
        for i in range(len(data['Computer Cases'][p])):
            reviewcount += 1
            if data['Computer Cases'][p][i]['AuthorID'] not in authors:
                authors.append(data['Computer Cases'][p][i]['AuthorID'])
            if data['Computer Cases'][p][i]['AuthorID'] == "Anonymous":
                anon +=1      
    except:
        continue

"""
for i in data:
    for j in data[j]:
        try:
            data[i][j][0]
            newcount += 1
            for k in range(len(data[i][j])):
                reviewcount += 1
                if data[i][j][k]['AuthorID'] not in authors:
                    authors.append(data[i][j][k]['AuthorID'])
        except:
            continue
"""

print("Total Scanned: " + str(count))
print("Total items with Reviews: " + str(newcount))
print("Total Reviews:", reviewcount)
print("Total Authors:", len(authors) )
print("Anonymous:", anon)