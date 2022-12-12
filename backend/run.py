print('Begin imports...')
import argparse
from typing import Iterable, List, Tuple
from embed import load_model_hebbia, encode_document_with_stride
from mongo import upload_metadata_to_mongo, connect_to_mongo, lookup_passage_contents
from vector import batch_upsert, get_pinecone_query
import os
from utils import timing
from models import Document
from s3 import upload_to_s3


# @timing
# def get_unprocessed_docs(docs: List[Document], db) -> List[Document]:
#     # we maybe don't need to do this, can simply insert 
#     # and that will fail for existing ids
#     to_insert = []
#     for doc in docs:
#         # skip if already exists
#         if db.docs.find_one({"_id": doc.hash_contents, 'processed': True}):
#             print(f"Skipping {doc} because it already exists and is processed")
#         else:
#             to_insert.append(doc)

# @timing
# def mark_document_finished_processing(docs: List[Document], db):
#     # TODO batch...
#     for doc in docs:
#         db.docs.update_one({"_id": doc.hash_contents}, {"$set": {"processed": True}})
#     return None


@timing
def process_docs(all_docs: List[Document], db, index, model, tokenizer) -> None:
    """
    TODO want to only both uploading docs which have not been uploaded yet
    
    Eventually will return Task IDs
    """
    docs = all_docs #get_unprocessed_docs(all_docs, db)
    
    passages = [
        embeddings
        for doc in docs
        for embeddings in encode_document_with_stride(doc, model, tokenizer)
    ]
    upload_metadata_to_mongo(docs, passages, db)
    # upload_to_s3(docs)

    all_embeddings = [passage.to_pinecone() for passage in passages]
    batch_upsert(all_embeddings, index)
    # mark_document_finished_processing(docs, db)


def execute_query(query: str, top_k: int, db, model, index):
    vector_results = get_pinecone_query(query, index, model, top_k=top_k)
    vector_ids = [r["id"] for r in vector_results]
    mongo_contents = lookup_passage_contents(db, vector_ids)

    for i, (vector_result, content) in enumerate(zip(vector_results, mongo_contents)):
        print(f'{i}: id={vector_result["id"]} score={vector_result["score"]} | {content["text"]}')

    return mongo_contents