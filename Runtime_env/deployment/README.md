# Deployment README.md

The application leverages [**Terraform**](http://terraform.io) to define and provision the underlying infrastructure. The application uses CloudBuild to build and deploy the containers for the application.

## Setup

**Prerequisites:**

1. A Google Cloud project.
2. Terraform installed on your local machine.
3. The account running the terraform must have the necessary permissions. Recommended roles listed below:
- roles/serviceusage.serviceUsageAdmin
- roles/resourcemanager.projectIamAdmin
- roles/iam.serviceAccountAdmin
- roles/iam.serviceAccountUser
- roles/storage.admin
- roles/artifactregistry.admin
- roles/run.admin
- roles/cloudbuild.builds.editor

## Step-by-Step Guide (Cloud Build)
1. **Configure Env Variables**

   - Edit [`deployment/config/dev.yaml`](config/dev.yaml) with your Google Cloud settings. There are certain variables that must be set manually and some variables that will be auto-populated if you run `build.py`. These variables that must be set manually are marked below as required.

   | Variable                               | Description                                                          | Required |
   | ---------------------------------------| -------------------------------------------------------------------- | :------: |
   | PROJECT_ID                             | Google Cloud Project ID for resource deployment.                     |   Yes    |
   | VERTEX_AI_LOCATION                     | The region to use for the various resources.                         |   Yes    |
   | AGENT_BUILDER_LOCATION                 | The region to use for Agent Builder (options shown below).           |   Yes    |
   | AGENT_INDUSTRY_TYPE                    | The selected industry type (options shown below).                    |   Yes    |
   | AGENT_ORCHESTRATION_FRAMEWORK          | The selected agent framework (options shown below).                  |   Yes    |
   | AGENT_FOUNDATION_MODEL                 | The selected foundation model (options shown below).                 |   Yes    |
   | USER_AGENT                             | The name of the agent.                                               |   Yes    |
   | AGENT_DESCRIPTION                      | The description of the agent.                                        |   Yes    |
   | FRONTEND_URL                           | The URL of frontend Cloud Run service. Used for CORS policy setting. |   No     |
   | GCS_STAGING_BUCKET                     | The name of the Staging bucket for Vertex AI resources.              |   No     |
   | DATA_STORE_ID                          | The ID of the Vertex AI Search Datastore                             |   No     |
   | GOOGLE_GENAI_USE_VERTEXAI              | Boolean value (set to "TRUE" if using ADK)                           |   No     |
   | GOOGLE_CLOUD_PROJECT                   | Google Cloud Project ID for resource deployment. (Used by ADK)       |   No     |
   | GOOGLE_CLOUD_LOCATION                  | The region to use for the various resources. (Used by ADK)           |   No     |

   - Options:

      AGENT_BUILDER_LOCATION:
      - "us"
      - "global"

      AGENT_INDUSTRY_TYPE:
      - "finance"
      - "healthcare"
      - "retail"

      AGENT_ORCHESTRATION_FRAMEWORK:
      - "langchain_prebuilt_agent"
      - "langchain_vertex_ai_agent_engine_agent" # use if using Agent Engine deployment
      - "langgraph_prebuilt_agent"
      - "langgraph_vertex_ai_agent_engine_agent" # use if using Agent Engine deployment
      - "llamaindex_agent"  # can use with either Agent Engine or Cloud Run deployment
      - "agent_development_kit_agent"  # can use with either Agent Engine or Cloud Run deployment"

      AGENT_FOUNDATION_MODEL:
      - "gemini-2.5-pro"
      - "gemini-2.5-flash"
      - "gemini-2.5-flash-lite"
      - "gemini-2.0-flash"
      - "gemini-1.5-pro"
      - "gemini-1.5-flash"
      - "claude-3-7-sonnet" # requires permission / signing T&C; must be us-east5
      - "claude-3-5-sonnet-v2" # requires permission / signing T&C; must be us-east5
      - "llama-4-maverick-17b-128e-instruct-maas" # requires the model to be enabled
      - "llama-4-scout-17b-16e-instruct-maas" # requires the model to be enabled
      - "llama-3.3-70b-instruct-maas" # requires the model to be enabled
      - "llama-3.1-405b-instruct-maas" # requires the model to be enabled

   - Example Configuration:
   ```python
   PROJECT_ID: next-2024-industry-demos
   VERTEX_AI_LOCATION: us-central1
   AGENT_BUILDER_LOCATION: us
   AGENT_INDUSTRY_TYPE: finance
   AGENT_ORCHESTRATION_FRAMEWORK: langgraph_prebuilt_agent
   AGENT_FOUNDATION_MODEL: gemini-2.0-flash
   USER_AGENT: agentsmithy-starter-agent
   AGENT_DESCRIPTION: "This is a test agent"
   ```

   - If you want your agent runtime to use an Agent Engine deployment, specify this using the `AGENT_ENGINE_RESOURCE_ID` variable shown below. Do not define this variable if you do not want to use Agent Engine. Example:
   `AGENT_ENGINE_RESOURCE_ID: projects/599247973214/locations/us-central1/reasoningEngines/5008011581729013760`

   - If you want to use Agent Development Kit as your orchestration framework, specify this using the `GOOGLE_GENAI_USE_VERTEXAI`, `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION` variables shown below. Example:

    GOOGLE_GENAI_USE_VERTEXAI: 'TRUE'
    GOOGLE_CLOUD_PROJECT: next-2024-industry-demos
    GOOGLE_CLOUD_LOCATION: us-central1

2. **Run Cloud Build Job**

   - The file [`deployment/cd/dev.yaml`](cd/dev.yaml) contains a Cloud Build Manifest that will build and push your agent backend container and deploy it to Cloud Run. There are a couple of substitution variables to be set when using this file. 

   | Variable                               | Description                                                                           | Required |
   | ---------------------------------------| ------------------------------------------------------------------------------------- | :------: |
   | _CONTAINER_NAME                        | The name of the backend container. Defaults to "agent_runtime"                        |   No     |
   | _PROJECT_ID                            | Google Cloud Project ID for resource deployment.                                      |   Yes    |
   | _ARTIFACT_REGISTRY_REPO_NAME           | Artifact registry for containers.                                                     |   Yes    |
   | _SERVICE_NAME                          | The name of the backend Cloud Run service. Defaults to "agent-runtime-service"        |   No     |
   | _REGION                                | The region to use for the container and Cloud Run service. Defaults to "us-central1"  |   No     |

   - Example run:
   `gcloud builds submit --config deployment/cd/dev.yaml --substitutions _CONTAINER_NAME=agent_runtime,_PROJECT_ID=next-2024-industry-demos,_ARTIFACT_REGISTRY_REPO_NAME=my_artifact_registry,_SERVICE_NAME=agent-runtime-service,_REGION=us-central1 .`


## Step-by-Step Guide (Terraform)

1. **Configure Terraform Variables**

   - Edit [`deployment/terraform/vars/env.tfvars`](terraform/vars/env.tfvars) with your Google Cloud settings. These will be auto-populated if you run `build.py`, which will source these variables from `deployment/config/dev.yaml`. Terraform will use `prod_project_id` by default.

   | Variable                                    | Description                                                     | Required |
   | ------------------------------------------- | --------------------------------------------------------------- | :------: |
   | prod_project_id                             | Google Cloud Project ID for resource deployment. [prod]         |   Yes    |
   | stage_project_id                            | Google Cloud Project ID for resource deployment. [stage]        |   No     |
   | dev_project_id                              | Google Cloud Project ID for resource deployment. [dev]          |   No     |
   | region                                      | Google Cloud region for resource deployment.                    |   Yes    |
   | agent_name                                  | Name of the Agent, used for creating resources.                 |   Yes    |
   | default_agents_prefix                       | Default naming prefix for resources.                            |   Yes    |
   | vertex_ai_staging_bucket                    | Staging bucket for Vertex AI resources.                         |   Yes    |
   | artifact_registry_repo_name                 | Artifact registry for containers.                               |   Yes    |
   | backend_cloud_run_service_name              | The name of the backend Cloud Run service.                      |   Yes    |
   | frontend_cloud_run_service_name             | The name of the frontend Cloud Run service.                     |   Yes    |

2. **Deploy Infrastructure with Terraform**

   - First, open a terminal and enable required Google Cloud APIs:

   ```bash
   gcloud config set project $YOUR_DEV_PROJECT
   gcloud services enable serviceusage.googleapis.com cloudresourcemanager.googleapis.com
   ```

   - Then, navigate to the Terraform directory:

   ```bash
   cd deployment/terraform
   ```

   - Initialize Terraform:

   ```bash
   terraform init
   ```

   - Apply the Terraform configuration:

   ```bash
   terraform apply --var-file vars/env.tfvars
   ```

   - Type 'yes' when prompted to confirm

After completing these steps, your infrastructure will be set up and ready for deployment!

3. **De-Provision Infrastructure with Terraform**

   - Open a terminal and navigate to the Terraform directory:

   ```bash
   cd deployment/terraform
   ```

   - Initialize Terraform:

   ```bash
   terraform init
   ```

   - Apply the Terraform configuration:

   ```bash
   terraform destroy --var-file vars/env.tfvars
   ```

   - Type 'yes' when prompted to confirm

4. There is an optional counter that sents a request to our AgentSmithy server which increments when this terraform script is run. This allows us to track number of runs. The post request is empty and no information is sent over to this server other than an empty request. If you wish to opt-out of this counter, you can do so by setting the following [terraform/variables.tf](terraform/variables.tf) block to false:

```terraform
variable "increment_runs" {
  type        = bool
  description = "Whether to increment installs counter."
  default     = false
}
```