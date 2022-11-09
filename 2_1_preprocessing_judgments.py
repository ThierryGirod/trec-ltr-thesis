from ltr.data import CorpusApi, Config
import json
import re
import os

def split(dataList, batchSize):

    for i in range(0, len(dataList), batchSize):
        yield dataList[i:i + batchSize]

def preprocess():
    
    queries = CorpusApi.getTrainQueriesAsDict()
    judgments = CorpusApi.getTrainQrels()

    # Preprocess the judgments
    for judgment in judgments:
        # Get query text
        judgment.query = queries[judgment.query]
        # Remove punctuations
        judgment.query = re.sub('[^\w\s]', '', judgment.query)
        
    # Split judgments in batches
    batchSize = 1000
    batches = []
    for batch in split(judgments, batchSize):
        batches.append(batch)
    
    #  Add negative queries for eatch query and save them
    # 1. get queries per batch and relevant documents
    # 2. fill every query with unrelevant documents from batch
    # 3. create new batch list with all the relevant and irrelevant judgments
    # 4. save batch        

if __name__ == '__main__':
    preprocess()