from typing import Iterable, List, Tuple
from utils import hash_sha256
from functools import cache, cached_property
from sentence_transformers import SentenceTransformer
from utils import timing
from models import Document, PassageEmbedding
from transformers import AutoTokenizer, AutoModel
import torch


@timing
def load_tokenizer_hebbia():
    return AutoTokenizer.from_pretrained("sentence-transformers/msmarco-MiniLM-L-6-v3")


@timing
def load_automodel_hebbia():
    return AutoModel.from_pretrained("sentence-transformers/msmarco-MiniLM-L-6-v3")


@timing
def load_model_hebbia():
    """384-dimensional embeddings"""
    return SentenceTransformer("sentence-transformers/msmarco-MiniLM-L-6-v3")


# @timing
# def get_embeddings_with_metadata(
#     model: SentenceTransformer,
#     document: Document,
# ) -> Iterable[Tuple[str, List[float], dict]]:
#     print(f'Getting embeddings with {model} for {document} with {len(document.lines)} lines {len(document.contents)} total chars...')
#     embeddings = model.encode(document.lines, show_progress_bar=True)
#     # {'document': document.hash, 'line': line_number} # now storing this in separate DB
#     # vectors are initially set to inactive {'active': False}
#     with_metadata = [
#         (hash_sha256(line), vector.tolist(), {})
#         for (line, vector)
#         in zip(document.lines, embeddings)
#     ]
#     print(f'Got {len(with_metadata)} embeddings with metadata')
#     return with_metadata


# ==========================================================================================
# Need fancy handling for tokenizer with stride
# https://huggingface.co/sentence-transformers/msmarco-MiniLM-L-6-v3


# def simple_tokenize_str(text: str, tokenizer: AutoTokenizer) -> List[str]:
#     result = tokenizer(text)
#     print(result)
#     token_ids = result["input_ids"]
#     print(token_ids)
#     decoded = [tokenizer.decode(x) for x in token_ids]
#     print(decoded)
#     return decoded


# @timing
def tokenize_with_stride(s: str, tokenizer: AutoTokenizer) -> dict:
    """
    means max overlap of Stride between segments
    https://huggingface.co/sentence-transformers/msmarco-MiniLM-L-6-v3

    https://colab.research.google.com/github/huggingface/notebooks/blob/master/examples/question_answering.ipynb#scrollTo=V2Fk7XXb5Ix1
    """
    # if you don't return tensors, will get error later when passing to model
    result = tokenizer(
        s,
        max_length=100,
        padding=True,
        truncation=True,
        stride=50,
        return_overflowing_tokens=True,
        return_tensors="pt",
    )
    # print(f'Got {len(result["input_ids"])} passages with lengths: {[len(x) for x in result["input_ids"]]}')
    # for x in result["input_ids"]: print(t.decode(x))

    # if you don't do this forward pass will throw error on unexpected kwarg
    del result["overflow_to_sample_mapping"]
    return result


# Mean Pooling - Take attention mask into account for correct averaging
# @timing
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[
        0
    ]  # First element of model_output contains all token embeddings
    input_mask_expanded = (
        attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    )
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
        input_mask_expanded.sum(1), min=1e-9
    )


# @timing
def encode_document_with_stride(
    document: Document,
    model: AutoModel,
    tokenizer: AutoTokenizer,
) -> List[PassageEmbedding]:  # Id, embedding, metadata, raw text
    """
    https://huggingface.co/sentence-transformers/msmarco-MiniLM-L-6-v3
    """
    # print(f'encode_document_with_stride: {document.hash_contents}:"{document.name}" with {len(document.contents)} chars')
    encoded_input: dict = tokenize_with_stride(document.contents, tokenizer)
    # print('Encoding tokenized input...')
    with torch.no_grad():
        model_output = model(**encoded_input)
    sentence_embeddings = mean_pooling(model_output, encoded_input["attention_mask"])
    result = sentence_embeddings.tolist()
    # print(f'Got {len(result)} result embeddings! Rolling out with metadata...')

    # unzip and flatten
    with_metadata = []
    for i, (embedding, token_ids) in enumerate(zip(result, encoded_input["input_ids"])):
        decoded_str = tokenizer.decode(token_ids, skip_special_tokens=True)
        # print(f'{i}: {decoded_str}')
        passage_id = document.hash_contents + "|" + str(i)
        passage = PassageEmbedding(
            id=passage_id,
            embedding=embedding,
            metadata={},
            text=decoded_str,
            document_id=document.hash_contents,
        )
        with_metadata.append(passage)

    return with_metadata
