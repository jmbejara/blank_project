"""Run or update the project. This file uses the `doit` Python package. It works
like a Makefile, but is Python-based

"""

#######################################
## Configuration and Helpers for PyDoit
#######################################
## Make sure the src folder is in the path
import sys

sys.path.insert(1, "./src/")

import shutil
from os import environ, getcwd, path
from pathlib import Path

from colorama import Fore, Style, init

## Custom reporter: Print PyDoit Text in Green
# This is helpful because some tasks write to sterr and pollute the output in
# the console. I don't want to mute this output, because this can sometimes
# cause issues when, for example, LaTeX hangs on an error and requires
# presses on the keyboard before continuing. However, I want to be able
# to easily see the task lines printed by PyDoit. I want them to stand out
# from among all the other lines printed to the console.
from doit.reporter import ConsoleReporter

from settings import config

try:
    in_slurm = environ["SLURM_JOB_ID"] is not None
except:
    in_slurm = False


class GreenReporter(ConsoleReporter):
    def write(self, stuff, **kwargs):
        doit_mark = stuff.split(" ")[0].ljust(2)
        task = " ".join(stuff.split(" ")[1:]).strip() + "\n"
        output = (
            Fore.GREEN
            + doit_mark
            + f" {path.basename(getcwd())}: "
            + task
            + Style.RESET_ALL
        )
        self.outstream.write(output)


if not in_slurm:
    DOIT_CONFIG = {
        "reporter": GreenReporter,
        # other config here...
        # "cleanforget": True, # Doit will forget about tasks that have been cleaned.
        "backend": "sqlite3",
        "dep_file": "./.doit-db.sqlite",
    }
else:
    DOIT_CONFIG = {"backend": "sqlite3", "dep_file": "./.doit-db.sqlite"}
init(autoreset=True)


BASE_DIR = config("BASE_DIR")
DATA_DIR = config("DATA_DIR")
MANUAL_DATA_DIR = config("MANUAL_DATA_DIR")
OUTPUT_DIR = config("OUTPUT_DIR")
OS_TYPE = config("OS_TYPE")
PUBLISH_DIR = config("PUBLISH_DIR")
USER = config("USER")

## Helpers for handling Jupyter Notebook tasks
# fmt: off
## Helper functions for automatic execution of Jupyter notebooks
environ["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"
def jupyter_execute_notebook(notebook):
    return f"jupyter nbconvert --execute --to notebook --ClearMetadataPreprocessor.enabled=True --log-level WARN --inplace ./src/{notebook}.ipynb"
def jupyter_to_html(notebook, output_dir=OUTPUT_DIR):
    return f"jupyter nbconvert --to html --log-level WARN --output-dir={output_dir} ./src/{notebook}.ipynb"
def jupyter_to_md(notebook, output_dir=OUTPUT_DIR):
    """Requires jupytext"""
    return f"jupytext --to markdown --log-level WARN --output-dir={output_dir} ./src/{notebook}.ipynb"
def jupyter_to_python(notebook, build_dir):
    """Convert a notebook to a python script"""
    return f"jupyter nbconvert --log-level WARN --to python ./src/{notebook}.ipynb --output _{notebook}.py --output-dir {build_dir}"
def jupyter_clear_output(notebook):
    return f"jupyter nbconvert --log-level WARN --ClearOutputPreprocessor.enabled=True --ClearMetadataPreprocessor.enabled=True --inplace ./src/{notebook}.ipynb"
# fmt: on


def copy_file(origin_path, destination_path, mkdir=True):
    """Create a Python action for copying a file."""

    def _copy_file():
        origin = Path(origin_path)
        dest = Path(destination_path)
        if mkdir:
            dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origin, dest)

    return _copy_file


##################################
## Begin rest of PyDoit tasks here
##################################


def task_config():
    """Create empty directories for data and output if they don't exist"""
    return {
        "actions": ["ipython ./src/settings.py"],
        "targets": [DATA_DIR, OUTPUT_DIR],
        "file_dep": ["./src/settings.py"],
        "clean": [],
    }


