from fastapi import FastAPI, UploadFile
from run import execute_query

from mongo import connect_to_mongo, clear_mongo_collections
from embed import load_model_hebbia, load_tokenizer_hebbia, load_automodel_hebbia
from vector import init_pinecone_and_get_index, clear_pinecone_index
from pydantic import BaseModel
from run import process_docs, glob_docs
from models import Document

app = FastAPI()


#===============================================================================
# Models

class QueryParams(BaseModel):
    query: str
    top_k: int = 10


#===============================================================================
# Endpoints

@app.post("/query")
async def query(params: QueryParams):
    return execute_query(
        params.query, params.top_k, app.mongo_db, app.embedding_model, app.pinecone_index
    )


@app.post("/upload")
async def upload_many(files: list[UploadFile]):
    print(f'received filesnames: {[file.filename for file in files]}')
    docs = []
    for file in files:
        contents = await file.read() # TODO could par
        doc = Document(name=file.filename, contents=contents)
        docs.append(doc)

    # TODO async and then return task ID
    process_result = process_docs(
        docs, app.mongo_db, app.pinecone_index, app.automodel, app.tokenizer
    )
    return {'result': 'All docs successfully processed'}


@app.post("/reupload_all")
async def upload_all():
    clear_pinecone_index(app.pinecone_index)
    clear_mongo_collections(app.mongo_db)

    docs = glob_docs('../data/essays')
    process_result = process_docs(
        docs, app.mongo_db, app.pinecone_index, app.automodel, app.tokenizer
    )
    return {'result': 'All docs successfully processed'}

#===============================================================================
# App startup

@app.on_event("startup")
async def load_pinecone_index():
    app.pinecone_index = init_pinecone_and_get_index()

@app.on_event("shutdown")
async def shutdown_pinecone_index():
    app.pinecone_index.close()

@app.on_event("startup")
async def load_ml_models():
    # TODO refactor to only load one model instead of the same one twice
    app.embedding_model = load_model_hebbia()
    app.automodel = load_automodel_hebbia()
    app.tokenizer = load_tokenizer_hebbia()

@app.on_event("startup")
async def start_mongo_client():
    app.mongo_client, app.mongo_db = connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_client.close()

