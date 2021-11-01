import numpy
from mtcnn.mtcnn import MTCNN
from util import getImageFromUrl
from PIL import Image
from io import BytesIO

detector = MTCNN()

def getFaces(url):
    img = getImageFromUrl(url)
    img = Image.open(BytesIO(img))
    ary = numpy.asarray(img)
    return detector.detect_faces(ary)

print(getFaces("https://m.media-amazon.com/images/M/MV5BMjJkNDg5ZDctM2RlZS00NjFmLTkxZjktMWE5NGQzMDg4NDFhXkEyXkFqcGdeQXVyMTMwMDM1OTQ@._V1_.jpg"))

def getFaceAction(payload):
    if 'url' not in payload:
        return {
            'type': 'InvalidArgumentError',
            'message': 'url should be in the payload!'
        }
    
    return {
        'faces': getFaces(payload['url'])
    }
