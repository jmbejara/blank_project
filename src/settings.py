"""Load project configurations from .env files.
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

"""

from pathlib import Path

## Helper for determining OS
from platform import system

from decouple import config as _config
from pandas import to_datetime


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
        abs_path = (d["BASE_DIR"] / path).resolve()
    return abs_path


d = {}

d["OS_TYPE"] = get_os()

# Absolute path to root directory of the project
d["BASE_DIR"] = Path(__file__).absolute().parent.parent

# fmt: off
## Other .env variables
d["START_DATE"] = _config("START_DATE", default="1965-01-29", cast=to_datetime)
d["END_DATE"] = _config("END_DATE", default="2022-12-31", cast=to_datetime)
d["PIPELINE_DEV_MODE"] = _config("PIPELINE_DEV_MODE", default=True, cast=bool)
d["PIPELINE_THEME"] = _config("PIPELINE_THEME", default="pipeline")

## Paths
d["DATA_DIR"] = if_relative_make_abs(_config('DATA_DIR', default=Path('_data'), cast=Path))
d["MANUAL_DATA_DIR"] = if_relative_make_abs(_config('MANUAL_DATA_DIR', default=Path('data_manual'), cast=Path))
d["OUTPUT_DIR"] = if_relative_make_abs(_config('OUTPUT_DIR', default=Path('_output'), cast=Path))
d["PUBLISH_DIR"] = if_relative_make_abs(_config('PUBLISH_DIR', default=Path('_output/publish'), cast=Path))
# fmt: on


## Name of Stata Executable in path
if d["OS_TYPE"] == "windows":
    d["STATA_EXE"] = _config("STATA_EXE", default="StataMP-64.exe")
elif d["OS_TYPE"] == "nix":
    d["STATA_EXE"] = _config("STATA_EXE", default="stata-mp")
else:
    raise ValueError("Unknown OS type")


def config(*args, **kwargs):
    key = args[0]
    default = kwargs.get("default", None)
    cast = kwargs.get("cast", None)
    if key in d:
        var = d[key]
        if default is not None:
            raise ValueError(
                f"Default for {key} already exists. Check your settings.py file."
            )
        if cast is not None:
            # Allows for re-emphasizing the type of the variable
            # But does not allow for changing the type of the variable
            # if the variable is defined in the settings.py file
            if type(cast(var)) is not type(var):
                raise ValueError(
                    f"Type for {key} is already set. Check your settings.py file."
                )
    else:
        # If the variable is not defined in the settings.py file,
        # then fall back to using decouple normally.
        var = _config(*args, **kwargs)
    return var


def create_dirs():
    ## If they don't exist, create the _data and _output directories
    d["DATA_DIR"].mkdir(parents=True, exist_ok=True)
    d["OUTPUT_DIR"].mkdir(parents=True, exist_ok=True)
    # (d["BASE_DIR"] / "_docs").mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    create_dirs()
