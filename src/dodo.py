"""Run or update the project. This file uses the `doit` Python package. It works
like a Makefile, but is Python-based
"""
import config
from pathlib import Path
from doit.tools import run_once

OUTPUT_DIR = Path(config.output_dir)
DATA_DIR = Path(config.data_dir)

## Helper functions for automatic execution of Jupyter notebooks
def jupyter_execute_notebook(notebook):
    return f"jupyter nbconvert --execute --to notebook --ClearMetadataPreprocessor.enabled=True --inplace {notebook}.ipynb"
def jupyter_to_html(notebook):
    return f"jupyter nbconvert --to html --output-dir='../output' {notebook}.ipynb"
def jupyter_to_md(notebook):
    """Requires jupytext"""
    return f"jupytext --to markdown {notebook}.ipynb"
def jupyter_to_python(notebook, build_dir):
    """Requires jupytext"""
    return f"jupyter nbconvert --to python {notebook}.ipynb --output {notebook}.py --output-dir {build_dir}"
def jupyter_clear_output(notebook):
    return f"jupyter nbconvert --ClearOutputPreprocessor.enabled=True --ClearMetadataPreprocessor.enabled=True --inplace {notebook}.ipynb"



def task_pull_fred():
    """
    """
    file_dep = ['load_fred.py']
    file_output = [DATA_DIR / 'pulled' / 'fred.parquet']
    targets = [OUTPUT_DIR / file for file in file_output]

    return {
        'actions': [
            "ipython ./load_fred.py",
        ],
        'targets': targets,
        'file_dep': file_dep
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
    """
    """
    file_dep = ['example_table.py']
    file_output = ['example_table.tex']
    targets = [OUTPUT_DIR / file for file in file_output]

    return {
        'actions': [
            "ipython ./example_table.py",
        ],
        'targets': targets,
        'file_dep': file_dep
    }

def task_example_plot():
    """Example plots
    """
    file_dep = ['example_plot.py', 'load_fred.py']
    file_output = ['example_plot.png']
    targets = [OUTPUT_DIR / file for file in file_output]

    return {
        'actions': [
            "ipython ./example_plot.py",
        ],
        'targets': targets,
        'file_dep': file_dep
    }


def task_convert_notebooks_to_scripts():
    """Preps the notebooks for presentation format.
    Execute notebooks with summary stats and plots and remove metadata.
    """
    build_dir = Path('./_build')
    build_dir.mkdir(parents=True, exist_ok=True)

    notebooks = [
        '01_example_notebook.ipynb',
        ]
    file_dep = notebooks
    stems = [notebook.split('.')[0] for notebook in notebooks]
    targets = [build_dir / f'{stem}.py' for stem in stems]

    actions = [
        # *[jupyter_execute_notebook(notebook) for notebook in notebooks_to_run],
        # *[jupyter_to_html(notebook) for notebook in notebooks_to_run],
        *[jupyter_clear_output(notebook) for notebook in stems],
        *[jupyter_to_python(notebook, build_dir) for notebook in stems],
        ]
    return {
        "actions": actions,
        "targets": targets,
        'task_dep':[],
        "file_dep": file_dep,
    }


def task_run_notebooks():
    """Preps the notebooks for presentation format.
    Execute notebooks with summary stats and plots and remove metadata.
    """
    notebooks_to_run_as_md = [
        '01_example_notebook.ipynb',
        ]
    stems = [notebook.split('.')[0] for notebook in notebooks_to_run_as_md]

    file_dep = [
        # 'load_other_data.py',
        *[Path('./_build') / f'{stem}.py' for stem in stems],
        ]

    targets = [
        ## 01_example_notebook.ipynb output
        OUTPUT_DIR / 'sine_graph.png',
        ## Notebooks converted to HTML
        *[OUTPUT_DIR / f'{stem}.html' for stem in stems],
        ]

    actions = [
        *[jupyter_execute_notebook(notebook) for notebook in stems],
        *[jupyter_to_html(notebook) for notebook in stems],
        *[jupyter_clear_output(notebook) for notebook in stems],
        # *[jupyter_to_python(notebook, build_dir) for notebook in notebooks_to_run],
        ]
    return {
        "actions": actions,
        "targets": targets,
        'task_dep':[],
        "file_dep": file_dep,
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


def task_compile_latex_docs():
    """Example plots
    """
    file_dep = [
        "../reports/report_example.tex",
        "../reports/slides_example.tex",
        "example_plot.py",
        "example_table.py",
        ]
    file_output = [
        "../reports/report_example.pdf",
        "../reports/slides_example.pdf",
        ]
    targets = [file for file in file_output]

    return {
        'actions': [
            "latexmk -xelatex -cd ../reports/report_example.tex", # Compile
            "latexmk -xelatex -c -cd ../reports/report_example.tex", # Clean
            "latexmk -xelatex -cd ../reports/slides_example.tex", # Compile
            "latexmk -xelatex -c -cd ../reports/slides_example.tex", # Clean
            # "latexmk -CA -cd ../reports/",
        ],
        'targets': targets,
        'file_dep': file_dep
    }


