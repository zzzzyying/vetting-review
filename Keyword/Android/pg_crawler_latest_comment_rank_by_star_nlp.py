# encoding=utf8
from pymongo import MongoClient
# import trans
import time
# use http://gearman.org/examples/reverse/ later
import sys
import pycompatibility as compat

from langdetect import detect
import io
import re
import pg_crawler_latest_comment_util as review_util

import nlp

def removeTags(str):
    return re.compile('<div.*<\/div>').sub('',str)
    
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
    for k in list(rank_info):
        if review_db_util.has_offline(k):
            if k in rank_info:
                del rank_info[k]
        if review_db_util.has_reported(k):
            if k in rank_info:
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
    threshold=0.3
    doc_set = {}
    s_review = sorted(rank_info.items(), key = lambda x:x[1], reverse = True)
    for k in s_review:
        str_en=""
        print("*** [{}] [{}] {} {} ***".format(k[0], k[1], reivew_db["comment"].find({"appid":k[0]}).count(), reivew_db["comment"].find({"appid":k[0], "usr_star":"1"}).count()))
        for r in reivew_db["comment"].find({"appid":k[0], "usr_star":"1"}):
            print("[{}] [{}] [{}]".format(r["language"],r["usr_star"], r["usr_comment"]))
            if k[1]>threshold:
                # str_en+=(removeTags(r["usr_comment"])+" ")
                if r["usr_comment"]!='':
                    if r["language"] not in doc_set:
                        doc_set[r["language"]]=[]
                    doc_set[r["language"]].append(removeTags(r["usr_comment"]))
        print ("https://play.google.com/store/apps/details?id=" + k[0] + "\n")
        # print (str_en)
        # if str_en!='':
        #     doc_set_en.append(str_en)
    # print (doc_set)
        # compat.wait4input()
    # nlp.lda(doc_set["EN"],10,5,10)
    # nlp.count("EN",doc_set["EN"])
    # nlp.count("CN",doc_set["CN"])
    kwdlst_en=(['download'])
    kwdlst_cn=(['下载'])
    en_corpus=nlp.gen_corpus("EN",doc_set["EN"])
    cn_corpus=nlp.gen_corpus("CN",doc_set["CN"])
    nlp.show_revelant(kwdlst_en,en_corpus)
    nlp.show_revelant(kwdlst_cn,cn_corpus)
