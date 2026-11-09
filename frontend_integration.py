import os
import requests
from databricks.sdk import WorkspaceClient

def call_bob_backend(backend_url: str, advisor_id: str) -> dict:
    # Uses the frontend app's own DATABRICKS_CLIENT_ID/SECRET injected by Databricks.
    workspace_client = WorkspaceClient()
    auth_headers = workspace_client.config.authenticate()

    response = requests.get(
        f"{backend_url.rstrip('/')}/api/v1/advisors/{advisor_id}/bob",
        headers=auth_headers,
        timeout=(5, 30),
    )
    response.raise_for_status()
    return response.json()