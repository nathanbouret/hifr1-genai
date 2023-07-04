
import sys
# sys.path.insert(1, "../../")

from corpus_processor.src.corpus_to_text import read_documents
from context_generator.src.split_docs import split_docus_to_chuncks
from context_generator.src.extract_embeddings import extract_embeddings_from_documents 

DATA_DIR = r'C:/Users/hbayahme/.vscode/projects/hifr1-genai/corpus_processor/data'

def doc_to_vector(embeddings, doc_type, vector_store_name='FAISS'):
    # 1. reading all documents (.txt or .pdf) 
    # 2. spliting documents to chincks of texts
    # 3. extracting the embeddings of splited documents using a LLM model
    # 4. store vector representation of chuncks in a vector store

    docs = read_documents(data_dir=DATA_DIR, type=doc_type)
    texts = split_docus_to_chuncks(docs)
    vector_store = extract_embeddings_from_documents(texts, embeddings, vector_store_name)   # TODO try Chroma or Vertex AI Matching Engine instead of FAISS
    return vector_store

def get_vectorstore_retriever(vector_store):
    # Init your retriever. Asking for just 1 document back
    retriever = vector_store.as_retriever()
    return retriever