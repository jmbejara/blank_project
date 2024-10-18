"""
NOTES:

- Dataframe names must have no spaces, and must start with an alphabetic character.

"""

from datetime import date, datetime
from pathlib import Path
from typing import Union
import config
import jinja2
import json
import os
import shutil


BASE_DIR = config.BASE_DIR
OUTPUT_DIR = config.OUTPUT_DIR
PIPELINE_DEV_MODE = config.PIPELINE_DEV_MODE
PIPELINE_THEME = config.PIPELINE_THEME

DOCS_BUILD_DIR = BASE_DIR / Path("_docs")


def read_specs(base_dir=BASE_DIR):
    base_dir = Path(base_dir)
    with open(base_dir / "pipeline.json", "r") as file:
        specs = json.load(file)
    for pipeline_id in specs:
        pipeline_specs = specs[pipeline_id]
        source_last_modified_date = get_most_recent_pipeline_source_modification(
            base_dir
        )
        pipeline_specs["source_last_modified_date"] = (
            source_last_modified_date.strftime("%Y-%m-%d %H:%M:%S")
        )  # Format the date
        if "import_from" in pipeline_specs:
            sub_base_dir = Path(pipeline_specs["import_from"])
            sub_specs = read_specs(base_dir=sub_base_dir)
            pipeline_specs = sub_specs[pipeline_id]
            pipeline_specs["pipeline_prod_directory"] = (
                Path(sub_base_dir).resolve().as_posix()
            )
            specs[pipeline_id] = pipeline_specs
    return specs


def get_file_publish_plan(base_dir=BASE_DIR, pipeline_dev_mode=PIPELINE_DEV_MODE):
    specs = read_specs(base_dir=base_dir)
    pipeline_ids = get_pipeline_id_list(specs)

    dataset_plan = {}
    chart_plan_download = {}
    chart_plan_static = {}

    download_chart_dir_download = Path(DOCS_BUILD_DIR) / "download_chart"
    download_chart_dir_static = Path(DOCS_BUILD_DIR) / "_static"

    download_dataframe_dir = Path(DOCS_BUILD_DIR) / "download_dataframe"
    download_chart_dir_download.mkdir(parents=True, exist_ok=True)
    download_dataframe_dir.mkdir(parents=True, exist_ok=True)
    download_chart_dir_static.mkdir(parents=True, exist_ok=True)

    for pipeline_id in pipeline_ids:

        pipeline_specs = specs[pipeline_id]
        if pipeline_dev_mode:
            pipeline_specs["pipeline_prod_directory"] = BASE_DIR.as_posix()
        pipeline_prod_dir = Path(pipeline_specs["pipeline_prod_directory"])

        for dataframe_id in pipeline_specs["dataframes"]:
            dataframe_specs = pipeline_specs["dataframes"][dataframe_id]

            path_to_parquet_data = Path(dataframe_specs["path_to_parquet_data"])
            filepath = pipeline_prod_dir / path_to_parquet_data
            dataset_plan[filepath] = (
                download_dataframe_dir / f"{pipeline_id}_{dataframe_id}.parquet"
            )

            path_to_excel_data = Path(dataframe_specs["path_to_excel_data"])
            filepath = pipeline_prod_dir / path_to_excel_data
            dataset_plan[filepath] = (
                download_dataframe_dir / f"{pipeline_id}_{dataframe_id}.xlsx"
            )

        for chart_id in pipeline_specs["charts"]:
            # Plan for copying HTML chart to download folder
            chart_specs = pipeline_specs["charts"][chart_id]
            path_to_html_chart = Path(chart_specs["path_to_html_chart"])
            filepath = pipeline_prod_dir / path_to_html_chart
            chart_plan_download[filepath] = (
                download_chart_dir_download / f"{pipeline_id}_{chart_id}.html"
            )

            # Plan for copying HTML chart to _static folder for display
            chart_specs = pipeline_specs["charts"][chart_id]
            path_to_html_chart = Path(chart_specs["path_to_html_chart"])
            filepath = pipeline_prod_dir / path_to_html_chart
            chart_plan_static[filepath] = (
                download_chart_dir_static / f"{pipeline_id}_{chart_id}.html"
            )

            # Plan for copying Excel chart to download folder
            chart_specs = pipeline_specs["charts"][chart_id]
            path_to_excel_chart = Path(chart_specs["path_to_excel_chart"])
            filepath = pipeline_prod_dir / path_to_excel_chart
            chart_plan_download[filepath] = (
                download_chart_dir_download / f"{pipeline_id}_{chart_id}.xlsx"
            )

    return dataset_plan, chart_plan_download, chart_plan_static


