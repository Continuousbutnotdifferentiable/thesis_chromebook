# imports needed and logging
import pickle
import csv
import gzip
import gensim 
import logging
import sys
from gensim.parsing.preprocessing import preprocess_string
from gensim.test.utils import get_tmpfile
from gensim.models import KeyedVectors
 
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# List of ntlkStopwords current as of July 6, 2018
ntlkStopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'youre', 'youve', 'youll', 'youd', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'shes', 'her', 'hers', 'herself', 'it', 'its', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'thatll', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'dont', 'should', 'shouldve', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'arent', 'couldn', 'couldnt', 'didn', 'didnt', 'doesn', 'doesnt', 'hadn', 'hadnt', 'hasn', 'hasnt', 'haven', 'havent', 'isn', 'isnt', 'ma', 'mightn', 'mightnt', 'mustn', 'mustnt', 'needn', 'neednt', 'shan', 'shant', 'shouldn', 'shouldnt', 'wasn', 'wasnt', 'weren', 'werent', 'won', 'wont', 'wouldn', 'wouldnt']

# Sysarg must be a .txt.gz
inFile  = sys.argv[1]
nostop = True

# Setup string names for file io
string45 = "vecs_45"
string55 = "vecs_55"
string60 = "vecs_60"
string65 = "vecs_65"
string70 = "vecs_70"
string75 = "vecs_75"
nostopstring = "_nostop"

# Unpickle the documents list
documents = pickle.load(open(inFile,'rb'))

# Trains 4 models using vector sizes 45, 55, 60, 65, 70 and 75
model45 = gensim.models.Word2Vec(documents,size=45,window=10,min_count=2,workers=10)
model45.train(documents, total_examples=len(documents), epochs=10)
word_vectors_45 = model45.wv

model55 = gensim.models.Word2Vec(documents,size=55,window=10,min_count=2,workers=10)
model55.train(documents, total_examples=len(documents), epochs=10)
word_vectors_55 = model55.wv

model60 = gensim.models.Word2Vec(documents,size=60,window=10,min_count=2,workers=10)
model60.train(documents, total_examples=len(documents), epochs=10)
word_vectors_60 = model60.wv

model65 = gensim.models.Word2Vec(documents,size=65,window=10,min_count=2,workers=10)
model65.train(documents, total_examples=len(documents), epochs=10)
word_vectors_65 = model65.wv

model70 = gensim.models.Word2Vec(documents,size=70,window=10,min_count=2,workers=10)
model70.train(documents, total_examples=len(documents), epochs=10)
word_vectors_70 = model70.wv

model75 = gensim.models.Word2Vec(documents,size=75,window=10,min_count=2,workers=10)
model75.train(documents, total_examples=len(documents), epochs=10)
word_vectors_75 = model75.wv

if nostop:
    word_vectors_45.save(string45+nostopstring+".kv")
    word_vectors_55.save(string55+nostopstring+".kv")
    word_vectors_60.save(string60+nostopstring+".kv")
    word_vectors_65.save(string65+nostopstring+".kv")
    word_vectors_70.save(string70+nostopstring+".kv")
    word_vectors_75.save(string75+nostopstring+".kv")

else:
    word_vectors_45.save(string45+".kv")
    word_vectors_55.save(string55+".kv")
    word_vectors_60.save(string60+".kv")
    word_vectors_65.save(string65+".kv")
    word_vectors_70.save(string70+".kv")
    word_vectors_75.save(string75+".kv")