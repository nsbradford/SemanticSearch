print("Begin imports...")
from tqdm import tqdm
import argparse
from typing import Iterable, List, Tuple
from backend.embed import load_model_hebbia, encode_document_with_stride
from backend.mongo import (
    upload_metadata_to_mongo,
    connect_to_mongo,
    lookup_passage_contents,
)
from backend.vector import batch_upsert, get_pinecone_query
import os
from backend.utils import timing, find_postfix, find_prefix
from backend.models import (
    Document,
    QueryFullAnswer,
    PassageEmbedding,
    QueryPassageAnswer,
)


from collections import defaultdict


@timing
def get_unprocessed_docs(docs: List[Document], db) -> List[Document]:
    # we maybe don't need to do this, can simply insert
    # and that will fail for existing ids
    to_insert = []
    for doc in docs:
        # skip if already exists , 'processed': True
        if db.docs.find_one({"_id": doc.hash_contents}):
            print(f"Skipping {doc} because it already exists and is processed")
        else:
            to_insert.append(doc)
    return to_insert


# @timing
# def mark_document_finished_processing(docs: List[Document], db):
#     # TODO batch...
#     for doc in docs:
#         db.docs.update_one({"_id": doc.hash_contents}, {"$set": {"processed": True}})
#     return None


@timing
def glob_docs(dir) -> List[Document]:
    print(f'Loading directory "{dir}"...')
    documents = []
    for file in os.listdir(dir):
        if file.endswith(".txt"):
            full_path = os.path.join(dir, file)
            # print(full_path)
            with open(full_path, "r") as f:
                file_contents = f.read()
                # file_contents_hash = hash(file_contents)
                # print(f'file_contents_hash={file_contents_hash}')
                doc = Document(name=file, contents=file_contents)
                print(doc)
                documents.append(doc)

    return documents


@timing
def encode_all_docs(docs, model, tokenizer):
    # TODO par with upserts to vector db
    passages = []
    for doc in tqdm(docs):
        embeddings = encode_document_with_stride(doc, model, tokenizer)
        passages.extend(embeddings)
    return passages


@timing
def process_docs(all_docs: List[Document], db, index, model, tokenizer) -> None:
    """
    TODO want to only both uploading docs which have not been uploaded yet

    Eventually will return Task IDs
    """
    docs = get_unprocessed_docs(all_docs, db)
    if docs:
        passages = encode_all_docs(docs, model, tokenizer)
        upload_metadata_to_mongo(docs, passages, db)
        # upload_to_s3(docs)
        all_embeddings = [passage.to_pinecone() for passage in passages]
        batch_upsert(all_embeddings, index)
        # mark_document_finished_processing(docs, db)
    return None


@timing
def present_passage(passage: PassageEmbedding, db) -> QueryPassageAnswer:
    # fetch all passages immediately before and after
    doc_id = passage.document_id
    seq = passage.sequence_num
    before_id = doc_id + "|" + str(seq - 1)
    after_id = doc_id + "|" + str(seq + 1)
    print(f"Looking up: before_id={before_id} after_id={after_id} doc_id={doc_id}")
    before = db.passages.find_one({"_id": before_id})
    after = db.passages.find_one({"_id": after_id})
    document_name = db.docs.find_one({"_id": doc_id})["name"]
    # merge the passages so there's not duplicate in the before and answer
    before_text = (
        find_prefix(before=before["text"], text=passage.text) if before else ""
    )
    after_text = find_postfix(text=passage.text, after=after["text"]) if after else ""
    answer = QueryPassageAnswer(
        before_text=before_text,
        passage_text=passage.text,
        after_text=after_text,
        document_name=document_name,
        document_id=doc_id,
    )
    answer.debug_full_text()
    return answer


@timing
def merge_top_passages(passages: List[PassageEmbedding]) -> List[PassageEmbedding]:
    # eliminate if any results overlap; i.e.
    seen = defaultdict(set)  # doc id => set of seen
    answer = []
    for passage in passages:
        doc_id = passage.document_id
        seq = passage.sequence_num
        adjacent = set([seq, seq - 1, seq + 1])
        if len(adjacent & seen[doc_id]) == 0:
            print(
                f"Adding {passage.id} because it does not overlap with a previous passage"
            )
            answer.append(passage)
            seen[doc_id].add(seq)
        else:
            print(f"Skipping {passage.id} because it overlaps with a previous passage")
    return answer


@timing
def execute_query(query: str, top_k: int, db, model, index) -> QueryFullAnswer:
    vector_results = get_pinecone_query(query, index, model, top_k=top_k)
    vector_ids = [r["id"] for r in vector_results]
    passages: List[PassageEmbedding] = lookup_passage_contents(db, vector_ids)

    for i, (vector_result, passage) in enumerate(zip(vector_results, passages)):
        print(
            f'{i}: id={vector_result["id"]} score={vector_result["score"]} | {passage.text}'
        )

    filtered = merge_top_passages(passages)[:3]
    results = [present_passage(passage, db) for passage in filtered]
    return QueryFullAnswer(results=results)
