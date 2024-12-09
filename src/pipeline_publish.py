"""
NOTES:

- Dataframe names must have no spaces, and must start with an alphabetic character.

"""

import json
import os
import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import Union

import jinja2
import polars as pl

import config

BASE_DIR = config.BASE_DIR
OUTPUT_DIR = config.OUTPUT_DIR
PIPELINE_DEV_MODE = config.PIPELINE_DEV_MODE
PIPELINE_THEME = config.PIPELINE_THEME
PUBLISH_DIR = config.PUBLISH_DIR
USER = config.USER

DOCS_BUILD_DIR = BASE_DIR / Path("_docs")


def validate_pipeline_json_path(path: Path) -> bool:
    """
    Validates that a pipeline.json file exists in the specified directory.
    """
    pipeline_json = path / "pipeline.json"
    if not pipeline_json.is_file():
        raise ValueError(f"No pipeline.json found in directory: {path}")
    return True


def resolve_path(path_input: Union[str, dict]) -> Path:
    """
    Resolves a path that can be either a direct path string or a dictionary
    of platform-specific paths.

    Parameters
    ----------
    path_input : Union[str, dict]
        Either a string representing a direct path, or a dictionary containing
        platform-specific paths with 'Windows' and/or 'Unix' keys

    Returns
    -------
    Path
        The resolved path appropriate for the current platform

    Raises
    ------
    ValueError
        If using a dict input and no valid path is found for the current platform

    Examples
    --------
    >>> resolve_path('/path/to/dir')  # Direct path
    PosixPath('/path/to/dir')
    >>> resolve_path({'Windows': 'C:/data', 'Unix': '/home/data'})  # Platform-specific
    WindowsPath('C:/data')  # or PosixPath('/home/data') depending on platform
    """
    result_path = None

    if isinstance(path_input, str):
        result_path = Path(path_input)
    else:
        # Handle dict case (platform-specific paths)
        import platform

        is_windows = platform.system().lower() == "windows"

        if is_windows and "Windows" in path_input:
            result_path = Path(path_input["Windows"])
        elif not is_windows and "Unix" in path_input:
            result_path = Path(path_input["Unix"])

        if result_path is None:
            raise ValueError(
                f"No valid path found for current platform ({platform.system()}). "
                f"Available paths: {list(path_input.keys())}"
            )

    return result_path


def read_specs(base_dir=BASE_DIR):
    """
    Read the pipeline specifications from a JSON file and process them.
    This will also handle imported pipeline specifications. It
    will also create a mapping of dataframe_id to linked chart_ids
    and a mapping of data

    Parameters
    ----------
    base_dir : Union[str, Path]
        The base directory where the pipeline.json file is located.

    Returns
    -------
    dict
        A dictionary containing the specifications for all pipelines,
        including linked charts for each dataframe and linked dataframes
        for each pipeline.
    """
    base_dir = Path(base_dir)  # Convert base_dir to a Path object
    with open(base_dir / "pipeline.json", "r") as file:
        specs = json.load(file)  # Load the JSON specifications

    for pipeline_id in specs:
        pipeline_specs = specs[pipeline_id]  # Get specs for the current pipeline
        source_last_modified_date = get_most_recent_pipeline_source_modification(
            base_dir
        )  # Get the last modified date
        pipeline_specs["source_last_modified_date"] = (
            source_last_modified_date.strftime("%Y-%m-%d %H:%M:%S")
        )  # Format and store the last modified date
        pipeline_specs["pipeline_base_dir"] = base_dir.resolve().as_posix()

        # Handle imported pipeline specifications if applicable
        if "import_from" in pipeline_specs:
            sub_base_dir = resolve_path(pipeline_specs["import_from"])
            validate_pipeline_json_path(sub_base_dir)
            sub_specs = read_specs(base_dir=sub_base_dir)  # Recursively read specs
            pipeline_specs = sub_specs[pipeline_id]  # Update with imported specs
            # Set the production directory
            pipeline_specs["pipeline_base_dir"] = sub_base_dir.resolve().as_posix()

            specs[pipeline_id] = pipeline_specs  # Update the main specs

        # Create a mapping of dataframe_id to linked chart_ids
        dataframe_to_charts = {
            dataframe_id: [] for dataframe_id in pipeline_specs["dataframes"]
        }  # Initialize mapping

        for chart_id in pipeline_specs["charts"]:
            chart_specs = pipeline_specs["charts"][
                chart_id
            ]  # Get specs for the current chart
            dataframe_id = chart_specs["dataframe_id"]  # Identify the linked dataframe
            if dataframe_id in dataframe_to_charts:
                dataframe_to_charts[dataframe_id].append(
                    chart_id
                )  # Link chart_id to dataframe_id

        # Update dataframe_specs with the linked charts
        for dataframe_id, chart_ids in dataframe_to_charts.items():
            pipeline_specs["dataframes"][dataframe_id]["linked_charts"] = (
                chart_ids  # Add linked charts
            )

    return specs  # Return the complete specifications


