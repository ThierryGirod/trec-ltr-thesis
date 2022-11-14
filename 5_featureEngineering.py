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
            efi.ttf_values=\"  tf(title,'where'),
                                tf(title,'is'),
                                tf(title,'westminster'),
                                tf(title,'california')
            \" 
            efi.htf_values=\"  tf(headings,'where'),
                                tf(headings,'is'),
                                tf(headings,'westminster'),
                                tf(headings,'california')
            \" 
            efi.btf_values=\"  tf(body,'where'),
                                tf(body,'is'),
                                tf(body,'westminster'),
                                tf(body,'california')
            \" 
            efi.dtf_values=\"  tf(_text_,'where'),
                                tf(_text_,'is'),
                                tf(_text_,'westminster'),
                                tf(_text_,'california')
            \" 
            efi.tidf_values=\"  idf(title,'where'),
                                idf(title,'is'),
                                idf(title,'westminster'),
                                idf(title,'california')
            \" 
            efi.hidf_values=\"  idf(headings,'where'),
                                idf(headings,'is'),
                                idf(headings,'westminster'),
                                idf(headings,'california')
            \" 
            efi.bidf_values=\"  idf(body,'where'),
                                idf(body,'is'),
                                idf(body,'westminster'),
                                idf(body,'california')
            \" 
            efi.didf_values=\"  idf(_text_,'where'),
                                idf(_text_,'is'),
                                idf(_text_,'westminster'),
                                idf(_text_,'california')
            \" 
            efi.ttfidf_values=\"  product(tf(title,'where'),idf(title,'where')),
                                product(tf(title,'is'),idf(title,'is')),
                                product(tf(title,'westminster'),idf(title,'westminster')),
                                product(tf(title,'california'),idf(title,'california'))
            \" 
            efi.htfidf_values=\"  product(tf(headings,'where'),idf(headings,'where')),
                                product(tf(headings,'is'),idf(headings,'is')),
                                product(tf(headings,'westminster'),idf(headings,'westminster')),
                                product(tf(headings,'california'),idf(headings,'california'))
            \" 
            efi.btfidf_values=\"  product(tf(body,'where'),idf(body,'where')),
                                product(tf(body,'is'),idf(body,'is')),
                                product(tf(body,'westminster'),idf(body,'westminster')),
                                product(tf(body,'california'),idf(body,'california'))
            \" 
            efi.dtfidf_values=\"  product(tf(_text_,'where'),idf(_text_,'where')),
                                product(tf(_text_,'is'),idf(_text_,'is')),
                                product(tf(_text_,'westminster'),idf(_text_,'westminster')),
                                product(tf(_text_,'california'),idf(_text_,'california'))
            \" 
    ]""",
    'q': "id:msmarco_doc_05_72507775 OR id:msmarco_doc_19_673141443 OR id:msmarco_doc_19_673231526 OR id:msmarco_doc_10_1691063043",
    'rows': 10,
    'wt': 'json'  
}

response = requests.post(f'{Solr.solrUrl}{collectionName}/select', data=solrQuery).json()
print(response)

for doc in response['response']['docs']:
    # Parse '[features] array', ie
    # title_bm25=0.0,overview_bm25=13.237938,vote_average=7.0'
    features = doc['[features]']
    features = features.split(',')
    features = [float(ftr.split('=')[1]) for ftr in features]

    print(f"id:{doc['id']} {features}")
