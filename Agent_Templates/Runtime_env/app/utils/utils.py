# ==============================================================================
# Copyright 2025 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# ==============================================================================
"""Module that contains a function for exporting toml package dependencies to
requirements.txt format"""
import os

import toml
from vertexai import agent_engines
import yaml

def get_requirements_from_toml(pyproject_file="pyproject.toml"):
    """
    Reads a pyproject.toml file and extracts dependencies to generate a
    requirements.txt-compatible list. Handles extras correctly.

    Args:
        pyproject_file (str): Path to the pyproject.toml file.
        This is from the route dir.

    Returns:
        list: A list of strings, where each string is a dependency in the
              format expected by requirements.txt (e.g., "fastapi==0.110.3").
              Returns an empty list if the dependencies section is not found or
              if there's an error reading the file.
    """
    try:
        with open(pyproject_file, "r", encoding='utf-8') as f:
            data = toml.load(f)

        dependencies = data.get("tool", {}).get("poetry", {}).get("dependencies", {})

        if not dependencies:
            print("No dependencies section found in pyproject.toml.")
            return []

        requirements = []
        for package, version_info in dependencies.items():
            if package == "python":  # Skip python version specifier
                continue

            if isinstance(version_info, str):
                requirements.append(f"{package}>={version_info.replace('^', '')}")

            elif isinstance(version_info, dict):
                version = version_info.get("version")
                extras = version_info.get("extras")

                if extras:
                    extras_str = ",".join(extras)
                    requirements.append(f"{package}[{extras_str}]>={version.replace('^', '')}")
            else:
                print(f"Warning: Unexpected dependency format for {package}: {version_info}")

        return requirements

    except FileNotFoundError:
        print(f"Error: File not found: {pyproject_file}")
        return []
    except toml.TomlDecodeError as e:
        print(f"Error decoding TOML: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []


def read_yaml_file(filepath: str) -> dict:
    """Reads a yaml and returns file contents as a dict. Defaults to utf-8 encoding.

    Args:
        filepath (str): Path to the yaml.

    Returns:
        dict: Contents of the yaml.

    Raises:
        Exception: If an error is encountered reading the file.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            file_dict = yaml.safe_load(file)
        file.close()
    except yaml.YAMLError as err:
        raise yaml.YAMLError(f"Error reading file. {err}'") from err
    return file_dict


def load_env_from_yaml(filepath: str):
    """
    Loads environment variables from a YAML file and sets them in the os.environ.

    Args:
        filepath (str): The path to the YAML file containing the environment variables.

    Raises:
        FileNotFoundError: If the specified YAML file does not exist.
        yaml.YAMLError: If there is an error parsing the YAML file.
    """
    try:
        env_vars = read_yaml_file(filepath)

        if env_vars is None:  # Handle empty YAML files
            print(f"Warning: YAML file {filepath} is empty.")
            return

        if not isinstance(env_vars, dict):
            raise TypeError(f"YAML file {filepath} must contain a dictionary at the top level.")

        for key, value in env_vars.items():
            if not isinstance(key, str):
                raise TypeError(f"Key '{key}' in YAML file must be a string.")
            if not isinstance(value, (str, int, float, bool, type(None))):
                raise TypeError(f"Value for key '{key}' in YAML file must be a string, number, boolean, or None. Found type: {type(value)}")

            # Convert value to string for setting in os.environ
            os.environ[key] = str(value)

    except FileNotFoundError:
        raise FileNotFoundError(f"YAML file not found: {filepath}")


def deploy_agent_to_agent_engine(
    agent,
    user_agent: str,
    description: str
):
    """
    Deploys the Vertex AI agent engine to a remote managed endpoint.

    Args:
        agent: The agent to be deployed to agent engine.
            Will be an .agent_executor in the case of langchain/langgraph
        user_agent: The name of the agent
        description: The description of the agent

    Returns:
        Remote Agent Engine agent.

    Exception:
        An error is encountered during deployment.
    """
    try:
        remote_agent = agent_engines.create(
            agent,
            requirements=get_requirements_from_toml(),
            display_name=user_agent,
            description=description,
            extra_packages=["./app", "./deployment/config"],
        )
    except Exception as e:
        raise RuntimeError(f"Error deploying Agent Engine Agent. {e}") from e

    return remote_agent