def get_sphinx_file_alignment_plan(base_dir=BASE_DIR, docs_build_dir=DOCS_BUILD_DIR):
    specs = read_specs(base_dir=base_dir)
    pipeline_ids = get_pipeline_id_list(specs)

    dataset_plan = {}
    chart_plan_download = {}
    chart_plan_static = {}
    download_chart_dir_download = Path(docs_build_dir) / "download_chart"
    download_chart_dir_static = Path(docs_build_dir) / "_static"

    download_dataframe_dir = Path(docs_build_dir) / "download_dataframe"
    download_chart_dir_download.mkdir(parents=True, exist_ok=True)
    download_dataframe_dir.mkdir(parents=True, exist_ok=True)
    download_chart_dir_static.mkdir(parents=True, exist_ok=True)

    for pipeline_id in pipeline_ids:
        pipeline_specs = specs[pipeline_id]
        pipeline_base_dir = Path(pipeline_specs["pipeline_base_dir"])

        for dataframe_id in pipeline_specs["dataframes"]:
            dataframe_specs = pipeline_specs["dataframes"][dataframe_id]

            path_to_parquet_data = Path(dataframe_specs["path_to_parquet_data"])
            file_path = pipeline_base_dir / path_to_parquet_data
            dataset_plan[file_path] = (
                download_dataframe_dir / f"{pipeline_id}_{dataframe_id}.parquet"
            )

            path_to_excel_data = Path(dataframe_specs["path_to_excel_data"])
            file_path = pipeline_base_dir / path_to_excel_data
            dataset_plan[file_path] = (
                download_dataframe_dir / f"{pipeline_id}_{dataframe_id}.xlsx"
            )

        for chart_id in pipeline_specs["charts"]:
            # Plan for copying HTML chart to download folder
            chart_specs = pipeline_specs["charts"][chart_id]
            path_to_html_chart = Path(chart_specs["path_to_html_chart"])
            file_path = pipeline_base_dir / path_to_html_chart
            chart_plan_download[file_path] = (
                download_chart_dir_download / f"{pipeline_id}_{chart_id}.html"
            )

            # Plan for copying HTML chart to _static folder for display
            chart_specs = pipeline_specs["charts"][chart_id]
            path_to_html_chart = Path(chart_specs["path_to_html_chart"])
            file_path = pipeline_base_dir / path_to_html_chart
            chart_plan_static[file_path] = (
                download_chart_dir_static / f"{pipeline_id}_{chart_id}.html"
            )

    return dataset_plan, chart_plan_download, chart_plan_static


