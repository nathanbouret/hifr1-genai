
from typing import Optional

from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import InternalServerError
from google.api_core.exceptions import RetryError
from google.cloud import documentai 

# from google.cloud.documentai_toolbox import gcs_utilities #for batches larger than 1000

def batch_process_documents(
    project_id: str,
    location: str,
    processor_id: str,
    gcs_output_uri: str,
    gcs_input_prefix: str = None,
    field_mask: Optional[str] = None,
    timeout: int = 400,
) -> None:
    # You must set the `api_endpoint` if you use a location other than "us".
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # Specify a GCS URI Prefix to process an entire directory
    gcs_prefix = documentai.GcsPrefix(gcs_uri_prefix=gcs_input_prefix)
    input_config = documentai.BatchDocumentsInputConfig(gcs_prefix=gcs_prefix)

    # Cloud Storage URI for the Output Directory
    gcs_output_config = documentai.DocumentOutputConfig.GcsOutputConfig(
        gcs_uri=gcs_output_uri, field_mask=field_mask
    )

    # Where to write results
    output_config = documentai.DocumentOutputConfig(gcs_output_config=gcs_output_config)

    # The full resource name of the processor, e.g.:
    # projects/{project_id}/locations/{location}/processors/{processor_id}
    
    name = client.processor_path(project_id, location, processor_id)

    request = documentai.BatchProcessRequest(
        name=name,
        input_documents= input_config,
        document_output_config=output_config,
    )
    
    # BatchProcess returns a Long Running Operation (LRO)
    operation = client.batch_process_documents(request)

    # Continually polls the operation until it is complete.
    # This could take some time for larger files
    # Format: projects/{project_id}/locations/{location}/operations/{operation_id}
    try:
        print(f"Waiting for operation {operation.operation.name} to complete...")
        operation.result(timeout=timeout)
    # Catch exception when operation doesn't finish before timeout
    except (RetryError, InternalServerError) as e:
        print(e.message)

    # Once the operation is complete,
    # get output document information from operation metadata
    metadata = documentai.BatchProcessMetadata(operation.metadata)

    if metadata.state != documentai.BatchProcessMetadata.State.SUCCEEDED:
        raise ValueError(f"Batch Process Failed: {metadata.state_message}")


#NOTE: not tested only for more than 1000 docs at the time

# def create_batches_sample(
#     gcs_bucket_name: str,
#     gcs_prefix: str,
#     batch_size: int = 50,
# ) -> None:
#     # Creating batches of documents for processing
#     batches = gcs_utilities.create_batches(
#         gcs_bucket_name=gcs_bucket_name, gcs_prefix=gcs_prefix, batch_size=batch_size
#     )

#     print(f"{len(batches)} batch(es) created.")
#     for batch in batches:
#         print(f"{len(batch.gcs_documents.documents)} files in batch.")
#         print(batch.gcs_documents.documents)

#         # Use as input for batch_process_documents()
#         # Refer to https://cloud.google.com/document-ai/docs/send-request
#         # for how to send a batch processing request
#         request = documentai.BatchProcessRequest(
#             name="processor_name", input_documents=batch
#         )