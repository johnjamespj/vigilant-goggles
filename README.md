# Face Index
Face Index is a public database of face indices of public figures that can be used to identify the database to identify public figures in a novel image. **The project is under in heavy development**.

## Quick Overview

* The first stage of the project a way to mine image and name of public figures from wikipedia. Wikipedia dump is the most obvious place to start rather that manually crawl all the pages. The problem with wikipedia dump is large and hard to extract information. I used WikiData, a machine-readable wikipedia. Basically wikidata organize wikipedia as JSON document for each articles and information such as age or whether the subject of the article is a human is organized as properties of the given JSON.
* I download wikidata dump to a EC2 instance and extracted image url, name and article id from wikidata. Then I used 3 large machine (c6i.12xlarge) with AWS EMR with Apache Spark I extracted all the names.
* Then the images should be downloaded and use the downloaded image to extract image embedding using one of following models - DeepFace, OpenFace and FaceNet.
* Use an effective way to organize the data so that nearest neigbour can be calculated fast using Annoy Index.


