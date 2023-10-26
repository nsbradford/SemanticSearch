from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile

from backend.embed import (
    load_automodel_hebbia,
    load_model_hebbia,
    load_tokenizer_hebbia,
)
from backend.llm import llm_get
from backend.models import Document, LLMChatCompletionRequest, QueryParams
from backend.mongo import connect_to_mongo
from backend.run import execute_query, glob_docs, process_docs
from backend.utils import load_middleware
from backend.vector import init_pinecone_and_get_index

load_dotenv()
app = FastAPI()
load_middleware(app)

# ===============================================================================
# Endpoints


@app.post("/query")
async def query(params: QueryParams):
    return execute_query(
        params.query,
        params.top_k,
        app.mongo_db,
        app.embedding_model,
        app.pinecone_index,
    )


@app.post("/llm/")
async def llm(request: LLMChatCompletionRequest):
    result = await llm_get(request.model, request.messages, request.sessionId)
    return { 'text': result }


@app.get("/document/{doc_id}")
async def document(doc_id):
    db = app.mongo_db
    print(f"Searching for doc_id: {doc_id}")
    doc = db.docs.find_one({"_id": doc_id})
    print(f"found doc: {doc}")
    return doc


@app.post("/upload")
async def upload(files: list[UploadFile]):
    print(f"received filesnames: {[file.filename for file in files]}")
    docs = []
    for file in files:
        contents = await file.read()  # TODO could par
        doc = Document(name=file.filename, contents=contents)
        docs.append(doc)

    # later make async and then return task ID
    process_result = process_docs(
        docs, app.mongo_db, app.pinecone_index, app.automodel, app.tokenizer
    )
    return {"result": "All docs successfully processed"}


@app.post("/reupload_all")
async def reupload_all():
    # clear_pinecone_index(app.pinecone_index)
    # clear_mongo_collections(app.mongo_db)

    docs = glob_docs("../data/essays")
    process_result = process_docs(
        docs, app.mongo_db, app.pinecone_index, app.automodel, app.tokenizer
    )
    return {"result": "All docs successfully processed"}


# ===============================================================================
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