def copy_according_to_plan(publish_plan, mkdir=False):
    """
    Copies files from source paths to destination paths as specified in the publish_plan.

    Params
    ------
    publish_plan: dict
        A dictionary where keys are source file paths and values are destination file paths.
    """
    for source, destination in publish_plan.items():
        # Ensure both source and destination are Path objects
        source_path = Path(source)
        destination_path = Path(destination)

        # Create parent directories if needed
        if mkdir:
            destination_path.parent.mkdir(parents=True, exist_ok=True)

        # Copy the file content only, without attempting to copy permissions
        shutil.copyfile(source_path, destination_path)

        # Try to set reasonable permissions after copying
        try:
            os.chmod(destination_path, 0o644)  # rw-r--r-- for files
        except (OSError, PermissionError):
            # If we can't set permissions, just continue
            pass


def get_pipeline_id_list(specs):
    pipelines = [pipeline for pipeline in specs]
    return pipelines


def generate_all_pipeline_docs(
    specs,
    docs_build_dir=DOCS_BUILD_DIR,
    base_dir=BASE_DIR,
):
    """
    Params
    ------
    specs: dict
        This is a dict that contains specs for all pipelines to be processed.
    docs_build_dir: Path
        This is the output directory, where all generated docs will be placed.
    base_dir: Path
        This is used to identify the inputs. It's the base directory of the current project.
        This is used to tell
        the docs builder where all templates are stored, since the pipeline requires
        that they be stored in a consistent spot relative to the base directory
        of the project.
    """
    pipeline_ids = get_pipeline_id_list(specs)

    for pipeline_id in pipeline_ids:
        pipeline_specs = specs[pipeline_id]
        pipeline_base_dir = Path(pipeline_specs["pipeline_base_dir"])

        generate_pipeline_docs(
            pipeline_id,
            pipeline_specs,
            pipeline_base_dir=pipeline_base_dir,
            docs_build_dir=docs_build_dir,
            base_dir=base_dir,
        )
        if PIPELINE_THEME == "chart_book":
            # Copy pipeline README to pipelines directory
            pipeline_readme_dir = docs_build_dir / "pipelines"
            pipeline_readme_dir.mkdir(parents=True, exist_ok=True)

            source_path = pipeline_base_dir / "README.md"
            with open(source_path, "r") as file:
                readme_content = file.readlines()

            # Remove the first two lines, add line with link to pipeline GitHub repo and
            # to index.html in html build dir, and then join the rest of the README.
            pipeline_name = pipeline_specs["pipeline_name"]
            git_repo_URL = pipeline_specs["git_repo_URL"]
            readme_text = f"# `{pipeline_id}` {pipeline_name} \n\n " + (
                f'Pipeline GitHub Repo <a href="{git_repo_URL}">{git_repo_URL}.</a>\n\n\n'
                + f'Pipeline Web Page <a href="{git_repo_URL}">{git_repo_URL}.</a>\n\n\n'
                + "".join(readme_content[2:])
            )

            readme_destination_filepath = (
                pipeline_readme_dir / f"{pipeline_id}_README.md"
            )
            file_path = readme_destination_filepath
            with open(file_path, mode="w", encoding="utf-8") as file:
                file.write(readme_text)

    ## Dataframe and Pipeline List in index.md
    table_file_map = get_dataframes_and_dataframe_docs(base_dir=base_dir)
    dataframe_file_list = list(table_file_map.values())
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(base_dir))

    if PIPELINE_THEME == "chart_book":
        # Render dataframe.md
        template = environment.get_template("docs_src/dataframes.md")
        rendered_page = template.render(
            dataframe_file_list=dataframe_file_list,
        )
        # Copy to build directory
        file_path = docs_build_dir / "dataframes.md"
        with open(file_path, mode="w", encoding="utf-8") as file:
            file.write(rendered_page)

        # Render dataframe.md
        template = environment.get_template("docs_src/pipelines.md")
        rendered_page = template.render(specs=specs, dot_or_dotdot="..")
        # Copy to build directory
        file_path = docs_build_dir / "pipelines.md"
        with open(file_path, mode="w", encoding="utf-8") as file:
            file.write(rendered_page)

        readme_text = ""

        # Render and copy index.md in chart base theme
        template = environment.get_template("docs_src/index.md")
        index_page = template.render(
            specs=specs,
            dataframe_file_list=dataframe_file_list,
            pipeline_specs=pipeline_specs,
            readme_text=readme_text,
            pipeline_page_link=f"./pipelines/{pipeline_id}_README.md",
            dot_or_dotdot=".",
        )
        file_path = docs_build_dir / "index.md"
        with open(file_path, mode="w", encoding="utf-8") as file:
            file.write(index_page)

    elif PIPELINE_THEME == "pipeline":
        source_path = base_dir / "README.md"
        with open(source_path, "r") as file:
            readme_content = file.readlines()

        # Remove the first two lines and join the rest
        readme_text = "".join(readme_content[2:])

        # Render and copy index.md in pipeline themes
        template = environment.get_template("docs_src/index.md")
        index_page = template.render(
            specs=specs,
            dataframe_file_list=dataframe_file_list,
            pipeline_specs=pipeline_specs,
            readme_text=readme_text,
            pipeline_page_link="./index.md",
            dot_or_dotdot=".",
        )
        file_path = docs_build_dir / "index.md"
        with open(file_path, mode="w", encoding="utf-8") as file:
            file.write(index_page)

    else:
        raise ValueError("Invalid Pipeline theme")

    pass


