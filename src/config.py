"""Load project configurations from .env files.
Provides easy access to paths and credentials used in the project.
Meant to be used as an imported module.

If `config.py` is run on its own, it will create the appropriate
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

"""

from decouple import config
from pathlib import Path
from pandas import to_datetime

## Helper for determining OS
from platform import system


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


OS_TYPE = get_os()

# Absolute path to root directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

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
        abs_path = (BASE_DIR / path).resolve()
    return abs_path


# fmt: off
## Other .env variables
WRDS_USERNAME = config("WRDS_USERNAME", default="")
START_DATE = config("START_DATE", default="1913-01-01", cast=to_datetime)
END_DATE = config("END_DATE", default="2023-10-01", cast=to_datetime)
PIPELINE_DEV_MODE = config("PIPELINE_DEV_MODE", default=True, cast=bool)
PIPELINE_THEME = config("PIPELINE_THEME", default="pipeline")

## Paths
DATA_DIR = if_relative_make_abs(config('DATA_DIR', default=Path('_data'), cast=Path))
MANUAL_DATA_DIR = if_relative_make_abs(config('MANUAL_DATA_DIR', default=Path('data_manual'), cast=Path))
OUTPUT_DIR = if_relative_make_abs(config('OUTPUT_DIR', default=Path('_output'), cast=Path))
DOCS_PUBLISH_DIR = if_relative_make_abs(config('DOCS_PUBLISH_DIR', default=Path('docs'), cast=Path))
# fmt: on


## Name of Stata Executable in path
if OS_TYPE == "windows":
    STATA_EXE = config("STATA_EXE", default="StataMP-64.exe")
elif OS_TYPE == "nix":
    STATA_EXE = config("STATA_EXE", default="stata-mp")
else:
    raise ValueError("Unknown OS type")


if __name__ == "__main__":

    ## If they don't exist, create the _data and _output directories
    (DATA_DIR).mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "intermediate").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "scratch").mkdir(parents=True, exist_ok=True)

    # Sometimes, I'll create other folders to organize the data
    # (DATA_DIR / 'intermediate').mkdir(parents=True, exist_ok=True)
    # (DATA_DIR / 'derived').mkdir(parents=True, exist_ok=True)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "_docs").mkdir(parents=True, exist_ok=True)
