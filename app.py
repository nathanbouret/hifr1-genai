import streamlit as st
from GenaiHachathonHI import run, chain_QA


LLM_CONFIG = config.llm_config()
CHATLLM_CONFIG = config.chat_llm_config()
EMBEDDING_CONFIG = config.embedding_config()


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
        answer = run(selected_role, selected_question)
        st.write(answer)


def chat_behavior():
    selected_role = st.selectbox(label='Your rule', options=roles)
    user_text_question = st.text_input(label='Enter some text')
    if user_text_question:
        # answer = run(selected_role, user_text_question)
        llm_response = chain_QA(selected_role, user_text_question)
        st.write(llm_response['result'])
        for source in llm_response["source_documents"]:
            st.write(source.metadata['source'])


if __name__ == "__main__":
    st.write("# GenAI Hachathon 2023 - HI team!")
    option = st.radio("Select a mode for interaction with HI application:", ('LLM QA', 'Chat'))

    if  option == "LLM QA":
        question_answering_behavior()
    elif option == "Chat":
        chat_behavior()