def generate_pipeline_docs(
    pipeline_id,
    pipeline_specs,
    pipeline_base_dir=BASE_DIR,
    docs_build_dir=DOCS_BUILD_DIR,
    base_dir=BASE_DIR,
):
    for dataframe_id in pipeline_specs["dataframes"]:
        generate_dataframe_docs(
            dataframe_id,
            pipeline_id,
            pipeline_specs,
            docs_build_dir,
            pipeline_base_dir=pipeline_base_dir,
        )

    for chart_id in pipeline_specs["charts"]:
        generate_chart_docs(
            chart_id,
            pipeline_id,
            pipeline_specs,
            docs_build_dir,
            pipeline_base_dir=pipeline_base_dir,
        )

    pass


def generate_dataframe_docs(
    dataframe_id,
    pipeline_id,
    pipeline_specs,
    docs_build_dir,
    pipeline_base_dir=BASE_DIR,
):
    """
    Generates documentation for a specific dataframe, including the most recent data dates.

    Params
    ------
    dataframe_id: str
        The identifier for the dataframe.
    pipeline_id: str
        The identifier for the pipeline.
    pipeline_specs: dict
        Specifications for the pipeline.
    docs_build_dir: Path
        The directory where the docs will be built.
    base_dir: Path
        The base directory of the pipeline project folder.
    """
    pipeline_base_dir = Path(pipeline_base_dir)
    dataframe_specs = pipeline_specs["dataframes"][dataframe_id]

    path_to_dataframe_doc = Path(dataframe_specs["path_to_dataframe_doc"]).as_posix()
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(pipeline_base_dir))
    template = environment.get_template(path_to_dataframe_doc)
    # The name of the date column in the parquet file (default: "date").
    date_col = dataframe_specs["date_col"]

    if PIPELINE_THEME == "pipeline":
        pipeline_page_link = "../index.md"
        dataframe_path_prefix = "../dataframes/"
    elif PIPELINE_THEME == "chart_book":
        pipeline_page_link = f"../pipelines/{pipeline_id}_README.md"
        dataframe_path_prefix = ""
    else:
        raise ValueError("Invalid Pipeline theme")
    link_to_dataframe_docs = (
        Path(dataframe_path_prefix) / f"{pipeline_id}_{dataframe_id}.md"
    ).as_posix()
    # Compute the absolute path to the parquet file
    parquet_path = (
        pipeline_base_dir / dataframe_specs["path_to_parquet_data"]
    ).resolve()

    # Process the parquet file and get the min and max dates
    most_recent_data_min, most_recent_data_max = find_most_recent_valid_datapoints(
        parquet_path, date_col
    )

    # Render the template with the new variables
    table_page = template.render(
        dataframe_specs,
        dataframe_specs=dataframe_specs,
        link_to_dataframe_docs=link_to_dataframe_docs,
        dataframe_id=dataframe_id,
        pipeline_id=pipeline_id,
        pipeline_specs=pipeline_specs,
        pipeline_page_link=pipeline_page_link,
        most_recent_data_min=most_recent_data_min,
        most_recent_data_max=most_recent_data_max,
        dot_or_dotdot="..",
    )
    # print(table_page)

    (docs_build_dir / "dataframes").mkdir(parents=True, exist_ok=True)
    filename = f"{pipeline_id}_{dataframe_id}.md"
    file_path = docs_build_dir / "dataframes" / filename
    with open(file_path, mode="w", encoding="utf-8") as file:
        file.write(table_page)


