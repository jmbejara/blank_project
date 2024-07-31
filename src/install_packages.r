#!/usr/bin/env Rscript
# current_dir <- getwd()
# cat("Current working directory:", current_dir, "\n")

#### <<< Load .env
library(fs)
library(dotenv)

if (file.exists(".env")) {
  dotenvpath <- path(".env")
} else {
  dotenvpath <- path("../.env")
}
load_dot_env(dotenvpath)
R_LIB <- Sys.getenv("R_LIB")
OUTPUT_DIR <- Sys.getenv("OUTPUT_DIR", unset="./data")
#### >>>


# Read the requirements file
packages <- readLines("r_requirements.txt")

# Function to install packages if not already installed
install_if_missing <- function(package) {
  if (!requireNamespace(package, quietly = TRUE)) {
    cat("Installing package:", package, "\n")
    install.packages(package, repos = "https://cran.rstudio.com/", lib=R_LIB)
  }
}

# Apply the function to each package
sapply(packages, install_if_missing)

print("All packages installed successfully!")
filepath <- path(OUTPUT_DIR, "R_packages_installed.txt")
# if file at filepath does not exist, create it
if (!file.exists(filepath)) {
  file.create(filepath)
}