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
"""Module to build all different combinations of agents.

Recommended run configuration: python -W ignore -m deploy_combos
"""
import csv
import os
import importlib
import subprocess

import yaml
import vertexai

from app.orchestration.server_utils import get_agent_from_config
from app.utils.utils import deploy_agent_to_agent_engine

PROJECT_ID = "agentsmithy-dev"
VERTEX_AI_LOCATION = "us-central1"
GCS_STAGING_BUCKET = "gs://agentsmithy_staging"
OUTPUT_CONFIG_FILE = "deployment/config/dev.yaml"
OUTPUT_COMBOS_FILE = "deployment/config/next_agent_deployments.csv"

vertexai.init(
    project=PROJECT_ID,
    location=VERTEX_AI_LOCATION,
    staging_bucket=GCS_STAGING_BUCKET
)


def write_yaml_file(filepath: str, contents: dict, mode: str):
    """Writes a dictionary to yaml. Defaults to utf-8 encoding.

    Args:
        filepath (str): Path to the file.
        contents (dict): Dictionary to be written to yaml.
        mode (str): Read/write mode to be used.

    Raises:
        Exception: An error is encountered while writing the file.
    """
    try:
        with open(filepath, mode, encoding='utf-8') as file:
            yaml.safe_dump(contents, file, sort_keys=False)
        file.close()
    except yaml.YAMLError as err:
        raise yaml.YAMLError(f'Error writing to file. {err}') from err


def write_file(filepath: str, text: str, mode: str):
    """Writes a file at the specified path. Defaults to utf-8 encoding.

    Args:
        filepath (str): Path to the file.
        text (str): Text to be written to file.
        mode (str): Read/write mode to be used.

    Raises:
        Exception: An error is encountered writing the file.
    """
    try:
        with open(filepath, mode, encoding='utf-8') as file:
            file.write(text)
        file.close()
    except OSError as err:
        raise OSError(f'Error writing to file. {err}') from err


