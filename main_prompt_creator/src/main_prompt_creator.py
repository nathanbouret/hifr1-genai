
from langchain import PromptTemplate

def create_prompt_1(user_question, user_role, context):

    template = f""" Follow exactly those 5 steps:
        1. Read the context below and aggregrate this data
        Context : {context}
        2. Answer the Question using only this context.
        3. consider the role of user who asked the question as {user_role}.
        4. Show the source for your answers
        5. Show the values of investment and location if they are mentioned in the context.
        Question: {user_question}
        If you don't have any context and are unsure of the answer, reply that you don't know about this topic. """
    
    prompt = PromptTemplate(
        input_variables=[],
        template=template,
    )

    return prompt

# debugging test  
if __name__=="__main__":
    p = create_prompt_1("user_question", "user_role", "context")
    print(p.format())