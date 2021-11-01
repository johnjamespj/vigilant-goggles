from PIL import Image
import numpy
from keras_facenet import FaceNet
import base64
from io import BytesIO
from PIL import Image

from util import getImageFromUrl

# embedder = FaceNet(weights_filepath="./models/20180402-114759-weights.h5", model_download=True)
embedder = FaceNet()

def getEmbedderExtractor():
    return embedder

def extractFromBytes(img):
    image = Image.open(BytesIO(img))
    image = image.convert('RGB')

    ary = numpy.asarray(image)
    return embedder.extract(ary, threshold=0.5)

def extractFaceFromArray(facePixelArray):
    return embedder.extract(facePixelArray)

def makeEmbeddingSerializable(embeddings):
    for face in embeddings:
        face["embedding"] = base64.b64encode(face["embedding"].tobytes())
    return embeddings

def embeddingFromUrl(url):
    img = getImageFromUrl(url)
    return extractFromBytes(img)

def extractEmbeddingAction(payload):
    if 'url' not in payload:
        return {
            'type': 'InvalidArgumentError',
            'message': 'url should be in the payload!'
        }

    return {
        'embeddings': makeEmbeddingSerializable(embeddingFromUrl(payload['url']))
    }
