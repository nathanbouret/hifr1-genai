import vertexai
from vertexai.preview.language_models import ChatModel, InputOutputTextPair

vertexai.init(project="gen-hi-france-genai-force1", location="us-central1")
chat_model = ChatModel.from_pretrained("chat-bison@001")
parameters = {
    "temperature": 0.2,
    "max_output_tokens": 256,
    "top_p": 0.8,
    "top_k": 40
}

context = ""

attention_prompt = """what is the first word? and the last word?"""

prompt = """what are the main ideas of the paragraph?"""

chat = chat_model.start_chat(context)

# first prompt to force the model to pay attention to the context
response = chat.send_message(attention_prompt, **parameters)
# print(f"Response from Model: {response.text}")

# response based on context
response = chat.send_message(prompt, **parameters)
print(f"Response from Model: {response.text}")