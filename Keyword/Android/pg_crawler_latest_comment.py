#encoding=utf8
import sys, os

from pymongo import MongoClient
from langdetect import detect

# use http://gearman.org/examples/reverse/ later

if __name__ == '__main__':


    client = MongoClient('mongodb://192.168.10.143:27017')
    reivew_db = client['pg_crawler']

# query app id first
    pipe = [
            {'$group': {'_id': '$appid', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}}
        ]

    rs = reivew_db['comment'].aggregate(pipeline=pipe)
#    appid_aggregate = []

# for each appid
    ll = 1
    for i in rs:
#        print i['_id']
        #print i["_id"]
        if reivew_db['offline'].find({"appid": i["_id"]}).count() == 0:
#        if offline) == 0:
            for ireivew in reivew_db['comment'].find({"appid": i["_id"]}):
                #print detect(ireivew['usr_name'])
                review = ireivew['usr_comment']
                review_title = ireivew['usr_name']
                review_star = ireivew['usr_star']

                #if review.lower().find(u"廣告") != -1 or review_title.lower().find(u"廣告") != -1:
                #if review.lower().find("dumb") != -1 or review.lower().find("dumb") != -1:
                #if review.lower().find("trash") != -1 or review.lower().find("trash") != -1:
                #if review.lower().find(u"只有广告") != -1 or review_title.lower().find(u"只有广告") != -1:
                # if review.lower().find(u"广告") != -1 or review_title.lower().find(u"广告") != -1:
                #if review.lower().find(u"审核") != -1 or review_title.lower().find(u"审核") != -1:
                #if review.lower().find(u"骗人") != -1 or review_title.lower().find(u"骗人") != -1:
                #if review.lower().find(u"骗子") != -1 or review_title.lower().find(u"骗子") != -1:
                #if review.lower().find(u"骗钱") != -1 or review_title.lower().find(u"骗钱") != -1:
                #if review.lower().find(u"欺诈") != -1 or review_title.lower().find(u"欺诈") != -1:
                #if review.lower().find(u"自启") != -1 or review_title.lower().find(u"自启") != -1:
                # if review.lower().find(u"病毒") != -1 or review_title.lower().find(u"病毒") != -1:
                # if review.lower().find(u"话费") != -1 or review_title.lower().find(u"话费") != -1:
                #if review.lower().find(u"不要下载") != -1 or review_title.lower().find(u"不要下载") != -1:
                #if review.lower().find(u"不要安装") != -1 or review_title.lower().find(u"不要安装") != -1:
                #if review.lower().find(u"假的") != -1 or review_title.lower().find(u"假的") != -1:
                # if review.lower().find("fake") != -1 or review_title.lower().find("fake") != -1:
                #if review.lower().find("can't play") != -1 or review_title.lower().find("can't play") != -1:
                # if review.lower().find("can't use") != -1 or review_title.lower().find("can't use") != -1:
                # if review.lower().find("scam") != -1 or review_title.lower().find("scam") != -1:
                # if review.lower().find("fraud") != -1 or review_title.lower().find("fraud") != -1:
                #if review.lower().find("cheat") != -1 or review_title.lower().find("cheat") != -1:
                #if review.lower().find("ads") != -1 or review_title.lower().find("ads") != -1:
                # if review.lower().find("virus") != -1 or review_title.lower().find("virus") != -1:
                # if review.lower().find("torjan") != -1 or review_title.lower().find("torjan") != -1:
                # if review.lower().find("root") != -1 or review_title.lower().find("root") != -1:
                # if review.lower().find("airtime") != -1 or review_title.lower().find("airtime") != -1:
                #if review.lower().find("fraud") != -1 or review_title.lower().find("fraud") != -1:
                if review_star =='1':
                    if review.lower().find("airtime") != -1 or review_title.lower().find("airtime") != -1:

                        ll += 1
                        # if ll % 20 == 0:
                        #     t = raw_input()
                        # print ireivew
                        print "\t %s %s %s %s: %s" %(i["_id"], ireivew['usr_star'], ireivew['usr_date'], ireivew['usr_name'], ireivew['usr_comment'])


    client.close()

    print "**** done *****"
