import numpy as np
import pickle

count = 0

inPickle = "pickle_dictionary_vecs_75_.p"
compressionDictionary = pickle.load(open(inPickle,'rb'))
badVec = [0]*75
for word, vector in compressionDictionary.items():
    if not np.allclose(badVec,vector,atol=1e-01):
        for word2,vector2 in compressionDictionary.items():
            if word != word2:
                if np.allclose(vector2,vector,atol=1e-01):
                    print(word," ",word2)
                    print(vector)
    else:
        print(word)