

from typing import Dict, List
from typing import Dict, List
import csv
import json
from os import listdir
from os.path import isfile, join
import os

from ltr.Judgment import Judgment
from . import Config

def getDevQueriesAsDict() -> Dict[int, str]:
    """
    Returns the downloaded developer queries as dict with the id as key and the query as value
    """
    queries = {}
    with open(Config.DEV1_QUERIES_TSV, 'r') as tsv:
        tsvReader = csv.reader(tsv, delimiter='\t')
        for line in tsvReader:
            queries[line[0]] = line[1]
    
    return queries

def getTrainQueriesAsDict() -> Dict[int, str]:
    """
    Returns the downloaded train queries as dict with the id as key and the query as value
    """
    queries = {}
    with open(Config.TRAIN_QUERIES_TSV, 'r') as tsv:
        tsvReader = csv.reader(tsv, delimiter='\t')
        for line in tsvReader:
            queries[line[0]] = line[1]
    
    return queries

def getDevQrels() -> List:
    """
    Returns the downloaded developer QRELS as list
    """
    qrels = []
    with open(Config.DEV1_QRELS_TSV, 'r') as tsv:
        tsvReader = csv.reader(tsv, delimiter='\t')
        for line in tsvReader:
            qrels.append(Judgment(line[0],'',line[1],line[2],line[3]))
    
    return qrels

def getTrainQrels() -> List:
    """
    Returns the downloaded developer QRELS as list
    """
    qrels = []
    with open(Config.TRAIN_QRELS_TSV, 'r') as tsv:
        tsvReader = csv.reader(tsv, delimiter='\t')
        for line in tsvReader:
            qrels.append(Judgment(line[0],'',line[1],line[2],line[3]))
    
    return qrels

# Function from https://microsoft.github.io/msmarco/TREC-Deep-Learning.html
def getDocumentFromCorpus(documentId: str):
    """
    Returns a document from the corpus by a given id
    """
    (string1, string2, bundlenum, position) = documentId.split('_')
    assert string1 == 'msmarco' and string2 == 'doc'

    with open(f'{Config.CORPUS_DIRECTORY}/msmarco_doc_{bundlenum}', 'rt', encoding='utf8') as inFh:
        inFh.seek(int(position))
        jsonString = inFh.readline()
        document = json.loads(jsonString)
        assert document['docid'] == documentId
        return document

def getCorpusFileByFile(processed: bool = False):
    """
    Returns a generator function that returns all the files from the corpus directory
    """
    files = []
    if processed == True:
        files = [join(Config.CORPUS_PROCESSED_DIRECTORY, file) for file in listdir(Config.CORPUS_PROCESSED_DIRECTORY) if isfile(join(Config.CORPUS_PROCESSED_DIRECTORY, file))]
    else:
        files = [join(Config.CORPUS_DIRECTORY, file) for file in listdir(Config.CORPUS_DIRECTORY) if isfile(join(Config.CORPUS_DIRECTORY, file))]
    for file in files:
        yield file

def saveListAsJson(path: str, list: List):
    """
    Saves a list of values as json
    """
    with open(path, 'w') as jsonFile:
        json.dump(list, jsonFile, indent=4)

def deleteFile(path: str):
    if(os.path.isfile(path)):
        #os.remove() function to remove the file
        os.remove(path)
        #Printing the confirmation message of deletion
        print(f'{path} deleted successfully')
        

def getJudgmentsBatchFileByFile():
    """
    Returns a generator function that returns all the judgment batches files from the directory
    """
    files = []
   
    files = [join(Config.JUDGMENTS_BATCHES_DIRECTORY, file) for file in listdir(Config.JUDGMENTS_BATCHES_DIRECTORY) if isfile(join(Config.JUDGMENTS_BATCHES_DIRECTORY, file))]
    for file in files[:1]:
        yield file
        
def saveListAsFile(path: str, list: List):
    """
    Saves a list of values as as file
    """
    with open(path, 'w') as file:
        for item in list:
            file.write("%s\n" % item)
        print(f'File written: {path}')