library(arrow)
library(dotenv)
load_dot_env()

DATA_DIR <- Sys.getenv("DATA_DIR")

# Print the value to stdout
# cat("DATA_DIR:", DATA_DIR, "\n")
filepath <- file.path(DATA_DIR, "pulled", "fred.parquet")

# Read the Parquet file into a tibble
fred_tibble <- read_parquet("fred.parquet")

# Display the first few rows of the tibble
print(head(fred_tibble))