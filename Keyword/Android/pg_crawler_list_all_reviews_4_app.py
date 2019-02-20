#encoding=utf8
import sys, os
import pycompatibility as compat
from pymongo import MongoClient
from langdetect import detect
#from google.cloud import translate

# use http://gearman.org/examples/reverse/ later
if __name__ == '__main__':

    client = MongoClient('mongodb://192.168.10.143:27017')
    reivew_db = client['pg_crawler']

    for r in reivew_db.comment.find({"appid": "com.google.android.youtube"}):
        print r["usr_comment"]
        
    client.close()

    print ("**** done *****")
