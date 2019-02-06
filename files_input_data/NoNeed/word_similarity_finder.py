import pickle
import gensim
import sys
import gzip
import logging
from gensim.models import KeyedVectors

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# List of ntlkStopwords current as of July 6, 2018
ntlkStopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'youre', 'youve', 'youll', 'youd', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'shes', 'her', 'hers', 'herself', 'it', 'its', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'thatll', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'dont', 'should', 'shouldve', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'arent', 'couldn', 'couldnt', 'didn', 'didnt', 'doesn', 'doesnt', 'hadn', 'hadnt', 'hasn', 'hasnt', 'haven', 'havent', 'isn', 'isnt', 'ma', 'mightn', 'mightnt', 'mustn', 'mustnt', 'needn', 'neednt', 'shan', 'shant', 'shouldn', 'shouldnt', 'wasn', 'wasnt', 'weren', 'werent', 'won', 'wont', 'wouldn', 'wouldnt']


inFile = sys.argv[1]



word_vectors_50_nostop = KeyedVectors.load("vecs_50_nostop.kv", mmap='r')
word_vectors_200_nostop = KeyedVectors.load("vecs_200_nostop.kv", mmap='r')

word_vectors_50 = KeyedVectors.load("vecs_50.kv", mmap='r')
word_vectors_200 = KeyedVectors.load("vecs_200.kv", mmap='r')


word_vectors_nostop = word_vectors_50_nostop

def read_input(input_file):
    """This function reads the input file which is in gzip format"""
    
    logging.info("reading file {0}...this may take a while".format(input_file))
    
    with gzip.open (input_file, 'rb') as f:
        for i, line in enumerate (f): 

            if (i%10000==0):
                logging.info ("read {0} reviews".format (i))
            # do some pre-processing and return a list of words for each review text
            yield gensim.utils.simple_preprocess (line)

def getSimilarity(item):
    return item[2]


documents = list (read_input (inFile))

for doc in documents:
        for word in doc:
            if word in ntlkStopwords:
                doc.remove(word)

#Stopwords 50 Version

dissimilarList = []
similarList = []


word_vectors = word_vectors_50
for file in range(0,30):
    fileList = []
    for i in range(0,len(documents[file])-1):
        if documents[file][i] in word_vectors_nostop.vocab and documents[file][i+1] in word_vectors_nostop.vocab:
            if (word_vectors.similarity(documents[file][i],documents[file][i+1])) <= .09 and (word_vectors.similarity(documents[file][i],documents[file][i+1])) >= .08:
                dissimilarList.append((documents[file][i],documents[file][i+1],word_vectors.similarity(documents[file][i],documents[file][i+1])))
            if (word_vectors.similarity(documents[file][i],documents[file][i+1])) <= .95 and (word_vectors.similarity(documents[file][i],documents[file][i+1])) >= .7:
                similarList.append((documents[file][i],documents[file][i+1],word_vectors.similarity(documents[file][i],documents[file][i+1])))

dissimilarList = sorted(dissimilarList[1:],key=getSimilarity)
similarList = sorted(similarList[1:],key=getSimilarity)

dissimilarList.insert(0,("n = 50 | stopped | similarity between .08 and .09"))
similarList.insert(0,("n = 50 | stopped | similarity between .7 and .95"))

with open("dissimilar_50_stop.txt",'w') as f:
    f.write("%s\n" % dissimilarList[0])
    for item in dissimilarList[1:]:
        f.write(' '.join(str(s) for s in item) + '\n')

with open("similar_50_stop.txt",'w') as f:
    f.write("%s\n" % similarList[0])
    for item in similarList[1:]:
        f.write(' '.join(str(s) for s in item) + '\n')

#Stopwords 200 Version

dissimilarList = []
similarList = []

word_vectors = word_vectors_200

for file in range(0,30):
    fileList = []
    for i in range(0,len(documents[file])-1):
        if documents[file][i] in word_vectors_nostop.vocab and documents[file][i+1] in word_vectors_nostop.vocab:
            if (word_vectors.similarity(documents[file][i],documents[file][i+1])) <= .09 and (word_vectors.similarity(documents[file][i],documents[file][i+1])) >= .08:
                dissimilarList.append((documents[file][i],documents[file][i+1],word_vectors.similarity(documents[file][i],documents[file][i+1])))
            if (word_vectors.similarity(documents[file][i],documents[file][i+1])) <= .95 and (word_vectors.similarity(documents[file][i],documents[file][i+1])) >= .7:
                similarList.append((documents[file][i],documents[file][i+1],word_vectors.similarity(documents[file][i],documents[file][i+1])))

