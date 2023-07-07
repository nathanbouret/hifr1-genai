
do_zero_shot_classification = False

def gcp_config():
    GCP_CONFIG = {
        'PROJECT_NAME' : 'gen-hi-france-genai-force1',
        'PROJECT_ID' : 'gen-hi-france-genai-force1',
        'PROJECT_NUMBER' : '881178893280',
        'REGION' : 'us-central1',
        'BUCKET' : 'gs://corpus-fr1-hack',
        'BUCKET_NAME': 'corpus-fr1-hack',
        'DIMENSIONS' : 768
    }
    return GCP_CONFIG


def embedding_config():
    EMBEDDING_CONFIG = {
        'TEXT_EMBEDDING_MODEL_NAME' : "textembedding-gecko@001",
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
            'temperature' : 0.2,
            'top_p' : 0.95,
            'top_k' : 40
    }
    return CHATLLM_CONFIG


def document_processor_config():
    DOCUMENT_PROCESSOR_CONFIG = {
        'PROCCESOR_LOCATION' : 'us', # An `api_endpoint` must be set if you use a location other than "us".
        'BUCKET_OUTPUT_URI' : 'gs://corpus-fr1-hack/document_obj/',   # Must end with a trailing slash `/`. Format: gs://bucket/directory/subdirectory/
        'BUCKET_INPUT_PREFIX': 'gs://corpus-fr1-hack/pdf/',   # Format: gs://bucket/directory/
        'PROCESSOR_DISPLAY_NAME' : "PDF_TO_TXT_PROCESSOR",  # Must be unique per project, e.g.: "My Processor"
        'PROCESSOR_TYPE': "OCR_PROCESSOR",
        'BUCKET_TXT_NAME': 'txt'
    }
    return DOCUMENT_PROCESSOR_CONFIG

