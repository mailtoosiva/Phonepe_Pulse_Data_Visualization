import os
import subprocess
import shutil
# from GitPython import Repo # Uncomment if you prefer GitPython

# Configuration (or load from config.ini)
GITHUB_REPO_URL = "https://github.com/PhonePe/pulse.git"
RAW_DATA_DIR = "data/raw_data/"

def clone_phonepe_pulse_repo():
    """Clones the PhonePe Pulse GitHub repository."""
    if os.path.exists(RAW_DATA_DIR):
        print(f"Removing existing {RAW_DATA_DIR}...")
        shutil.rmtree(RAW_DATA_DIR)
        print("Existing directory removed.")

    print(f"Cloning {GITHUB_REPO_URL} into {RAW_DATA_DIR}...")
    try:
        # Using subprocess for simple git clone
        subprocess.run(["git", "clone", GITHUB_REPO_URL, RAW_DATA_DIR], check=True)
        print("Repository cloned successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        print("Please ensure Git is installed and accessible in your PATH.")
    except FileNotFoundError:
        print("Error: 'git' command not found. Please ensure Git is installed.")

    # Alternative with GitPython (if installed: pip install GitPython)
    # try:
    #     Repo.clone_from(GITHUB_REPO_URL, RAW_DATA_DIR)
    #     print("Repository cloned successfully using GitPython!")
    # except Exception as e:
    #     print(f"Error cloning repository with GitPython: {e}")

if __name__ == "__main__":
    clone_phonepe_pulse_repo()