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
# Data source to get project numbers
data "google_project" "projects" {
  for_each   = local.deploy_project_ids
  project_id = each.value
}

# Grant Cloud Run SA the required permissions to run the application
resource "google_project_iam_member" "cloud_run_app_sa_roles" {
  for_each = {
    for pair in setproduct(keys(local.deploy_project_ids), var.cloud_run_app_roles) :
    join(",", pair) => {
      project = local.deploy_project_ids[pair[0]]
      role    = pair[1]
    }
  }

  project    = each.value.project
  role       = each.value.role
  member     = "serviceAccount:${google_service_account.cloud_run_app_sa[split(",", each.key)[0]].email}"
  depends_on = [resource.google_project_service.shared_services]
}
