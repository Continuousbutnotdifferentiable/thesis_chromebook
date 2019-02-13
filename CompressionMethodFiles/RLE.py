# RLE.py
# Run Length Encoding Compressor, adapted from Data Compression: The Complete Reference, Solomon, 1998

def rleCompressor(inString):
# This function takes a string as input and returns the RLE compression of that string
    
    outString = ""
    count = 1
    
    if len(inString) == 0:
        pass
    
    else:
        for i in range(len(inString)):
            if i + 1 == len(inString) or inString[i] != inString[i+1]:
                if count == 1:
                    outString += inString[i]
                else:
                    outString += (str(count)+inString[i])
                    count = 1
            else:
                count += 1
    return outString
    
# Run Length Encoding Decompressor, adapted from Data Compression: The Complete Reference, Solomon

def rleDecompressor(inString):
# This function takes a RLE encoded string from rleCompressor and returns the original string

    outString = ''
    countString = ''
    
    for i in inString:
        while str.isdigit(i):
            countString += i
            break
        if not str.isdigit(i):
            if countString == '':
                countString = 1
            outString += (i*int(countString))
            countString = ''
    return outString
