# Import necessary libraries
import streamlit as st  # For creating web apps
from elasticsearch import Elasticsearch  # For interacting with Elasticsearch
from sentence_transformers import SentenceTransformer  # For generating sentence embeddings
import pandas as pd  # For data manipulation

# Initialize the Elasticsearch client with authentication details
es_client = Elasticsearch(
    "http://localhost:9200",
    basic_auth=('elastic', 'password')  # Actual credentials should be replaced here
)

# Load the sentence embedding model that was used to generate embeddings for the data
model = SentenceTransformer('all-MiniLM-L6-v2')

# Set Streamlit page configuration with a project name and an optional icon
st.set_page_config(page_title="Movie Search Engine", page_icon=":mag:")

# Display the main title of the Streamlit app
st.title("Movie Search Engine")

# Display developer details in the sidebar
# Adjust the path for the profile photo as necessary
st.sidebar.image("profile_photo.jpg", width=100, use_column_width='always')
st.sidebar.markdown("**Developer:** Sravan Chowdary")
st.sidebar.markdown("**ID:** 1002147954")
st.sidebar.markdown("**Email:** sxn7954@gmail.com")
st.sidebar.markdown("**Phone no:** +1 9121032156")

# Create a text input widget in Streamlit for user queries
user_query = st.text_input("Enter your search query:")

# Define a function to perform a search operation using Elasticsearch
def search_es(query, es_client, index_name='movie_embeddings_index', top_n=10):
    # Embed the user's query using the same model as the data
    query_embedding = model.encode([query])
    query_vector = query_embedding[0].tolist()  # Convert the embedding to a list for Elasticsearch

    # Define an Elasticsearch script query for finding similar vectors
    script_query = {
        "script_score": {
            "query": {"match_all": {}},  # This matches all documents but scores them based on the script
            "script": {
                "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",  # Cosine similarity script
                "params": {"query_vector": query_vector}  # Passes the query vector to the script
            }
        }
    }

    # Execute the search query in Elasticsearch
    response = es_client.search(
        index=index_name,
        body={
            "size": top_n,  # Limits the number of search results returned
            "query": script_query,  # Uses the script query defined above
            "_source": ["title", "director", "star1", "star2"]  # Specifies which fields to return in the results
        }
    )

    # Process the search results to extract relevant fields
    results = [{
        "Title": hit["_source"]["title"],  # Extract the title
        "Director": hit["_source"].get("director", "N/A"),  # Extract the director, defaulting to 'N/A' if not found
        "Star 1": hit["_source"].get("star1", "N/A"),  # Extract the first star
        "Star 2": hit["_source"].get("star2", "N/A")  # Extract the second star
    } for hit in response["hits"]["hits"]]
    return results

# Perform the search if the user has entered a query and display the results
if user_query:
    results = search_es(user_query, es_client)
    if results:
        # Convert the results to a DataFrame for display
        df = pd.DataFrame(results)
        # Apply custom styling to enhance the display of the search results
        st.markdown("""
        <style>
        .big-font {
            font-size:20px !important;
            font-weight: bold;
        }
        .dataframe th {
            background-color: #0198E1;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Display the search results with custom styling
        st.markdown('<p class="big-font">Closest entries found:</p>', unsafe_allow_html=True)
        st.table(df)
    else:
        # Display a message if no matching entries were found
        st.write("No matching entries found.")
