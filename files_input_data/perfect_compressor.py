#perfect compressor

import gensim
import pickle
import re
import csv
import sys
import gzip
import logging
import numpy
import string
from numpy import linalg
from scipy.spatial import distance
from gensim.models import KeyedVectors

DECIMAL_PLACES = 0

def head_to_head_undo(vector1,vector2,length):
    newWord = []
    for i in range(length):
        newWord.append(vector1[i]+vector2[i])
    return newWord


def headToHead(word1,word2):
    newVector = []
    for i in range(0,len(word1)):
        newVector.append(word2[i]-word1[i])
    return newVector

def vectorShrinker(vector):
    newVector = []
    for entry in vector:
        newVector.append(int(round(entry)))
    return newVector  

def fileOpener(inFile):
    inFileArray = [""]
    count = 0
    index = 0
    alpha = False
    with open(inFile) as f:
        while True:
            c = f.read(1)
            if not c:
                break
            else:
                if c.isupper():
                    count += 1
                if not alpha:
                    if c.isalpha():
                        alpha = True
                        inFileArray.append(c)
                        index += 1
                    else:
                        inFileArray[index] += c 
                else:
                    if c.isalpha() == False:
                        alpha = False
                        inFileArray.append(c)
                        index += 1
                    else:
                        inFileArray[index] += c
    return inFileArray[1:]

def outArrayMaker(inFileArray, word_vectors):
    outArray = []
    for item in inFileArray:
            if item.lower() in word_vectors.vocab:
                vector = [0] * length
                for i in range(len(item)):
                    if item[i].isupper():
                        vector.append(i)
                outArray.append(vector)
            else:
                outArray.append(item)
    return outArray

def decapitalizer(inFileArray):
    newArray = []
    for item in inFileArray:
        newArray.append(item.lower())
    return newArray

def indexGetter(array,index):
    for item in array[index+1:]:
        if isinstance(item,list):
            return array.index(item)



logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def vectorDictionaryMaker(inArray,noStop = True):
    vecDict = dict()
    for i in inArray:
        vecDict["vecs"+str(i)+"_nostop"] = KeyedVectors.load("vecs"+str(i)+"_nostop.kv", mmap='r')
    return vecDict

def fileCompressor(inFileArray,vecDict):
    for string, vector in vecDict.items():
        word_vectors = vector
        length = int(re.findall("\d+",string)[0])
        fileDictionary = {}
        outArray = outArrayMaker(inFileArray,word_vectors)
        decapArray = decapitalizer(inFileArray)
        firstWord = True
        i = 0
        while i in range(len(decapArray)):
            if firstWord:
                if decapArray[i] not in word_vectors.vocab:
                    continue
                else:
                    # CHANGE THIS TO BE LESS SLOPPY CALL FUNCTION
                    outArray[i][:length] = vectorShrinker(word_vectors[decapArray[i]])
                    firstWord = False
            newVector1 = vectorShrinker(word_vectors[decapArray[i]])
            newIndex = indexGetter(outArray,i)
            if newIndex == None:
                break
            newVector2 = vectorShrinker(word_vectors[decapArray[newIndex]])
            vectorBetween = headToHead(newVector1,newVector2)
            outArray[newIndex][:length] = vectorBetween
            fileDictionary[decapArray[i]] = newVector1
            fileDictionary[decapArray[newIndex]] = newVector2
            i = newIndex
        with open("pickle_dictionary_"+string+".p", 'wb') as f:  
            pickle.dump(fileDictionary, f)
        f.close()
        with open("vectors_out_"+string+".txt", 'w') as g:
            for item in outArray:
                g.write("%s\n"%item)
        g.close()

# NEED TO HANDLE MULTIPLE SPACES, BAD(NO) SPACES.. COULD USE "IS ALPHA??"
# Inting vectors doesnt work, need to use different rounding.

def driver():
    inFile = "review1.txt"
    inFileArray = fileOpener(inFile)
    numArray = [4,5,6]
    vectorDict = vectorDictionaryMaker(numArray)
    fileCompressor(inFileArray,vectorDict)
    sys.exit("ALL DONE")