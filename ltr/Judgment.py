from dataclasses import dataclass

@dataclass
class Judgment:
    query: str
    queryText: str
    iteration: int
    docId: str
    relevancy: int