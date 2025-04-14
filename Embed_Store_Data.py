# Import the necessary libraries
import pandas as pd  # For data manipulation and analysis
from sentence_transformers import SentenceTransformer  # For generating sentence embeddings
from elasticsearch import Elasticsearch  # For interacting with the Elasticsearch service
import hashlib  # For generating hash values for unique identifiers

# Initialize the Elasticsearch client with authentication details
es_client = Elasticsearch(
    "http://localhost:9200",
    basic_auth=('elastic', 'password')  # Replace with your actual Elasticsearch credentials
)

# Load a pre-trained sentence embedding model
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load the cleaned dataset from a CSV file
cleaned_dataset_path = "cleaned_imdb_top_1000.csv"  # Path to the dataset file
cleaned_data_df = pd.read_csv(cleaned_dataset_path)  # Load the dataset into a pandas DataFrame

# Define the name of the Elasticsearch index where the data will be stored
es_index_name = 'movie_embeddings_index'

# Check if the specified Elasticsearch index exists; if not, create it
if not es_client.indices.exists(index=es_index_name):
    # Define the settings and mappings for the new index
    index_settings = {
        "settings": {},
        "mappings": {
            "properties": {
                "title": {"type": "text"},  # Field for storing movie titles
                "director": {"type": "text"},  # Field for storing director names
                "star1": {"type": "text"},  # Field for storing the name of the first star
                "star2": {"type": "text"},  # Field for storing the name of the second star
                "embedding": {"type": "dense_vector", "dims": 384}  # Field for storing sentence embeddings
            }
        }
    }
    # Create the index with the defined settings and mappings
    es_client.indices.create(index=es_index_name, body=index_settings)

# Function to generate embeddings from batched data
def process_and_embed_data(batch):
    # Concatenate relevant information into a single string for each movie
    concatenated_info = batch['Series_Title'] + ' ' + batch['Director'] + ' ' + batch['Star1'] + ' ' + batch['Star2']
    # Generate embeddings for the concatenated strings
    embeddings = sentence_model.encode(concatenated_info.tolist(), show_progress_bar=False)
    return embeddings

# Function to index the embeddings and additional information in Elasticsearch
def index_embeddings(data, embeddings):
    for idx, embedding_vector in enumerate(embeddings):
        # Generate a unique document ID by hashing the movie title
        document_id = hashlib.sha256(data['Series_Title'].iloc[idx].encode('utf-8')).hexdigest()

        # Prepare the document body with the movie information and embedding
        document_body = {
            "title": data['Series_Title'].iloc[idx],
            "director": data['Director'].iloc[idx],
            "star1": data['Star1'].iloc[idx],
            "star2": data['Star2'].iloc[idx],
            "embedding": embedding_vector.tolist()  # Convert the embedding to a list for storage
        }

        # Index the document in Elasticsearch using the generated document ID
        es_client.index(index=es_index_name, id=document_id, body=document_body)

# Process and index the dataset in batches to efficiently manage memory usage
batch_size = 100  # Define the size of each batch
for start_idx in range(0, len(cleaned_data_df), batch_size):
    end_idx = min(start_idx + batch_size, len(cleaned_data_df))  # Determine the end index of the current batch
    batch = cleaned_data_df.iloc[start_idx:end_idx]  # Extract the current batch from the DataFrame
    embeddings = process_and_embed_data(batch)  # Generate embeddings for the batch
    index_embeddings(batch, embeddings)  # Index the embeddings and additional information in Elasticsearch
    print(f"Processed and indexed batch {start_idx+1} to {end_idx}")

print("Completed embedding and storing all records.")
