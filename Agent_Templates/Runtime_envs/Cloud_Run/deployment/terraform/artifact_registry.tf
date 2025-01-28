resource "google_artifact_registry_repository" "my-repo" {
  location      = var.region
  repository_id = local.artifact_registry_repo_name
  description   = "Repo for Generative AI applications"
  format        = "DOCKER"
  project       = var.prod_project_id
  depends_on    = [resource.google_project_service.cicd_services, resource.google_project_service.shared_services]
}