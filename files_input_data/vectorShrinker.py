# vectorShrinker.py
from gensim.models import KeyedVectors
import numpy
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def vectorShrinker(modelFilename,precision=0,normalized=False):
    """ Takes a vector model and truncates the vectors for each word to the given precision. 
        Much help from: https://stackoverflow.com/questions/46647945/how-to-manually-change-the-vector-dimensions-of-a-word-in-gensim-word2vec
    """
    Unique = False
    while not Unique:
        logging.info("Current precision is to {0} decimal places.".format(precision))
        model = KeyedVectors.load(modelFilename, mmap='r')
        rounder(model,precision,normalized)
        Unique = checkUnique(model)
        if Unique:
            model.save("unique_"+modelFilename)
            return 0
        elif precision >= 9:
            return 1
        precision += 1

def rounder(model,precision,normalized):
    """ Handles in-place rounding of all vectors in a model. """

    for i in range(0,len(model.vocab)):
            if not normalized:
                model.wv.syn0[i] = numpy.round(model.wv.syn0[i],precision)

def checkUnique(model):
    """ Checks all vectors against each other for uniqueness. """
    
    for j in range(0,len(model.vocab)):
        if j % 1000 == 0:
            logging.info ("checked {0} words".format (j))
        for k in range(0,len(model.vocab)):
            if k % 20000 == 0:
                logging.info ("checked against {0} words".format(k))
            if j == k:
                continue
            else:
                if numpy.array_equal(model.wv.syn0[j],model.wv.syn0[k]):
                    return False
    return True