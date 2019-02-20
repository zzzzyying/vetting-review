# encoding=utf8

from pymongo import MongoClient
# import trans
import time
# use http://gearman.org/examples/reverse/ later
# import sys
# reload(sys)
# sys.setdefaultencoding( "utf-8" )

from langdetect import detect
import time
import datetime
import trans
import re
import sys
import pycompatibility as compat
import pg_crawler_latest_comment_util as review_util

def gen_pipe_with_key(keywords):
    pipe = {}

    for key in keywords.keys():

        tmp_pipe = [{"$match": {"$or": []}}]
        for kw in keywords[key]:
            #tmp_pipe[0]["$match"]["$or"].append({"usr_comment": {"$regex": kw, '$options':'i'}})
            tmp_pipe[0]["$match"]["$or"].append({"usr_comment": {"$regex": kw, '$options':'i'}, "usr_star": "1"})

        pipe[key] = tmp_pipe

    return pipe


def append_keyword(keywords, objs):
    retMe = []
    for obji in objs:
        obji["key"] = []
        for ix in keywords[obji["type"]]:
            if obji["usr_comment"].lower().find(ix) >= 0:
            #if obji["usr_comment"].lower().find(ix) >= 0 and obji["usr_star"] == "1":
                obji["key"].append(ix)
        retMe.append(obji)
    return retMe


def convertTimeStamp2Str(timeStamp):
    tArray = time.localtime(timeStamp)
    return time.strftime("%Y-%m-%d", tArray)

def removeTags(str):
    return re.compile('<div.*<\/div>').sub('',str)
    
if __name__ == '__main__':
    
    # generate key word dict
    review_db_util = review_util.pg_crawler_latest_comment_util()
    keylist = review_db_util.get_keywords_list("./keyword.txt")
    
    # generate query pipe
    p = gen_pipe_with_key(keylist)

    client = MongoClient('mongodb://192.168.10.143:27017')
    reivew_db = client['pg_crawler']

    comments_obj = []

    for catetory in p.keys():
        rs = reivew_db['comment'].aggregate(pipeline=p[catetory])

        for i in rs:
            i["type"] = catetory
            comments_obj.append(i)

    comments_obj = append_keyword(keylist, comments_obj)

    cluster = {}
    for obj in comments_obj:
        if obj["appid"] in cluster.keys():
            cluster[obj["appid"]].append(obj)
        else:
            cluster[obj["appid"]] = [obj]


    client = MongoClient('mongodb://192.168.10.143:27017')
    reivew_db = client['pg_crawler']

    ll = 0
    for appid in cluster.keys():
        if review_db_util.has_offline(appid):
            continue
        if review_db_util.has_reported(appid):
            continue

        related_reviews = len(cluster[appid])
        all_reviews = reivew_db.comment.find({"appid": appid}).count()

        print(">> Clustering: {}, [{}] All {} reviews, {} reviews hit keyword.".format(appid, str(round(float(related_reviews)/all_reviews, 3)*100)+"%", all_reviews, related_reviews))
        date = "nil"
        for review in cluster[appid]:
            ll += 1
            if ll % 40 == 0:
                compat.wait4input()
            try:
                date = convertTimeStamp2Str(trans.trans(review['language'], review['usr_date']))
            except:
                date = "nil"
            # ll += 1
            # if ll % 20 == 0:
                # t = input()
            print("\t[{}] [{}] [{}] [{}] {}".format(date, review["type"], review["usr_star"], review["key"], review["usr_comment"]))
