# Copyright 2025 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# pylint: disable=C0301
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
AGENT_FOUNDATION_MODEL = os.getenv("AGENT_FOUNDATION_MODEL", "gemini-2.0-flash")
AGENT_ENGINE_RESOURCE_ID = os.getenv("AGENT_ENGINE_RESOURCE_ID", "")
USER_AGENT = os.getenv("USER_AGENT", "unset")
AGENT_DESCRIPTION = os.getenv("AGENT_DESCRIPTION", "unset")
DATA_STORE_ID = os.getenv("DATA_STORE_ID", "unset")
