from solr import Solr
from ltr.data import CorpusApi
import json
import requests

collectionName = 'test'
Solr.createCollection(collectionName)
Solr.enableLtr(collectionName)

Solr.createTextField(collectionName, 'docid')
Solr.createTextField(collectionName, 'url')
Solr.createTextField(collectionName, 'title')
Solr.createTextField(collectionName, 'headings')
Solr.createTextField(collectionName, 'body')


# only for test
LTRPS_SOLR_HOST = 'localhost'
LTRPS_SOLR_PORT = '8983'
solrUrl = f'http://{LTRPS_SOLR_HOST}:{LTRPS_SOLR_PORT}/api/collections'
solrFull = f'{solrUrl}/{collectionName}/update?commit=true'

for file in CorpusApi.getCorpusFileByFile(processed = True):    
    with open(file, 'r') as jsonFile:
        print(f'start loading')
        headers = {"Content-Type": "application/json"}
        print(solrFull)
        response = requests.post(solrFull, data=jsonFile, headers=headers)
        print(f'data send')
        print(response.json())