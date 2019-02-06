import pickle
import ast
import sys
import gzip
import logging
import numpy as np

inPickle = sys.argv[1]
inVectors = sys.argv[2]
outFile = inVectors[-12:-4] + "decompressed_" + ".txt"

def head_to_head_undo(vector1,vector2,length):
    newWord = []
    for i in range(length):
        newWord.append(vector1[i]+vector2[i])
    newWord.extend(vector2[length:])
    return newWord

def indexGetter(array,index):
    for item in array[index+1:]:
        if isinstance(item,list):
            return array.index(item,index)

def intxtToArray(filename):
    with open(inVectors,"r+") as f:
        readList = f.readlines()
    outArray = []
    for item in readList:
        if item[0] == '[':
            outArray.append(ast.literal_eval(item))
        else:
            itemCopy = item[:-1]
            outArray.append(item[:-1])
    f.close()
    return outArray

def vectorProcessor(vector,dictionary,length):
    word = ''
    for dWord, dVector in dictionary.items():
        if np.allclose(vector[:length],dVector,atol=1e-01):
            for i in range(len(dWord)):
                if i in vector[length:]:
                    word += dWord[i].upper()
                else:
                    word += dWord[i]
    return word

def decimalize(vector):
    newVec = []
    for entry in vector:
        newVec.append(entry/10)
    return newVec

if inPickle[-2:] != ".p":
    print("First arg must be .p (pickle) file.")
    sys.exit(-1)

if inVectors[-4:] != ".txt":
    print("Second arg must be .txt file.")
    sys.exit(-1)
# Load the pickled dictionary
compressionDictionary = pickle.load(open(inPickle,'rb'))

length = int(inPickle[-5:-3])
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
    vector1 = head_to_head_undo(vector1,inArray[index],length)
    outString += vectorProcessor(vector1,compressionDictionary,length)
    i = index
    
with open(outFile,"w") as f:
    f.write(outString)
f.close