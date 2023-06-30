
from google.api_core.client_options import ClientOptions
from google.cloud import documentai  # type: ignore


#project_id = "gen-hi-france-genai-force1"
#location = "us"
#processor_id = "97ebbf63e06f596b" # Create processor before running sample
#file_path = ".\corpus\bayer_future_trends.pdf"
#mime_type = "application/pdf" # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
# field_mask = "text,entities,pages.pageNumber"  # Optional. The fields to return in the Document object.
# processor_version_id = "YOUR_PROCESSOR_VERSION_ID" # Optional. Processor version to use

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