def find_most_recent_valid_datapoints(parquet_path, date_col="date"):
    """
    date_col:
        The name of the date column in the parquet file (default: "date").
    """
    # Read the parquet file using Polars
    df = pl.read_parquet(parquet_path)

    # Ensure date_col is of datetime type for proper comparison
    if df[date_col].dtype != pl.Datetime:
        df = df.with_columns(pl.col(date_col).cast(pl.Datetime, strict=False))

    # Compute the most recent date where each column is not null
    most_recent_dates = df.select(
        [
            pl.col(date_col).filter(pl.col(col).is_not_null()).max().alias(col)
            for col in df.columns
            if col != date_col
        ]
    )

    # Extract the dates and filter out None values
    dates_list = [date for date in most_recent_dates.row(0) if date is not None]

    # Compute min and max dates
    if dates_list:
        most_recent_data_min = min(dates_list).strftime("%Y-%m-%d %H:%M:%S")
        most_recent_data_max = max(dates_list).strftime("%Y-%m-%d %H:%M:%S")
    else:
        most_recent_data_min = "N/A"
        most_recent_data_max = "N/A"

    return most_recent_data_min, most_recent_data_max


def generate_chart_docs(
    chart_id,
    pipeline_id,
    pipeline_specs,
    docs_build_dir,
    pipeline_base_dir=BASE_DIR,
):
    pipeline_base_dir = Path(pipeline_base_dir)

    # Get all specs related to the chart
    chart_specs = pipeline_specs["charts"][chart_id]
    dataframe_id = chart_specs["dataframe_id"]
    dataframe_specs = pipeline_specs["dataframes"][dataframe_id]

    path_to_chart_doc = Path(chart_specs["path_to_chart_doc"]).as_posix()
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(pipeline_base_dir))
    template = environment.get_template(path_to_chart_doc)

    if PIPELINE_THEME == "pipeline":
        pipeline_page_link = "../index.md"
        dataframe_path_prefix = "../dataframes/"
    elif PIPELINE_THEME == "chart_book":
        pipeline_page_link = f"../pipelines/{pipeline_id}_README.md"
        dataframe_path_prefix = "../dataframes/"
    else:
        raise ValueError("Invalid Pipeline theme")

    # Compute the absolute path to the parquet file
    parquet_path = (
        pipeline_base_dir / dataframe_specs["path_to_parquet_data"]
    ).resolve()

    # Fetch the last modified datetime of the parquet file
    dataframe_last_updated = get_last_modified_datetime(parquet_path)

    # Get and format paths to charts
    path_to_html_chart_unix = pipeline_base_dir / Path(
        chart_specs["path_to_html_chart"]
    )

    link_to_dataframe_docs = (
        Path(dataframe_path_prefix) / f"{pipeline_id}_{dataframe_id}.md"
    ).as_posix()

    # Render chart page
    chart_page = template.render(
        chart_specs,
        chart_specs=chart_specs,
        chart_id=chart_id,
        dataframe_id=dataframe_id,
        dataframe_specs=dataframe_specs,
        link_to_dataframe_docs=link_to_dataframe_docs,
        pipeline_id=pipeline_id,
        pipeline_specs=pipeline_specs,
        path_to_html_chart_unix=path_to_html_chart_unix,
        pipeline_page_link=pipeline_page_link,
        dataframe_last_updated=dataframe_last_updated.strftime("%Y-%m-%d %H:%M:%S"),
        dot_or_dotdot="..",
    )
    # print(chart_page)

    (docs_build_dir / "charts").mkdir(parents=True, exist_ok=True)
    filename = f"{pipeline_id}_{chart_id}.md"
    file_path = docs_build_dir / "charts" / filename
    with open(file_path, mode="w", encoding="utf-8") as file:
        file.write(chart_page)


