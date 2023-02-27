from solr import Solr
import nltk
from nltk.corpus import stopwords

# Get the stopwords from nltk and import them to the collection
def addStopWords():
    collectionName = 'thesis-ltr'
    language = 'english'
    nltk.download('stopwords')
    Solr.addStopWords(collectionName, stopwords.words(language), language)
    
    
    
if __name__ == '__main__':
    addStopWords()