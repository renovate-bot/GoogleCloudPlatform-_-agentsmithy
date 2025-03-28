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
# Create default cloud run services with temporary containers
resource "google_cloud_run_v2_service" "backend-service" {
  for_each = local.deploy_project_ids
  project  = each.value
  name     = var.backend_cloud_run_service_name
  location = var.region
  deletion_protection = false

  template {
    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello"
    }
    service_account = google_service_account.cloud_run_app_sa[each.key].email
  }
  depends_on = [resource.google_project_service.shared_services, resource.google_project_iam_member.cloud_run_app_sa_roles]
}

resource "google_cloud_run_service_iam_binding" "backend_access" {
  for_each = local.deploy_project_ids
  project  = each.value
  location = google_cloud_run_v2_service.backend-service[each.key].location
  service  = google_cloud_run_v2_service.backend-service[each.key].name
  role     = "roles/run.invoker"
  members = [
    "allUsers"
  ]
}

resource "google_cloud_run_v2_service" "frontend-service" {
  for_each = local.deploy_project_ids
  project  = each.value
  name     = var.frontend_cloud_run_service_name
  location = var.region
  deletion_protection = false

  template {
    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello"
    }
    service_account = google_service_account.cloud_run_app_sa[each.key].email
  }
  depends_on = [resource.google_project_service.shared_services, resource.google_project_iam_member.cloud_run_app_sa_roles]
}

resource "google_cloud_run_service_iam_binding" "frontend_access" {
  for_each = local.deploy_project_ids
  project  = each.value
  location = google_cloud_run_v2_service.frontend-service[each.key].location
  service  = google_cloud_run_v2_service.frontend-service[each.key].name
  role     = "roles/run.invoker"
  members = [
    "allUsers"
  ]
}