def copy_according_to_publish_plan(publish_plan):
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

        # Copy the file from source to destination
        shutil.copy2(source_path, destination_path)


def get_pipeline_id_list(specs):
    pipelines = [pipeline for pipeline in specs]
    return pipelines


def generate_all_pipeline_docs(
    specs,
    docs_build_dir=DOCS_BUILD_DIR,
    pipeline_dev_mode=PIPELINE_DEV_MODE,
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
        if pipeline_dev_mode:
            pipeline_specs["pipeline_prod_directory"] = BASE_DIR.as_posix()
        pipeline_prod_dir = Path(pipeline_specs["pipeline_prod_directory"])
        generate_pipeline_docs(
            pipeline_id,
            pipeline_specs,
            docs_build_dir=docs_build_dir,
        )
        if PIPELINE_THEME == "chart_base":
            # Copy pipeline README to pipelines directory
            pipeline_readme_dir = docs_build_dir / "pipelines"
            pipeline_readme_dir.mkdir(parents=True, exist_ok=True)

            source_path = pipeline_prod_dir / "README.md"
            with open(source_path, "r") as file:
                readme_content = file.readlines()

            # Remove the first two lines and join the rest
            pipeline_name = pipeline_specs["pipeline_name"]
            readme_text = f"# `{pipeline_id}` {pipeline_name} \n\n " + (
                "".join(readme_content[2:])
            )

            readme_destination_filepath = (
                pipeline_readme_dir / f"{pipeline_id}_README.md"
            )
            filepath = readme_destination_filepath
            with open(filepath, mode="w", encoding="utf-8") as file:
                file.write(readme_text)

    ## Dataframe and Pipeline List in index.md
    table_file_map = get_dataframes_and_dataframe_docs(base_dir=BASE_DIR)
    dataframe_file_list = list(table_file_map.values())
    path_to_docs_src = BASE_DIR / "docs_src"
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(path_to_docs_src))

    if PIPELINE_THEME == "chart_base":
        # Render dataframe.md
        template = environment.get_template("dataframes.md")
        rendered_page = template.render(
            dataframe_file_list=dataframe_file_list,
        )
        # Copy to build directory
        filepath = docs_build_dir / "dataframes.md"
        with open(filepath, mode="w", encoding="utf-8") as file:
            file.write(rendered_page)

        # Render dataframe.md
        template = environment.get_template("pipelines.md")
        rendered_page = template.render(specs=specs)
        # Copy to build directory
        filepath = docs_build_dir / "pipelines.md"
        with open(filepath, mode="w", encoding="utf-8") as file:
            file.write(rendered_page)

        readme_text = ""

        # Render and copy index.md in Data Browser theme
        template = environment.get_template("index.md")
        index_page = template.render(
            specs=specs,
            dataframe_file_list=dataframe_file_list,
            pipeline_specs=pipeline_specs,
            readme_text=readme_text,
            pipeline_page_link=f"./pipelines/{pipeline_id}_README.md",
        )
        filepath = docs_build_dir / "index.md"
        with open(filepath, mode="w", encoding="utf-8") as file:
            file.write(index_page)

    elif PIPELINE_THEME == "pipeline":
        source_path = Path(pipeline_specs["pipeline_prod_directory"]) / "README.md"
        with open(source_path, "r") as file:
            readme_content = file.readlines()

        # Remove the first two lines and join the rest
        readme_text = "".join(readme_content[2:])

        # Render and copy index.md in pipeline themes
        template = environment.get_template("index.md")
        index_page = template.render(
            specs=specs,
            dataframe_file_list=dataframe_file_list,
            pipeline_specs=pipeline_specs,
            readme_text=readme_text,
            pipeline_page_link=f"./index.md",
        )
        filepath = docs_build_dir / "index.md"
        with open(filepath, mode="w", encoding="utf-8") as file:
            file.write(index_page)

    else:
        raise ValueError("Invalid Pipeline theme")

    pass


