from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from TurkishStemmer import TurkishStemmer
from gensim import corpora, models
import gensim
from pymongo import MongoClient
from langdetect import detect
from collections import Counter
from itertools import chain
import thulac
from progress.bar import Bar
# landetect later
tokenizer = RegexpTokenizer(r'\w+')
# create English stop words list
# en_stop = get_stop_words('en')
# Create p_stemmer of class PorterStemmer
# p_stemmer = PorterStemmer()

def lda(doc_set,num_topics,num_words,passes):#for EN only
    texts=gen_corpus('EN',doc_set)
    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts)
    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts]
    # generate LDA model
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word = dictionary, passes=passes)
    print(ldamodel.print_topics(num_topics=num_topics, num_words=num_words))
    return
    
def count_corpus(doc_set):
    t=list(chain.from_iterable(doc_set))
    c=Counter(t)
    print(c.most_common(1000))
    return
    
def count(lan,doc_set):#for EN only
    texts=gen_corpus(lan,doc_set)
    count_corpus(texts)
    return
    
def gen_corpus(lan,doc_set):
    # list for tokenized documents in loop
    texts = []
    bar = Bar('Generating '+lan+' corpus', max=len(doc_set))
    if lan=='CN':
        thu1 = thulac.thulac(seg_only=False)  #默认模式
        with open("./stopword_cn.txt", encoding='UTF-8') as f:
            lines = f.read().splitlines()
            stopwords=sorted(set(lines))
        for i in doc_set:
            text = thu1.cut(i, text=False)  #进行一句话分词
            l = [item[0] for item in text]
        # print(l)
            # for i in b:
            #     print (i)
            stemmed = [i for i in l if i not in stopwords]
            # texts.append(l)
            texts.append(stemmed)
            bar.next()
        # print (stemmed)
        bar.finish()
    if lan in ['EN','RU','TR']:
        # loop through document list
        for i in doc_set:
            # clean and tokenize document string
            raw = i.lower()
            tokens = tokenizer.tokenize(raw)
            # remove stop words from tokens
            stopped_tokens = [i for i in tokens if not i in get_stop_words(lan.lower())]
            # stem tokens
            stemmer = PorterStemmer()
            if lan =='EN':
                stemmer = PorterStemmer()
            if lan =='RU':
                stemmer = SnowballStemmer("russian")
            if lan =='TR':
                stemmer = TurkishStemmer()
            stemmed_tokens = [stemmer.stem(i) for i in stopped_tokens]
            # add tokens to list
            texts.append(stemmed_tokens)
            bar.next()
        bar.finish()
    bar.finish()
    return texts
    
def show_revelant(keywords,corpus):
    l = dict.fromkeys(keywords, [])
    r = dict.fromkeys(keywords, [])
    for i in keywords:
        for j in corpus:
            if i in j:
                # print (i, j)
                k=j.index(i)
                try:
                    l[i].append(j[k-1])
                except IndexError:
                    l[i].append('#start#')
                try:
                    r[i].append(j[k+1])
                except IndexError:
                    r[i].append('#end#')
        print('Left of '+i+' :')
        print(Counter(l[i]).most_common(100))
        print('Right of '+i+' :')
        print(Counter(r[i]).most_common(100))
    return l,r