
# Utils
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

# custom methods
from context_generator.src.vectorizer import doc_to_vector
from context_generator.src.vectorizer import get_vectorstore_retriever
from context_generator.src.sampler import get_relevant_documents
from utils.utils import get_source_file
from context_generator.src.vectorizer import load_vector_store_local
from corpus_processor.src.file_processor import document_processor
from corpus_processor.src.corpus_to_text import read_documents_from_bucket


def generate_context(user_question, embeddings, vector_store_flag=False):

    # document_processor() #DONT RUN THIS FUNCTION / create and run a processor to convert .pdf files to .json files (Document obj) from google bucket data directory
    read_documents_from_bucket()

    vector_store = None
    if not vector_store_flag:
        vector_store = doc_to_vector(embeddings, vector_store_method='FAISS')
    else:
        vector_store = load_vector_store_local('vector_store_index', embeddings)

    # vector_store = doc_to_vector(embeddings, doc_type='txt', vector_store_name='FAISS')
    retriever = get_vectorstore_retriever(vector_store)

    # find top k similar chuncks of the documents to user input query
    top_k = 4
    docs_top_k = get_relevant_documents(retriever, top_k, user_question)

    for idx, doc in enumerate(docs_top_k[:top_k]):
        print(f"========== K:{idx} ==========")
        print(f"========== {get_source_file(doc.metadata['source'])} ==========")
        print(f"{doc.page_content}")
        print(f"=========================================================================")
    # prepare a prompt where top k similar chuncks is a context for the LLM
    context = "\n".join([doc.page_content for doc in docs_top_k])

    return context