def generate_pipeline_docs(
    pipeline_id,
    pipeline_specs,
    docs_build_dir=DOCS_BUILD_DIR,
):
    pipeline_prod_directory = Path(pipeline_specs["pipeline_prod_directory"])
    for dataframe_id in pipeline_specs["dataframes"]:

        generate_dataframe_docs(
            dataframe_id,
            pipeline_id,
            pipeline_specs,
            docs_build_dir,
            base_dir=pipeline_prod_directory,
        )

    for chart_id in pipeline_specs["charts"]:
        generate_chart_docs(
            chart_id,
            pipeline_id,
            pipeline_specs,
            docs_build_dir,
            base_dir=pipeline_prod_directory,
        )

    pass


def generate_dataframe_docs(
    dataframe_id, pipeline_id, pipeline_specs, docs_build_dir, base_dir=BASE_DIR
):
    """
    Generates documentation for a specific dataframe, including the last updated timestamp.

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
        The base directory of the pipeline production.
    """
    path_to_docs_src = base_dir / "docs_src"
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(path_to_docs_src))
    template = environment.get_template(f"dataframes/{pipeline_id}_{dataframe_id}.md")
    dataframe_specs = pipeline_specs["dataframes"][dataframe_id]

    if PIPELINE_THEME == "pipeline":
        pipeline_page_link = f"../index.md"
    elif PIPELINE_THEME == "chart_base":
        pipeline_page_link = f"../pipelines/{pipeline_id}_README.md"
    else:
        raise ValueError("Invalid Pipeline theme")

    # Compute the absolute path to the parquet file
    parquet_path = (base_dir / dataframe_specs["path_to_parquet_data"]).resolve()

    # Fetch the last modified datetime of the parquet file
    dataframe_last_updated = get_last_modified_datetime(parquet_path)

    # Render the template with the additional "dataframe_last_updated" field
    table_page = template.render(
        dataframe_specs=dataframe_specs,
        dataframe_id=dataframe_id,
        pipeline_id=pipeline_id,
        pipeline_specs=pipeline_specs,
        pipeline_page_link=pipeline_page_link,
        dataframe_last_updated=dataframe_last_updated.strftime("%Y-%m-%d %H:%M:%S"),
    )

    (docs_build_dir / "dataframes").mkdir(parents=True, exist_ok=True)
    filename = f"{pipeline_id}_{dataframe_id}.md"
    filepath = docs_build_dir / "dataframes" / filename
    with open(filepath, mode="w", encoding="utf-8") as file:
        file.write(table_page)


def generate_chart_docs(
    chart_id, pipeline_id, pipeline_specs, docs_build_dir, base_dir=BASE_DIR
):
    path_to_docs_src = base_dir / "docs_src"
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(path_to_docs_src))
    template = environment.get_template(f"charts/{pipeline_id}_{chart_id}.md")

    # Get all specs related to the chart
    chart_specs = pipeline_specs["charts"][chart_id]
    dataframe_id = chart_specs["dataframe_id"]
    dataframe_specs = pipeline_specs["dataframes"][dataframe_id]

    if PIPELINE_THEME == "pipeline":
        pipeline_page_link = f"../index.md"
    elif PIPELINE_THEME == "chart_base":
        pipeline_page_link = f"../pipelines/{pipeline_id}_README.md"
    else:
        raise ValueError("Invalid Pipeline theme")

    # Compute the absolute path to the parquet file
    parquet_path = (base_dir / dataframe_specs["path_to_parquet_data"]).resolve()

    # Fetch the last modified datetime of the parquet file
    dataframe_last_updated = get_last_modified_datetime(parquet_path)

    # Get and format paths to charts
    path_to_html_chart_unix = base_dir / Path(chart_specs["path_to_html_chart"])

    # Render chart page
    chart_page = template.render(
        chart_specs=chart_specs,
        chart_id=chart_id,
        dataframe_id=dataframe_id,
        dataframe_specs=dataframe_specs,
        pipeline_id=pipeline_id,
        pipeline_specs=pipeline_specs,
        path_to_html_chart_unix=path_to_html_chart_unix,
        pipeline_page_link=pipeline_page_link,
        dataframe_last_updated=dataframe_last_updated.strftime("%Y-%m-%d %H:%M:%S"),
    )

    (docs_build_dir / "charts").mkdir(parents=True, exist_ok=True)
    filename = f"{pipeline_id}_{chart_id}.md"
    filepath = docs_build_dir / "charts" / filename
    with open(filepath, mode="w", encoding="utf-8") as file:
        file.write(chart_page)


