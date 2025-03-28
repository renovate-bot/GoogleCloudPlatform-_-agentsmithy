# Copyright 2025 Google LLC
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
# Your Production Google Cloud project id
prod_project_id = ""

# Your Staging Google Cloud project id
stage_project_id = ""

# Your Dev Google Cloud project id
dev_project_id = ""

# The Google Cloud region you will use to deploy the infrastructure
region = ""

# The name of your agent
agent_name = ""

# Be careful to follow naming guidelines (must be a short string with no numbers or dashes)
default_agents_prefix = "genai agents"

# The name of your GCP storage bucket
vertex_ai_staging_bucket = ""

# The name of the artifact registry
artifact_registry_repo_name = ""

# The name of the backend agent service
backend_cloud_run_service_name = ""

# The name of the frontend agent service
frontend_cloud_run_service_name = ""
