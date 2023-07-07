

# sys.path.insert(1, "../../")
from langchain.vectorstores import FAISS
from corpus_processor.src.corpus_to_text import read_txt_files_from_bucket
from context_generator.src.split_docs import split_docus_to_chuncks
from context_generator.src.extract_embeddings import extract_embeddings_from_documents 
# from context_generator.src.zero_shot_classifier import zero_shot_classification
from context_generator.src.extract_embeddings import CustomVertexAIEmbeddings

from config import config
import streamlit as st

# Embedding
EMBEDDING_CONFIG = config.embedding_config()
EMBEDDING_QPM = EMBEDDING_CONFIG['EMBEDDING_QPM']
EMBEDDING_NUM_BATCH = EMBEDDING_CONFIG['EMBEDDING_NUM_BATCH']
EMBEDDING_MODEL_NAME = EMBEDDING_CONFIG['TEXT_EMBEDDING_MODEL_NAME']
# embedding model initialization
embeddings = CustomVertexAIEmbeddings(
    model_name=EMBEDDING_MODEL_NAME,
    requests_per_minute=EMBEDDING_QPM,
    num_instances_per_batch=EMBEDDING_NUM_BATCH,
    )


def doc_to_vector(embeddings, vector_store_method='FAISS'):
    # 1. reading all documents (.txt) from google bucket
    # 2. spliting documents to chincks of texts
    # 3. extracting the embeddings of splited documents using a LLM model
    # 4. store vector representation of chuncks in a vector store

    docs = read_txt_files_from_bucket()
    texts = split_docus_to_chuncks(docs)
    print(f'number of txt files: {len(docs)} and number of chunks: {len(texts)}')
    # if config.do_zero_shot_classification:
    #     topics = ["challenge", "innovation", "investment", "achievement"]
    #     result = zero_shot_classification(texts, topics, 0.8)
    
    vector_store = extract_embeddings_from_documents(texts, embeddings, vector_store_method)   # TODO try Chroma or Vertex AI Matching Engine instead of FAISS
    save_vector_store_local(vector_store, 'vector_store_index')
    return vector_store


def save_vector_store_local(vector_store, vector_store_path):
    vector_store.save_local(vector_store_path)



def load_vector_store_local(vector_store_path, embedding_model):
    vector_store = FAISS.load_local(vector_store_path, embedding_model)
    return vector_store


def get_vectorstore_retriever(vector_store, top_k):
    # Init your retriever. Asking for just 1 document back
    retriever = vector_store.as_retriever(search_kwargs={"k": top_k})
    return retriever