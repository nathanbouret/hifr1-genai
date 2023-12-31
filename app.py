import streamlit as st
from streamlit_chat import message
import vertexai
from vertexai.preview.language_models import TextGenerationModel
from vertexai.preview.language_models import ChatModel

from langchain.chat_models import ChatVertexAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)

from config import config
from LLM_engine.src.llm import CustomVertexAIEmbeddings
from LLM_engine.src.llm import call_llm_answer_Q, call_llm_refine_question, call_llm_chat
from context_generator.src.context_generator import generate_context
from main_prompt_creator.src.main_prompt_creator import create_prompt_1

# VECTOR_STORE_FLAG = True
VECTOR_STORE_FLAG = config.vector_store_flag

EMBEDDING_CONFIG = config.embedding_config()
requests_per_minute = EMBEDDING_CONFIG.get("EMBEDDING_QPM")
num_instances_per_batch = EMBEDDING_CONFIG.get("EMBEDDING_NUM_BATCH")

# print(requests_per_minute)

# embedding model initialization
embeddings = CustomVertexAIEmbeddings(
    requests_per_minute=requests_per_minute,
    num_instances_per_batch=num_instances_per_batch
)
# 'what was the main goal behind investing in cloud technology?'
# how can pharmaceutical companies drive value growth?

roles = ['business analyst', 'CxO', 'legal dep']
questions_BA = ['which companies are leaders in the life science industry recently?',
                'how much are the incomes of Merck company in 2022?'
                ]
questions_CxO = ['how can pharmaceutical companies drive value growth?',
                'where healthcare companies have invested more recently?',
                'where pharmaceuticals companies invest?',
                'what have been the most challenges for healthcare companies since 2020?',
                'what are the key industrial capabilities of pharmaceutical companies?',
                ]
question_legalDP = ['what is ....']

topics = ['Innovation','Business','Insights','Challenges']

def get_conversation_string():
    conversation_string = ""
    for i in range(len(st.session_state['responses'])-1):
        
        conversation_string += "Human: "+st.session_state['requests'][i] + "\n"
        conversation_string += "Bot: "+ st.session_state['responses'][i+1] + "\n"
        print('conversation_string: ', conversation_string)
    return conversation_string


def run_llm_QA_pipeline(selected_role, user_text_question, vector_store_flag):

    # get configuration infos
    GCP_CONFIG = config.gcp_config()
    LLM_CONFIG = config.llm_config()
    # EMBEDDING_CONFIG = config.embedding_config()

    PROJECT_ID = GCP_CONFIG.get('PROJECT_ID')
    REGION = GCP_CONFIG.get('REGION')
    vertexai.init(project=PROJECT_ID, location=REGION)

    # generate context
    context = generate_context(user_question=user_text_question, embeddings=embeddings, vector_store_flag=vector_store_flag)

    # create main prompt
    main_prompt = create_prompt_1(user_question=user_text_question, user_role=selected_role, context=context)

    # call llm to answer
    answer = call_llm_answer_Q(
        GCP_CONFIG=GCP_CONFIG, 
        LLM_CONFIG=LLM_CONFIG, 
        main_prompt=main_prompt)
    # answer = answer.text

    return answer

def run_llm_chat_pipeline(selected_topic, refined_user_question, message_history, vector_store_flag):
    
    # get configuration infos
    GCP_CONFIG = config.gcp_config()
    CHATLLM_CONFIG = config.chat_llm_config()
    # EMBEDDING_CONFIG = config.embedding_config()

    PROJECT_ID = GCP_CONFIG.get('PROJECT_ID')
    REGION = GCP_CONFIG.get('REGION')
    vertexai.init(project=PROJECT_ID, location=REGION)

    weight = int(len(refined_user_question.split(" "))/2)

    context_prompt = refined_user_question + weight*(f" {selected_topic}")

    # generate context
    context = generate_context(user_question = context_prompt, embeddings=embeddings, vector_store_flag=vector_store_flag)
    
    # call llm chat to answer
    answer = call_llm_chat(
        CHATLLM_CONFIG=CHATLLM_CONFIG, 
        GCP_CONFIG=GCP_CONFIG, 
        user_question=refined_user_question, 
        context=context, 
        message_history=message_history)

    return answer


def question_answering_behavior(): 
    selected_role = st.selectbox(label='Your role', options=roles)

    if selected_role and selected_role=='business analyst':
        selected_question = st.selectbox(label='Question', options=questions_BA)
    elif selected_role and selected_role=='CxO':
        selected_question = st.selectbox(label='Question', options=questions_CxO)
    elif selected_role and selected_role=='legal dep':
        selected_question = st.selectbox(label='Question', options=question_legalDP)

    submitted_question = st.button(key='question_submit_buttom', label='Submit')
    if submitted_question:
        # answer = run(selected_role, selected_question)
        answer = run_llm_QA_pipeline(selected_role, selected_question, vector_store_flag=VECTOR_STORE_FLAG)
        st.write(answer)


