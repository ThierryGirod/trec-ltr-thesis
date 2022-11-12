from solr import Solr
from ltr.data import CorpusApi
import json
import requests

def indexing():

    collectionName = 'thesis-ltr'
    Solr.createCollection(collectionName)
    Solr.enableLtr(collectionName)

    #Solr.createTextField(collectionName, 'docid')
    Solr.createTextField(collectionName, 'url')
    Solr.createTextField(collectionName, 'title')
    Solr.createTextField(collectionName, 'headings')
    Solr.createTextField(collectionName, 'body')
    Solr.addCopyField(collectionName, '*', '_text_')

    for file in CorpusApi.getCorpusFileByFile(processed = True):    
        Solr.indexFile(collectionName, file)
        
if __name__ == '__main__':
    indexing()