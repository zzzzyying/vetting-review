#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import json
import string
import sys
import gensim
from gensim.models import Word2Vec
#from smart_open import smart_open
import logging
import re
#import langid
import jieba
#from Crypto.SelfTest.Random.test__UserFriendlyRNG import multiprocessing
import io
import multiprocessing

class embedding(object):
    def __init__(self, stop_words_path):
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.stopwords_path = stop_words_path
        self.model = None
        self.sentences_count = 0
        self.file_count = 0
        self.none_chinese_file = 0
        logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        pass

    def _is_chinese(self, sentence):
        for ch in sentence.decode('utf-8'):
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def show_static_data(self):
        print("Total {} sentences".format(self.sentences_count))
        print("Total {} files".format(self.file_count))        
        print("Total {} NONE chinese files".format(self.none_chinese_file))        
    
        with open("./log.log", "a") as fwh:
            fwh.write("Total {} sentences\n".format(self.sentences_count))
            fwh.write("Total {} files\n".format(self.file_count))
            fwh.write("Total {} NONE chinese files\n".format(self.none_chinese_file))
                        
    def _gen_model(self, model_path, sentences_collection):
        if os.path.isfile(model_path):
            self.model = Word2Vec.load(model_path)  
            self.model.build_vocab(sentences_collection, update = True)
        else:
            self.model = Word2Vec(sentences_collection, min_count = 1, workers = multiprocessing.cpu_count()-2)                                        
        self.model.train(sentences_collection, total_examples=len(sentences_collection), epochs=self.model.iter)  
          
        if self.model != None:            
            self.model.save(model_path)           
        return
    
    def gen_model(self, copus_path, back_up, model_path):
        stopwords = [line.strip() for line in io.open(self.stopwords_path, 'r', encoding='utf-8').readlines()]        
        sentences_collection = []

        for dirpath, dirnames, filenames in os.walk(copus_path): 
            for filename in filenames:
                f = os.path.join(dirpath, filename)
                print (" - processing {} file: {}").format(self.file_count, f)
                result = None
                try:                
                    result = [json.loads(line) for line in io.open(f, 'r', encoding='utf-8')]
                except:
                    print (" - err in processing {} file: {}").format(self.file_count, f)
                    continue    
                sentences = []
                for dic in result:
                    if self._is_chinese(dic["value"]):
                        my_re = '[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\n]+'                        
                        clean_sentence = re.sub(my_re, "", dic["value"])

                        seg_data = jieba.cut(clean_sentence, cut_all = True)    # I am preferred to use True

                        clean_list = [i for i in seg_data if i not in stopwords]
                        clean_list = filter(None, clean_list)
#                         print clean_sentence                          
#                         for i in clean_list:
#                             print i 
#                         print clean_list
                        if len(clean_list) == 0:
                            continue 
                        sentences.append(clean_list)
                        self.sentences_count += 1
                
                self.file_count += 1
                if len(sentences) == 0:
                    self.none_chinese_file += 1
                else:
                    sentences_collection += sentences  #do NOT use append
                # in case of crashing  
                if self.file_count % 5000 == 0 and len(sentences_collection) != 0: # load is time consuming
                    self._gen_model(model_path, sentences_collection)
                    sentences_collection = []

                os.system("mv \"{}\" \"{}\"".format(f, back_up))    # so I can catch err
        
        if len(sentences_collection) != 0:
            self._gen_model(model_path, sentences_collection)                
        return
    
if __name__ == "__main__":

# https://www.jianshu.com/p/5f04e97d1b27   
# model.save_word2vec_format('/tmp/mymodel.txt',binary=False)    
    print "**** start ****"
    myEmbedding = embedding("./stopwords.txt")
    myEmbedding.gen_model("/data/literal", "/data/corpus_bak", "./model")
    myEmbedding.show_static_data()

# 电子邮件
# 电子
# 新邮件
# 电子书
# 电子邮箱
# 子书
# 新邮
# 帐户
# 邮箱
# 发送到    
#     model = gensim.models.Word2Vec.load("./model")
#     for v in model.most_similar(positive=[u'生日'], topn=20):
#         print v[0]
    print "**** done *****"
