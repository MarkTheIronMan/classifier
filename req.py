import requests
from service import FindAll

def GetActualUserAgent(): 
    url = 'https://www.whatismybrowser.com/guides/the-latest-user-agent/chrome'
    req = requests.get(url, timeout = 10)
    start = req.text.find('Mozilla')
    end = req.text[start:].find('</span>')
    return req.text[start:start + end]

def PrepareUrl(url):
    dotscount = list(FindAll('.', url))
    size = len(dotscount)
    if size > 2:
        url = url[:4] + url[dotscount[size-2]+1:]
    if url.find('http') == -1:
        return 'http://' + url
        
    
def GetMainPageUrl(url):
    slash = list(FindAll('/',url))
    size = len(slash)
    if size < 3:
        return url
    return url[:slash[2]]


def Parse(url): #get content of page
    #user_agent = GetActualUserAgent()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
    url = PrepareUrl(GetMainPageUrl(url))
    try:
        req = requests.get(url, headers={'User-Agent':user_agent}, timeout = 10)
    except Exception:
        return '202'
    if req.status_code == 200:
        print('200')
        return req.text
    return '201'

