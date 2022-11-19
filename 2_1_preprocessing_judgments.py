from ltr.Judgment import Judgment
from ltr.data import CorpusApi, Config
import json
import re
import os
from itertools import permutations
from dataclasses import asdict

def split(dataList, batchSize):

    for i in range(0, len(dataList), batchSize):
        yield dataList[i:i + batchSize]

def preprocess():
    
    queries = CorpusApi.getTrainQueriesAsDict()
    judgments = CorpusApi.getTrainQrels()

    # Preprocess the judgments
    for judgment in judgments:
        # Get query text
        judgment.queryText = queries[judgment.query]
        # Remove punctuations
        judgment.queryText = re.sub('[^\w\s]', '', judgment.query)
        
    # Split judgments in batches
    batchSize = 1000
    batches = []
    for batch in split(judgments, batchSize):
        batches.append(batch)
    
    #  Add negative queries for each query and save them
    # 1. Get permutations of all judgment pairs
    # 2. When the first judgment does not have the same query as the second one 
    #    create a new judgment that marks the document from judgment 2 as 
    #    irrelevant for query from judgment 1
    # 3. Extend the current positive batch with all the negative samples
    # 4. Save batch        
    for i, batch in enumerate(batches):
        negativeBatch = []
        for judg1, judg2 in permutations(batch,2):
            if judg1.query != judg2.query:
                # Add document judg2 as irrelevant to query from judg1
                negativeBatch.append(Judgment(judg1.query, judg1.queryText, judg1.iteration, judg2.docId, 0))
        batch.extend(negativeBatch)
        
        CorpusApi.saveListAsJson(f'{Config.DATA_DIRECTORY}/train/judgments/batch_{i}.json', [asdict(judgment) for judgment in batch])
        
        print(f'Batch #{i} processed')
        del batch
        
if __name__ == '__main__':
    preprocess()