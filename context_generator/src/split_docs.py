
from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_docus_to_chuncks(documents):

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)
    print(f"# of chuncks from all the documents = {len(docs)}")

    return docs


# def split_docus_to_chuncks_paragraph_wise(documents):
#     paragraphs = []
#     len_prv_chunk = 0
#     for i in range(len(documents)):
        
#         text = documents[i].page_content
#         if len(text) < 100:


#     # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#     # docs = text_splitter.split_documents(documents)
#     # print(f"# of chuncks from all the documents = {len(docs)}")

#     return True