from fastapi import FastAPI, UploadFile
from run import execute_query

from mongo import connect_to_mongo, clear_mongo_collections
from embed import load_model_hebbia, load_tokenizer_hebbia, load_automodel_hebbia
from vector import init_pinecone_and_get_index, clear_pinecone_index
from pydantic import BaseModel
from run import process_docs, glob_docs
from models import Document
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
async def upload(files: list[UploadFile]):
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
async def reupload_all():
    # clear_pinecone_index(app.pinecone_index)
    # clear_mongo_collections(app.mongo_db)

    docs = glob_docs('../data/essays')
    process_result = process_docs(
        docs, app.mongo_db, app.pinecone_index, app.automodel, app.tokenizer
    )
    return {'result': 'All docs successfully processed'}

@app.get("/document/{doc_id}")
async def document(doc_id):
    db = app.mongo_db
    print(f'Searching for doc_id: {doc_id}')
    doc = db.docs.find_one({'_id': doc_id})
    print(f'found doc: {doc}')
    return doc

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

