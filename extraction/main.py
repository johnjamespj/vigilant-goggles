import bz2
import os
from io import BytesIO
import csv

from embedding import extractFromFilename
import boto3

s3resoure = boto3.resource('s3')
bucket = s3resoure.Bucket(os.environ['BUCKET'])

embeddingsPerObj = int(os.environ["UNIT_COUNT"])
file = os.environ['DUMP']

def parseCSVLine(line):
    return list(csv.reader([line]))[0]

def saveFileToS3(buffer, name):
    bucket.upload_fileobj(buffer, name)
    pass

def main():
    # iterate through lines
    removedHeader = False

    tempObj = BytesIO()
    idx = 0
    with bz2.BZ2File(os.path.expanduser(file), 'r') as fp:
        for line in fp:
            if not removedHeader:
                removedHeader = True
                continue
            
            line = parseCSVLine(line.decode('utf8').replace('\r\n', ''))
            line[0] = int(line[0])
            id, url = line

            # compute embedding
            embedding = extractFromFilename(url)

            # store it as a byte buffer of a ByteIO
            if embedding is not None:
                tempObj.write(idx.to_bytes(2, byteorder='big'))
                tempObj.write(embedding.tobytes())

            # save it to s3 1000 where computed
            if idx != 0 and idx % embeddingsPerObj == 0:
                # saves to s3
                tempObj.seek(0)
                saveFileToS3(tempObj, 'block-%s' % idx)
                tempObj = BytesIO()
            
            print('(%s completed)' % (idx))
            idx += 1

main()