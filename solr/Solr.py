import requests

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
    response = requests.post(collectionConfigUrl, json=deleteLtrQueryParser)
    print(response)
    
    response = requests.post(collectionConfigUrl, json=addLtrQueryParser).json()
    print(response)
    
    deleteLtrTransformer = { "delete-transformer": "features" }
    addLtrTransformer =  {
      "add-transformer": {
        "name": "features",
        "class": "org.apache.solr.ltr.response.transform.LTRFeatureLoggerTransformerFactory",
        "fvCacheName": "QUERY_DOC_FV"
    }}

    print(f"Adding LTR Doc Transformer for {collectionName} collection")
    response = requests.post(collectionConfigUrl, json=deleteLtrTransformer).json()
    print(response)
    response = requests.post(collectionConfigUrl, json=addLtrTransformer).json()
    print(response)
    
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