from google.auth.credentials import Credentials

project_path = "capgemini-genai-hackathon.com/gen-hi-france-genai-force1"
project_id = "gen-hi-france-genai-force1"
project_num = "881178893280"
credentials = Credentials
location = "europe-west1"
bucket = "'gs://my_staging_bucket'"

def init_sample(
    project = None,
    location = None,
    experiment = None,
    staging_bucket = None,
    credentials = None,
    encryption_spec_key_name = None,
):

    from google.cloud import aiplatform

    aiplatform.init(
        # your Google Cloud Project ID or number, environment default used is not set
        project=project,

        # the Vertex AI region you will use, defaults to us-central1
        location=location,
        
        # the name of the experiment to use to track logged metrics and parameters
        experiment=experiment,

        # Google Cloud Storage bucket in same region as location, used to stage artifacts
        staging_bucket=staging_bucket,

        # custom google.auth.credentials.Credentials, environment default creds used if not set
        credentials=credentials,

        # customer managed encryption key resource name, will be applied to all Vertex AI resources if set
        encryption_spec_key_name=encryption_spec_key_name,
    )

init_sample(project = project_id, location = location, staging_bucket = bucket, credentials = credentials)
