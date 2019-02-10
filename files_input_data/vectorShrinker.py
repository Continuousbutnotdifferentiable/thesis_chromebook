# vectorShrinker.py
from gensim.models import KeyedVectors
import numpy as np
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
        npArray = modelToArray(model)
        Unique = npArrayUniqueChecker(npArray)
        if Unique:
            model.save("unique_"+str(precision)+modelFilename)
            return 0
        elif precision > 8:
            return 1
        precision += 1

def rounder(model,precision,normalized):
    """ Handles in-place rounding of all vectors in a model. """

    for i in range(0,len(model.vocab)):
            if not normalized:
                model.wv.syn0[i] = np.round(model.wv.syn0[i],precision)

def npArrayUniqueChecker(array):
    """ Takes an array of arrays and returns a boolean value if all the vectors in 
    the new numpy array are unique. """

    npArray = np.zeros(shape=(len(array),len(array[0])))
    # This step is redundant, but it makes the code portable
    for i in range(0,len(array)):
        npArray[i] = array[i]

    uniqueArray = np.unique(npArray, axis=0)
    
    if len(npArray) == len(uniqueArray):
        return True
    return False

def modelToArray(model):
    """ Takes a model and returns a numpy array of its vectors. """

    npArray = np.zeros(shape=(len(model.vocab),model.wv.syn0[0].shape[0]))
    for i in range(0,len(model.vocab)):
        npArray[i] = model.wv.syn0[i]
    return npArray
