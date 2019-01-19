#encoding=utf8
import sys, os

from pymongo import MongoClient
from langdetect import detect
#from google.cloud import translate

# use http://gearman.org/examples/reverse/ later
if __name__ == '__main__':

    client = MongoClient('mongodb://192.168.10.143:27017')
    reivew_db = client['pg_crawler']

# query app id first
    pipe = [
            {'$group': {'_id': '$appid', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}}
        ]

    rs = reivew_db['offline'].aggregate(pipeline=pipe)
#    appid_aggregate = []

# for each appid
    for i in rs:
#        print i['_id']
        print (i["_id"])
        annie_db = client['pg_crawler']['apps_annie']
        annie_db_app_obj = annie_db.find({"appid": i["_id"]})
        for j in annie_db_app_obj:
            annie_db_app_inst = j
        '''
        print "\t %s \t %s" %(annie_db_app_inst["category"], str(annie_db_app_inst["rank"]))
        '''
        for ireivew in reivew_db['comment'].find({"appid": i["_id"]}):
            #print detect(ireivew['usr_name'])
            print ("\t %s \t %s \t %s \t%s: \t%s" %(annie_db_app_inst["category"], ireivew['usr_date'], ireivew['usr_star'], ireivew['usr_name'], ireivew['usr_comment']))

        t = raw_input()
    client.close()

    print ("**** done *****")