def execute_process(command: str):
    """Executes an external shell process.

    Args:
        command (str): Command to execute.

    Raises:
        Exception: An error occured while executing the script.
    """
    try:
        result = subprocess.run([command],
                       shell=True,
                       check=True,
                       capture_output=True,
                       text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as err:
        raise RuntimeError(f'Error executing process. {err}') from err


def append_dict_to_csv(data, csv_file):
    """Appends a dictionary to a CSV file.  If the file exists and
    has a header, the header is not rewritten. If the file doesn't
    exist, it creates the file and writes the header.

    Args:
        data (dict): The dictionary to append.
        csv_file (str): The path to the CSV file.
    """

    file_exists = os.path.isfile(csv_file)

    try:
        with open(csv_file, 'a', newline='') as csvfile:  # Use 'a' for append mode
            writer = csv.writer(csvfile)

            if not file_exists:
                # Write the header row (keys of the dictionary) only if the file doesn't exist
                writer.writerow(data.keys())

            # Write the data row (values of the dictionary)
            writer.writerow(data.values())

    except Exception as e:
        print(f"An error occurred: {e}")


data_stores_list = [
    {
        "data_store_id": "next-25-finance-dev_1742232104413",
        "industry": "finance",
        "user_agent": "agentsmithy-finance-agent",
        "agent_description": "This agent is intended to demonstrate finance agentic workflows.",
    },
    {
        "data_store_id": "next-25-healthcare-dev_1742232182064",
        "industry": "healthcare",
        "user_agent": "agentsmithy-healthcare-agent",
        "agent_description": "This agent is intended to demonstrate healthcare agentic workflows.",
    },
    {
        "data_store_id": "next-25-retail-dev_1742233012087",
        "industry": "retail",
        "user_agent": "agentsmithy-retail-agent",
        "agent_description": "This agent is intended to demonstrate retail agentic workflows.",
    }
]

ae_orchestration_frameworks_list = [
    ("langchain_vertex_ai_agent_engine_agent", "langchain-ae"),
    ("langgraph_vertex_ai_agent_engine_agent", "langgraph-ae"),
    ("llamaindex_agent", "llamaindex"),
]

ae_foundation_models_list = [
    ("gemini-2.0-flash", "gem20-f"),
    ("gemini-1.5-pro", "gem15-p"),
    # ("claude-3-7-sonnet", "cla37-so"), # Claude doesn't work with AE for now
    # ("claude-3-5-sonnet-v2", "cla35-so-v2"), # Claude doesn't work with AE for now
    ("llama-3.3-70b-instruct-maas", "lla33-70b"),
    ("llama-3.1-405b-instruct-maas", "lla31-405b"),
]

def deploy_combos(
    data_stores: list,
    orchestration_frameworks: list,
    foundation_models: list,
    deploy_to_agent_engine: bool = False,
) -> list:
    cnt = 0
    user_configs = []
    ae_deployed_resource_ids = []
    for ds_config in data_stores:
        for (framework_long, framework_short) in orchestration_frameworks:
            for (model_long, model_short) in foundation_models:
                cnt += 1

                config = {
                    "PROJECT_ID": PROJECT_ID,
                    "VERTEX_AI_LOCATION": VERTEX_AI_LOCATION,
                    "GCS_STAGING_BUCKET": GCS_STAGING_BUCKET,
                    "AGENT_BUILDER_LOCATION": "us",
                    "DATA_STORE_ID": ds_config["data_store_id"],
                    "FRONTEND_URL": "https://test-chatbot-ui-599247973214.us-central1.run.app", # This isn't being used for now
                    "AGENT_INDUSTRY_TYPE": ds_config["industry"],
                    "AGENT_ORCHESTRATION_FRAMEWORK": framework_long,
                    "AGENT_FOUNDATION_MODEL": model_long,
                    "USER_AGENT": ds_config["user_agent"],
                    "AGENT_DESCRIPTION": ds_config["agent_description"]
                }

                user_configs.append(config)
                suffix = f'-{ds_config["industry"]}-{framework_short}-{model_short}-{"ae" if deploy_to_agent_engine else "fastapi"}'

                write_yaml_file(
                    filepath=OUTPUT_CONFIG_FILE,
                    contents=config,
                    mode="w"
                )

                if deploy_to_agent_engine:
                    # TODO figure out a better way to dynamically get these env after they are written
                    import app.orchestration.config
                    importlib.reload(app.orchestration.config)

                    agent_manager = get_agent_from_config(
                        agent_orchestration_framework=framework_long,
                        agent_foundation_model=model_long,
                        industry_type=ds_config["industry"]
                    )

                    print(f"Deploying Agent to Agent Engine: {config}")
                    remote_agent = None
                    if framework_long == "llamaindex_agent":
                        remote_agent = deploy_agent_to_agent_engine(
                            agent_manager,
                            ds_config["user_agent"],
                            ds_config["agent_description"]
                        )
                        # If AGENT_ENGINE_RESOURCE_ID is set, then the agent will query the remote agent
                        config["AGENT_ENGINE_RESOURCE_ID"] = remote_agent.resource_name

                    elif framework_long == "langgraph_vertex_ai_agent_engine_agent" or framework_long == "langchain_vertex_ai_agent_engine_agent":
                        remote_agent = deploy_agent_to_agent_engine(
                            agent_manager.agent_executor,
                            ds_config["user_agent"],
                            ds_config["agent_description"]
                        )
                        config["AGENT_ENGINE_RESOURCE_ID"] = remote_agent.resource_name

                    # Rewrite yaml to indicate that it's using AE now:
                    write_yaml_file(
                        filepath=OUTPUT_CONFIG_FILE,
                        contents=config,
                        mode="w"
                    )

                execute_process(
                    f"gcloud builds submit --config deployment/cd/dev.yaml --substitutions _SUFFIX={suffix} .",
                )

                # Get URL of the deployed Cloud Run instance
                result = execute_process(
                    f'''gcloud run services list --region=us-central1 --filter="SERVICE:'agent-runtime{suffix}'" --format="value(URL)" ''',
                )

                # Add metadata and write to a file:
                if not deploy_to_agent_engine:
                    config["AGENT_ENGINE_RESOURCE_ID"] = "N/A"
                config["RUNTIME_ENV_SELECTION"] = "AgentEngine" if deploy_to_agent_engine else "CloudRun/FastApi"
                config["CLOUD_RUN_URL"] = result

                append_dict_to_csv(config, OUTPUT_COMBOS_FILE)
                print(f"Agent: agent-runtime{suffix} Deployed.")
                # Next, deploy the equivalent frontend

    print("Total Combinations:", cnt)
    return ae_deployed_resource_ids



cr_orchestration_frameworks_list = [
    ("langchain_prebuilt_agent", "langchain-pre"),
    ("langgraph_prebuilt_agent", "langgraph-pre"),
    ("llamaindex_agent", "llamaindex")
]

cr_foundation_models_list = [
    ("gemini-2.0-flash", "gem20-f"),
    ("gemini-1.5-pro", "gem15-p"),
    ("claude-3-7-sonnet", "cla37-so"),
    ("claude-3-5-sonnet-v2", "cla35-so-v2"),
    ("llama-3.3-70b-instruct-maas", "lla33-70b"),
    ("llama-3.1-405b-instruct-maas", "lla31-405b"),
]

# Set up Cloud Run combos
deploy_combos(
    data_stores=data_stores_list,
    orchestration_frameworks=cr_orchestration_frameworks_list,
    foundation_models=cr_foundation_models_list,
    deploy_to_agent_engine=False
)


# Set up Agent Engine combos
deploy_combos(
    data_stores=data_stores_list,
    orchestration_frameworks=ae_orchestration_frameworks_list,
    foundation_models=ae_foundation_models_list,
    deploy_to_agent_engine=True
)
