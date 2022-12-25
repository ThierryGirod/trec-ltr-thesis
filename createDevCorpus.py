from ltr.Judgment import Judgment
from ltr.data import CorpusApi, Config

judgments = CorpusApi.getTrainQrels()


devCorpus = []

for j in judgments:
    doc = CorpusApi.getDocumentFromCorpus(j.docId)
    devCorpus.append(doc)
    print(f'{len(devCorpus)}/{len(judgments)} finished doc {j.docId}')

print(f'finished {len(devCorpus)}')
CorpusApi.saveListAsJson('/home/ubuntu/trec-ltr-thesis/devCorpus.json', devCorpus)