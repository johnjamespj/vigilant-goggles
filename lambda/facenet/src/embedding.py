import os
from PIL import Image
import urllib.request as request
from io import BytesIO
import numpy
from keras_facenet import FaceNet
import base64

embedder = FaceNet(weights_filepath="./models/20180402-114759-weights.h5", model_download=True)

def makeEmbeddingSerializable(embeddings):
    for face in embeddings:
        face["embedding"] = base64.b64encode(face["embedding"].tobytes())
    return embeddings

def embeddingFromUrl(url):
    img = getImageFromUrl(url)
    return extractFromBytes(img)

def getImageFromUrl(url):
    req = request.Request(url, headers={'User-Agent': 'Face-Indexer/1.0'})
    return request.urlopen(req).read()

def extractFromBytes(img):
    image = Image.open(BytesIO(img))
    ary = numpy.asarray(image)
    return embedder.extract(ary, threshold=0.5)

def extractEmbeddingAction(payload):
    return {
        'embedding': makeEmbeddingSerializable(embeddingFromUrl(payload['url']))
    }
