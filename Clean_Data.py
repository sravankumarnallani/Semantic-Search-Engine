import pandas as pd

# Load the dataset into a pandas DataFrame.
movies_df = pd.read_csv("imdb_top_1000.csv")

# Select the columns needed for the semantic search embedding.
# These are 'Series_Title', 'Overview', 'Star1', 'Star2', and 'Director'.
selected_columns_df = movies_df[['Series_Title', 'Overview', 'Star1', 'Star2', 'Director']]

# Clean the columns.
# Here, we'll perform basic cleaning such as filling missing values and removing leading/trailing spaces.
cleaned_df = selected_columns_df.fillna('')  # Replaces any NaN values with empty strings.
cleaned_df = cleaned_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Concatenate the selected columns into a single column.
# This creates a unified text representation of each movie for semantic analysis or search.
# We're using a simple space as a separator. 
cleaned_df['Concatenated_Info'] = cleaned_df.apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

# The 'Concatenated_Info' column now contains cleaned, concatenated text of the selected columns.
# This is useful for semantic search embeddings or other text analysis tasks.
print(cleaned_df['Concatenated_Info'].head())

# Optionally, save the DataFrame to a new CSV file if we need to use it outside this script.
cleaned_df.to_csv("cleaned_imdb_top_1000.csv", index=False)
