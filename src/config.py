"""Load project configurations from .env files.
Provides easy access to paths and credentials used in the project.
Meant to be used as an imported module.
"""
from pathlib import Path
import os
from dotenv import find_dotenv, dotenv_values


path_to_env = find_dotenv()
is_env_not_found = path_to_env == ''

if is_env_not_found:
    # If not found, use default relative paths
    path_to_env = find_dotenv(".env.relative_example")

env = dotenv_values(path_to_env)
data_dir = Path(env['DATA_DIR'])
output_dir = Path(env['OUTPUT_DIR'])

if __name__ == "__main__":
    pass
    
