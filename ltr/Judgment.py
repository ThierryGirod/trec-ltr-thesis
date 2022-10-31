from dataclasses import dataclass

@dataclass
class Judgment:
    query: str
    iteration: int
    docId: str
    relevancy: int