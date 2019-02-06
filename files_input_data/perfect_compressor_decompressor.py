#perfect compressor
import ast
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

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def headToHeadUndo(vector1,vector2,length):
    """Undos the HeadToHead operation for decompression"""
    newWord = []
    for i in range(length):
        newWord.append(vector1[i]+vector2[i])
    return newWord

def intxtToArray(inVectors):
    """Takes .txt file of vectors and literals and parses them into new array"""
    with open(inVectors,"r+") as f:
        readList = f.readlines()
    outArray = []
    for item in readList:
        # Handles arrays
        if item[0] == '[':
            outArray.append(ast.literal_eval(item))
        # Handles literals removing newlines
        else:
            # itemCopy = item[:-1] no idea why this line is here...
            outArray.append(item[:-1])
    f.close()
    return outArray

def vectorProcessor(vector,dictionary,length):
    """ Takes a vector and a dictionary of words and vectors and returns the corresponding word correctly cased"""
    word = ''
    for dWord, dVector in dictionary.items():
        if numpy.allclose(vector[:length],dVector,atol=1e-01):
            for i in range(len(dWord)):
                # Handles capitalization
                if i in vector[length:]:
                    word += dWord[i].upper()
                else:
                    word += dWord[i]
    return word

def headToHead(word1,word2):
    """ Does tip to tail operation to determine the vector between words"""
    newVector = []
    for i in range(0,len(word1)):
        newVector.append(word2[i]-word1[i])
    return newVector

def vectorShrinker(vector):
    """ Makes vectors with integer precision """
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

def outArrayMaker(inFileArray, word_vectors,length):
    """ Takes the vector for a word and handles the uppercase letter 
    (stores that information inside the vector)
    
    """
    outArray = []
    for item in inFileArray:
            if item.lower() in word_vectors.vocab:
                vector = [0] * length
                for i in range(len(item)):
                    # Checks case and appends the index for decompression
                    if item[i].isupper():
                        vector.append(i)
                outArray.append(vector)
            else:
                # Otherwise appends literal
                outArray.append(item)
    return outArray

def decapitalizer(inFileArray):
    """ Decapitalizes all the words in the file array """
    newArray = []
    for item in inFileArray:
        newArray.append(item.lower())
    return newArray

def indexGetter(array,index):
    """ Gets the index of the next vectorized word"""
    for item in array[index+1:]:
        if isinstance(item,list):
            return array.index(item)

def vectorDictionaryMaker(inArray,noStop = True):
    """ Opens the keyed vectors and saves them into a dictionary """
    vecDict = dict()
    for i in inArray:
        vecDict["vecs"+str(i)+"_nostop"] = KeyedVectors.load("vecs"+str(i)+"_nostop.kv", mmap='r')
    return vecDict

def headToHeadCompressor(inFileArray,vecDict):
    for string, vector in vecDict.items():
        
        word_vectors = vector
        length = int(re.findall("\d+",string)[0])
        fileDictionary = {}
        outArray = outArrayMaker(inFileArray,word_vectors,length)
        decapArray = decapitalizer(inFileArray)
        firstWord = True
        
        i = 0
        while i in range(len(decapArray)):
            if firstWord:
                if decapArray[i] not in word_vectors.vocab:
                    continue
                else:
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

def wordonlyCompressor(inFileArray,vectDict):
    for string, vector in vectDict.items():
        word_vectors = vector
        length = int(re.findall("\d+",string)[0])
        fileDictionary = {}
        outArray = outArrayMaker(inFileArray,word_vectors,length)
        decapArray = decapitalizer(inFileArray)
        i = 0
        for i in range(len(decapArray)):
            if decapArray[i] in word_vectors.vocab:
                newVector1 = vectorShrinker(word_vectors[decapArray[i]])
                outArray[i][:length] = newVector1
                fileDictionary[decapArray[i]] = newVector1
        with open("pickle_dictionary_wordonly"+string+".p", 'wb') as f:  
            pickle.dump(fileDictionary, f)
        f.close()
        with open("vectors_out_nohead_wordonly"+string+".txt", 'w') as g:
            for item in outArray:
                g.write("%s\n"%item)
        g.close()

def headToHeadDecompressor(inPickle,inVectors):

    if inPickle[-2:] != ".p":
        print("First arg must be .p (pickle) file.")
        sys.exit(-1)

    if inVectors[-4:] != ".txt":
        print("Second arg must be .txt file.")
        sys.exit(-1)
    # Load the pickled dictionary
    compressionDictionary = pickle.load(open(inPickle,'rb'))

    outFile = inVectors[-12:-4] + "decompressed_" + ".txt"

    length = int(re.findall("\d+",string)[0])
    inArray = intxtToArray(inVectors)

    firstWord = True
    outString = ''
    
    i = 0
    
    while i in range(len(inArray)):
        
        while firstWord:
            if isinstance(inArray[i],list):
                vector1 = inArray[i]
                outString += vectorProcessor(vector1,compressionDictionary,length)
                firstWord = False
            else:
                outString += inArray[i]
        
        index = indexGetter(inArray,i)
        
        if index == None:
            index = i+1
            while len(inArray) > index:
                outString += inArray[index]
                index += 1
            break
        
        for item in inArray[i+1:index]:
            outString += item 
        
        vector1 = headToHeadUndo(vector1,inArray[index],length)
        outString += vectorProcessor(vector1,compressionDictionary,length)
        
        i = index
        
    with open(outFile,"w") as f:
        f.write(outString)
    f.close

def driver():
    inFile = "review1.txt"
    inFileArray = fileOpener(inFile)
    numArray = [4]
    vectorDict = vectorDictionaryMaker(numArray)
    headToHeadCompressor(inFileArray,vectorDict)
    wordonlyCompressor(inFileArray,vectorDict)
    sys.exit("ALL DONE")