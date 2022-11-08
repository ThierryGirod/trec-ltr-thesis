from solr import Solr
from ltr.data import CorpusApi
import json
import requests

collectionName = 'thesis-ltr'
Solr.createCollection(collectionName)
Solr.enableLtr(collectionName)

#Solr.createTextField(collectionName, 'docid')
Solr.createTextField(collectionName, 'url')
Solr.createTextField(collectionName, 'title')
Solr.createTextField(collectionName, 'headings')
Solr.createTextField(collectionName, 'body')

for file in CorpusApi.getCorpusFileByFile(processed = True):    
    Solr.indexFile(collectionName, file)