from typing import Any, Iterable, List, Tuple
import pinecone
from dotenv import load_dotenv
import os
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from backend.utils import chunks, timing


@timing
def init_pinecone() -> None:
    load_dotenv()
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone.init(api_key=pinecone_api_key, environment="us-west1-gcp")
    print("connected to pinecone")
    print("Indexes:", pinecone.list_indexes())


def init_pinecone_and_get_index() -> pinecone.Index:
    init_pinecone()
    index_name = "semantic-384"
    assert index_name in pinecone.list_indexes()
    index_quickstart = pinecone.Index(index_name, pool_threads=30)
    return index_quickstart


# def upsert():
#     print('Upsert vectors...')
#     # Upsert sample data (5 8-dimensional vectors)
#     index_quickstart.upsert([
#         ("A", [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]),
#         ("B", [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]),
#         ("C", [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]),
#         ("D", [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]),
#         ("E", [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
#     ])


# TODO this takes the exact same amount of time... why?
@timing
def batch_upsert_parallel(
    embeddings: Iterable[Tuple[str, List[float], dict]],
    index: pinecone.Index,
):
    """
    https://docs.pinecone.io/docs/insert-data#sending-upserts-in-parallel
    """
    print(f"Upserting {len(embeddings)} vectors in parallel...")

    # Upsert data with 100 vectors per upsert request asynchronously
    # - Create pinecone.Index with pool_threads=30 (limits to 30 simultaneous requests)
    # - Pass async_req=True to index.upsert()
    # Send requests in parallel
    print("Sending requests in parallel...")
    async_results = [
        index.upsert(vectors=ids_vectors_chunk, async_req=True)
        for ids_vectors_chunk in chunks(embeddings, batch_size=100)
    ]
    print("Waiting for results...")
    # Wait for and retrieve responses (this raises in case of error)
    return [async_result.get() for async_result in async_results]


@timing
def batch_upsert(
    embeddings: Iterable[Tuple[str, List[float], dict]], index: pinecone.Index
):
    """
    Batch upserts in 100 or fewer.
    https://docs.pinecone.io/docs/insert-data
    """
    print(f"Upserting {len(embeddings)} vectors sequentially...")
    with tqdm(total=len(embeddings)) as pbar:
        for ids_vectors_chunk in chunks(embeddings, batch_size=100):
            index.upsert(vectors=ids_vectors_chunk)
            pbar.update(len(ids_vectors_chunk))


@timing
def get_pinecone_query(
    query: str,
    index: pinecone.Index,
    model: SentenceTransformer,
    top_k: int,
) -> List[Any]:
    embeddings = model.encode([query], show_progress_bar=True)
    query_embedding = embeddings[0].tolist()
    print(f'Querying Pinecone index={index} for "{query}"')
    query_results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_values=False,
        include_metadata=False,
        # filter={
        #     "active": True,
        # },
    )
    matches = query_results["matches"]
    for match in matches:
        # del match['values']
        print(match)
    return matches


@timing
def clear_pinecone_index(index):
    print(f"deleting index {index}...")
    print(index.describe_index_stats())
    index.delete(delete_all=True)


def create_index():
    init_pinecone()
    pinecone.create_index("semantic-384", dimension=384, metric="cosine", pod_type="p1")


if __name__ == "__main__":
    # index = init_pinecone_and_get_index()
    # index.delete(ids=["id-1", "id-2"], namespace='example-namespace')
    # index.delete(delete_all=True) # , namespace=''

    # create new index
    create_index()
    print("Indexes:", pinecone.list_indexes())

    # do some deletions
    # pinecone.delete_index("semantic-768")
    # index = init_pinecone_and_get_index()
    # clear_pinecone_index(index)

    # index_quickstart = pinecone.Index("quickstart")
    # print(index_quickstart.describe_index_stats())

    # print(
    #     index_quickstart.query(
    #     vector=[0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
    #     top_k=3,
    #     include_values=True
    #     )
    # )
    # pinecone.delete_index("quickstart")
    # print('done')
