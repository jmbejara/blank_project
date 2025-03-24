"""Load project configurations from .env files or from the command line.

Provides easy access to paths and credentials used in the project.
Meant to be used as an imported module.

If `settings.py` is run on its own, it will create the appropriate
directories.

For information about the rationale behind decouple and this module,
see https://pypi.org/project/python-decouple/

Note that decouple mentions that it will help to ensure that
the project has "only one configuration module to rule all your instances."
This is achieved by putting all the configuration into the `.env` file.
You can have different sets of variables for difference instances,
such as `.env.development` or `.env.production`. You would only
need to copy over the settings from one into `.env` to switch
over to the other configuration, for example.


Example
-------
Create a file called `myexample.py` with the following content:
```
from settings import config
DATA_DIR = config("DATA_DIR")

print(f"Using DATA_DIR: {DATA_DIR}")
```
and run
```
>>> python myexample.py --DATA_DIR=/path/to/data
/path/to/data
```
and compare to
```
>>> export DATA_DIR=/path/to/other
>>> python myexample.py
/path/to/other
```

"""

import sys
from pathlib import Path
from platform import system

import pandas as pd
from decouple import config as _config


def find_all_caps_cli_vars(argv=sys.argv):
    """Find all command line arguments that are all caps.

    Find all command line arguments that are all caps and defined
    with a long option, for example, --DATA_DIR or --MANUAL_DATA_DIR.
    When that option is found, the value of the option is returned.

    For example, if the command line is:
    ```
    python settings.py --DATA_DIR=/path/to/data --MANUAL_DATA_DIR=/path/to/manual_data
    ```
    Then the function will return:
    ```
    {'DATA_DIR': '/path/to/data', 'MANUAL_DATA_DIR': '/path/to/manual_data'}
    ```

    For example:
    ```
    >>> argv = [
        '/opt/homebrew/Caskroom/mambaforge/base/envs/ftsf/lib/python3.12/site-packages/ipykernel_launcher.py',
        '--f=/Users/jbejarano/Library/Jupyter/runtime/kernel-v37ea18e94713e364855d5610175b766ee99909eab.json',
        '--DATA_DIR=/path/to/data',
        '--MANUAL_DATA_DIR=/path/to/manual_data'
    ]
    >>> cli_vars = find_all_caps_cli_vars(argv)
    >>> cli_vars
    {'DATA_DIR': '/path/to/data', 'MANUAL_DATA_DIR': '/path/to/manual_data'}
    ```
    """
    result = {}
    i = 0
    while i < len(argv):
        arg = argv[i]
        # Handle --VAR=value format
        if arg.startswith("--") and "=" in arg and arg[2:].split("=")[0].isupper():
            var_name, value = arg[2:].split("=", 1)
            result[var_name] = value
        # Handle --VAR value format (where value is the next argument)
        elif arg.startswith("--") and arg[2:].isupper() and i + 1 < len(argv):
            var_name = arg[2:]
            value = argv[i + 1]
            # Only use this value if it doesn't look like another option
            if not value.startswith("--"):
                result[var_name] = value
                i += 1  # Skip the next argument since we used it as a value
        i += 1
    return result


cli_vars = find_all_caps_cli_vars()

########################################################
## Define defaults
########################################################
defaults = {}

# Absolute path to root directory of the project
if "BASE_DIR" in cli_vars:
    defaults["BASE_DIR"] = Path(cli_vars["BASE_DIR"])
else:
    defaults["BASE_DIR"] = Path(__file__).absolute().parent.parent


# OS type
def get_os():
    os_name = system()
    if os_name == "Windows":
        return "windows"
    elif os_name == "Darwin":
        return "nix"
    elif os_name == "Linux":
        return "nix"
    else:
        return "unknown"


if "OS_TYPE" in cli_vars:
    defaults["OS_TYPE"] = cli_vars["OS_TYPE"]
else:
    defaults["OS_TYPE"] = get_os()


## Stata executable
def get_stata_exe():
    """Get the name of the Stata executable based on the OS type."""
    if defaults["OS_TYPE"] == "windows":
        return "StataMP-64.exe"
    elif defaults["OS_TYPE"] == "nix":
        return "stata-mp"
    else:
        raise ValueError("Unknown OS type")


if "STATA_EXE" in cli_vars:
    defaults["STATA_EXE"] = cli_vars["STATA_EXE"]
else:
    defaults["STATA_EXE"] = get_stata_exe()

## Dates
defaults["START_DATE"] = pd.to_datetime("1913-01-01")
defaults["END_DATE"] = pd.to_datetime("2024-12-31")


## File paths
def if_relative_make_abs(path):
    """If a relative path is given, make it absolute, assuming
    that it is relative to the project root directory (BASE_DIR)

    Example
    -------
    ```
    >>> if_relative_make_abs(Path('_data'))
    WindowsPath('C:/Users/jdoe/GitRepositories/blank_project/_data')

    >>> if_relative_make_abs(Path("C:/Users/jdoe/GitRepositories/blank_project/_output"))
    WindowsPath('C:/Users/jdoe/GitRepositories/blank_project/_output')
    ```
    """
    path = Path(path)
    if path.is_absolute():
        abs_path = path.resolve()
    else:
        abs_path = (defaults["BASE_DIR"] / path).resolve()
    return abs_path


defaults = {
    "DATA_DIR": if_relative_make_abs(Path("_data")),
    "MANUAL_DATA_DIR": if_relative_make_abs(Path("data_manual")),
    "OUTPUT_DIR": if_relative_make_abs(Path("_output")),
    **defaults,
}


def config(
    var_name,
    default=None,
    cast=None,
    settings_py_defaults=defaults,
    cli_vars=cli_vars,
    convert_dir_vars_to_abs_path=True,
):
    """Config defines a variable that can be used in the project. The definition of variables follows
    an order of precedence:
    1. Command line arguments
    2. Environment variables
    3. Settings.py file
    4. Defaults defined in-line in the local file
    5. Error
    """

    # 1. Command line arguments (highest priority)
    if var_name in cli_vars and cli_vars[var_name] is not None:
        value = cli_vars[var_name]
        # Apply cast if provided
        if cast is not None:
            value = cast(value)
        if "DIR" in var_name and convert_dir_vars_to_abs_path:
            value = if_relative_make_abs(Path(value))
        return value

    # 2. Environment variables through decouple
    # Use decouple but with a sentinel default to detect if it was found
    env_sentinel = object()
    env_value = _config(var_name, default=env_sentinel)
    if env_value is not env_sentinel:
        # Found in environment
        if cast is not None:
            env_value = cast(env_value)
        if "DIR" in var_name and convert_dir_vars_to_abs_path:
            env_value = if_relative_make_abs(Path(env_value))
        return env_value

    # 3. Settings.py defaults dictionary
    if var_name in defaults:
        default_value = defaults[var_name]
        # If default_value is directly usable (not a dict with metadata)
        if cast is not None:
            default_value = cast(default_value)
        return default_value

    # 4. Use the default value provided in the local file. Error if not found
    return _config(var_name, default=default, cast=cast)


def create_directories():
    config("DATA_DIR").mkdir(parents=True, exist_ok=True)
    config("OUTPUT_DIR").mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    create_directories()
