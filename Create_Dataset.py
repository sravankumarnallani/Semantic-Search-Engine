# Import necessary libraries
import kaggle  # For accessing and downloading datasets from Kaggle.
import pandas as pd  # For data manipulation and analysis.
import zipfile  # For extracting files from a zip archive.

# Authenticate the Kaggle API client.
# This step requires a valid Kaggle API token on your machine.
kaggle.api.authenticate()

# Define the dataset location on Kaggle.
kaggle_dataset_path = "harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows"

# Download the dataset zip file from Kaggle.
# The dataset contains the top 1000 movies and TV shows as listed on IMDb.
kaggle.api.dataset_download_files(kaggle_dataset_path, quiet=False)

# Specify the path to the downloaded zip file and the extraction directory.
zip_file_path = "imdb-dataset-of-top-1000-movies-and-tv-shows.zip"
extraction_directory = "."

# Extract the dataset from the zip file.
with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
    zip_ref.extractall(extraction_directory)

# Load the dataset into a pandas DataFrame.
# The dataset is assumed to be in CSV format.
movies_df = pd.read_csv("imdb_top_1000.csv")

# Display the column names of the dataset to understand its structure.
print(movies_df.columns)

# Display the titles and overviews of the first 10 movies/TV shows in the dataset.
# This helps in getting a quick overview of some of the top listings.
print(movies_df[["Series_Title", "Overview"]].head(10))
