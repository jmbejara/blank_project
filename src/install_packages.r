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
USER <- Sys.getenv("USER")
R_LIB <- Sys.getenv("R_LIB")
OUTPUT_DIR <- Sys.getenv("OUTPUT_DIR")
#### >>>


# Read the requirements file
packages <- readLines("r_requirements.txt")
packages <- packages[!grepl("^#", packages)]

## Options for installing arrow
# See https://stackoverflow.com/a/73054288
# and https://arrow.apache.org/docs/r/articles/install.html
Sys.setenv(NOT_CRAN = "true")

# Function to install packages if not already installed
r_lib = sprintf(R_LIB, USER)
install_if_missing <- function(package) {
  if (!requireNamespace(package, quietly = TRUE)) {
    cat("Installing package:", package, "\n")
    install.packages(package, repos = "https://cran.rstudio.com/", dependencies=TRUE, lib=r_lib)

    # uses library on each to see if its loadable, and if not calls quit with a non-0 status.
    # https://stackoverflow.com/a/52638148
    if ( ! library(package, character.only=TRUE, logical.return=TRUE) ) {
        quit(status=1, save='no')
    }
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