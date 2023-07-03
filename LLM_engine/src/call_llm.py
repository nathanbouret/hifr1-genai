 Utils
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