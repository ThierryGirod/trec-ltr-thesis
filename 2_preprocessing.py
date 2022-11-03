from ltr.data import CorpusApi, Config
import json
import re


def preprocess():

    files = []

    for corpusFile in CorpusApi.getCorpusFileByFile():
        files.append(corpusFile)

    for file in files:
    
        with open(file, 'r') as jsonFile:

            fileName = file.split('/')[-1]
            print(f'Start processing {fileName}')

            # Load the documents
            lines = jsonFile.readlines()

            # Load the documents into list
            documents = []
            for line in lines:
                document = json.loads(line)
                documents.append(document)

            # Preprocess the documents
            for i, document in enumerate(documents):
                # replace linebreaks with whitespaces
                document['title'] = re.sub('\n', ' ', document['title'])
                document['headings'] = re.sub('\n', ' ', document['headings'])
                document['body'] = re.sub('\n', ' ', document['body'])

                # replace punctuations
                document['title'] = re.sub('[^\w\s]', '', document['title'])
                document['headings'] = re.sub('[^\w\s]', '', document['headings'])
                document['body'] = re.sub('[^\w\s]', '', document['body'])

                # lower casing
                document['title'] = document['title'].lower()
                document['headings'] = document['headings'].lower()
                document['body'] = document['body'].lower()

                # replace multiple whitespaces with only one
                # must be at the end of the preprocessing step
                document['title'] = re.sub('\s{1,}', ' ', document['title'])
                document['headings'] = re.sub('\s{1,}', ' ', document['headings'])
                document['body'] = re.sub('\s{1,}', ' ', document['body'])

                print(f'{fileName}:{i+1}/{len(documents)} processed')
            
            CorpusApi.saveListAsJson(f'{Config.CORPUS_ROOT_DIRECTORY}/processed/{fileName}_processed.json', documents)
            print(f'End processing {fileName}')
        

if __name__ == '__main__':
    preprocess()