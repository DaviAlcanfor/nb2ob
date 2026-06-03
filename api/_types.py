from typing import List, TypedDict



class Sources(TypedDict):
    id: str
    title: str
    content: str

class SummarizedSource(TypedDict):
    id: str
    title: str
    summary: str

class Notebook(TypedDict):
    id: str
    title: str
    sources_count: int
    sources: List[Sources]
    summaries: List[SummarizedSource]

