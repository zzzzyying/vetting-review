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

import io
import multiprocessing

from pymongo import MongoClient
from langdetect import detect

import langid
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords


def gen_model(model_path, sentences_collection):
    if os.path.isfile(model_path):
        model = Word2Vec.load(model_path)  
        model.build_vocab(sentences_collection, update = True)
    else:
        model = Word2Vec(sentences_collection, min_count = 1, workers = multiprocessing.cpu_count()-2)                                        
    model.train(sentences_collection, total_examples=len(sentences_collection), epochs=model.iter)  
      
    if model != None:            
        model.save(model_path)           
    return
 
def main():
    print "**** start ****"   
    logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')     

    clean_corpus = []
    stopWords = set(stopwords.words('english'))
    client = MongoClient('mongodb://192.168.10.143:27017')
    reivew_db = client['pg_crawler']
#    reivew_db = client['comment']
    
    review_collection = reivew_db.comment.find()
#    review_collection = reivew_db.us_appstore_apps_comment.find()

    model_path = "./googleplay_review_embedding_eng"    
#    model_path = "./ios_review_embedding_eng"
        
    status = 0
    valid_status = 0
    print "**** collecting review ****"     

    for r in review_collection:
        status += 1
        clean_sentence = []
        #review = r['usr_comment'].lower()
        review = r['usr_comment']
        #print r['usr_comment']
        if langid.classify(review)[0] == 'en':
            #print i['usr_comment']
            corpus = word_tokenize(review)
   
            for w in corpus:
                if w not in stopWords:
                    clean_sentence.append(w)
        
        if len(clean_sentence) != 0:
            clean_corpus.append(clean_sentence)
            valid_status += 1
            #print clean_corpus   
        if status % 10000 == 0 and len(clean_corpus) != 0:
            print (" - total: {}, valid: {}\n").format(status, valid_status)  
            gen_model(model_path, clean_corpus)
            clean_corpus = []
    
    if len(clean_corpus) != 0:
        gen_model(model_path, clean_corpus)
    print (" - total: {}, valid: {}\n").format(status, valid_status)      
    print "**** done *****"              
if __name__ == "__main__":
    
    main()
    model = gensim.models.Word2Vec.load("./googleplay_review_embedding_eng")
    for v in model.most_similar(positive=[u'scam'], topn=20):
        print v[0]
'''
with lower()

fake
bs
rip
stupid
trust
51₹
joke
idiot
greedy
regret
useless
reapeat
wants
company
garbage
rubbish
ya
excpect
waste
comments
'''    

'''
without lower()

fake
idiots
bs
joke
garbage
payed
trash
lie
legit
Scam
banned
trust
stupid
shame
rubbish
waste
rip
obviously
advertise
steal
bogus
huh
cheating
fraud
charged
company
charge
con
😡
jelly

'''
