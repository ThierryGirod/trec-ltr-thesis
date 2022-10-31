

from typing import Dict, List
from typing import Dict, List
import csv
import json

from ltr.Judgment import Judgment
from . import Config

def getDevQueriesAsDict() -> Dict[int, str]:
    queries = {}
    with open(Config.DEV1_QUERIES_TSV, 'r') as tsv:
        tsvReader = csv.reader(tsv, delimiter='\t')
        for line in tsvReader:
            queries[line[0]] = line[1]
    
    return queries

def getDevQrels() -> List:
    qrels = []
    with open(Config.DEV1_QRELS_TSV, 'r') as tsv:
        tsvReader = csv.reader(tsv, delimiter='\t')
        for line in tsvReader:
            qrels.append(Judgment(line[0],line[1],line[2],line[3]))
    
    return qrels

# Function from https://microsoft.github.io/msmarco/TREC-Deep-Learning.html
def getDocumentFromCorpus(document_id: str):
    (string1, string2, bundlenum, position) = document_id.split('_')
    assert string1 == 'msmarco' and string2 == 'doc'

    with open(f'{Config.CORPUS_DIRECTORY}/msmarco_doc_{bundlenum}', 'rt', encoding='utf8') as in_fh:
        in_fh.seek(int(position))
        json_string = in_fh.readline()
        document = json.loads(json_string)
        assert document['docid'] == document_id
        return document