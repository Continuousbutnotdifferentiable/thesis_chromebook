from gensim.models import KeyedVectors
import numpy as np
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def makeUniqueModel(modelFilename,precision=0):
    """ Takes a vector model and truncates the vectors until all vectors are unique. 
    Much help from: https://stackoverflow.com/questions/46647945/how-to-manually-change-the-vector-dimensions-of-a-word-in-gensim-word2vec
    """
    mapping = [0,1]
    model = rounder(modelFilename,precision)
    
    while len(mapping)> 0:
        print("The number of duplicates is:", len(mapping))
        mapping = numpyGetUniqueIndices(modelToArray(model))
        if len(mapping) > 0:
            precision += 1
            newModel = rounder(modelFilename,precision)
            for i in mapping:
                model.wv.syn0[i] = newModel.wv.syn0[i]
        else:
            model.save(modelFilename)
            return model



def modelToArray(model):
    """ Takes a model and returns a numpy array of its vectors. """

    npArray = np.zeros(shape=(len(model.vocab),model.wv.syn0[0].shape[0]))
    
    for i in range(0,len(model.vocab)):
        npArray[i] = model.wv.syn0[i]
    return npArray

def rounder(modelFilename,precision):
    """ Returns a model with rounding of all vectors in a model up to input precision. """


    logging.info("Current precision: {0}.".format(precision))

    model = KeyedVectors.load(modelFilename, mmap='r')
    for i in range(0,len(model.vocab)):
        model.wv.syn0[i] = np.round(model.wv.syn0[i],precision)
    return model

def numpyGetUniqueIndices(array):
    """ Takes a numpy array and returns an array of elements with duplicate indices. 
    developed with help from:
    https://stackoverflow.com/questions/49342589/get-indices-of-unique-values-in-numpy
    and
    https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
    """
    
    numVecs = len(array)
    a,indices = np.unique(array,return_index = True, axis=0)
    indexList = np.arange(numVecs)
        
    if numVecs > len(indices):
        logging.info("Current number of duplicates: {0}.".format(numVecs - len(indices)))
        return np.setdiff1d(indexList,indices)
    else:
        return []
