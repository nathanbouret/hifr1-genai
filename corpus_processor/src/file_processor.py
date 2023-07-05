# from utils import *
from corpus_processor.src.batch_processor import *
from config import config
from corpus_processor.src.utils import *


def document_processor():
    # Project information
    GCP_CONFIG = config.gcp_config()
    project_id = GCP_CONFIG['PROJECT_ID']

    # Processor information
    DOCUMENT_PROCESSOR_CONFIG = config.document_processor_config() 
    processor_location =  DOCUMENT_PROCESSOR_CONFIG['PROCCESOR_LOCATION']
    gcs_input_prefix = DOCUMENT_PROCESSOR_CONFIG['BUCKET_INPUT_PREFIX']
    gcs_output_uri = DOCUMENT_PROCESSOR_CONFIG['BUCKET_OUTPUT_URI']  # Must end with a trailing slash `/`. Format: gs://bucket/directory/subdirectory/
    processor_display_name = DOCUMENT_PROCESSOR_CONFIG['PROCESSOR_DISPLAY_NAME']
    processor_type = DOCUMENT_PROCESSOR_CONFIG['PROCESSOR_TYPE']  # Use fetch_processor_types(project_id, location) to get available processor types
 
    # mime_type = "application/pdf"  # Use "text/plain" for txt. Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
    # field_mask = "text,entities,pages.pageNumber"  # Optional. The fields to return in the Document object.
 
    new_processor = create_processor(project_id = project_id, location = processor_location, processor_display_name = processor_display_name, processor_type = processor_type)
    print(new_processor)
    processor_id = new_processor.split('/')[-1]

    batch_process_documents(project_id = project_id,
                            location = processor_location,
                            processor_id = processor_id,
                            gcs_output_uri = gcs_output_uri,
                            gcs_input_prefix = gcs_input_prefix,
                            timeout=1500
                            )

    delete_processor(project_id = project_id, 
                    location = processor_location, 
                    processor_id = processor_id
                    )


