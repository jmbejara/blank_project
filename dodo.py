"""Run or update the project. This file uses the `doit` Python package. It works
like a Makefile, but is Python-based
"""

#######################################
## Configuration and Helpers for PyDoit
#######################################

## Make sure the src folder is in the path
import sys

sys.path.insert(1, "./src/")

## Custom reporter: Print PyDoit Text in Green
# This is helpful because some tasks write to sterr and pollute the output in
# the console. I don't want to mute this output, because this can sometimes
# cause issues when, for example, LaTeX hangs on an error and requires
# presses on the keyboard before continuing. However, I want to be able
# to easily see the task lines printed by PyDoit. I want them to stand out
# from among all the other lines printed to the console.
from doit.reporter import ConsoleReporter
from colorama import Fore, Style, init


class GreenReporter(ConsoleReporter):
    def write(self, stuff, **kwargs):
        self.outstream.write(Fore.GREEN + stuff + Style.RESET_ALL)


DOIT_CONFIG = {
    "reporter": GreenReporter,
    # other config here...
}
init(autoreset=True)

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


os_type = get_os()

##################################
## Begin rest of PyDoit tasks here
##################################
import config
from pathlib import Path
from doit.tools import run_once

OUTPUT_DIR = Path(config.OUTPUT_DIR)
DATA_DIR = Path(config.DATA_DIR)


## Helpers for handling Jupyter Notebook tasks
# fmt: off
## Helper functions for automatic execution of Jupyter notebooks
def jupyter_execute_notebook(notebook):
    return f"jupyter nbconvert --execute --to notebook --ClearMetadataPreprocessor.enabled=True --inplace ./src/{notebook}.ipynb"
def jupyter_to_html(notebook, output_dir=OUTPUT_DIR):
    return f"jupyter nbconvert --to html --output-dir={output_dir} ./src/{notebook}.ipynb"
def jupyter_to_md(notebook, output_dir=OUTPUT_DIR):
    """Requires jupytext"""
    return f"jupytext --to markdown --output-dir={output_dir} ./src/{notebook}.ipynb"
def jupyter_to_python(notebook, build_dir):
    """Convert a notebook to a python script"""
    return f"jupyter nbconvert --to python ./src/{notebook}.ipynb --output _{notebook}.py --output-dir {build_dir}"
def jupyter_clear_output(notebook):
    return f"jupyter nbconvert --ClearOutputPreprocessor.enabled=True --ClearMetadataPreprocessor.enabled=True --inplace ./src/{notebook}.ipynb"
# fmt: on


def copy_notebook_to_folder(notebook_stem, origin_folder, destination_folder):
    origin_path = Path(origin_folder) / f"{notebook_stem}.ipynb"
    destination_folder = Path(destination_folder)
    destination_folder.mkdir(parents=True, exist_ok=True)
    destination_path = destination_folder / f"_{notebook_stem}.ipynb"
    if os_type == "nix":
        command = f"cp {origin_path} {destination_path}"
    else:
        command = f"copy  {origin_path} {destination_path}"
    return command


