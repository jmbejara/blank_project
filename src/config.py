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
import pandas as pd

## Helper for determining OS
import platform


def get_os():
    os_name = platform.system()
    if os_name == "Windows":
        return "windows"
    elif os_name == "Darwin":
        return "nix"
    elif os_name == "Linux":
        return "nix"
    else:
        return "unknown"


OS_TYPE = get_os()

# fmt: off
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = (BASE_DIR / config('DATA_DIR', default=Path('data'), cast=Path)).resolve()
OUTPUT_DIR = (BASE_DIR / config('OUTPUT_DIR', default=Path('output'), cast=Path)).resolve()
DOCS_PUBLISH_DIR = (BASE_DIR / config('DOCS_PUBLISH_DIR', default=Path('docs'), cast=Path)).resolve()
WRDS_USERNAME = config("WRDS_USERNAME", default="")
START_DATE = config("START_DATE", default="1913-01-01", cast=pd.to_datetime)
END_DATE = config("END_DATE", default="2023-10-01", cast=pd.to_datetime)
# fmt: on

if OS_TYPE == "windows":
    STATA_EXE = config("STATA_EXE", default="StataMP-64.exe")
elif OS_TYPE == "nix":
    STATA_EXE = config("STATA_EXE", default="stata-mp")
else:
    raise ValueError("Unknown OS type")


if __name__ == "__main__":

    ## If they don't exist, create the data and output directories
    (DATA_DIR / "pulled").mkdir(parents=True, exist_ok=True)

    # Sometimes, I'll create other folders to organize the data
    # (DATA_DIR / 'intermediate').mkdir(parents=True, exist_ok=True)
    # (DATA_DIR / 'derived').mkdir(parents=True, exist_ok=True)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
