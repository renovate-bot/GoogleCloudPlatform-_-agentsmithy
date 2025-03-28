# AgentSmithy Backend

This readme details out to use the runtime environment portion of AgentSmithy.

## Getting Started

### Prerequisites

- Python >=3.10,<3.13
- Google Cloud SDK installed and configured
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management
- A development environment (e.g. your local IDE or, when running remotely on Google Cloud, [Cloud Shell](https://cloud.google.com/shell) or [Cloud Workstations](https://cloud.google.com/workstations)).

Use the downloaded folder as a starting point for your own Generative AI application.

### Installation

Create a python virtual environment and activate the venv:

```bash
python -m venv agentsmith-venv
source agentsmith-venv/bin/activate
```

Install required packages using Poetry:

```bash
pip install poetry
poetry install
```

### Setup

Set your default Google Cloud project and region:

```bash
export PROJECT_ID="YOUR_PROJECT_ID"
gcloud config set project $PROJECT_ID
gcloud auth application-default login
gcloud auth application-default set-quota-project $PROJECT_ID
```

## Commands

| Command              | Description                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------- |
| `make backend`       | Locally run the FastAPI server at `http://localhost:8000`                                   |


For full command options and usage, refer to the [Makefile](Makefile).

## API Spec

A Swagger doc can be found at: `http://localhost:4200/docs`

<p align="left">
    <img src="assets/images/docs_screenshot.png" alt="sample" width="1000"/>
</p>



## Local Testing

You can your agent server using Postman or cURL. Below is an example cURL command:

```bash
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d '{
    "input": {
        "input": {
            "messages": [
              {
                "type": "human",
                "content": "How did Alphabet perform in their earnings reports in Q4 2024?"
              }
            ],
            "user_id": "user123",
            "session_id": "session456"
        }
    }
  }' \
  "http://localhost:8000/streamQuery"
```


## Server Details

See [app/README.md](app/README.md) for more details related to the setup of the Agent and the backend server.


## Deployment

The repository includes Cloud Build and Terraform configurations for the setup of the Dev Google Cloud project.
See [deployment/README.md](deployment/README.md) for instructions.
