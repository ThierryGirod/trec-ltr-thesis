from solr import Solr
from ltr.data import CorpusApi
import json
import requests
import time

def indexing():
    try: 
        collectionName = 'thesis-ltr'
        typeName = 'custom_text_general_bm25_similarity'
        classicTypeName = 'custom_text_general_classic_similarity'
        Solr.createTextType(collectionName, typeName)
        Solr.createClassicSimilarityTextType(collectionName, classicTypeName)
        Solr.createTextField(collectionName, 'url', typeName)
        Solr.createTextField(collectionName, 'title', typeName)
        Solr.createTextField(collectionName, 'title_classic', classicTypeName)
        Solr.createTextField(collectionName, 'headings', typeName)
        Solr.createTextField(collectionName, 'headings_classic', classicTypeName)
        Solr.createTextField(collectionName, 'body', typeName)
        Solr.createTextField(collectionName, 'body_classic', classicTypeName)
        Solr.createTextField(collectionName, '_copy_all_', typeName)
        Solr.createTextField(collectionName, '_copy_all_classic_', classicTypeName)
        
        Solr.addCopyField(collectionName, 'title', '_copy_all_')
        Solr.addCopyField(collectionName, 'headings', '_copy_all_')
        Solr.addCopyField(collectionName, 'body', '_copy_all_')
        
        Solr.addCopyField(collectionName, 'title', 'title_classic')
        Solr.addCopyField(collectionName, 'headings', 'headings_classic')
        Solr.addCopyField(collectionName, 'body', 'body_classic')
        
        Solr.addCopyField(collectionName, 'title_classic', '_copy_all_classic_')
        Solr.addCopyField(collectionName, 'headings_classic', '_copy_all_classic_')
        Solr.addCopyField(collectionName, 'body_classic', '_copy_all_classic_')

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