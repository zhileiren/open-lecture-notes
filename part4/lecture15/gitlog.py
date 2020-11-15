#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymongo

client = pymongo.MongoClient()
db = client['test']
table = db['gitlog']

with open("git.log") as f:
    lines = f.readlines()

for line in lines:
    time, author, commit_id, message = line.split("::")
    table.insert_one({"time": time, 
                  "author": author,
                  "commit_id": commit_id,
                  "message": message.strip()})

for doc in table.find():
    print(f"time: {doc['time']}; author: {doc['author']}; id: {doc['commit_id']}; msg: {doc['message']}")

