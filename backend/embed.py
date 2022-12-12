from typing import Iterable, List, Tuple
from utils import hash_sha256
from functools import cache, cached_property
from sentence_transformers import SentenceTransformer
from utils import timing
from models import Document
from transformers import AutoTokenizer


def tokenize_str(text: str, tokenizer: AutoTokenizer) -> List[str]:
    result = tokenizer(text)
    token_ids = result["input_ids"]
    print(token_ids)
    decoded = [tokenizer.decode(x) for x in token_ids]
    return decoded


def load_tokenizer_hebbia():
    return AutoTokenizer.from_pretrained('sentence-transformers/msmarco-MiniLM-L-6-v3')


def load_model_hebbia():
    """384-dimensional embeddings"""
    return SentenceTransformer('sentence-transformers/msmarco-MiniLM-L-6-v3')


@timing
def get_embeddings_with_metadata(
    model: SentenceTransformer,
    document: Document,
) -> Iterable[Tuple[str, List[float], dict]]:
    print(f'Getting embeddings with {model} for {document} with {len(document.lines)} lines {len(document.contents)} total chars...')
    embeddings = model.encode(document.lines, show_progress_bar=True)
    # {'document': document.hash, 'line': line_number} # now storing this in separate DB
    # vectors are initially set to inactive {'active': False}
    with_metadata = [
        (hash_sha256(line), vector.tolist(), {})
        for (line, vector) 
        in zip(document.lines, embeddings)
    ]
    print(f'Got {len(with_metadata)} embeddings with metadata')
    return with_metadata
