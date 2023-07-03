
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
from vectorizer import doc_to_vector
from vectorizer import get_vectorstore_retriever
from sampler import get_relevant_documents


def generate_context(user_question, embeddings):

    vector_store = doc_to_vector(embeddings, doc_type='txt', vector_store_name='FAISS')
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