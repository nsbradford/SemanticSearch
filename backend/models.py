from functools import cache, cached_property
from pydantic import BaseModel
from typing import List
from utils import remove_duplicates, hash_sha256


class PassageEmbedding(BaseModel):
    id: str
    embedding: List[float]
    metadata: dict
    text: str
    document_id: str


    @property
    def sequence_num(self) -> int:
        return int(self.id.split('|')[1])

    def to_pinecone(self):
        return (self.id, self.embedding, self.metadata)
    
    def to_mongo(self):
        d = self.dict()
        d['_id'] = self.id
        del d['id']
        return d
    
    @staticmethod
    def from_mongo(dict):
        d = dict.copy()
        d['id'] = d['_id']
        del d['_id']
        return PassageEmbedding(**d)


class QueryPassageAnswer(BaseModel):
    # passage: PassageEmbedding
    # before: PassageEmbedding
    # after: PassageEmbedding
    before_text: str
    passage_text: str
    after_text: str
    document_name: str

    def debug_full_text(self) -> None:
        print(f"\nBEFORE:{self.before_text}")
        print(f'TARGET:{self.passage_text}')
        print(f'AFTER:{self.after_text}')
        print(f'\nCombined: {self.before_text}{self.passage_text}{self.after_text}')


class QueryFullAnswer(BaseModel):
    # query: str
    results: List[QueryPassageAnswer]


class Document(BaseModel):
    name: str
    contents: str

    class Config:
        arbitrary_types_allowed = True
        keep_untouched = (cached_property,)

    def __str__(self):
        return f'Document(name={self.name}, hash={self.hash_contents})'

    @cached_property
    def hash_contents(self) -> str:
        return hash_sha256(self.contents)

    @cached_property
    def lines(self) -> List[str]:
        return self.contents.splitlines()

    def mongo_dict(self) -> dict:
        d = self.dict()
        d['_id'] = self.hash_contents
        d['lines'] = [
            {hash_sha256(line): i} for i, line in enumerate(self.lines)
        ]
        # d['is_active'] = False
        d['processed'] = 'IN_PROGRESS' # or 'COMPLETE'
        return d
    
    def mongo_dict_lines(self) -> List[dict]:
        line_dicts = [
            {   # not an elegant way to handle duplicates, but oh well
                '_id': hash_sha256(line),
                'documents': [self.hash_contents],
                'text': line,
            }
            for (line_number, line) in enumerate(self.lines)
        ]
        deduped = remove_duplicates(line_dicts, key=lambda d: d['_id'])
        print(f'Got {len(line_dicts)} line dicts, deduped to {len(deduped)}')
        return deduped