# def chat_behavior():
#     selected_role = st.selectbox(label='Your rule', options=roles)
#     user_text_question = st.text_input(label='Enter some text')
    
#     if user_text_question:
#         answer = run_llm_pipeline(selected_role, user_text_question)
#         print(answer)

#         # st.write(answer['result'])
#         st.write(answer)
#         # for source in answer["source_documents"]:
#         #     st.write(source.metadata['source'])

def on_topic_selector_changed():
    selected_option = st.session_state['topic_selector']
    print("========> ",selected_option)
    del st.session_state['requests']
    del st.session_state['responses']
    st.session_state['input'] = ''
    st.session_state['query_text'] = ''

def user_experience_changed():
    selected_option = st.session_state['user_experience_option']
    print("========> ",selected_option)
    st.session_state['query_text'] = ''
    if selected_option == 'Chat':
        print("Chat...........")
    else:
        del st.session_state['requests']
        del st.session_state['responses']
        st.session_state['input'] = ''

def submit():
    st.session_state['query_text'] = st.session_state['input']
    st.session_state['input'] = ''

def chat_behavior():
    # get configuration infos
    GCP_CONFIG = config.gcp_config()
    LLM_CONFIG = config.llm_config()
    CHATLLM_CONFIG = config.chat_llm_config()

    selected_topic = st.selectbox(label='Main topic', options=topics, key='topic_selector', on_change=on_topic_selector_changed)

    st.subheader("Looking for more insights? Ask ChatCEO...")
    if 'responses' not in st.session_state:
        st.session_state['responses'] = ["How can I assist you?"]
    if 'requests' not in st.session_state:
        st.session_state['requests'] = []

    if 'buffer_memory' not in st.session_state:
        st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)
        print('================= st.session_state.buffer_memory ================\n',  st.session_state.buffer_memory)
    
    if 'query_text' not in st.session_state:
        st.session_state['query_text'] = ''

    # system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer the question as truthfully as possible using the provided context, 
    # and if the answer is not contained within the text below, say 'I don't know'""")

    # topic_msg_template = SystemMessagePromptTemplate.from_template(template= selected_topic)

    human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

    prompt_template = ChatPromptTemplate.from_messages(
        [
        #system_msg_template, 
        MessagesPlaceholder(variable_name="history"), 
        human_msg_template])
    
    print('prompt_template: ', prompt_template)

    # container for chat history
    response_container = st.container()
    # container for text box
    textcontainer = st.container()

    with textcontainer:
        st.text_input("Query: ", key="input", on_change=submit)
        user_question = st.session_state['query_text'] 
        if user_question:
            with st.spinner("typing..."):
                # conversation history
                conversation_string = get_conversation_string()

                # call LLM to refine and enhance the question
                refined_user_question = call_llm_refine_question(
                    GCP_CONFIG=GCP_CONFIG, 
                    LLM_CONFIG=LLM_CONFIG,
                    conversation=conversation_string, 
                    user_question=user_question)

                # st.subheader("Refined Query:")
                # st.write(refined_user_question)

                # get messages history
                message_history = st.session_state.requests + st.session_state.responses
                # print('message_history: ', message_history)

                # prompt = f"Answer: {user_question}. If you do not understand answer this instead: {refined_user_question}"

                # call llm_chat pipeline to answer
                response = run_llm_chat_pipeline(
                    selected_topic = selected_topic, 
                    refined_user_question = user_question, # refined_user_question, 
                    message_history = message_history,
                    vector_store_flag = VECTOR_STORE_FLAG
                )

                print(f"Response from Model: {response.text}")

            st.session_state.requests.append(user_question)
            st.session_state.responses.append(response.text) 

            print('st.session_state.requests: ', st.session_state.requests)
            print('st.session_state.responses: ', st.session_state.responses)
    with response_container:
        if st.session_state['responses']:
            for i in range(len(st.session_state['responses'])):
                print('*********************')
                print('2: ', st.session_state['responses'])
                message(st.session_state['responses'][i], key=str(i))
                if i < len(st.session_state['requests']):
                    message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')
    st.session_state['query_text'] = ''

if __name__ == "__main__":
    st.write("# ChatCEO")
    option = st.radio("Choose user experience:", ("Chat", 'LLM QA'), key='user_experience_option', on_change=user_experience_changed)

    if  option == "LLM QA":
        question_answering_behavior()
    elif option == "Chat":
        chat_behavior()
