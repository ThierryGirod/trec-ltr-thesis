from solr import Solr
from ltr.data import CorpusApi
import json
import requests
import time

def indexing():
    try: 
        collectionName = 'thesis-ltr'
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
    except Exception as e:
        print(e)
        
if __name__ == '__main__':
    indexing()