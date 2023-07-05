import time
from typing import List

from langchain.vectorstores import FAISS
from langchain.vectorstores import Chroma
from langchain.embeddings import VertexAIEmbeddings
from pydantic import BaseModel


class CustomVertexAIEmbeddings(VertexAIEmbeddings, BaseModel):
    requests_per_minute: int
    num_instances_per_batch: int

    # Overriding embed_documents method
    def embed_documents(self, texts: List[str]):
        limiter = rate_limit(self.requests_per_minute)
        results = []
        docs = list(texts)

        while docs:
            # Working in batches because the API accepts maximum 5
            # documents per request to get embeddings
            head, docs = (
                docs[: self.num_instances_per_batch],
                docs[self.num_instances_per_batch :],
            )
            chunk = self.client.get_embeddings(head)
            results.extend(chunk)
            next(limiter)

        return [r.values for r in results]


# Utility functions for Embeddings API with rate limiting
def rate_limit(max_per_minute):
    period = 60 / max_per_minute
    print("Waiting")
    while True:
        before = time.time()
        yield
        after = time.time()
        elapsed = after - before
        sleep_time = max(0, period - elapsed)
        if sleep_time > 0:
            print(".", end="")
            time.sleep(sleep_time)


def extract_embeddings_from_documents(documents, embedding_model, vector_store_method='FAISS'):
    print(vector_store_method)
    # Store docs in local vectorstore as index
    if vector_store_method == 'FAISS':
        vector_store = FAISS.from_documents(documents, embedding_model)
    elif vector_store_method == 'chroma':
        vector_store = Chroma.from_documents(documents, embedding_model)
    return vector_store

