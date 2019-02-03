# imports needed and logging
import pickle
import gzip
import gensim 
import logging
import sys
from gensim.parsing.preprocessing import remove_stopwords
from gensim.test.utils import get_tmpfile
from gensim.models import KeyedVectors

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# List of ntlkStopwords current as of July 6, 2018
NTLK_STOPWORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'youre', 'youve', 'youll', 'youd', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'shes', 'her', 'hers', 'herself', 'it', 'its', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'thatll', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'dont', 'should', 'shouldve', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'arent', 'couldn', 'couldnt', 'didn', 'didnt', 'doesn', 'doesnt', 'hadn', 'hadnt', 'hasn', 'hasnt', 'haven', 'havent', 'isn', 'isnt', 'ma', 'mightn', 'mightnt', 'mustn', 'mustnt', 'needn', 'neednt', 'shan', 'shant', 'shouldn', 'shouldnt', 'wasn', 'wasnt', 'weren', 'werent', 'won', 'wont', 'wouldn', 'wouldnt']

# Sysarg must be a .txt.gz
if len(sys.argv) > 1:
    inFile  = sys.argv[1]

# Unpickle the documents list
def readInput(inputFile, pickleOut=True, noStop = True):
    """This function reads the input file which is in gzip format"""
    
    if inputFile.endswith(".txt.gz"):
        logging.info("file {0} opened. Preprocessing and pickling.".format(inputFile))
        outFile = inputFile[:-7]+".p"
    
    else:
        logging.info("file {0} could not be opened. file extension needs to be .txt.gz".format(inputFile))
        sys.exit("please use the correct file extension.")

    logging.info("reading file {0}...this may take a while".format(inputFile))
    documents = []
    with gzip.open (inputFile, 'rb') as f:
        for i, line in enumerate (f):

            if (i%10000==0):
                logging.info ("read {0} reviews".format (i))
            # do some pre-processing and return a list of words for each review text
            documents.append(gensim.utils.simple_preprocess (line))
    print(documents[1])
    print(documents[2])

    if noStop:
        documents = removeStopwords(documents)

    print(documents[1])
    print(documents[2])
    if pickleOut:
        with open(outFile, 'wb') as f:
            pickle.dump(documents, f)
        f.close()
    
    return documents


def trainVecs(dimensionList, documents, noStop = True, numEpochs = 15):
    for i in dimensionList:
        outString = "vecs"+str(i)
        if noStop:
            outString += "_nostop"
        model = gensim.models.Word2Vec(documents,size=i,window=7,min_count=2,workers=10)
        model.train(documents, total_examples=len(documents), epochs=numEpochs)
        word_vectors = model.wv
        word_vectors.save(outString+".kv")

def removeStopwords(docsList):
    newList = []
    for doc in docsList:
        copyList = []
        for word in doc:
            if len(remove_stopwords(word)) > 0:
                copyList.append(remove_stopwords(word))
        if len(copyList) > 0:    
            newList.append(copyList)
    return newList

def driver():
    documents = readInput("reviews_data.txt.gz")
    numList = [4,5,6,300,500]
    trainVecs(numList,documents)
    sys.exit("ALL DONE")