def task_pull_fred():
    """ """
    file_dep = ["./src/load_fred.py"]
    file_output = ["fred.parquet"]
    targets = [DATA_DIR / "pulled" / file for file in file_output]

    return {
        "actions": [
            "ipython ./src/load_fred.py",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }


# def task_pull_data_via_presto():
#     """
#     Run several data pulls

#     This will run commands like this:
#     presto-cli --output-format=CSV_HEADER --file=/data/unixhome/src/sql_gross_performance.sql > /data/unixhome/src/sometest.csv

#     """
#     sql_pulls_dict = {
#         'sometest.sql':'sometest.csv',
#     }
#     file_dep = list(sql_pulls_dict.keys())
#     file_output = list(sql_pulls_dict.values())

#     targets = [PRIVATE_DATA_DIR / 'sql_pulled' / file for file in file_output]

#     def action_string(sql_file, csv_output):
#         s = f"""
#             ssh sql.someurl.com <<-'ENDSSH'
#             echo Starting Presto Pull Command for {sql_file}
#             cd {getcwd()}
#             presto-cli --output-format=CSV_HEADER --file={sql_file} > {csv_output}
#             """
#         return s
#     actions = [
#                 action_string(sql_file,
#                               (PRIVATE_DATA_DIR / 'sql_pulled' / sql_pulls_dict[sql_file])
#                               ) for sql_file in sql_pulls_dict
#             ]
#     return {
#         "actions":actions,
#         "targets": targets,
#         'task_dep':[],
#         "file_dep": file_dep,
#     }


def task_summary_stats():
    """ """
    file_dep = ["./src/example_table.py"]
    file_output = [
        "example_table.tex",
        "pandas_to_latex_simple_table1.tex",
    ]
    targets = [OUTPUT_DIR / file for file in file_output]

    return {
        "actions": [
            "ipython ./src/example_table.py",
            "ipython ./src/pandas_to_latex_demo.py",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }


def task_example_plot():
    """Example plots"""
    file_dep = [Path("./src") / file for file in ["example_plot.py", "load_fred.py"]]
    file_output = ["example_plot.png"]
    targets = [OUTPUT_DIR / file for file in file_output]

    return {
        "actions": [
            "ipython ./src/example_plot.py",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }


notebook_tasks = {
    "01_example_notebook.ipynb": {
        "file_dep": ["./src/load_fred.py"],
        "targets": [Path(OUTPUT_DIR) / "GDP_graph.png"],
    },
    "02_interactive_plot_example.ipynb": {
        "file_dep": [],
        "targets": [],
    },
}


def task_convert_notebooks_to_scripts():
    """Convert notebooks to script form to detect changes to source code rather
    than to the notebook's metadata.
    """
    build_dir = Path(OUTPUT_DIR)
    build_dir.mkdir(parents=True, exist_ok=True)

    for notebook in notebook_tasks.keys():
        notebook_name = notebook.split(".")[0]
        yield {
            "name": notebook,
            "actions": [
                # jupyter_execute_notebook(notebook_name),
                # jupyter_to_html(notebook_name),
                # copy_notebook_to_folder(notebook_name, Path("./src"), "./docs/_notebook_build/"),
                jupyter_clear_output(notebook_name),
                jupyter_to_python(notebook_name, build_dir),
            ],
            "file_dep": [Path("./src") / notebook],
            "targets": [],
            "clean": True,
            "verbosity": 0,
        }


def task_run_notebooks():
    """Preps the notebooks for presentation format.
    Execute notebooks if the script version of it has been changed.
    """

    for notebook in notebook_tasks.keys():
        notebook_name = notebook.split(".")[0]
        yield {
            "name": notebook,
            "actions": [
                jupyter_execute_notebook(notebook_name),
                jupyter_to_html(notebook_name),
                copy_notebook_to_folder(
                    notebook_name, Path("./src"), "./docs/_notebook_build/"
                ),
                jupyter_clear_output(notebook_name),
                # jupyter_to_python(notebook_name, build_dir),
            ],
            "file_dep": [
                OUTPUT_DIR / f"_{notebook_name}.py",
                *notebook_tasks[notebook]["file_dep"],
            ],
            "targets": [
                OUTPUT_DIR / f"{notebook_name}.html",
                *notebook_tasks[notebook]["targets"],
            ],
            "clean": True,
            "verbosity": 0,
        }


def task_compile_latex_docs():
    """Compile the LaTeX documents to PDFs"""
    file_dep = [
        "./reports/report_example.tex",
        "./reports/slides_example.tex",
        "./src/example_plot.py",
        "./src/example_table.py",
    ]
    file_output = [
        "./reports/report_example.pdf",
        "./reports/slides_example.pdf",
    ]
    targets = [file for file in file_output]

    return {
        "actions": [
            "latexmk -xelatex -cd ./reports/report_example.tex",  # Compile
            "latexmk -xelatex -c -cd ./reports/report_example.tex",  # Clean
            "latexmk -xelatex -cd ./reports/slides_example.tex",  # Compile
            "latexmk -xelatex -c -cd ./reports/slides_example.tex",  # Clean
            # "latexmk -CA -cd ../reports/",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }


def task_compile_sphinx_docs():
    """Compile Sphinx Docs"""
    file_dep = [
        "./docs/conf.py",
        "./docs/index.rst",
        "./docs/myst_markdown_demos.md",
        "./docs/api.rst",
    ]
    targets = [
        "./docs/_build/html/index.html",
        "./docs/_build/html/myst_markdown_demos.html",
        "./docs/_build/html/api.html",
    ]

    return {
        "actions": ["sphinx-build -M html ./docs/ ./docs/_build"],
        "targets": targets,
        "file_dep": file_dep,
        "task_dep": ["run_notebooks"],
        "clean": True,
    }


# def task_knit_RMarkdown_files():
#     """Preps the RMarkdown files for presentation format.
#     This will knit the RMarkdown files for easier sharing of results.
#     """
#     files_to_knit = [
#         'shift_share.Rmd',
#         ]

#     files_to_knit_stems = [file.split('.')[0] for file in files_to_knit]

#     file_dep = [
#         'load_performance_and_loan_merged.py',
#         *[file + ".Rmd" for file in files_to_knit_stems],
#         ]

#     file_output = [file + '.html' for file in files_to_knit_stems]
#     targets = [OUTPUT_DIR / file for file in file_output]

#     def knit_string(file):
#         return f"""Rscript -e 'library(rmarkdown); rmarkdown::render("{file}.Rmd", output_format="html_document", OUTPUT_DIR="../output/")'"""
#     actions = [knit_string(file) for file in files_to_knit_stems]
#     return {
#         "actions": [
#                     "module use -a /opt/aws_opt/Modulefiles",
#                     "module load R/4.2.2",
#                     *actions],
#         "targets": targets,
#         'task_dep':[],
#         "file_dep": file_dep,
#     }
