# encoding=utf8
from pymongo import MongoClient
# import trans
import time
# use http://gearman.org/examples/reverse/ later
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from langdetect import detect
import io

import pg_crawler_latest_comment_util as review_util

if __name__ == '__main__':

    client = MongoClient('mongodb://192.168.10.143:27017')
    reivew_db = client['pg_crawler']
    review_db_util = review_util.pg_crawler_latest_comment_util()

    rank_info = {}
    # get all pkg_name
    annie_db = reivew_db['apps_annie']
    for j in annie_db.find():
        rank_info[j["appid"]] = float(0)
    
    # remove reported pkg
    for k in rank_info.keys():
        if review_db_util.has_offline(k):
            if rank_info.has_key(k):            
                del rank_info[k]            
        if review_db_util.has_reported(k):
            if rank_info.has_key(k):
                del rank_info[k]            
    # get percentage of 1 ranked app
    for k in rank_info.keys():
        total = reivew_db["comment"].find({"appid":k}).count()
        p_total = reivew_db["comment"].find({"appid":k, "usr_star":"1"}).count()
        if total!= 0:
            rank_info[k] = float(p_total) / total
        else:
            rank_info[k] = 0    
    # print 1 by 1
    s_review = sorted(rank_info.items(), key = lambda x:x[1], reverse = True)
    for k in s_review:
        t = raw_input()

        print("*** [{}] [{}] {} {} ***".format(k[0], k[1], reivew_db["comment"].find({"appid":k[0]}).count(), reivew_db["comment"].find({"appid":k[0], "usr_star":"1"}).count()))
        for r in reivew_db["comment"].find({"appid":k[0], "usr_star":"1"}):
            print("[{}] [{}]".format(r["usr_star"], r["usr_comment"]))
