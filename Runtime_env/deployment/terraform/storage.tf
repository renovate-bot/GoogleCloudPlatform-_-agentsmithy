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
terraform {
  required_version = ">= 1.0.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "< 7.0.0"
    }
  }
}

resource "google_storage_bucket" "vertex_ai_staging_bucket" {
  for_each = local.deploy_project_ids
  name                        = "${var.vertex_ai_staging_bucket}"
  location                    = var.region
  project                     = each.value
  uniform_bucket_level_access = true
  force_destroy               = true
  depends_on                  = [resource.google_project_service.shared_services]
}
