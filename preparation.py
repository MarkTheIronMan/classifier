## ['wordval', 'size_norm', 'tel', 'address', 'it', 'ads', 'sc'] - list of features

SIZE_MAX = 3200000

from service import find_all, load_from_json, load_from_txt

lbad = load_from_json('arbitrage_words')
lgood = load_from_json('business_words')
stopwords = load_from_txt('stopwords.txt')

def get_page_size(string):
    return len(string)

def get_norm_size(string):
    return round(GetPageSize(string)/SIZE_MAX, 3)

def delete_special_symbols(string):
    f = [string]
    f = [x.replace('\n','').replace('&amp;','').replace('|','').replace('-','').replace('?','').replace('\t','').replace('&gt','') for x in f]
    return f[0]

def get_title(string):
    try:
        start = string.find('<title>')
        end = string.find('</title>')
    except AttributeError:
        return ''
    if (start == -1) or (end == -1):
        return ''
    return delete_special_symbols(string[start+7:end])

def find_h1(string):
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
    return delete_special_symbols(temp[brack+1:end])

def find_h2(string):
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
    return delete_special_symbols(temp[brack+1:end])

def find_h3(string):
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
    return delete_special_symbols(temp[brack+1:end])

def clear_brackets(string):
    if type(string) is not str:
        return ''
    is_bracket_exists = True
    while isBracketExists:
        start = string.find('<')
        end = string.find('>')
        if end > start and start != -1:
            string = string[:start] + string[end + 1:]
            continue
        if start == -1 or end == -1:
            is_bracket_exists = False
        if end < start:
            return string
    if not is_bracket_exists:
        return string

def sum_headers(string):
    return find_h1(string) + find_h2(string) + find_h3(string)

def form_cloud_of_words(string):
    cloud = find_title(string)
    header = sum_headers(string)
    cloud += header
    return clear_brackets(cloud.lower())

def count_word_val(cloud, lgood, lbad):
    val = 0.5
    add_val = 0
    cloud = cloud.split()
    for word in cloud:
        if word in stopwords:
            continue
        try:
            good_val = lgood[word]
        except KeyError:
            good_val = 1
        try:
            bad_val = lbad[word]
        except KeyError:
            bad_val = 1
        if good_val >= ba_val:
            add_val += (good_val - bad_val)/300
        else:
            add_val += (good_val - bad_val)/190
    if len(cloud) != 0:
        val += add_val    
    return val

def is_tel(string): #add existence of tel
    if string.find("tel:") != -1:
        return 1
    return 0

def is_address(string): #add existence of address
    if string.find("address") != -1:
        return 1
    return 0

def is_inputbox(string): #add existence of Input type
    if string.find("input type:") != -1:
        return 1
    return 0

def is_ads(string): #add existence of ad blocks by keyword "adsby"
    if string.find("adsby") != -1:
        return 1
    return 0

def get_sc(string): #added count of word "search" / lenght of document
    mlist = list(find_all('search', string))
    return round(len(mlist) * 60 / len(string), 3)

def form_query_to_model(string): # form 
    if not string:
        return 203
    return [[count_word_val(form_cloud_of_words(string), lgood, lbad), 
            get_size_norm(string), is_tel(string), 
            is_address(string), is_inputbox(string), 
            is_ads(string), get_sc(string)]] 