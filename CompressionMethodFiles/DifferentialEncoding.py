#DifferentialEncoding.py
#Differential Encoder, adapted from Data Compression: The Complete Reference, Solomon, 1998

def diffEncoder(inString):
# This function takes a string of numbers and returns a string which represents their differential encoding
    
    stringList = list(map(float,str.split(inString)))
    outString = str(stringList[0]) + ' '

    for i in range(0,len(stringList)-1):
        if i == len(stringList) - 2:
            outString += str('%g'%(stringList[i+1] - stringList[i]))
    else:
        outString += str('%g'%(stringList[i+1] - stringList[i])) + ' '

    return(outString)

#Differential Decoder, adapted from Data Compression: The Complete Reference, Solomon, 1998

def diffDecoder(inString):
# This function takes a string of numbers from the diffEncoder function and returns a string of the initial values
    
    stringList = list(map(float,str.split(inString)))
    current = '%g'%stringList[0]
    outString = str(current) + ' '
    
    for i in range(0,len(stringList)-1):
        if i == len(stringList) - 2:
            outString += str('%g'%(stringList[i+1] + current))
        else:
            current = stringList[i+1] + float(current)
            outString += str('%g'%(current)) + ' '
  
    return(outString)