
from langchain import PromptTemplate

def create_prompt_1(user_question, user_role, context):

    template = f""" Follow exactly those 6 steps:
        1. Read the context below and aggregrate this data
        2. Answer the Question below using only the Context and considering the role of user as "{user_role}".
        4. Show results in bullet points.
        4. Show the source for your answers.
        5. Show the values of investment and location if they are mentioned in the context.
        6. If you don't have any context and are unsure of the answer, reply that you don't know about this topic.
        Question: {user_question} 
        Context : {context}
        """
    
    prompt = PromptTemplate(
        input_variables=[],
        template=template,
    )

    return prompt

# debugging test  
if __name__=="__main__":
    p = create_prompt_1("user_question", "user_role", "context")
    print(p.format())