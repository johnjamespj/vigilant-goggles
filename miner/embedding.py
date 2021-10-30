from PIL import Image
import urllib.request as request
from io import BytesIO
import numpy
from keras_facenet import FaceNet
import hashlib
from urllib.parse import quote

embedder = FaceNet()

def extraction(url):
    if url is None:
        return
    
    try:
        req = request.Request(url, headers={'User-Agent': 'Face-Indexer/1.0'})
        img = request.urlopen(req).read()
        image = Image.open(BytesIO(img))
        ary = numpy.asarray(image)
        return embedder.extract(ary, threshold=0.95)
    except:
        pass

def findImagePath(filename, width=500):
    try:
        filename = bytes(filename, "utf-8").decode("unicode_escape").replace(" ", "_")
    except:
        return None
    hash = hashlib.md5(filename.encode()).hexdigest()
    path = 'https://upload.wikimedia.org/wikipedia/commons/thumb/' + hash[:1] + '/' + hash[:2] + '/' + quote(filename) + ('/%ipx-' % width) + quote(filename)
    return path

def processImage(filename):
    imageUrl = findImagePath(filename)
    faces = extraction(imageUrl)
    
    if faces is None:
        return
    elif len(faces) == 0:
        return
    
    # float32 512 len array
    return faces[0]['embedding']