dissimilarList = sorted(dissimilarList[1:],key=getSimilarity)
similarList = sorted(similarList[1:],key=getSimilarity)

dissimilarList.insert(0,("n = 200 | stopped | similarity between .08 and .09"))
similarList.insert(0,("n = 200 | stopped | similarity between .7 and .95"))

with open("dissimilar_200_stop.txt",'w') as f:
    f.write("%s\n" % dissimilarList[0])
    for item in dissimilarList[1:]:
        f.write(' '.join(str(s) for s in item) + '\n')

with open("similar_200_stop.txt",'w') as f:
    f.write("%s\n" % similarList[0])
    for item in similarList[1:]:
        f.write(' '.join(str(s) for s in item) + '\n')


#noStop 50 Version

dissimilarList = []
similarList = []

word_vectors = word_vectors_50_nostop
for file in range(0,30):
    fileList = []
    for i in range(0,len(documents[file])-1):
        if documents[file][i] in word_vectors_nostop.vocab and documents[file][i+1] in word_vectors_nostop.vocab:
            if (word_vectors.similarity(documents[file][i],documents[file][i+1])) <= .09 and (word_vectors.similarity(documents[file][i],documents[file][i+1])) >= .08:
                dissimilarList.append((documents[file][i],documents[file][i+1],word_vectors.similarity(documents[file][i],documents[file][i+1])))
            if (word_vectors.similarity(documents[file][i],documents[file][i+1])) <= .95 and (word_vectors.similarity(documents[file][i],documents[file][i+1])) >= .7:
                similarList.append((documents[file][i],documents[file][i+1],word_vectors.similarity(documents[file][i],documents[file][i+1])))

dissimilarList = sorted(dissimilarList[1:],key=getSimilarity)
similarList = sorted(similarList[1:],key=getSimilarity)

dissimilarList.insert(0,("n = 50 | noStop | similarity between .08 and .09"))
similarList.insert(0,("n = 50 | noStop | similarity between .7 and .95"))

with open("dissimilar_50_nostop.txt",'w') as f:
    f.write("%s\n" % dissimilarList[0])
    for item in dissimilarList[1:]:
        f.write(' '.join(str(s) for s in item) + '\n')

with open("similar_50_nostop.txt",'w') as f:
    f.write("%s\n" % similarList[0])
    for item in similarList[1:]:
        f.write(' '.join(str(s) for s in item) + '\n')

#Stopwords 200 Version

dissimilarList = []
similarList = []

word_vectors = word_vectors_200_nostop

for file in range(0,30):
    fileList = []
    for i in range(0,len(documents[file])-1):
        if documents[file][i] in word_vectors_nostop.vocab and documents[file][i+1] in word_vectors_nostop.vocab:
            if (word_vectors.similarity(documents[file][i],documents[file][i+1])) <= .09 and (word_vectors.similarity(documents[file][i],documents[file][i+1])) >= .08:
                dissimilarList.append((documents[file][i],documents[file][i+1],word_vectors.similarity(documents[file][i],documents[file][i+1])))
            if (word_vectors.similarity(documents[file][i],documents[file][i+1])) <= .95 and (word_vectors.similarity(documents[file][i],documents[file][i+1])) >= .7:
                similarList.append((documents[file][i],documents[file][i+1],word_vectors.similarity(documents[file][i],documents[file][i+1])))


dissimilarList = sorted(dissimilarList[1:],key=getSimilarity)
similarList = sorted(similarList[1:],key=getSimilarity)

dissimilarList.insert(0,("n = 200 | noStop | similarity between .08 and .09"))
similarList.insert(0,("n = 200 | noStop | similarity between .7 and .95"))

with open("dissimilar_200_nostop.txt",'w') as f:
    f.write("%s\n" % dissimilarList[0])
    for item in dissimilarList[1:]:
        f.write(' '.join(str(s) for s in item) + '\n')

with open("similar_200_nostop.txt",'w') as f:
    f.write("%s\n" % similarList[0])
    for item in similarList[1:]:
        f.write(' '.join(str(s) for s in item) + '\n')

