
from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_docus_to_chuncks(documents):

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    print(f"# of chuncks from all the documents = {len(docs)}")

    return docs