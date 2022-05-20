"""Provides easy access to paths and credentials used in the project.
Meant to be used as an imported module.

Example
-------

import config
path = config.output_dir
path

## The config YAML should look something like this:
# config.yml

# Primary paths
data_dir: "C:/..."
private_data_dir:  # Left blank because not used
output_dir: "C:/..."

# Alternate paths
data_dir_alt:
output_dir_alt:
private_data_dir_alt:

"""
import yaml
from pathlib import Path
with open("../config.yml") as f:
    config = yaml.safe_load(f)

def _read_config_entry(key):
    entry = config[key]
    if entry is None:
        p = None
    else:
        p = Path(entry)
    return p

data_dir = _read_config_entry("data_dir")
output_dir = _read_config_entry("output_dir")
private_data_dir = _read_config_entry("private_data_dir")

def switch_to_alt():
    """Right now the default paths are on my local computer. The alternate
    paths are for when I'm doing some remote work on another server.
    This function allows you to interactively switch to the alternate.
    These are left blank for now.
    """
    global data_dir
    global output_dir
    global private_data_dir

    data_dir = _read_config_entry("data_dir_alt")
    output_dir = _read_config_entry("output_dir_alt")
    private_data_dir = _read_config_entry("private_data_dir_alt")