def _get(base_dir=BASE_DIR, dep_or_target="dep", pipeline_dev_mode=True):
    specs = read_specs(base_dir=base_dir)
    pipeline_ids = get_pipeline_id_list(specs)
    file_list = []
    for pipeline_id in pipeline_ids:
        pipeline_specs = specs[pipeline_id]
        pipeline_base_dir = Path(pipeline_specs["pipeline_base_dir"])

        for dataframe_id in pipeline_specs["dataframes"]:
            dataframe_specs = pipeline_specs["dataframes"][dataframe_id]
            if dep_or_target == "dep":
                file_path = pipeline_base_dir / dataframe_specs["path_to_dataframe_doc"]
            elif dep_or_target == "target":
                filename = f"{pipeline_id}_{dataframe_id}.md"
                file_path = base_dir / "_docs" / "dataframes" / filename
            else:
                raise ValueError
            file_list.append(file_path)
        for chart_id in pipeline_specs["charts"]:
            chart_specs = pipeline_specs["charts"][chart_id]
            if dep_or_target == "dep":
                file_path = pipeline_base_dir / chart_specs["path_to_chart_doc"]
            elif dep_or_target == "target":
                filename = f"{pipeline_id}_{chart_id}.md"
                file_path = base_dir / "_docs" / "charts" / filename
            else:
                raise ValueError
            file_list.append(file_path)
    return file_list


def get_file_deps(base_dir=BASE_DIR, pipeline_dev_mode=PIPELINE_DEV_MODE):
    file_deps = _get(
        base_dir=base_dir, dep_or_target="dep", pipeline_dev_mode=pipeline_dev_mode
    )
    return file_deps


def get_targets(base_dir=BASE_DIR):
    file_deps = _get(base_dir=base_dir, dep_or_target="target", pipeline_dev_mode=True)
    return file_deps


def get_dataframes_and_dataframe_docs(base_dir=BASE_DIR):
    specs = read_specs(base_dir=base_dir)
    pipeline_ids = get_pipeline_id_list(specs)
    table_file_map = {}
    for pipeline_id in pipeline_ids:
        pipeline_specs = specs[pipeline_id]
        for dataframe_id in pipeline_specs["dataframes"]:
            filename = Path(f"{pipeline_id}_{dataframe_id}.md")
            file_path = "dataframes" / filename
            pipeline_dataframe_id = f"{pipeline_id}_{dataframe_id}"
            table_file_map[pipeline_dataframe_id] = file_path.as_posix()
    return table_file_map


def get_last_modified_datetime(file_path: Union[Path, str]) -> datetime:
    """
    Returns the datetime that a file was last modified.

    Args:
        file_path (Union[Path, str]): A pathlib.Path object or a string representing the file path.

    Returns:
        datetime: A datetime object representing the last modification time.
    """
    file_path = Path(file_path)
    # Get the last modified time in seconds since the epoch
    mtime = os.path.getmtime(file_path)
    # Convert the time to a datetime object
    return datetime.fromtimestamp(mtime)


