import streamlit as st
import vertexai

from config import config

from LLM_engine.src.llm import CustomVertexAIEmbeddings
from LLM_engine.src.llm import call_llm
from context_generator.src.context_generator import generate_context
from main_prompt_creator.src.main_prompt_creator import create_prompt_1

# 'what was the main goal behind investing in cloud technology?'
# how can pharmaceutical companies drive value growth?

roles = ['business analyst', 'CxO', 'legal dep']
questions_BA = ['who is the leading life science company recently?',
                'how much are the incomes of companies in life science companies?'
                ]
questions_CxO = ['what is key industrial capabilities of the companies?',
                 'how can pharmaceutical companies drive value growth?',
                'where healthcare companies have been invested recently?',
                'where pharmaceuticals companies have been invested recently?',
                'what has been the challenges for healthcare companies since 2020?']
question_legalDP = ['what is ....']

def run_llm_pipeline(selected_role, user_text_question):

    # get configuration infos
    GCP_CONFIG = config.gcp_config()
    LLM_CONFIG = config.llm_config()
    CHATLLM_CONFIG = config.chat_llm_config()
    EMBEDDING_CONFIG = config.embedding_config()

    PROJECT_ID = GCP_CONFIG.get('PROJECT_ID')
    REGION = GCP_CONFIG.get('REGION')
    vertexai.init(project=PROJECT_ID, location=REGION)

    requests_per_minute = EMBEDDING_CONFIG.get("EMBEDDING_QPM")
    num_instances_per_batch = EMBEDDING_CONFIG.get("EMBEDDING_NUM_BATCH")

    print(requests_per_minute)

    # embedding model initialization
    embeddings = CustomVertexAIEmbeddings(
        requests_per_minute=requests_per_minute,
        num_instances_per_batch=num_instances_per_batch
    )

    # generate context
    context = generate_context(user_question=user_text_question, embeddings=embeddings)

    # create main prompt
    main_prompt = create_prompt_1(user_question=user_text_question, user_role=selected_role, context=context)

    # call llm to answer
    answer = call_llm(GCP_CONFIG, LLM_CONFIG, CHATLLM_CONFIG, main_prompt)
    # answer = answer.text

    return answer


# def question_answering_behavior(): 
#     selected_role = st.selectbox(label='Your role', options=roles)

#     if selected_role and selected_role=='business analyst':
#         selected_question = st.selectbox(label='Question', options=questions_BA)
#     elif selected_role and selected_role=='CxO':
#         selected_question = st.selectbox(label='Question', options=questions_CxO)
#     elif selected_role and selected_role=='legal dep':
#         selected_question = st.selectbox(label='Question', options=question_legalDP)

#     submitted_question = st.button(key='question_submit_buttom', label='Submit')
#     if submitted_question:
#         answer = run(selected_role, selected_question)
#         st.write(answer)


def chat_behavior():
    selected_role = st.selectbox(label='Your rule', options=roles)
    user_text_question = st.text_input(label='Enter some text')
    
    if user_text_question:
        answer = run_llm_pipeline(selected_role, user_text_question)
        print(answer)

        # st.write(answer['result'])
        st.write(answer)
        # for source in answer["source_documents"]:
        #     st.write(source.metadata['source'])


if __name__ == "__main__":
    st.write("# GenAI Hachathon 2023 - HI team!!")
    option = st.radio("Select a mode for interaction with HI application:", ('LLM QA', 'Chat'))

    if  option == "LLM QA":
        # question_answering_behavior()
        pass
    elif option == "Chat":
        chat_behavior()





