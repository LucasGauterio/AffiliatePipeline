import os
from google.cloud import secretmanager
from config.settings import AppSettings

def get_secret(secret_id: str) -> str:
    settings = AppSettings()
    if settings.ENV == "production":
        client = secretmanager.SecretManagerServiceClient()
        project_id = settings.GCP_PROJECT_ID
        if not project_id:
            raise ValueError("GCP_PROJECT_ID is required in production")
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    else:
        value = os.getenv(secret_id)
        if not value:
            raise ValueError(f"Secret {secret_id} not found in environment")
        return value
