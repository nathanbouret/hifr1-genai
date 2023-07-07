
## put here contexte sampling strategy ###


def get_relevant_documents(retriever, query_text):
    docs = retriever.get_relevant_documents(query_text)
    # print("\n\n".join([x.page_content[:1000] for x in docs[:top_k]]))
    return docs