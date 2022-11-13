from ltr.data import CorpusApi
from solr import Solr
import requests
import json
import re
    
collectionName = 'thesis-ltr'
response = requests.delete(f'{Solr.solrUrl}{collectionName}/schema/feature-store/{collectionName}')

print(response)

featureSet = [
    # Covered query terms
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
    # Covered query terms ratio
    {
      "name" : "title_coveredQueryTermsRatio",
      "store": "thesis-ltr",
      "class" : "org.apache.solr.ltr.feature.SolrFeature",
      "params" : {
        "q" : "{!func} div(sum(${tcqt_values}),${query_terms_length})"
      }
    },
    {
      "name" : "headings_coveredQueryTermsRatio",
      "store": "thesis-ltr",
      "class" : "org.apache.solr.ltr.feature.SolrFeature",
      "params" : {
        "q" : "{!func} div(sum(${hcqt_values}),${query_terms_length})"
      }
    },
    {
      "name" : "body_coveredQueryTermsRatio",
      "store": "thesis-ltr",
      "class" : "org.apache.solr.ltr.feature.SolrFeature",
      "params" : {
        "q" : "{!func} div(sum(${bcqt_values}),${query_terms_length})"
      }
    },
    {
      "name" : "document_coveredQueryTermsRatio",
      "store": "thesis-ltr",
      "class" : "org.apache.solr.ltr.feature.SolrFeature",
      "params" : {
        "q" : "{!func} div(sum(${dcqt_values}),${query_terms_length})"
      }
    },
    # Sum of inverse document frequency values
    {
      "name" : "title_idf",
      "store": "thesis-ltr",
      "class" : "org.apache.solr.ltr.feature.SolrFeature",
      "params" : {
        "q" : "{!func} sum(${tidf_values})"
      }
    },
    {
      "name" : "headings_idf",
      "store": "thesis-ltr",
      "class" : "org.apache.solr.ltr.feature.SolrFeature",
      "params" : {
        "q" : "{!func} sum(${hidf_values})"
      }
    },
    {
      "name" : "body_idf",
      "store": "thesis-ltr",
      "class" : "org.apache.solr.ltr.feature.SolrFeature",
      "params" : {
        "q" : "{!func} sum(${bidf_values})"
      }
    },
    {
      "name" : "document_idf",
      "store": "thesis-ltr",
      "class" : "org.apache.solr.ltr.feature.SolrFeature",
      "params" : {
        "q" : "{!func} sum(${didf_values})"
      }
    },
    # BM 25 Scores
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
                    json=featureSet).json()


print(response)