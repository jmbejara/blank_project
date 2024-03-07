import sys
from doit.tools import run_once
from pathlib import Path
import subprocess

sys.path.insert(1, './src/')

import config  # Dodo change 6

OUTPUT_DIR = Path(config.OUTPUT_DIR)
DATA_DIR = Path(config.DATA_DIR)

def task_cds_data_fetch():
    return {
        'actions': ['python src/cds_data_fetch.py'],
        'file_dep': ['src/cds_data_fetch.py'],
        'targets': [str(DATA_DIR / 'cds_data.csv')]  # Example output file
    }

def task_cds_processing():
    return {
        'actions': ['python src/cds_processing.py'],
        'file_dep': ['src/cds_processing.py'],
    }

def task_interest_rates():
    return {
        'actions': ['python src/interest_rates.py'],
        'file_dep': ['src/interest_rates.py'],
    }

# Add similar functions for each of your scripts

def task_variables_analysis():
    return {
        'actions': ['jupyter nbconvert --to notebook --execute src/variables_analysis.ipynb'],
        'file_dep': ['src/variables_analysis.ipynb'],
    }

def run_tests():
    test_files = [
        'src/test_cds_data.py',
        'src/test_interest_rates.py',
        'src/test_rates_processing.py'
    ]
    for test_file in test_files:
        subprocess.run(['python', test_file], check=True)


def task_compile_latex():
    return {
        'actions': ['pdflatex -output-directory=reports reports/Project_report.tex'],
        'file_dep': ['reports/Project_report.tex'],
        'targets': ['reports/Project_report.pdf']
    }

DOIT_CONFIG = {
    'default_tasks': ['cds_data_fetch', 'cds_processing', 'interest_rates', 'run_tests', 'variables_analysis', 'compile_latex']
}