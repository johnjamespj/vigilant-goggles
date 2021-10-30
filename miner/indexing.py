import os
import numpy as np
from random import randrange
from annoy import AnnoyIndex

dataPath = os.environ['DATA_PATH']

def saveEmbeddings(filename, embeddings):
    with open(filename, 'ab') as f:
        for embedding in embeddings:
            f.write(embedding.tobytes())

def importEmbeddings(filename, arrayLen, dtype=np.float32):
    byteSize = np.dtype(dtype).itemsize

    npArrays = []
    with open(filename, 'rb') as f:
        for i in range(0, arrayLen):
            npBytes = f.read(arrayLen * byteSize)
            npArrays.append(np.frombuffer(npBytes, dtype=dtype))

    return npArrays

def indexEmbeddings(filename, embeddings, ntree):
    f = len(embeddings[0])
    index = AnnoyIndex(f, 'euclidean')

    for i in range(0, len(embeddings)):
        index.add_item(i, embeddings[i])

    index.build(ntree)
    index.save(filename)

def testsaveEmbeddingsimportEmbeddings():
    npArys = []
    for i in range(0, 5):
        testList = [randrange(100) / (randrange(5) + 1) for i in range(100)]
        testList = np.array(testList, dtype=np.float32)
        npArys.append(testList)
    
    saveEmbeddings(dataPath + '/embeddings.bin', npArys)
    arrays = importEmbeddings(dataPath + '/embeddings.bin', 100, dtype=np.float32)
    print((arrays[0] == npArys[0]).all())

    indexEmbeddings(dataPath + '/embeddings.ann', npArys, 10)

    # deletes the file
    os.remove(dataPath + '/embeddings.bin')