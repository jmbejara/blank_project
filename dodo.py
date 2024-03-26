"""Run or update the project. This file uses the `doit` Python package. It works
like a Makefile, but is Python-based
"""

#######################################
## Configuration and Helpers for PyDoit
#######################################

## Make sure the src folder is in the path
import sys

sys.path.insert(1, "./src/")

from os import getcwd

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
    # "cleanforget": True, # Doit will forget about tasks that have been cleaned.
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
# def task_pull_fred():
#     """ """
#     file_dep = [
#         "./src/load_bloomberg.py",
#         "./src/load_CRSP_Compustat.py",
#         "./src/load_CRSP_stock.py",
#         "./src/load_fed_yield_curve.py",
#         ]
#     file_output = [
#         "bloomberg.parquet",
#         "CRSP_Compustat.parquet",
#         "CRSP_stock.parquet",
#         "fed_yield_curve.parquet",
#         ]
#     targets = [DATA_DIR / "pulled" / file for file in file_output]

#     return {
#         "actions": [
#             "ipython ./src/load_bloomberg.py",
#             "ipython ./src/load_CRSP_Compustat.py",
#             "ipython ./src/load_CRSP_stock.py",
#             "ipython ./src/load_fed_yield_curve.py",
#         ],
#         "targets": targets,
#         "file_dep": file_dep,
#         "clean": [],  # Don't clean these files by default.
#     }


##################################################
# Demo for automated SQL pulls from another server
##################################################
# def task_pull_data_via_presto():
#     """
#     Run several data pulls

#     This will run commands like this:
#     presto-cli --output-format=CSV_HEADER --file=presto_something.sql > ../data/pulled/presto_something.csv

#     May need to do this first:

#     sed -ri "/^presto/d" ~/.ssh/known_hosts
#     ssh -t presto.YOURURL.edu "kinit jdoe@YOURURL.edu"


#     """
#     sql_pulls = [
#         'sql_something.sql',
#         'sql_something2.sql',
#     ]

#     def sql_action_to_csv_command(sql_file, csv_output):
#         s = f"""
#             ssh presto.YOURURL.edu <<-'ENDSSH'
#             echo Starting Presto Pull Command for {sql_file}
#             cd {getcwd()}
#             presto-cli --output-format=CSV_HEADER --file=./src/{sql_file} > {csv_output}
#             """
#         return s

#     stems = [file.split(".")[0] for file in sql_pulls]
#     for file in stems:
#         target = DATA_DIR / "pulled" / f"{file}.csv"
#         yield {
#             "name": f"{file}.sql",
#             "actions": [sql_action_to_csv_command(f"{file}.sql", target)],
#             "file_dep": [Path("./src") / f"{file}.sql"],
#             "targets": [target],
#             "clean": [],
#             # "verbosity": 0,
#         }


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
            "targets": [OUTPUT_DIR / f"_{notebook_name}.py"],
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
            # "verbosity": 1,
        }


def task_compile_latex_docs():
    """Compile the LaTeX documents to PDFs"""
    file_dep = [
        "./reports/report_example.tex",
        "./reports/slides_example.tex",
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
            # f"latexmk -xelatex -halt-on-error -cd -output-directory=../output/ ./reports/report_example.tex",  # Compile
            # f"latexmk -xelatex -halt-on-error -c -cd -output-directory=../output/ ./reports/report_example.tex",  # Clean
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


###############################################################
## Uncomment the task below if you have R installed. See README
###############################################################
# rmarkdown_tasks = {
#     "03_example_regressions.Rmd": {
#         "file_dep": ["./src/load_fred.py"],
#         "targets": [],
#     },
#     # "03_example_regressions.Rmd": {
#     #     "file_dep": ["./src/load_fred.py"],
#     #     "targets": [],
#     # },
# }


# def task_knit_RMarkdown_files():
#     """Preps the RMarkdown files for presentation format.
#     This will knit the RMarkdown files for easier sharing of results.
#     """
#     # def knit_string(file):
#     #     return f"""Rscript -e "library(rmarkdown); rmarkdown::render('./src/03_example_regressions.Rmd', output_format='html_document', output_dir='./output/')"""
#     str_output_dir = str(OUTPUT_DIR).replace("\\", "/")
#     def knit_string(file):
#         """
#         Properly escapes the quotes and concatenates so that this will run.
#         The single line version above was harder to get right because of weird
#         quotation escaping errors.

#         Example command:
#         Rscript -e "library(rmarkdown); rmarkdown::render('./src/03_example_regressions.Rmd', output_format='html_document', output_dir='./output/')
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
