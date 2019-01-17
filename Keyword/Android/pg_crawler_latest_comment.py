# encoding=utf8

from pymongo import MongoClient
import trans
import time
# use http://gearman.org/examples/reverse/ later
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

from langdetect import detect
import time
import datetime
import trans

def gen_key_list():
    keyList = {}
    with open("./keyword.txt") as f:
        pkeyList = f.read().splitlines()

    current_category = ""
    for p in pkeyList:
        if p:
            if p.startswith(";"):
                continue
            elif p.startswith("#"):
                current_category = p.split()[1]
            else:
                if current_category in keyList.keys():
                    keyList[current_category].append(p)
                else:
                    keyList[current_category] = [p]

    return keyList


def gen_pipe_with_key(keys):
    pipe = {}

    for key in keys.keys():
        tmp_pipe = [{"$match": {"$or": []}}]

        for kw in keys[key]:
            tmp_pipe[0]["$match"]["$or"].append({"usr_comment": {"$regex": kw, '$options':'i'}})

        pipe[key] = tmp_pipe

    return pipe


def bind_key(keys, objs):
    tmp = []
    for obji in objs:
        obji["key"] = []
        for ix in keys[obji["type"]]:
            if obji["usr_comment"].lower().find(ix) >= 0:
                obji["key"].append(ix)
        tmp.append(obji)
    return tmp


def convertTimeStamp2Str(timeStamp):
    tArray = time.localtime(timeStamp)
    return time.strftime("%Y-%m-%d", tArray)


if __name__ == '__main__':

    # generate key word dict
    keylist = gen_key_list()
    # generate query pipe
    p = gen_pipe_with_key(keylist)

    client = MongoClient('mongodb://192.168.10.143:27017')
    reivew_db = client['pg_crawler']

    comments_obj = []

    for t in p.keys():
        rs = reivew_db['comment'].aggregate(pipeline=p[t])

        for i in rs:
            i["type"] = t
            comments_obj.append(i)

    comments_obj = bind_key(keylist, comments_obj)

    cluster = {}
    for obj in comments_obj:
        if obj["appid"] in cluster.keys():
            cluster[obj["appid"]].append(obj)
        else:
            cluster[obj["appid"]] = [obj]


    client = MongoClient('mongodb://192.168.10.143:27017')
    reivew_db = client['pg_crawler']

    ll = 0
    for app in cluster.keys():
        related_reviews = len(cluster[app])
        all_reviews = reivew_db.comment.find({"appid": app}).count()

        print(">> Clustering: {}, [{}] All {} reviews, Got {} closing reviews.".format(app, str(round(related_reviews/all_reviews, 3)*100)+"%", all_reviews, related_reviews))
        date = "nil"
        for review in cluster[app]:
            ll += 1
            if ll % 20 == 0:
                t = raw_input() 
                
            try:
                date = convertTimeStamp2Str(trans.trans(review['language'], review['usr_date']))
            except:
                date = "nil"    
            print("\t[{}] [{}] {} {} {}".format(date, review["type"], review["key"], review["usr_star"], review["usr_comment"]))


