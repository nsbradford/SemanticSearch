from pymongo import MongoClient
import pymongo
from dotenv import dotenv_values
from utils import timing, remove_duplicates
from models import Document, PassageEmbedding
from typing import List

# https://www.mongodb.com/languages/python/pymongo-tutorial

@timing
def connect_to_mongo():
    config = dotenv_values(".env")
    mongodb_client = MongoClient(config["MONGO_URI"])
    database = mongodb_client[config["MONGO_DB_NAME"]]
    print("Connected to the MongoDB database!")
    return mongodb_client, database


@timing
def clear_mongo_collections(db):
    db.docs.drop()
    db.passages.drop()


@timing
def upload_metadata_to_mongo(docs: List[Document], passages: List[PassageEmbedding], db):
    print(f"Uploading {len(docs)} documents to MongoDB...")
    db.docs.insert_many([d.mongo_dict() for d in docs])

    print(f"Uploading {len(passages)} lines to MongoDB...")
    passage_dicts = [p.to_mongo() for p in passages]    
    if passage_dicts:
        # print(f"sample: {passage_dicts[0]}")
        # https://stackoverflow.com/questions/61480444/mongodb-insertmany-and-skip-duplicates
        try:
            db.passages.insert_many(passage_dicts, ordered=False)
        except pymongo.errors.BulkWriteError as e:
            print(e.details)
            print('Got a BulkWriteError for duplicate keys, NBD, continuing...')
    return None


# @timing
# def upload_metadata_to_mongo_lines(database, docs: List[Document]):
#     # we probably don't need to do this, can simply insert 
#     # and that will fail for existing ids
#     to_insert = []
#     for doc in docs:
#         # skip if already exists
#         if database.docs.find_one({"_id": doc.hash_contents}):
#             print(f"Skipping {doc} because it already exists")
#         else:
#             to_insert.append(doc)

#     print(f"Uploading {len(to_insert)} documents to MongoDB...")
#     if to_insert:
#         database.docs.insert_many([d.mongo_dict() for d in to_insert])
    
#     lines = [line for d in to_insert for line in d.mongo_dict_lines()]
#     deduped_lines = remove_duplicates(lines, key=lambda d: d['_id'])
#     print(f"Uploading {len(deduped_lines)} lines to MongoDB...")
#     if deduped_lines:
#         print(f"sample: {deduped_lines[0]}")
#         # https://stackoverflow.com/questions/61480444/mongodb-insertmany-and-skip-duplicates
#         try:
#             database.lines.insert_many(deduped_lines, ordered=False)
#         except pymongo.errors.BulkWriteError as e:
#             print(e.details)
#             print('Got a BulkWriteError for duplicate keys, NBD, continuing...')
#     return None


@timing
def lookup_passage_contents(db, passage_ids: List[str]) -> List[dict]:
    passages_raw = list(db.passages.find({'_id': {'$in': passage_ids}}))
    print(f"Found {len(passages_raw)}/{len(passage_ids)} matching IDs in MongoDB")
    passages = [PassageEmbedding.from_mongo(p) for p in passages_raw]
    return passages