import os
import time
from typing import List

# Langchain
from pydantic import BaseModel
from langchain import PromptTemplate
from langchain.vectorstores import FAISS
from langchain.vectorstores import Chroma

from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

# Vertex AI
import vertexai
from langchain.chat_models import ChatVertexAI
from langchain.embeddings import VertexAIEmbeddings
from langchain.llms import VertexAI

from utils.utils import rate_limit
import config

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

def call_llm(GCP_CONFIG, LLM_CONFIG, CHATLLM_CONFIG, main_prompt):

    PROJECT_ID = GCP_CONFIG.get('PROJECT_ID')
    REGION = GCP_CONFIG.get('REGION')
    aiplatform.init(project=PROJECT_ID, location=REGION)
    vertexai.init(project=PROJECT_ID, location=REGION)

    # LLM model initialization
    llm = VertexAI(
        model_name = LLM_CONFIG['llm_name'],
        max_output_tokens = LLM_CONFIG['max_output_token'],
        temperature = LLM_CONFIG['temperature'],
        top_p = LLM_CONFIG['top_p'],
        top_k = LLM_CONFIG['top_k'],
        verbose = True,
    )

    # Chat model initialization
    chat = ChatVertexAI(
        model_name = CHATLLM_CONFIG['chatllm_name'],
        max_output_tokens = CHATLLM_CONFIG['max_output_token'],
        temperature = CHATLLM_CONFIG['temperature'],
        top_p = CHATLLM_CONFIG['top_p'],
        top_k = CHATLLM_CONFIG['top_k'],
        verbose=True,
    )

    # embedding model initialization
    embeddings = CustomVertexAIEmbeddings(
        requests_per_minute=EMBEDDING_CONFIG.get('EMBEDDING_QPM'),
        num_instances_per_batch=EMBEDDING_CONFIG.get('EMBEDDING_NUM_BATCH'),
        )

    answer = llm(prompt.format())
    print(f"LLM Output: {answer}")
    return answer
