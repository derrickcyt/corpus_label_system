# -*- coding:utf-8 -*-
import pymongo

client = pymongo.MongoClient("110.64.66.203", 27017)
db = client["corpus_label"]
# col = db["keyboard"]


def create_col(col_name):
    db.create_collection(col_name)


def get_col(col_name):
    return db[col_name]
