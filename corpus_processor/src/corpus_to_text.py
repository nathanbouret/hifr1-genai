
from pathlib import Path
from config import config
import numpy as np

from google.cloud import storage
from google.cloud import documentai
from google.api_core.client_options import ClientOptions
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from langchain.docstore.document import Document
# from langchain.document_loaders import GCSDirectoryLoader, GCSFileLoader  
# from google.cloud import documentai  # type: ignore  # import error to be fixed  


GCP_CONFIG = config.gcp_config()
DOCUMENT_PROCESSOR_CONFIG = config.document_processor_config()

project_name = GCP_CONFIG['PROJECT_NAME']
bucket_name = GCP_CONFIG['BUCKET_NAME']
bucket_txt_name = DOCUMENT_PROCESSOR_CONFIG['BUCKET_TXT_NAME']
prefix = 'document_obj'



#### this function initied by Marzieh -> to be updated and adapted by Alfredo
def read_documents_from_local(data_dir, read_from):
    if read_from == 'txt':
        loader = DirectoryLoader(data_dir, glob="./*.txt", loader_cls=TextLoader)
        documents = loader.load()
        print(f'# of .txt documents: {len(documents)}')
        # print(f'content of the first document:\n{documents[0].page_content[0:100]}...\n')
    if read_from == 'pdf':
        loader = DirectoryLoader(data_dir, glob="./*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()
        print(f'# of pages in .pdf documents: {len(documents)}')
        # print(f'content of the first document:\n{documents[0].page_content[0:100]}...\n')
    
    return documents

def read_documents_from_bucket():

    # loader = GCSDirectoryLoader(project_name=PROJECT_NAME, bucket=BUCKET_NAME, prefix=prefix)
    # documents = loader.load()
    # print(f'# of documents: {len(documents)}')
    # # print(f'content of the first document:\n{documents[0].page_content[0:100]}...\n')

    # Get List of Document Objects from the Output Bucket
    last_file_number = 0
    documents = []
    storage_client = storage.Client(project=project_name)
    output_blobs = storage_client.list_blobs(bucket_name, prefix=prefix)
    dic = {}
    for blob in output_blobs:
        print(blob.name)
        # Document AI may output multiple JSON files per source file
        if blob.content_type != "application/json":
            print(
                f"Skipping non-supported file: {blob.name} - Mimetype: {blob.content_type}"
            )
            continue
        path_parts = blob.name.split('/')
        if int(path_parts[2]) != last_file_number:
            txt = ''
            last_file_number = int(path_parts[2])
            max_key = max(dic.keys())
            for i in range(0, max_key+1):
                txt = txt + '\n' + dic[i]
            upload_txt(storage_client, bucket_name, bucket_txt_name, org_file_name, txt)
            dic = {}
        # Download JSON File as bytes object and convert to Document Object
        print(f"Fetching {blob.name}")
        document = documentai.Document.from_json(
            blob.download_as_bytes(), ignore_unknown_fields=True
        )
        org_file_name = Path(blob.name).stem
        chunk_num = int(org_file_name.split('-')[-1])
        org_file_name = org_file_name.split('-')[:-1]
        org_file_name = '-'.join(org_file_name)
        dic[chunk_num] = document.text
        # txt = txt + '\n' + document.text
        documents.append(document)

    max_key = max(dic.keys())
    txt = ''
    for i in range(0, max_key+1):
        txt = txt + '\n' + dic[i]
    upload_txt(storage_client, bucket_name, bucket_txt_name, org_file_name, txt)


def upload_txt(storage_client, bucket_name, bucket_txt_name, org_file_name, txt):
    # upload text format of a document into the google bucket
    bucket = storage_client.get_bucket(bucket_name)
    blob_path = bucket_txt_name + '/' + org_file_name
    blob_txt = bucket.blob(blob_path)
    blob_txt.content_type = 'text/plain'
    blob_txt.upload_from_string(txt)
    print(f'Successfully uploaded {org_file_name} to {bucket_name}/{bucket_txt_name}.')                


def read_txt_files_from_bucket():
    documents = []
    storage_client = storage.Client(project=project_name)
    output_blobs = storage_client.list_blobs(bucket_name, prefix=bucket_txt_name)
    for blob in output_blobs:
        print(blob.name)
        file_name = blob.name.split('/')[-1]
        downloaded_blob = blob.download_as_string()
        # print(downloaded_blob)
        new_doc = Document(page_content=downloaded_blob, metadata={'file_name': file_name})
        documents.append(new_doc)
    return documents

############################################################################################


#project_id = "gen-hi-france-genai-force1"
#location = "us"
#processor_id = "97ebbf63e06f596b" # Create processor before running sample
#file_path = ".\corpus\bayer_future_trends.pdf"
#mime_type = "application/pdf" # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
# field_mask = "text,entities,pages.pageNumber"  # Optional. The fields to return in the Document object.
# processor_version_id = "YOUR_PROCESSOR_VERSION_ID" # Optional. Processor version to use
"""
# TODO(developer): Uncomment these variables before running the sample.
project_id = "gen-hi-france-genai-force1"
location = "us"
processor_display_name = "test-doc" # Must be unique per project, e.g.: "My Processor"
processor_type = "Document OCR" # Use `fetch_processor_types()` to get available processor types
file_path = ".\corpus\bayer_future_trends.pdf"
mime_type = "application/pdf"  # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types



def quickstart(
    project_id: str,
    location: str,
    processor_display_name: str,
    processor_type: str,
    file_path: str,
    mime_type: str,
):
    # You must set the `api_endpoint`if you use a location other than "us".
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the location, e.g.:
    # `projects/{project_id}/locations/{location}`
    parent = client.common_location_path(project_id, location)

    # Create a Processor
    processor = client.create_processor(
        parent=parent,
        processor=documentai.Processor(
            display_name=processor_display_name, type_=processor_type
        ),
    )

    # Print the processor information
    print(f"Processor Name: {processor.name}")

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load binary data
    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    # Configure the process request
    # `processor.name` is the full resource name of the processor, e.g.:
    # `projects/{project_id}/locations/{location}/processors/{processor_id}`
    request = documentai.ProcessRequest(name=processor.name, raw_document=raw_document)

    result = client.process_document(request=request)

    # For a full list of `Document` object attributes, reference this page:
    # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
    document = result.document

    # Read the text recognition output from the processor
    print("The document contains the following text:")
    print(document.text)

quickstart(project_id = project_id,
    location=location,
    processor_display_name= processor_display_name,
    processor_type=processor_type,
    file_path=file_path,
    mime_type=mime_type)

"""