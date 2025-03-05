# ==============================================================================
# Copyright 2025 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# ==============================================================================
"""Module that contains a function for exporting toml package dependencies to
requirements.txt format"""
import toml

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
        with open(pyproject_file, "r") as f:
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
                requirements.append(f"{package}{version_info}")  # Simple version spec

            elif isinstance(version_info, dict):
                version = version_info.get("version")
                extras = version_info.get("extras")

                if version:
                    requirements.append(f"{package}{version}")

                if extras:
                    extras_str = ",".join(extras)
                    requirements.append(f"{package}[{extras_str}]")  # Handle extras
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
