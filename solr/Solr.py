import requests
import json
from nltk.tokenize import word_tokenize

LTRPS_SOLR_HOST = 'localhost'
LTRPS_SOLR_PORT = '8983'

solrUrl = f'http://{LTRPS_SOLR_HOST}:{LTRPS_SOLR_PORT}/solr/'
solrCollectionsApi = f'{solrUrl}admin/collections'


def deleteCollection(collectionName: str):
    
    deleteCollectionParams = [
        ('action', "delete"),
        ('name', collectionName)
    ]

    print(f"Deleting '{collectionName}' collection")
    response = requests.post(solrCollectionsApi, data=deleteCollectionParams).json()

def createCollection(collectionName: str):
    
    deleteCollection(collectionName)    

    # Create collection
    createCollectionParams = [
        ('action', "create"),
        ('name', collectionName),
        ('numShards', 1),
        ('replicationFactor', 1),
        ('collection.configName','thesis-ltr')]

    print(createCollectionParams)

    print(f"Creating '{collectionName}' collection")
    response = requests.post(solrCollectionsApi, data=createCollectionParams).json()
    print(response)

def enableLtr(collectionName: str):
    # First setup ltr jar in your solr installation
    # https://solr.apache.org/guide/solr/latest/query-guide/learning-to-rank.html#installation-of-ltr
    collectionConfigUrl = f'{solrUrl}{collectionName}/config'
    
    deleteLtrQueryParser = { "delete-queryparser": "ltr" }
    addLtrQueryParser = {
     "add-queryparser": {
        "name": "ltr",
            "class": "org.apache.solr.ltr.search.LTRQParserPlugin"
        }
    }

    print(f"Del/Adding LTR QParser for {collectionName} collection")
    print("------------")
    response = requests.post(collectionConfigUrl, json=deleteLtrQueryParser).json()
    print("Status: Success" if response["responseHeader"]["status"] == 0 else "Status: Failure; Response:[ " + str(response) + " ]" )
    print("------------")
    response = requests.post(collectionConfigUrl, json=addLtrQueryParser).json()
    print("Status: Success" if response["responseHeader"]["status"] == 0 else "Status: Failure; Response:[ " + str(response) + " ]" )
    
    deleteLtrTransformer = { "delete-transformer": "features" }
    addLtrTransformer =  {
      "add-transformer": {
        "name": "features",
        "class": "org.apache.solr.ltr.response.transform.LTRFeatureLoggerTransformerFactory",
        "fvCacheName": "QUERY_DOC_FV"
    }}

    print(f"Adding LTR Doc Transformer for {collectionName} collection")
    print("------------")
    response = requests.post(collectionConfigUrl, json=deleteLtrTransformer).json()
    print("Status: Success" if response["responseHeader"]["status"] == 0 else "Status: Failure; Response:[ " + str(response) + " ]" )
    print("------------")
    response = requests.post(collectionConfigUrl, json=addLtrTransformer).json()
    print("Status: Success" if response["responseHeader"]["status"] == 0 else "Status: Failure; Response:[ " + str(response) + " ]" )
    
def createTextType(collectionName: str, typeName: str):
    addTextType = {"add-field-type":{
        "name":typeName,
        "class":"solr.TextField",
        "positionIncrementGap":"100",
        "multiValued": "true",
        "indexAnalyzer":{
          "tokenizer":{
            "class":"solr.StandardTokenizerFactory"},
          "filters":[{
              "class":"solr.ManagedStopFilterFactory",
              "managed":"english",
              },
            {
              "class":"solr.LowerCaseFilterFactory"}]},
        "queryAnalyzer":{
          "tokenizer":{
            "class":"solr.StandardTokenizerFactory"},
          "filters":[{
              "class":"solr.ManagedStopFilterFactory",
              "managed":"english",
              },
            {
              "class":"solr.ManagedSynonymGraphFilterFactory",
              "managed":"english"},
            {
              "class":"solr.LowerCaseFilterFactory"}]}},
      
    }
    response = requests.post(f"{solrUrl}{collectionName}/schema", json=addTextType).json()
    print(f'Added {typeName}')
    
    
    
def createTextField(collectionName: str, fieldName: str, typeName: str):
    # Delete first existing field
    deleteField(collectionName, fieldName)
    
    addField = {"add-field":{ "name":fieldName, "type": typeName, "stored":"true", "indexed":"true", "multiValued":"false" }}
    response = requests.post(f"{solrUrl}{collectionName}/schema", json=addField).json()
    print(f'Added {fieldName}')

def deleteField(collectionName: str, fieldName: str):
    deleteField = {"delete-field":{ "name":fieldName }}
    response = requests.post(f"{solrUrl}{collectionName}/schema", json=deleteField).json()
    print(f'Deleted {fieldName}')

def addCopyField(collectionName: str, srcField: str, destField: str):
    rule = {"source": srcField, "dest": destField}
    copyField = {"add-copy-field": rule}

    response = requests.post(f"{solrUrl}{collectionName}/schema", json=copyField).json()
    print(f'Added {srcField}/{destField}')
    
