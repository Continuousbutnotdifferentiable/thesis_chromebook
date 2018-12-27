import pickle
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

inFile = "review1.txt"

word_vectors_5 = KeyedVectors.load("vecs_5_nostop.kv", mmap='r')
#word_vectors_10 = KeyedVectors.load("vecs_10_nostop.kv",mmap='r')
'''
word_vectors_35 = KeyedVectors.load("vecs_35_nostop.kv", mmap='r')
word_vectors_45 = KeyedVectors.load("vecs_45_nostop.kv", mmap='r')
word_vectors_55 = KeyedVectors.load("vecs_55_nostop.kv", mmap='r')
word_vectors_65 = KeyedVectors.load("vecs_65_nostop.kv", mmap='r')
word_vectors_75 = KeyedVectors.load("vecs_75_nostop.kv", mmap='r')
'''
    
vectorDictionary = {"vecs_05_":word_vectors_5}

distanceFunctionDictionary = {"head_to_head_":headToHead}

inFileArray = fileOpener(inFile)

for string, vector in vectorDictionary.items():
    word_vectors = vector
    length = int(string[5:7])
    fileDictionary = {}
    for functionName, function in distanceFunctionDictionary.items():
        outArray = outArrayMaker(inFileArray,word_vectors)
        decapArray = decapitalizer(inFileArray)
        firstWord = True
        i = 0
        for i in range(len(decapArray)):
            if decapArray[i] in word_vectors.vocab:
                newVector1 = vectorShrinker(word_vectors[decapArray[i]])
                outArray[i][:length] = newVector1
                fileDictionary[decapArray[i]] = newVector1
        with open("pickle_dictionary_"+string+".p", 'wb') as f:  
            pickle.dump(fileDictionary, f)
        f.close()
        with open("vectors_out_nohead_"+string+".txt", 'w') as g:
            for item in outArray:
                g.write("%s\n"%item)
        g.close()