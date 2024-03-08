#change 3

import sys
from pathlib import Path
import subprocess
sys.path.insert(1, './src/')
import config  # Dodo change 7

OUTPUT_DIR = Path(config.OUTPUT_DIR)
DATA_DIR = Path(config.DATA_DIR)


'''

'''

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

'''

def task_variables_analysis():
    return {
        'actions': ['jupyter nbconvert --to notebook --execute src/variables_analysis.ipynb'],
        'file_dep': ['src/variables_analysis.ipynb'],
    }
'''
    

# Function to run tests
def run_tests():
    test_files = [
        'src/test_calc_cds_returns.py',
        'src/test_cds_processing.py',
        'src/test_cds_data.py',
        'src/test_interest_rates.py',
        'src/test_rates_processing.py',
    ]
    for test_file in test_files:
        subprocess.run(['python', test_file], check=True)

# Define a doit task for running tests
def task_run_tests():
    return {
        'actions': [run_tests],
    }


def task_compile_latex():
    """Compile the LaTeX document Project_report.tex to PDF Project_report.pdf"""
    latex_file = "./reports/Project_report.tex"
    output_pdf = "./reports/Project_report.pdf"  # Change the output file name here

    return {
        'actions': [
            f"latexmk -xelatex -cd -jobname=Project_report {latex_file}",  # Compile
            f"latexmk -c -cd {latex_file}",  # Clean auxiliary files
        ],
        'file_dep': [latex_file],
        'targets': [output_pdf],
        'clean': True,  # Clean by default
    }


'''
def task_compile_latex():
    """Compile the LaTeX document report_example.tex to PDF report_example.pdf"""
    latex_file = "./reports/report_example.tex"
    output_pdf = "./reports/report_example.pdf"

    return {
        'actions': [
            f"latexmk -xelatex -cd -jobname=report_example {latex_file}",  # Compile
            f"latexmk -c -cd {latex_file}",  # Clean auxiliary files
        ],
        'file_dep': [latex_file],
        'targets': [output_pdf],
        'clean': True,  # Clean by default
    }
'''
'''
def task_compile_latex():
    """Compile the LaTeX document Project_report.tex to PDF Report_P15_DANK.pdf"""
    latex_file = "./reports/Project_report.tex"
    output_pdf = "./reports/Report_P15_DANK.pdf"

    return {
        'actions': [
            f"latexmk -xelatex -cd -jobname=Report_P15_DANK {latex_file}",  # Compile
            f"latexmk -c -cd {latex_file}",  # Clean auxiliary files
        ],
        'file_dep': [latex_file],
        'targets': [output_pdf],
        'clean': True,  
    }
'''

DOIT_CONFIG = {
    'default_tasks': ['cds_data_fetch', 'cds_processing', 'interest_rates', 'run_tests', 'compile_latex']
}
