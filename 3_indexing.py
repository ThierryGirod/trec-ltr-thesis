from solr import Solr
from ltr.data import CorpusApi
import json
import requests
import time

def indexing():

    collectionName = 'thesis-ltr'
    Solr.createCollection(collectionName)
    Solr.enableLtr(collectionName)
    
    # Todo: Managed Stopwords and synonyms filter einbauen

    #Solr.createTextField(collectionName, 'docid')
    typeName = 'custom_text_general'
    Solr.createTextType(collectionName, typeName)
    Solr.createTextField(collectionName, 'url', typeName)
    Solr.createTextField(collectionName, 'title', typeName)
    Solr.createTextField(collectionName, 'headings', typeName)
    Solr.createTextField(collectionName, 'body', typeName)
    Solr.addCopyField(collectionName, '*', '_text_')

    for file in CorpusApi.getCorpusFileByFile(processed = True):
        start = time.time()    
        Solr.indexFile(collectionName, file)
        #CorpusApi.deleteFile(file)
        end = time.time()
        print('Time taken for indexing file:', end - start)
        
if __name__ == '__main__':
    indexing()