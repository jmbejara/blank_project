"""Provides easy access to paths and credentials used in the project.
Meant to be used as an imported module.
"""
import yaml
from pathlib import Path

with open ('../config.yml') as f:
    config = yaml.safe_load(f)

data_dir = Path(config['data_dir'])
output_dir = Path(config['output_dir'])

def main():
    # Intentionally blank
    pass

if __name__ == '__main__':
    main()
