import subprocess
import os

WHEEL_URL = "gs://agent_framework/latest/google_genai_agents-0.0.2.dev20250304+733376416-py3-none-any.whl"
WHEEL_FILE = "google_genai_agents-0.0.2.dev20250204+723246417-py3-none-any.whl"

def download_wheel():
    if not os.path.exists(WHEEL_FILE):
        try:
            subprocess.check_call(["gsutil", "cp", WHEEL_URL, "."])
            print(f"Downloaded {WHEEL_FILE}")
        except subprocess.CalledProcessError as e:
            print(f"Error downloading wheel: {e}")
            raise

if __name__ == "__main__":
    download_wheel()
