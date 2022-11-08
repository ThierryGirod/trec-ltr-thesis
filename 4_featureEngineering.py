from ltr.data import CorpusApi
from solr import Solr
import requests
import json
import re

queries = CorpusApi.getDevQueriesAsDict()
judgments = CorpusApi.getDevQrels()

for judgment in judgments:
    judgment.query = queries[judgment.query]
    
collectionName = 'thesis-ltr'
requests.delete(f'{Solr.solrUrl}{collectionName}/schema/feature-store/{collectionName}')

featureSet = [
    {
      "name" : "title_bm25",
      "store": "thesis-ltr",
      "class" : "org.apache.solr.ltr.feature.SolrFeature",
      "params" : {
        "q" : "title:(${keywords})"
      }
    },
    {
      "name" : "headings_bm25",
      "store": "thesis-ltr",
      "class" : "org.apache.solr.ltr.feature.SolrFeature",
      "params" : {
        "q" : "headings:(${keywords})"
      }
    },
    {
      "name" : "body_bm25",
      "store": "thesis-ltr",
      "class" : "org.apache.solr.ltr.feature.SolrFeature",
      "params" : {
        "q" : "body:(${keywords})"
      }
    }
]

response = requests.put(f'{Solr.solrUrl}{collectionName}/schema/feature-store',
                    json=featureSet)



for i, judgment in enumerate(judgments):
    print(f'Start {i + 1}')
    judgment.query = re.sub('[^\w\s]', '', judgment.query)
    featureLoggingQuery = {
        "fl": f"id,title,[features store=thesis-ltr efi.keywords=\"{judgment.query}\"]",
        'q': f"id:{judgment.docId}",
        'rows': 10,
        'wt': 'json'  
    }
    
    print(featureLoggingQuery)

    response = requests.post(f'{Solr.solrUrl}{collectionName}/select', data=featureLoggingQuery)


    print(response.json())
    #features = response.json()['response']['docs'][0]['[features]']
    #judgment.features = [float(feature.split('=')[1]) for feature in features.split(',')]
    print(f'Processed {i + 1}/{len(judgments)}')

print(judgments)