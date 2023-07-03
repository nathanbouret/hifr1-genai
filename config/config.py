

def gcp_config():
    GCP_CONFIG = {
        'PROJECT_NAME' : 'gen-hi-france-genai-force1',
        'PROJECT_ID' : 'gen-hi-france-genai-force1',
        'PROJECT_NUMBER' : '881178893280',
        'REGION' : 'us-central1',
        'BUCKET' : 'gs://marzi-bucket',
        'DIMENSIONS' : 768
    }
    return GCP_CONFIG

def embedding_config():
    EMBEDDING_CONFIG = {
        'EMBEDDING_QPM' : 100,
        'EMBEDDING_NUM_BATCH' : 5
    }
    return EMBEDDING_CONFIG

def llm_config():
    LLM_CONFIG = {
            'llm_name': 'text-bison@001',
            'max_output_token' : 1024,
            'temperature' : 0.1,
            'top_p' : 0.8,
            'top_k' : 40
    }
    return LLM_CONFIG

def chat_llm_config():
    CHATLLM_CONFIG = {
            'chatllm_name': 'chat-bison@001',
            'max_output_token' : 1024,
            'temperature' : 0,
            'top_p' : 0.95,
            'top_k' : 40
    }
    return CHATLLM_CONFIG

def llm_embedding_config():
    LLM_EMBEDDING_CONFIG = {
            'text_embedding_name' : "textembedding-gecko@001"
    }
    return LLM_EMBEDDING_CONFIG