def get_most_recent_pipeline_source_modification(
    base_dir: Union[str, Path],
) -> datetime:
    base_dir = Path(base_dir)

    def get_latest_mod_time(directory: Path) -> datetime:
        latest_time = datetime.min
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = Path(root) / file
                mod_time = get_last_modified_datetime(file_path)
                if mod_time > latest_time:
                    latest_time = mod_time
        return latest_time

    # Get the most recent modification time in src directory
    src_latest = get_latest_mod_time(base_dir / "src")

    # Get modification times for dodo.py and pipeline.json
    dodo_time = get_last_modified_datetime(base_dir / "dodo.py")
    pipeline_time = get_last_modified_datetime(base_dir / "pipeline.json")
    docs_time = get_latest_mod_time(base_dir / "docs_src")

    # Return the most recent of all these times
    latest = max(src_latest, dodo_time, pipeline_time, docs_time)
    return latest


def _demo():
    specs = read_specs(base_dir=BASE_DIR)
    len(specs["charts"])
    len(specs["dataframes"])

    # Used for dodo.py
    file_deps = get_file_deps(base_dir=BASE_DIR)
    targets = get_targets(base_dir=BASE_DIR)

    # Used for injection into index.md
    table_file_map = get_dataframes_and_dataframe_docs(base_dir=BASE_DIR)

    # Used for moving files into download folder. Dict shows where files will be copied from and to
    dataset_plan, chart_plan_download, chart_plan_static = (
        get_sphinx_file_alignment_plan(base_dir=BASE_DIR, docs_build_dir=DOCS_BUILD_DIR)
    )
    publish_plan = dataset_plan | chart_plan_download
    list(publish_plan.keys())
    list(publish_plan.values())

    # Find date modified
    dt_modified = get_last_modified_datetime("mydata.parquet")
    print(f"Last modified: {dt_modified}")


def get_pipeline_publishing_plan(specs, publish_dir=PUBLISH_DIR):
    pipeline_ids = get_pipeline_id_list(specs)
    publishing_plan = {}

    def _add_file_to_plan(base_dir, file_path):
        full_path = base_dir / file_path
        # Check if the file exists before adding it to the plan
        if full_path.exists():
            publishing_plan[full_path] = publish_dir / file_path

    for pipeline_id in pipeline_ids:
        pipeline_specs = specs[pipeline_id]
        pipeline_base_dir = Path(pipeline_specs["pipeline_base_dir"])

        # Add README and pipeline.json files
        _add_file_to_plan(pipeline_base_dir, pipeline_specs["README_file_path"])
        _add_file_to_plan(pipeline_base_dir, "pipeline.json")

        # Process dataframes
        for dataframe_id in pipeline_specs["dataframes"]:
            dataframe_specs = pipeline_specs["dataframes"][dataframe_id]

            _add_file_to_plan(
                pipeline_base_dir, dataframe_specs["path_to_parquet_data"]
            )
            _add_file_to_plan(pipeline_base_dir, dataframe_specs["path_to_excel_data"])
            _add_file_to_plan(
                pipeline_base_dir, dataframe_specs["path_to_dataframe_doc"]
            )

        # Process charts
        for chart_id in pipeline_specs["charts"]:
            chart_specs = pipeline_specs["charts"][chart_id]

            _add_file_to_plan(pipeline_base_dir, chart_specs["path_to_html_chart"])
            _add_file_to_plan(pipeline_base_dir, chart_specs["path_to_chart_doc"])

    return publishing_plan


