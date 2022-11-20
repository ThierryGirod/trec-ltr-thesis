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




#response = requests.post(f'{Solr.solrUrl}{collectionName}/select', data=solrQuery).json()
#print(response)

#for doc in response['response']['docs']:
    # Parse '[features] array', ie
    # title_bm25=0.0,overview_bm25=13.237938,vote_average=7.0'
#    features = doc['[features]']
#    features = features.split(',')
#    features = [float(ftr.split('=')[1]) for ftr in features]

#    print(f"id:{doc['id']} {features}")
    

if __name__ == '__main__':
    featureLogging()
