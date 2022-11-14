from solr import Solr
import nltk
from nltk.corpus import stopwords


def addStopWords():
    collectionName = 'thesis-ltr'
    language = 'english'
    nltk.download('stopwords')
    Solr.addStopWords(collectionName, stopwords.words(language), language)
    
    
    
if __name__ == '__main__':
    addStopWords()