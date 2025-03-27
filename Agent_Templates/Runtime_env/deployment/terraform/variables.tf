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
variable "prod_project_id" {
  type        = string
  description = "**Production** Google Cloud Project ID for resource deployment."
}

variable "stage_project_id" {
  type        = string
  description = "**Stage** Google Cloud Project ID for resource deployment."
}

variable "dev_project_id" {
  type        = string
  description = "**Dev** Google Cloud Project ID for resource deployment."
}

variable "region" {
  type        = string
  description = "Google Cloud region for resource deployment."
  default     = "us-central1"
}

variable "agent_name" {
  description = "Name of the Agent"
  type        = string
}

variable "default_agents_prefix" {
  description = "Shortname for gen ai agent resources"
  type        = string
}

variable "vertex_ai_staging_bucket" {
  description = "Staging bucket for vertex ai resources"
  type        = string
}

variable "artifact_registry_repo_name" {
  description = "The name of the artifact registry"
  type        = string
}

variable "backend_cloud_run_service_name" {
  description = "Backend Cloud Run Service Name"
  type        = string
}

variable "frontend_cloud_run_service_name" {
  description = "Frontend Cloud Run Service Name"
  type        = string
}

variable "cloud_function_runs_counter_url" {
  type        = string
  description = "The URL of your Cloud Function to increment installs count."
  default     = "https://agentsmithy-terraform-runs-dev-599247973214.us-central1.run.app"
}

variable "increment_runs" {
  type        = bool
  description = "Whether to increment installs counter."
  default     = true
}

variable "cloud_run_app_roles" {
  description = "List of roles to assign to the Cloud Run app service account"
  type        = list(string)
  default = [
    "roles/aiplatform.user",
    "roles/discoveryengine.editor",
    "roles/logging.logWriter",
    "roles/cloudtrace.agent",
    "roles/storage.admin",
  ]
}
