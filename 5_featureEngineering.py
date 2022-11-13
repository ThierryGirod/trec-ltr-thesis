import requests
from solr import Solr

collectionName = 'thesis-ltr'


solrQuery = {
    "fl": """id,title,[features 
            store=thesis-ltr 
            efi.keywords=\"where is westminster california\" 
            efi.tcqt_values=\"  if(termfreq(title,'where'),1,0),
                                if(termfreq(title,'is'),1,0),
                                if(termfreq(title,'westminster'),1,0),
                                if(termfreq(title,'california'),1,0)
            \" 
            efi.hcqt_values=\"  if(termfreq(headings,'where'),1,0),
                                if(termfreq(headings,'is'),1,0),
                                if(termfreq(headings,'westminster'),1,0),
                                if(termfreq(headings,'california'),1,0)
            \"
            efi.bcqt_values=\"  if(termfreq(body,'where'),1,0),
                                if(termfreq(body,'is'),1,0),
                                if(termfreq(body,'westminster'),1,0),
                                if(termfreq(body,'california'),1,0)
            \"
            efi.dcqt_values=\"  if(termfreq(_text_,'where'),1,0),
                                if(termfreq(_text_,'is'),1,0),
                                if(termfreq(_text_,'westminster'),1,0),
                                if(termfreq(_text_,'california'),1,0)
            \"
            efi.query_terms_length=4
    ]""",
    'q': "id:msmarco_doc_05_72507775 OR id:msmarco_doc_19_673141443 OR id:msmarco_doc_19_673231526 OR id:msmarco_doc_10_1691063043",
    'rows': 10,
    'wt': 'json'  
}

response = requests.post(f'{Solr.solrUrl}{collectionName}/select', data=solrQuery)


for doc in response.json()['response']['docs']:
    # Parse '[features] array', ie
    # title_bm25=0.0,overview_bm25=13.237938,vote_average=7.0'
    features = doc['[features]']
    features = features.split(',')
    features = [float(ftr.split('=')[1]) for ftr in features]

    print(f"id:{doc['id']} [{features}]")