def indexFile(collectionName: str, path: str):
    solrIndexApi = f'{solrUrl}{collectionName}/update?commit=true'
    with open(path, 'r') as jsonFile:
        print(f'{path} loading')
        headers = {"Content-Type": "application/json"}
        response = requests.post(solrIndexApi, data=jsonFile, headers=headers)
        print(f'data send')
        print(response.json())
        
def addStopWords(collectionName: str, stopWords: list, lang: str):
  solrStopWordsApi = f'{solrUrl}{collectionName}/schema/analysis/stopwords/{lang}'
  response = requests.put(solrStopWordsApi, json=stopWords).json()
  print(response)
  
def removeStopWords(collectionName: str, stopWords: list, lang: str):
  solrStopWordsApi = f'{solrUrl}{collectionName}/schema/analysis/stopwords/{lang}'
  for word in stopWords:
    response = requests.delete(f'{solrStopWordsApi}/{word}').json()
    print(response)
    print(f'Deleted {word}')


def featureLoggingToFile(collectionName: str, path: str):
    solrQueryApi = f'{solrUrl}{collectionName}/select'
    data = []
    with open(path, 'r') as jsonFile:
      
      data = json.load(jsonFile)
      print(f'{path} loaded')  
    
    judgmentsPerQuery = {}
    for judgment in data:
      docs = judgmentsPerQuery.get(judgment['queryText'], [])
      docs.append(judgment)
      judgmentsPerQuery[judgment['queryText']] = docs.copy()
    
    for query, judgments in list(judgmentsPerQuery.items())[:1]:
      docIds = ' OR '.join([f"id:{j['docId']}" for j in judgments])
      queryTokens = word_tokenize(query)
      tcqtValues = ', '.join([f"if(termfreq(title,'{t}'),1,0)" for t in queryTokens])
      hcqtValues = ', '.join([f"if(termfreq(headings,'{t}'),1,0)" for t in queryTokens])
      bcqtValues = ', '.join([f"if(termfreq(body,'{t}'),1,0)" for t in queryTokens])
      dcqtValues = ', '.join([f"if(termfreq(_text_,'{t}'),1,0)" for t in queryTokens])
      ttfValues = ', '.join([f"tf(title,'{t}')" for t in queryTokens])
      htfValues = ', '.join([f"tf(headings,'{t}')" for t in queryTokens])
      btfValues = ', '.join([f"tf(body,'{t}')" for t in queryTokens])
      dtfValues = ', '.join([f"tf(_text_,'{t}')" for t in queryTokens])
      tidfValues = ', '.join([f"idf(title,'{t}')" for t in queryTokens])
      hidfValues = ', '.join([f"idf(headings,'{t}')" for t in queryTokens])
      bidfValues = ', '.join([f"idf(body,'{t}')" for t in queryTokens])
      didfValues = ', '.join([f"idf(_text_,'{t}')" for t in queryTokens])
      ttfidfValues = ', '.join([f"product(tf(title,'{t}'),idf(title,'{t}'))" for t in queryTokens])
      htfidfValues = ', '.join([f"product(tf(headings,'{t}'),idf(headings,'{t}'))" for t in queryTokens])
      btfidfValues = ', '.join([f"product(tf(body,'{t}'),idf(body,'{t}'))" for t in queryTokens])
      dtfidfValues = ', '.join([f"product(tf(_text_,'{t}'),idf(_text_,'{t}'))" for t in queryTokens])
      solrFeatureQuery = {
          "fl": f"""id,title,[features 
                  store=thesis-ltr 
                  efi.keywords=\"{query}\" 
                  efi.tcqt_values=\"  {tcqtValues}
                  \" 
                  efi.hcqt_values=\"  {hcqtValues}
                  \"
                  efi.bcqt_values=\"  {bcqtValues}
                  \"
                  efi.dcqt_values=\"  {dcqtValues}
                  \"
                  efi.query_terms_length={len(queryTokens)}
                  efi.ttf_values=\"  {ttfValues}
                  \" 
                  efi.htf_values=\"  {htfValues}
                  \" 
                  efi.btf_values=\"  {btfValues}
                  \" 
                  efi.dtf_values=\"  {dtfValues}
                  \" 
                  efi.tidf_values=\"  {tidfValues}
                  \" 
                  efi.hidf_values=\"  {hidfValues}
                  \" 
                  efi.bidf_values=\"  {bidfValues}
                  \" 
                  efi.didf_values=\"  {didfValues}
                  \" 
                  efi.ttfidf_values=\"  {ttfidfValues}
                  \" 
                  efi.htfidf_values=\"  {htfidfValues}
                  \" 
                  efi.btfidf_values=\"  {btfidfValues}
                  \" 
                  efi.dtfidf_values=\"  {dtfidfValues}
                  \" 
          ]""",
          'q': f"{docIds}",
          'rows': 10,
          'wt': 'json'  
      }
      print(f'{tcqtValues}{hcqtValues}{bcqtValues}{dcqtValues}')
      