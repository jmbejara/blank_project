"""Run or update the project. This file uses the `doit` Python package. It works
like a Makefile, but is Python-based
"""
import config
from pathlib import Path
from doit.tools import run_once

output_dir = config.output_dir
data_dir = config.data_dir


def task_summary_stats():
    """
    """
    file_dep = ['example_table.py', 'config.py']
    file_output = ['example_table.tex']
    targets = [output_dir / file for file in file_output]

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
    file_dep = ['example_plot.py', 'config.py']
    file_output = ['example_plot.png']
    targets = [output_dir / file for file in file_output]

    return {
        'actions': [
            "ipython ./example_plot.py",
        ],
        'targets': targets,
        'file_dep': file_dep
    }
