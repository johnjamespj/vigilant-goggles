import re
from pyspark import SparkContext
import os
import csv

from embedding import processImage

def filterOutPeoples(line):
    return (
        line != "[" and                                         # first line of the dump
        line != "]" and                                         # last line of the dump
        line.find('"type":"property"') == -1 and                # the entity is not a property
        line.find('"P31":[{') != -1 and                         # instance-of claim
        line.find('"id":"Q5"') != -1 and                        # instance-of (human) claim
        line.find('"P21":[{') != -1 and                         # sex-or-gender claim
        line.find('"P18":[{"') != -1                            # has a picture
    )

def parseHumanEntity(entityString):
    return (parseEntityID(entityString), parseImageUrl(entityString))

def parseEntityID(entityString):
    pos = re.search('"id":"[Q|P](\d+)"', entityString)
    return int(pos.group(1))

def parseImageUrl(entityString):
    compiledResult = re.search('"P18":\[.*?value":"([^\"]+)"', entityString)

    if compiledResult:
        return compiledResult.group(1)
    return None

def saveAsCsv(humanEntitiesBackup, filePath, rowHeader):
    with open(filePath, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(rowHeader)
        for humanEntity in humanEntitiesBackup:
            writer.writerow(humanEntity[0:len(rowHeader)])

def extractFaceEmbeddings(humanEntities):
    return (humanEntities[0], humanEntities[1], processImage(humanEntities[1]))

def runSpark():
    sc = SparkContext()

    dumpPath = os.environ['DUMP']
    dataPath = os.environ['DATA_PATH']

    # load dump
    dump = sc.textFile(dumpPath)

    # filter out non-human entities
    humanEntities = dump.filter(filterOutPeoples)

    # parse human entities
    humanEntities = humanEntities.map(parseHumanEntity)

    # backup the results
    # humanEntitiesBackup = humanEntities.collect()
    humanEntitiesBackup = humanEntities.take(1)
    saveAsCsv(humanEntitiesBackup, dataPath + '/human_entities_backup.csv', ['id', 'url'])

    humanEntitiesEmbeddings = humanEntities.map(extractFaceEmbeddings).filter(lambda x: x[2] is not None)
    # humanEntitiesEmbeddings = humanEntitiesEmbeddings.collect()
    humanEntitiesEmbeddings = humanEntitiesEmbeddings.take(2)
    saveAsCsv(humanEntitiesEmbeddings, dataPath + '/human_entities_embeddings.csv', ['id', 'url'])

    sc.stop()
    

runSpark()