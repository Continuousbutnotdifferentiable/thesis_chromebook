#ArithmeticCoding.py

## Probability Modeler, adapted from Data Compression: The Complete Reference, Solomon, 1998

def probabilityModeler(inString):
# Takes a string as input and returns a dictionary corresponding to
# the normalized probabilities for each item in the string.

    totalCount = 0
    probDict = dict()

    # Get the counts
    for i in range(0,len(inString)):
        character = inString[i]
        if character in probDict.keys():
            probDict[character] += 1
            totalCount += 1
        else:
            probDict[character] = 1
            totalCount += 1

    # Normalize
    for i, j in probDict.items():
        probDict[i] = j/totalCount
    
    return probDict
    
