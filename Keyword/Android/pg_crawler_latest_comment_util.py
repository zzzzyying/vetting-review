# encoding=utf8
from pymongo import MongoClient
import io

class pg_crawler_latest_comment_util(object):
    def __init__(self, db_path="mongodb://192.168.10.143:27017",dbname="pg_crawler",report_repo="track", offline_repo="offline"):
        self.db_path = db_path    
        self.dbname = dbname
        self.report_repo = report_repo
        self.offline_repo = offline_repo
        self.db_review = MongoClient(self.db_path)[self.dbname]

                
    def has_reported(self, pkg_name):
        if self.db_review[self.report_repo].find({"appid": pkg_name}).count() == 0:
            return False
        else:
            return True
    

    def has_offline(self, pkg_name):
        if self.db_review[self.offline_repo].find({"appid": pkg_name}).count() == 0:
            return False
        else:
            return True

    def get_keywords_list(self, kw_file):
        retMe = {}
        with io.open(kw_file, encoding='UTF-8') as frh:
            for line in frh.readlines():
                cline = line.strip()
                #print cline
                # comment or space
                if cline.startswith(";") or len(cline) == 0:
                    continue
                # cagetory
                elif cline.startswith("#"):
                    cur_category = cline[1:].strip()
                else:
                    if cur_category in retMe.keys():
                        retMe[cur_category].append(cline)
                    else:
                        retMe[cur_category] = [cline]                        
            
        return retMe

if __name__ == '__main__':
    my_util = pg_crawler_latest_comment_util()
    print my_util.get_key_list("./keyword.txt")