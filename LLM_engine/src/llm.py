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
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)

# Vertex AI
import vertexai
from vertexai.preview.language_models import TextGenerationModel
from vertexai.preview.language_models import ChatModel

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

def call_llm_answer_Q(GCP_CONFIG, LLM_CONFIG, main_prompt):

    PROJECT_ID = GCP_CONFIG.get('PROJECT_ID')
    REGION = GCP_CONFIG.get('REGION')
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

    answer = llm(main_prompt.format())
    # print(f"LLM Output: {answer}")
    return answer

def call_llm_refine_question(GCP_CONFIG, LLM_CONFIG, conversation, user_question):
    """
    Method uses llm model to correct and enhance the user question formulation 
    It takes into consideration the conversation history 
    """
    PROJECT_ID = GCP_CONFIG.get('PROJECT_ID')
    REGION = GCP_CONFIG.get('REGION')
    vertexai.init(project=PROJECT_ID, location=REGION)

    llm_model_to_refine_question = TextGenerationModel.from_pretrained("text-bison@001")
    
    answer = llm_model_to_refine_question.predict(
    max_output_tokens = LLM_CONFIG['max_output_token'],
    temperature = LLM_CONFIG['temperature'],
    top_p = LLM_CONFIG['top_p'],
    top_k = LLM_CONFIG['top_k'],
    prompt=f"Given the following user query and conversation log, formulate a question that would be the most relevant to provide the user with an answer from a knowledge base.\n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {user_question}\n\nRefined Query:",
    )
    return answer.text

def call_llm_chat(GCP_CONFIG, CHATLLM_CONFIG, user_question, context, message_history):

    PROJECT_ID = GCP_CONFIG.get('PROJECT_ID')
    REGION = GCP_CONFIG.get('REGION')
    vertexai.init(project=PROJECT_ID, location=REGION)

    # Chat model initialization
    chat_model = ChatModel.from_pretrained(model_name=CHATLLM_CONFIG.get('chatllm_name'))

    parameters = {
        "temperature": CHATLLM_CONFIG['temperature'],
        "max_output_tokens": CHATLLM_CONFIG['max_output_token'],
        "top_p": CHATLLM_CONFIG['top_p'],
        "top_k":  CHATLLM_CONFIG['top_k']
    }

    # fixed_template=f"""Answer the question as truthfully as possible using the provided [CONTEXT], 
    # and if the answer is not contained within the  [CONTEXT], say 'I don't know.'  [CONTEXT]={context}"""
    # chat = chat_model.start_chat(context=context, message_history=message_history)
    # chat = chat_model.start_chat(context=fixed_template)
    # chat = chat_model.start_chat(context = f"Consider this as [CONTEXT] = {context}")

    chat = chat_model.start_chat(context = f"Read this: {context}")
    chat.send_message("What is your opinion about the context? What else do you know?", **parameters)
    # Attention_please 
    # chat.send_message("what is the first word in [CONTEXT]? and the last word [CONTEXT]?", **parameters)

    answer = chat.send_message(user_question, **parameters)

    return answer
