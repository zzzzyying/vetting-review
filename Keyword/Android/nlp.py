from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
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
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

def lda(doc_set,num_topics,num_words,passes):#for EN only
    # list for tokenized documents in loop
    texts = []
    
    # loop through document list
    for i in doc_set:
        
        # clean and tokenize document string
        raw = i.lower()
        tokens = tokenizer.tokenize(raw)
    
        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if not i in en_stop]
        
        # stem tokens
        stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
        
        # add tokens to list
        texts.append(stemmed_tokens)
    
    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts)
        
    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts]
    
    # generate LDA model
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word = dictionary, passes=passes)
    
    print(ldamodel.print_topics(num_topics=num_topics, num_words=num_words))
    return
    
def count(doc_set):#for EN only
    # list for tokenized documents in loop
    texts = []
    
    # loop through document list
    for i in doc_set:
        
        # clean and tokenize document string
        raw = i.lower()
        tokens = tokenizer.tokenize(raw)
    
        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if not i in en_stop]
        
        # stem tokens
        stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
        
        # add tokens to list
        texts.append(stemmed_tokens)
    # print (texts)
    
    t=list(chain.from_iterable(texts))
    c=Counter(t)
    print(c.most_common(1000))
    return

def count_cn(doc_set):#for CH only
    # print (doc_set)
    texts = []
    thu1 = thulac.thulac(seg_only=False)  #默认模式
    with open("./stopword_cn.txt", encoding='UTF-8') as f:
        lines = f.read().splitlines()
        stopwords=sorted(set(lines))
    bar = Bar('Processing', max=len(doc_set))
    for i in doc_set:
        text = thu1.cut(i, text=False)  #进行一句话分词
        l = [item[0] for item in text]
    # print(l)
        # for i in b:
        #     print (i)
        stemmed = [i for i in l if i not in stopwords]
        texts.append(stemmed)
        bar.next()
    # print (stemmed)
    bar.finish()
    t=list(chain.from_iterable(texts))
    c=Counter(t)
    print(c.most_common(1000))
    return
