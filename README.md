Project 15: Palhares, Diogo. Cash-flow maturity and risk premia in CDS markets. The University of Chicago, 2013.
==================

# About this project

In our project, we endeavor to replicate and extend the empirical analysis presented in the study by He, Kelly, and Manela, specifically focusing on the factors and test assets associated with Credit Default Swap (CDS) markets. Our replication primarily involves reconstructing the CDS_01 to CDS_20 columns as delineated in "He_Kelly_Manela_Factors_And_Test_Assets_monthly.csv" [available in the P15_DANK/data/manual]. In order to construct the "CDS" the authors used the theoretical framework established by Palhares, Diogo, particularly his insights on cash-flow maturity and its influence on risk premia within CDS markets. 



To correctly replicate the desired output we used the formula delineated on page 10 of He, Kelly, and Manela work, based on Palhares framework:

$$
CDS^{ret}_t = \frac{CDS_t}{250}+ \Delta CDS_t \times RD_t.
$$

Where RD_t is a follows:

$$
RD_t = \frac{1}{4} \sum_{j=1}^{4M} e^{-\lambda j/4} - e^{-\left(\lambda + j\delta\right)/4},
$$

which provides a nuanced approach to assessing CDS risk premia in relation to cash-flow maturity. Our empirical analysis utilizes the dataset sourced from Markit-Credit Default Swap, encompassing a time span from January 1, 2001, to January 31, 2024. This dataset allows for a thorough examination of the CDS market over a significant period, offering insights into its evolution and the dynamics of risk premia within it.

Furthermore, we integrate data from the Federal Reserve Economic Data (FRED) database and the Federal Reserve (FED). This integration involves the extraction of rate data ranging from 3 to 6 months from the FRED, with the interest rates from 12 to 120 months from the FED from (31 January 2001 to 31 January 2024). Finally, we combine the datasets from the Markit-Credit Default Swap with the merged rates data. The inclusion of this rate data from FRED is instrumental in providing a more rounded and comprehensive understanding of the financial environment in which these CDS markets operate. 

# Quick Start
To quickest way to run code in this repo is to use the following steps. First, note that you must have TexLive installed on your computer and available in your path.
You can do this by downloading and installing it from here ([windows](https://tug.org/texlive/windows.html#install) and [mac](https://tug.org/mactex/mactex-download.html) installers).
Having installed LaTeX, open a terminal and navigate to the root directory of the project and create a conda environment using the following command:
```
conda create -n blank python=3.12
conda activate blank
```
and then install the dependencies with pip
```
pip install -r requirements.txt
```
You can then navigate to the `src` directory and then run 
```
doit
```
# General Directory Structure

 - The `data/manual` folder is used for the inclusion of datasets from the Federal Reserve (FED), the Federal Reserve Economic Data (FRED), and Markit. It also contains the `He_Kelly_Manela_Factors_And_Test_Assets_monthly.csv` file, which includes the CDS_01 to CDS_20 columns that we aim to replicate in our analysis. This comprehensive compilation of data provides a foundational base for our replication and extension of the empirical analysis presented by He, Kelly, and Manela.

The specific datasets included in the `data/manual` folder are:
- `He_Kelly_Manela_Factors.zip`: An archive containing the factors identified by He, Kelly, and Manela in their study.
- `He_Kelly_Manela_Factors_And_Test_Assets_monthly.csv`: A monthly breakdown of test assets and factors related to CDS markets.
- `crsp_a_treasuries_monthly.csv`: Monthly data on treasury securities, which is crucial for understanding the financial instruments in the broader market context.

By leveraging these datasets, we can closely follow the methodologies employed by He, Kelly, and Manela, while also incorporating additional data points from FED and FRED to enrich our analysis and provide a more rounded perspective on the evolution of CDS markets and risk premia dynamics.

 - The `output` folder, on the other hand, contains tables and figures that are generated from code. The entire folder should be able to be deleted, because the code can be run again, which would again generate all of the contents.

 - I'm using the `doit` Python module as a task runner. It works like `make` and the associated `Makefile`s. To rerun the code, install `doit` (https://pydoit.org/) and execute the command `doit` from the `src` directory. Note that doit is very flexible and can be used to run code commands from the command prompt, thus making it suitable for projects that use scripts written in multiple different programming languages.

 - I'm using the `.env` file as a container for absolute paths that are private to each collaborator in the project. You can also use it for private credentials, if needed. It should not be tracked in Git.

# Data and Output Storage

I'll often use a separate folder for storing data. I usually write code that will pull the data and save it to a directory in the data folder called "pulled"  to let the reader know that anything in the "pulled" folder could hypothetically be deleted and recreated by rerunning the PyDoit command (the pulls are in the dodo.py file).

I'll usually store manually created data in the "assets" folder if the data is small enough. Because of the risk of manually data getting changed or lost, I prefer to keep it under version control if I can.

Output is stored in the "output" directory. This includes tables, charts, and rendered notebooks. When the output is small enough, I'll keep this under version control. I like this because I can keep track of how tables change as my analysis progresses, for example.

Of course, the data directory and output directory can be kept elsewhere on the machine. To make this easy, I always include the ability to customize these locations by defining the path to these directories in environment variables, which I intend to be defined in the `.env` file, though they can also simply be defined on the command line or elsewhere. The `config.py` is reponsible for loading these environment variables and doing some like preprocessing on them. The `config.py` file is the entry point for all other scripts to these definitions. That is, all code that references these variables and others are loading by importing `config`.


# Dependencies and Virtual Environments

## Working with `pip` requirements

`conda` allows for a lot of flexibility, but can often be slow. `pip`, however, is fast for what it does.  You can install the requirements for this project using the `requirements.txt` file specified here. Do this with the following command:
```
pip install -r requirements.txt
```

The requirements file can be created like this:
```
pip list --format=freeze
```

## Working with `conda` environments

The dependencies used in this environment (along with many other environments commonly used in data science) are stored in the conda environment called `blank` which is saved in the file called `environment.yml`. To create the environment from the file (as a prerequisite to loading the environment), use the following command:

```
conda env create -f environment.yml
```

Now, to load the environment, use

```
conda activate blank
```

Note that an environment file can be created with the following command:

```
conda env export > environment.yml
```

However, it's often preferable to create an environment file manually, as was done with the file in this project.

Also, these dependencies are also saved in `requirements.txt` for those that would rather use pip. Also, GitHub actions work better with pip, so it's nice to also have the dependencies listed here. This file is created with the following command:

```
pip freeze > requirements.txt
```

### Alternative Quickstart using Conda
Another way to  run code in this repo is to use the following steps.
First, open a terminal and navigate to the root directory of the project and create a conda environment using the following command:
```
conda env create -f environment.yml
```
Now, load the environment with
```
conda activate blank
```
Now, navigate to the directory called `src`
and run
```
doit
```
That should be it!



**Other helpful `conda` commands**

- Create conda environment from file: `conda env create -f environment.yml`
- Activate environment for this project: `conda activate blank`
- Remove conda environment: `conda remove --name myenv --all`
- Create blank conda environment: `conda create --name myenv --no-default-packages`
- Create blank conda environment with different version of Python: `conda create --name myenv --no-default-packages python` Note that the addition of "python" will install the most up-to-date version of Python. Without this, it may use the system version of Python, which will likely have some packages installed already.

## `mamba` and `conda` performance issues

Since `conda` has so many performance issues, it's recommended to use `mamba` instead. I recommend installing the `miniforge` distribution. See here: https://github.com/conda-forge/miniforge
