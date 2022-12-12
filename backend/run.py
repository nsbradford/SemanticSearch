print('Begin imports...')
import argparse
from typing import Iterable, List, Tuple
from embed import get_embeddings_with_metadata, load_model_hebbia
from mongo import upload_docs_to_mongo, connect_to_mongo, lookup_line_contents
from vector import batch_upsert, get_pinecone_query
import os
from utils import timing
from models import Document
from s3 import upload_to_s3


@timing
def process_docs(documents: List[Document], db, model, index) -> None:
    # TODO want to only both uploading docs which have not been uploaded yet
    # Eventually will return Task IDs
    upload_to_s3(documents)
    upload_docs_to_mongo(db, documents)
    all_embeddings = [
        embeddings
        for doc in documents
        for embeddings in get_embeddings_with_metadata(model, doc)
    ]
    batch_upsert(all_embeddings, index)


def execute_query(query: str, top_k: int, db, model, index):
    results = get_pinecone_query(query, index, model, top_k=top_k)
    result_ids = [r["id"] for r in results]
    mongo_contents = lookup_line_contents(db, result_ids)

    for i, (result, content) in enumerate(zip(results, mongo_contents)):
        print(f'{i}: id={result["id"]} doc={content["documents"]} score={result["score"]} | {content["text"]}')
        
    return mongo_contents