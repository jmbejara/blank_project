import sys
from doit.tools import run_once
from pathlib import Path
import subprocess

sys.path.insert(1, './src/') #change3

import config  # Assuming config.py contains relevant configurations

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

def task_variables_analysis():
    return {
        'actions': ['jupyter nbconvert --to notebook --execute src/variables_analysis.ipynb'],
        'file_dep': ['src/variables_analysis.ipynb'],
    }

def run_tests():
    test_files = [
        'src/test_cds_data.py',
        'src/test_interest_rates.py',
        'src/test_misc_tools.py',
        'src/test_rates_processing.py'
    ]
    for test_file in test_files:
        subprocess.run(['python', test_file], check=True)

def task_run_tests():
    return {
        'actions': [run_tests],
        'file_dep': [
            'src/test_cds_data.py',
            'src/test_interest_rates.py',
        ],
    }

DOIT_CONFIG = {
    'default_tasks': ['cds_data_fetch', 'cds_processing', 'interest_rates', 'run_tests', 'variables_analysis']
}