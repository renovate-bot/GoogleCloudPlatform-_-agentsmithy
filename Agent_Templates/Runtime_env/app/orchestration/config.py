# ==============================================================================
# Copyright 2025 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# ==============================================================================
"""Module that sets up environment variables from a sourced config yaml file."""
import os

import google

from app.orchestration.constants import DEV_YAML_CONFIG_PATH
from app.utils.utils import load_env_from_yaml

# Initialize Google Cloud and Vertex AI
credentials, project_id = google.auth.default()

# Explicitly set env vars from file (used for agent engine)
load_env_from_yaml(DEV_YAML_CONFIG_PATH)

SERP_API_KEY = os.getenv("SERPER_API_KEY", "unset")
PROJECT_ID = os.getenv("PROJECT_ID", project_id)
VERTEX_AI_LOCATION = os.getenv("REGION", "us-central1")
GCS_STAGING_BUCKET = os.getenv("GCS_STAGING_BUCKET", "unset")
AGENT_BUILDER_LOCATION = os.getenv("AGENT_BUILDER_LOCATION", "us")
AGENT_INDUSTRY_TYPE = os.getenv("AGENT_INDUSTRY_TYPE", "unset")
AGENT_ORCHESTRATION_FRAMEWORK = os.getenv("AGENT_ORCHESTRATION_FRAMEWORK", "unset")
USER_AGENT = os.getenv("USER_AGENT", "unset")
AGENT_DESCRIPTION = os.getenv("AGENT_DESCRIPTION", "unset")
DATA_STORE_ID = os.getenv("DATA_STORE_ID", "unset")
