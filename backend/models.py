from functools import cache, cached_property
from pydantic import BaseModel
from typing import List
from utils import remove_duplicates, hash_sha256

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
        d['is_active'] = False
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