def create_dodo_file_with_mod_date(date, dodo_path, publish_dir=PUBLISH_DIR):
    """
    Create a Python file named 'dodo.py' with specified content and set its
    modification date.

    Parameters
    ----------
    date : datetime.datetime
        The desired modification date for the file.
    dodo_path : str
        The path to the original dodo file to reference in the content.
    publish_dir : str, optional
        The directory where the 'dodo.py' file will be created. Default is
        defined by `PUBLISH_DIR`.

    Notes
    -----
    The function creates the specified directory if it does not exist. The
    content of the file will include a reference to the original file at
    `dodo_path`.

    Examples
    --------
    >>> mod_date = datetime.datetime(2023, 11, 20, 14, 0)  # Example date
    >>> create_dodo_file_with_mod_date(mod_date, "path/to/original/dodo.py")
    """

    # Define the filename and content
    filename = "dodo.py"
    content = f"## Contents censored. See original file here: {dodo_path}"

    # Create the publish directory if it doesn't exist
    Path(publish_dir).mkdir(parents=True, exist_ok=True)

    # Write the content to create the file
    file_path = Path(publish_dir) / filename
    with open(file_path, "w") as f:
        f.write(content)  # Write the specified content to the file

    # Convert the datetime object to a timestamp
    timestamp = time.mktime(date.timetuple())

    # Set the modification time of the file
    os.utime(file_path, (timestamp, timestamp))

    # print(f"File '{filename}' created in '{publish_dir}' with modification date set to {date}.")

def copy_publishable_pipeline_files(specs, base_dir, publish_dir, verbose=True):
    """
    Copy unaligned files to the publishing directory and Sphinx templates.

    Parameters
    ----------
    specs : dict
        Specifications for the files to be copied.
    base_dir : Path
        The base directory where source files are located.
    publish_dir : Path
        The directory where files will be published.
    verbose : bool, optional
        Whether to print messages about copied files. Default is True.
    """
    # Copy unaligned files to publishing directory
    pipeline_publishing_plan = get_pipeline_publishing_plan(
        specs, publish_dir=publish_dir
    )
    copy_according_to_plan(pipeline_publishing_plan, mkdir=True)
    if verbose:
        for src, dst in pipeline_publishing_plan.items():
            print(f"Copied to {dst}")

    src_modification_date = get_most_recent_pipeline_source_modification(
        base_dir=base_dir
    )
    create_dodo_file_with_mod_date(
        src_modification_date,
        dodo_path=base_dir / "dodo.py",
        publish_dir=publish_dir,
    )
    if verbose:
        print(f"Copied to {publish_dir}/dodo.py")

    # Copy Sphinx Templates
    source_dir = base_dir / Path("./docs_src/_templates")
    destination_dir = publish_dir / Path("./docs_src/_templates")

    # Create the destination directory and ensure it exists
    os.makedirs(destination_dir, exist_ok=True)

    # Manually copy each file instead of using copytree
    for item in os.listdir(source_dir):
        s = source_dir / item
        d = destination_dir / item
        if os.path.isfile(s):
            # Copy the file content only
            shutil.copyfile(s, d)
            if verbose:
                print(f"Copied to {d}")
            try:
                os.chmod(d, 0o644)  # Try to set reasonable permissions
            except (OSError, PermissionError):
                pass

if __name__ == "__main__":
    DOCS_BUILD_DIR.mkdir(parents=True, exist_ok=True)

    ## Align files for use by Sphinx
    specs = read_specs(base_dir=BASE_DIR)

    dataset_plan, chart_plan_download, chart_plan_static = (
        get_sphinx_file_alignment_plan(base_dir=BASE_DIR, docs_build_dir=DOCS_BUILD_DIR)
    )

    copy_according_to_plan(dataset_plan)
    copy_according_to_plan(chart_plan_download)
    copy_according_to_plan(chart_plan_static)

    generate_all_pipeline_docs(
        specs,
        docs_build_dir=DOCS_BUILD_DIR,
    )

    if PIPELINE_THEME == "pipeline":
        copy_publishable_pipeline_files(specs, BASE_DIR, PUBLISH_DIR)
