ERRORS = {
    '200': 'OK',
    '201': 'Cannot load page',
    '202': 'Invalid URL',
    '203': 'No content from parsing'
    }


import json
import pickle


def SaveToJson(dictionary, filename): # serialize data into file:
    json.dump(dictionary, open(filename + ".json", 'w'))

def LoadFromJson(filename): # read data from file:
    return json.load(open(filename + ".json"))

def SaveToTxt(mlist, filename): # save list to txt file
    with open(filename, 'wb') as fp:
        pickle.dump(mlist, fp)

def LoadFromTxt(filename): # load list from txt file
    with open (filename, 'rb') as fp:
        return pickle.load(fp)


# Find all substrings in string
def FindAll(p, s):
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i+1)

def GetErrorEncode(num):
    try:
        res = ERRORS[num]
        return res
    except Exception:
        return 'Unknown code'