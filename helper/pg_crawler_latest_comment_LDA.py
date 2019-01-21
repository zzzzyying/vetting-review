from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
from pymongo import MongoClient
from langdetect import detect

# landetect later

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()
    
# create sample documents
client = MongoClient('mongodb://192.168.10.143:27017')
review_db = client['pg_crawler']

doc_set = []
for ireview in review_db['comment'].find({"usr_star": "1"}):
    # compile sample documents into a list
    lan = ""
    r_raw = ireview["usr_comment"]
    try:
        lan = detect(r_raw)
    except:
        lan = ""  
    if lan == "en":    
        doc_set.append(ireview["usr_comment"])

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
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=20, id2word = dictionary, passes=20)

print(ldamodel.print_topics(num_topics=20, num_words=4))
