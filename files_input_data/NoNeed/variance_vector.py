# variance_checker.py

import gensim
import pickle
import csv
import sys
import gzip
import logging
import numpy
from numpy import linalg
from scipy.spatial import distance
from gensim.models import KeyedVectors

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def headToHead(word1,word2):
    newVec = []
    for i in range(0,len(word1)):
        newVec.append(word2[i]-word1[i])
    return newVec

inFile = sys.argv[1]
nostop = True
if nostop:
    word_vectors_25 = KeyedVectors.load("vecs_25_nostop.kv", mmap='r')
    word_vectors_35 = KeyedVectors.load("vecs_35_nostop.kv", mmap='r')
    word_vectors_45 = KeyedVectors.load("vecs_45_nostop.kv", mmap='r')
    word_vectors_55 = KeyedVectors.load("vecs_55_nostop.kv", mmap='r')
    word_vectors_65 = KeyedVectors.load("vecs_65_nostop.kv", mmap='r')
    word_vectors_75 = KeyedVectors.load("vecs_75_nostop.kv", mmap='r')
    
vectorDictionary = {"vecs_25_":word_vectors_25, "vecs_35_":word_vectors_35, "vecs_45_":word_vectors_45,
                    "vecs_55_":word_vectors_55, "vecs_65_":word_vectors_65, "vecs_75_":word_vectors_75}

distanceFunctionDictionary = {"head_to_head_":headToHead}

print("Vectors Loaded")

documents = pickle.load(open(inFile,'rb'))

for string, vector in vectorDictionary.items():
    word_vectors = vector
    fileDictionary = {}
    for functionName, function in distanceFunctionDictionary.items():
        fileArray = []
        absArray =[]
        varianceArray = []
        for file in range(0,99):    
            for i in range(0,len(documents[file])-1):
                if documents[file][i] in word_vectors.vocab and documents[file][i+1] in word_vectors.vocab:
                    vector1 = word_vectors[documents[file][i]] 
                    vector2 = word_vectors[documents[file][i+1]] 
                    vectorBetween = function(vector1,vector2)
                    varianceArray.append(numpy.var(vectorBetween,dtype=numpy.float64))
        varNumpyArray = numpy.array(varianceArray,dtype=numpy.float64)
        mean = numpy.mean(varNumpyArray,axis=0,dtype=numpy.float64)
        stDev = numpy.std(varNumpyArray,axis=0,dtype=numpy.float64)
        threeStDev = 3 * stDev
        lo = mean - (2*stDev)
        hi = mean + threeStDev
        loArray = ["Words With Variance Lower than .2 and "+" "+string]
        hiArray = ["Words With Variance Higher than 3 StDev"+" "+string]
        for file in range(0,99):    
            for i in range(0,len(documents[file])-1):
                if documents[file][i] in word_vectors.vocab and documents[file][i+1] in word_vectors.vocab:
                    vector1 = word_vectors[documents[file][i]] 
                    vector2 = word_vectors[documents[file][i+1]]
                    words = documents[file][i] + " " + documents[file][i+1] 
                    vectorBetween = function(vector1,vector2)
                    variance = numpy.var(vectorBetween,dtype=numpy.float64)
                    if variance > hi:
                        hiArray.append(words)
                    if variance < .2:
                        loArray.append(words)

        if functionName == "head_to_head_":
            with open(functionName+'lo_variance_'+string+".txt","w") as f:
                for item in loArray:
                    f.write("%s\n" % item)
            f.close()
            with open(functionName+'hi_variance_'+string+".txt","w") as f:
                for item in hiArray:
                    f.write("%s\n" % item)
            f.close() 
        