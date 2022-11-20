import requests
from solr import Solr
from ltr.data import CorpusApi
import time


def featureLogging():
    
    collectionName = 'thesis-ltr'
    
    for batch in CorpusApi.getJudgmentsBatchFileByFile():
        start = time.time()
        print(f'Loading batch {batch}')    
        Solr.featureLoggingToFile(collectionName, batch)
        end = time.time()
        print('Time taken for feature logging:', end - start)


if __name__ == '__main__':
    featureLogging()
