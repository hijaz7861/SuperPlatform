from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Document:
    document_id: str
    title: str
    content: str
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class DocumentSection:
    title: str
    content: str


@dataclass
class DocumentAnalysis:
    document_id: str
    sections: List[DocumentSection]
    topics: List[str]
    word_count: int