def _get(base_dir=BASE_DIR, middle_dir="docs_src", pipeline_dev_mode=True):

    specs = read_specs(base_dir=base_dir)
    pipeline_ids = get_pipeline_id_list(specs)
    file_list = []
    for pipeline_id in pipeline_ids:

        pipeline_specs = specs[pipeline_id]
        if pipeline_dev_mode:
            pipeline_specs["pipeline_prod_directory"] = BASE_DIR.as_posix()
        pipeline_prod_dir = Path(pipeline_specs["pipeline_prod_directory"])

        for dataframe_id in pipeline_specs["dataframes"]:
            filename = Path(f"{pipeline_id}_{dataframe_id}.md")
            filepath = pipeline_prod_dir / middle_dir / "dataframes" / filename
            file_list.append(filepath)
        for chart_id in pipeline_specs["charts"]:
            filename = Path(f"{pipeline_id}_{chart_id}.md")
            filepath = pipeline_prod_dir / middle_dir / "charts" / filename
            file_list.append(filepath)
    return file_list


def get_file_deps(base_dir=BASE_DIR, pipeline_dev_mode=PIPELINE_DEV_MODE):
    file_deps = _get(
        base_dir=base_dir, middle_dir="docs_src", pipeline_dev_mode=pipeline_dev_mode
    )
    return file_deps


def get_targets(base_dir=BASE_DIR):
    file_deps = _get(base_dir=base_dir, middle_dir="_docs", pipeline_dev_mode=True)
    return file_deps


def get_dataframes_and_dataframe_docs(base_dir=BASE_DIR):
    specs = read_specs(base_dir=base_dir)
    pipeline_ids = get_pipeline_id_list(specs)
    table_file_map = {}
    for pipeline_id in pipeline_ids:
        pipeline_specs = specs[pipeline_id]
        for dataframe_id in pipeline_specs["dataframes"]:
            filename = Path(f"{pipeline_id}_{dataframe_id}.md")
            filepath = "dataframes" / filename
            pipeline_dataframe_id = f"{pipeline_id}_{dataframe_id}"
            table_file_map[pipeline_dataframe_id] = filepath.as_posix()
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
    base_dir: Union[str, Path]
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
    dataset_plan, chart_plan_download, chart_plan_static = get_file_publish_plan(
        base_dir=BASE_DIR, pipeline_dev_mode=PIPELINE_DEV_MODE
    )
    publish_plan = dataset_plan | chart_plan_download
    list(publish_plan.keys())
    list(publish_plan.values())

    # Find date modified
    dt_modified = get_last_modified_datetime("mydata.parquet")
    print(f"Last modified: {dt_modified}")


if __name__ == "__main__":

    DOCS_BUILD_DIR.mkdir(parents=True, exist_ok=True)

    specs = read_specs(base_dir=BASE_DIR)

    dataset_plan, chart_plan_download, chart_plan_static = get_file_publish_plan(
        base_dir=BASE_DIR, pipeline_dev_mode=PIPELINE_DEV_MODE
    )
    copy_according_to_publish_plan(dataset_plan)
    copy_according_to_publish_plan(chart_plan_download)
    copy_according_to_publish_plan(chart_plan_static)

    generate_all_pipeline_docs(
        specs,
        docs_build_dir=DOCS_BUILD_DIR,
        pipeline_dev_mode=PIPELINE_DEV_MODE,
    )
