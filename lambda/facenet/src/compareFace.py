from PIL import Image
from io import BytesIO
from embedding import getEmbedderExtractor, embeddingFromUrl
from util import getImageFromUrl
import numpy
from scipy import spatial

embedder = getEmbedderExtractor()

def getFaceEmbeddingFromUrlAndBox(url, box):
    img = getImageFromUrl(url)
    image = Image.open(BytesIO(img))
    image = image.convert('RGB')
    pixels = numpy.asarray(image)

    x1, y1, width, height = box
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    face = pixels[y1:y2, x1:x2]

    embedding = embedder.extract(face, threshold=0.5)

    if len(embedding) != 1:
        return None
    
    return embedding[0]['embedding']

def compareWithAll(faceA, faces):
    res = []
    for face in faces:
        res.append(spatial.distance.cosine(faceA, face))
    return res

def getComparisons(url1, url2, box):
    # extract face from box and url1
    embedding = getFaceEmbeddingFromUrlAndBox(url1, box)

    if embedding is None:
        return None

    # extract faces from url2
    faces = embeddingFromUrl(url2)
    facesEmbeddings = list(map(lambda x: x['embedding'], faces))

    # calculate all distances
    facesComparison = compareWithAll(embedding, facesEmbeddings)

    facesComparisonWithBox = []
    i = 0
    for face in facesComparison:
        box = faces[i]

        res = {
            'box': box['box'],
            'isSameFace': (0, 1)[face < 0.4],
            'distances': face
        }

        facesComparisonWithBox.append(res)
        i += 1
    
    return facesComparisonWithBox

def compareFaceAction(payload):
    if 'subjectUrl' not in payload or 'targetUrl' not in payload or 'box' not in payload or not isinstance(payload['box'], list) or len(payload['box']) != 4:
        return {
            'type': 'InvalidArgumentError',
            'message': 'url should be in the payload!'
        }

    res = getComparisons(payload['subjectUrl'], payload['targetUrl'], payload['box'])
    return {
        'comparison': res
    }