def task_pull_fred():
    """ """
    file_dep = [
        "./src/settings.py",
        "./src/pull_fred.py",
        "./src/pull_ofr_api_data.py",
    ]
    targets = [
        DATA_DIR / "fred.parquet",
        DATA_DIR / "ofr_public_repo_data.parquet",
    ]

    return {
        "actions": [
            "ipython ./src/settings.py",
            "ipython ./src/pull_fred.py",
            "ipython ./src/pull_ofr_api_data.py",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": [],  # Don't clean these files by default. The ideas
        # is that a data pull might be expensive, so we don't want to
        # redo it unless we really mean it. So, when you run
        # doit clean, all other tasks will have their targets
        # cleaned and will thus be rerun the next time you call doit.
        # But this one wont.
        # Use doit forget --all to redo all tasks. Use doit clean
        # to clean and forget the cheaper tasks.
    }


##############################$
## Demo: Other misc. data pulls
##############################$
# def task_pull_other():
#     """ """
#     file_dep = [
#         "./src/pull_bloomberg.py",
#         "./src/pull_CRSP_Compustat.py",
#         "./src/pull_CRSP_stock.py",
#         "./src/pull_fed_yield_curve.py",
#         ]
#     file_output = [
#         "bloomberg.parquet",
#         "CRSP_Compustat.parquet",
#         "CRSP_stock.parquet",
#         "fed_yield_curve.parquet",
#         ]
#     targets = [DATA_DIR / file for file in file_output]

#     return {
#         "actions": [
#             "ipython ./src/pull_bloomberg.py",
#             "ipython ./src/pull_CRSP_Compustat.py",
#             "ipython ./src/pull_CRSP_stock.py",
#             "ipython ./src/pull_fed_yield_curve.py",
#         ],
#         "targets": targets,
#         "file_dep": file_dep,
#         "clean": [],  # Don't clean these files by default.
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
    file_dep = [Path("./src") / file for file in ["example_plot.py", "pull_fred.py"]]
    file_output = ["example_plot.png"]
    targets = [OUTPUT_DIR / file for file in file_output]

    return {
        "actions": [
            # "date 1>&2",
            # "time ipython ./src/example_plot.py",
            "ipython ./src/example_plot.py",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }


def task_chart_repo_rates():
    """Example charts for Chart Book"""
    file_dep = [
        "./src/pull_fred.py",
        "./src/chart_relative_repo_rates.py",
    ]
    targets = [
        DATA_DIR / "repo_public.parquet",
        DATA_DIR / "repo_public.xlsx",
        DATA_DIR / "repo_public_relative_fed.parquet",
        DATA_DIR / "repo_public_relative_fed.xlsx",
        OUTPUT_DIR / "repo_rates.html",
        OUTPUT_DIR / "repo_rates_normalized.html",
        OUTPUT_DIR / "repo_rates_normalized_w_balance_sheet.html",
    ]

    return {
        "actions": [
            # "date 1>&2",
            # "time ipython ./src/chart_relative_repo_rates.py",
            "ipython ./src/chart_relative_repo_rates.py",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }


notebook_tasks = {
    "01_example_notebook_interactive.ipynb": {
        "file_dep": [],
        "targets": [],
    },
    "02_example_with_dependencies.ipynb": {
        "file_dep": ["./src/pull_fred.py"],
        "targets": [Path(OUTPUT_DIR) / "GDP_graph.png"],
    },
    "03_public_repo_summary_charts.ipynb": {
        "file_dep": [
            "./src/pull_fred.py",
            "./src/pull_ofr_api_data.py",
            "./src/pull_public_repo_data.py",
        ],
        "targets": [
            OUTPUT_DIR / "repo_rate_spikes_and_relative_reserves_levels.png",
            OUTPUT_DIR / "rates_relative_to_midpoint.png",
        ],
    },
}


def task_convert_notebooks_to_scripts():
    """Convert notebooks to script form to detect changes to source code rather
    than to the notebook's metadata.
    """
    build_dir = Path(OUTPUT_DIR)

    for notebook in notebook_tasks.keys():
        notebook_name = notebook.split(".")[0]
        yield {
            "name": notebook,
            "actions": [
                jupyter_clear_output(notebook_name),
                jupyter_to_python(notebook_name, build_dir),
            ],
            "file_dep": [Path("./src") / notebook],
            "targets": [OUTPUT_DIR / f"_{notebook_name}.py"],
            "clean": True,
            "verbosity": 0,
        }


# fmt: off
def task_run_notebooks():
    """Preps the notebooks for presentation format.
    Execute notebooks if the script version of it has been changed.
    """
    for notebook in notebook_tasks.keys():
        notebook_name = notebook.split(".")[0]
        yield {
            "name": notebook,
            "actions": [
                """python -c "import sys; from datetime import datetime; print(f'Start """ + notebook + """: {datetime.now()}', file=sys.stderr)" """,
                jupyter_execute_notebook(notebook_name),
                jupyter_to_html(notebook_name),
                copy_file(
                    Path("./src") / f"{notebook_name}.ipynb",
                    OUTPUT_DIR / f"{notebook_name}.ipynb",
                    mkdir=True,
                ),
                jupyter_clear_output(notebook_name),
                # jupyter_to_python(notebook_name, build_dir),
                """python -c "import sys; from datetime import datetime; print(f'End """ + notebook + """: {datetime.now()}', file=sys.stderr)" """,
            ],
            "file_dep": [
                OUTPUT_DIR / f"_{notebook_name}.py",
                *notebook_tasks[notebook]["file_dep"],
            ],
            "targets": [
                OUTPUT_DIR / f"{notebook_name}.html",
                OUTPUT_DIR / f"{notebook_name}.ipynb",
                *notebook_tasks[notebook]["targets"],
            ],
            "clean": True,
        }
# fmt: on


# ###############################################################
# ## Task below is for LaTeX compilation
# ###############################################################


def task_compile_latex_docs():
    """Compile the LaTeX documents to PDFs"""
    file_dep = [
        "./reports/report_example.tex",
        "./reports/my_article_header.sty",
        "./reports/slides_example.tex",
        "./reports/my_beamer_header.sty",
        "./reports/my_common_header.sty",
        "./reports/report_simple_example.tex",
        "./reports/slides_simple_example.tex",
        "./src/example_plot.py",
        "./src/example_table.py",
    ]
    targets = [
        "./reports/report_example.pdf",
        "./reports/slides_example.pdf",
        "./reports/report_simple_example.pdf",
        "./reports/slides_simple_example.pdf",
    ]

    return {
        "actions": [
            # My custom LaTeX templates
            "latexmk -xelatex -halt-on-error -cd ./reports/report_example.tex",  # Compile
            "latexmk -xelatex -halt-on-error -c -cd ./reports/report_example.tex",  # Clean
            "latexmk -xelatex -halt-on-error -cd ./reports/slides_example.tex",  # Compile
            "latexmk -xelatex -halt-on-error -c -cd ./reports/slides_example.tex",  # Clean
            # Simple templates based on small adjustments to Overleaf templates
            "latexmk -xelatex -halt-on-error -cd ./reports/report_simple_example.tex",  # Compile
            "latexmk -xelatex -halt-on-error -c -cd ./reports/report_simple_example.tex",  # Clean
            "latexmk -xelatex -halt-on-error -cd ./reports/slides_simple_example.tex",  # Compile
            "latexmk -xelatex -halt-on-error -c -cd ./reports/slides_simple_example.tex",  # Clean
            #
            # Example of compiling and cleaning in another directory. This often fails, so I don't use it
            # f"latexmk -xelatex -halt-on-error -cd -output-directory=../_output/ ./reports/report_example.tex",  # Compile
            # f"latexmk -xelatex -halt-on-error -c -cd -output-directory=../_output/ ./reports/report_example.tex",  # Clean
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }

notebook_sphinx_pages = [
    "./docs/notebooks/EX_" + notebook.split(".")[0] + ".html"
    for notebook in notebook_tasks.keys()
]
sphinx_targets = [
    "./docs/index.html",
    "./docs/myst_markdown_demos.html",
    "./docs/apidocs/index.html",
    *notebook_sphinx_pages,
]

def task_compile_sphinx_docs():
    """Compile Sphinx Docs"""
    notebook_scripts = [
        OUTPUT_DIR / ("_" + notebook.split(".")[0] + ".py")
        for notebook in notebook_tasks.keys()
    ]
    file_dep = [
        "./README.md",
        "./pipeline.json",
        *notebook_scripts,
    ]

    return {
        "actions": [
            "chartbook generate -f",
        ],  # Use docs as build destination
        # "actions": ["sphinx-build -M html ./docs/ ./docs/_build"], # Previous standard organization
        "targets": sphinx_targets,
        "file_dep": file_dep,
        "task_dep": ["run_notebooks",],
        "clean": True,
    }


###############################################################
## Uncomment the task below if you have R installed. See README
###############################################################


# def task_install_r_packages():
#     """Example R plots"""
#     file_dep = [
#         "r_requirements.txt",
#         "./src/install_packages.R",
#     ]
#     targets = [OUTPUT_DIR / "R_packages_installed.txt"]

#     return {
#         "actions": [
#             "Rscript ./src/install_packages.R",
#         ],
#         "targets": targets,
#         "file_dep": file_dep,
#         "clean": True,
#     }


# def task_example_r_script():
#     """Example R plots"""
#     file_dep = [
#         "./src/pull_fred.py",
#         "./src/example_r_plot.R"
#     ]
#     targets = [
#         OUTPUT_DIR / "example_r_plot.png",
#     ]

#     return {
#         "actions": [
#             "Rscript ./src/example_r_plot.R",
#         ],
#         "targets": targets,
#         "file_dep": file_dep,
#         "task_dep": ["pull_fred"],
#         "clean": True,
#     }


# rmarkdown_tasks = {
#     "04_example_regressions.Rmd": {
#         "file_dep": ["./src/pull_fred.py"],
#         "targets": [],
#     },
#     # "04_example_regressions.Rmd": {
#     #     "file_dep": ["./src/pull_fred.py"],
#     #     "targets": [],
#     # },
# }


# def task_knit_RMarkdown_files():
#     """Preps the RMarkdown files for presentation format.
#     This will knit the RMarkdown files for easier sharing of results.
#     """
#     # def knit_string(file):
#     #     return f"""Rscript -e "library(rmarkdown); rmarkdown::render('./src/04_example_regressions.Rmd', output_format='html_document', output_dir='./_output/')"""
#     str_output_dir = str(OUTPUT_DIR).replace("\\", "/")
#     def knit_string(file):
#         """
#         Properly escapes the quotes and concatenates so that this will run.
#         The single line version above was harder to get right because of weird
#         quotation escaping errors.

#         Example command:
#         Rscript -e "library(rmarkdown); rmarkdown::render('./src/04_example_regressions.Rmd', output_format='html_document', output_dir='./_output/')
#         """
#         return (
#             "Rscript -e "
#             '"library(rmarkdown); '
#             f"rmarkdown::render('./src/{file}.Rmd', "
#             "output_format='html_document', "
#             f"output_dir='{str_output_dir}')\""
#         )

#     for notebook in rmarkdown_tasks.keys():
#         notebook_name = notebook.split(".")[0]
#         file_dep = [f"./src/{notebook}", *rmarkdown_tasks[notebook]["file_dep"]]
#         html_file = f"{notebook_name}.html"
#         targets = [f"{OUTPUT_DIR / html_file}", *rmarkdown_tasks[notebook]["targets"]]
#         actions = [
#             # "module use -a /opt/aws_opt/Modulefiles",
#             # "module load R/4.2.2",
#             knit_string(notebook_name)
#         ]

#         yield {
#             "name": notebook,
#             "actions": actions,
#             "file_dep": file_dep,
#             "targets": targets,
#             "clean": True,
#             # "verbosity": 1,
#         }


###################################################################
## Uncomment the task below if you have Stata installed. See README
###################################################################

# if OS_TYPE == "windows":
#     STATA_COMMAND = f"{config.STATA_EXE} /e"
# elif OS_TYPE == "nix":
#     STATA_COMMAND = f"{config.STATA_EXE} -b"
# else:
#     raise ValueError(f"OS_TYPE {OS_TYPE} is unknown")

# def task_example_stata_script():
#     """Example Stata plots

#     Make sure to run
#     ```
#     net install doenv, from(https://github.com/vikjam/doenv/raw/master/) replace
#     ```
#     first to install the doenv package: https://github.com/vikjam/doenv.
#     """
#     file_dep = [
#         "./src/pull_fred.py",
#         "./src/example_stata_plot.do",
#     ]
#     targets = [
#         OUTPUT_DIR / "example_stata_plot.png",
#     ]
#     return {
#         "actions": [
#             f"{STATA_COMMAND} do ./src/example_stata_plot.do",
#         ],
#         "targets": targets,
#         "file_dep": file_dep,
#         "task_dep": ["pull_fred"],
#         "clean": True,
#         "verbosity": 2,
#     }
