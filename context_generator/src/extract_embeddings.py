from langchain.vectorstores import FAISS
from langchain.vectorstores import Chroma



def extract_embeddings_from_documents(documents, embedding_model, vector_store_name):
    print(vector_store_name)
    # Store docs in local vectorstore as index
    if vector_store_name == 'FAISS':
        vector_store = FAISS.from_documents(documents, embedding_model)
    elif vector_store_name == 'chroma':
        vector_store = Chroma.from_documents(documents, embeddings)
    return vector_store