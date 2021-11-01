import urllib.request as request

def getImageFromUrl(url):
    req = request.Request(url, headers={'User-Agent': 'Face-Indexer/1.0'})
    return request.urlopen(req).read()

