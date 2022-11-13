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
      "name" : "title_coveredQueryTerms",
      "store": "thesis-ltr",
      "class" : "org.apache.solr.ltr.feature.SolrFeature",
      "params" : {
        "q" : "{!func} sum(${tcqt_values})"
      }
    },
    {
      "name" : "headings_coveredQueryTerms",
      "store": "thesis-ltr",
      "class" : "org.apache.solr.ltr.feature.SolrFeature",
      "params" : {
        "q" : "{!func} sum(${hcqt_values})"
      }
    },
    {
      "name" : "body_coveredQueryTerms",
      "store": "thesis-ltr",
      "class" : "org.apache.solr.ltr.feature.SolrFeature",
      "params" : {
        "q" : "{!func} sum(${bcqt_values})"
      }
    },
    {
      "name" : "document_coveredQueryTerms",
      "store": "thesis-ltr",
      "class" : "org.apache.solr.ltr.feature.SolrFeature",
      "params" : {
        "q" : "{!func} sum(${dcqt_values})"
      }
    },
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
    }, 
    {
      "name" : "document_bm25",
      "store": "thesis-ltr",
      "class" : "org.apache.solr.ltr.feature.SolrFeature",
      "params" : {
        "q" : "_text_:(${keywords})"
      }
    },
]

response = requests.put(f'{Solr.solrUrl}{collectionName}/schema/feature-store',
                    json=featureSet)


print(response.json())