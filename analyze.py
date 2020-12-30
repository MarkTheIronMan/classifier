## ['wordval', 'size_norm', 'tel', 'address', 'it', 'ads', 'sc'] - list of features

SIZE_MAX = 3200000

from service import FindAll, LoadFromJson, LoadFromTxt

lbad = LoadFromJson('arbitrage_words')
lgood = LoadFromJson('business_words')
stopwords = LoadFromTxt('stopwords.txt')

def GetPageSize(string):
    return len(string)

def GetSizeNorm(string):
    return round(GetPageSize(string)/SIZE_MAX, 3)

def DeleteSpecialSymbols(string):
    f = [string]
    f = [x.replace('\n','').replace('&amp;','').replace('|','').replace('-','').replace('?','').replace('\t','').replace('&gt','') for x in f]
    return f[0]

def FindTitle(string):
    try:
        start = string.find('<title>')
        end = string.find('</title>')
    except AttributeError:
        return ''
    if (start == -1) or (end == -1):
        return ''
    return DeleteSpecialSymbols(string[start+7:end])

def FindH1(string):
    try:
        start = string.find('<h1')
        if start != -1:
            temp = string[start+3:start + 500]
            brack = temp.find('>')
            end = temp.find('</h1>')
    except AttributeError:
        return ''
    if (start == -1) or (end == -1):
        return ''
    return DeleteSpecialSymbols(temp[brack+1:end])

def FindH2(string):
    try:
        start = string.find('<h2')
        if start != -1:
            temp = string[start+3:start + 500]
            brack = temp.find('>')
            end = temp.find('</h2>')
    except AttributeError:
        return ''
    if (start == -1) or (end == -1):
        return ''
    return DeleteSpecialSymbols(temp[brack+1:end])

def FindH3(string):
    try:
        start = string.find('<h3')
        if start != -1:
            temp = string[start+3:start + 500]
            brack = temp.find('>')
            end = temp.find('</h3>')
    except AttributeError:
        return ''
    if (start == -1) or (end == -1):
        return ''
    return DeleteSpecialSymbols(temp[brack+1:end])

def ClearBrackets(string):
    if type(string) is not str:
        return ''
    isBracketExists = True
    while isBracketExists:
        start = string.find('<')
        end = string.find('>')
        if end > start and start != -1:
            string = string[:start] + string[end + 1:]
            continue
        if start == -1 or end == -1:
            isBracketExists = False
        if end < start:
            return string
    if not isBracketExists:
        return string

def FindHeaders(string):
    return FindH1(string) + FindH3(string) + FindH3(string)

def FormCloudOfWords(string):
    cloud = FindTitle(string)
    header = FindHeaders(string)
    cloud += header
    return ClearBrackets(cloud.lower())

def CountWordVal(cloud, lgood, lbad):
    val = 0.5
    add_val = 0
    cloud = cloud.split()
    for word in cloud:
        if word in stopwords:
            continue
        try:
            goodval = lgood[word]
        except KeyError:
            goodval = 1
        try:
            badval = lbad[word]
        except KeyError:
            badval = 1
        if goodval >= badval:
            add_val += (goodval - badval)/300
        else:
            add_val += (goodval - badval)/190
    if len(cloud) != 0:
        val += add_val
        
    return val

def GetTel(string): #add existence of tel
    if string.find("tel:") != -1:
        return 1
    return 0

def GetAddress(string): #add existence of address
    if string.find("address") != -1:
        return 1
    return 0

def GetInputBox(string): #add existence of Input type
    if string.find("input type:") != -1:
        return 1
    return 0

def GetADS(string): #add existence of ad blocks
    if string.find("adsby") != -1:
        return 1
    return 0

def GetSC(string): #added count of word "search" / lenght of document
    mlist = list(FindAll('search', string))
    return round(len(mlist) * 60 / len(string), 3)

def FormRequestToModel(string): # form 
    if not string:
        return '203'
    return [[CountWordVal(FormCloudOfWords(string), lgood, lbad), 
            GetSizeNorm(string), GetTel(string), 
            GetAddress(string), GetInputBox(string), 
            GetADS(string), GetSC(string)]] 