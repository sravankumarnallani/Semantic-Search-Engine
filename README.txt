# Semantic Search Engine

This project is a semantic search engine powered by Elasticsearch and Streamlit. It allows users to input a query and retrieves the most semantically similar entries from a pre-indexed Elasticsearch database.

## Developer

- **Name:** Sravan Chowdary
- **ID:** 1002147954

## Features

- User-friendly web interface for submitting search queries.
- Semantic search capabilities to find the most relevant entries in the database.
- Display of search results with relevance ranking.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher is installed on your machine.
- Elasticsearch 7.x is running locally or remotely with access details known.

## Installation

1. Download project to your local machine:

2. Navigate to the project directory:

    ```bash
    cd semantic-search-engine
    ```

3. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. Start the Streamlit application:

    ```bash
    streamlit run streamlit_app.py
    ```

2. Open your web browser and go to the URL provided by Streamlit, typically `http://localhost:8501`.

## Configuring Elasticsearch

Ensure your Elasticsearch instance is running and accessible. The application expects the following default credentials:

- **Host:** http://localhost:9200
- **Username:** elastic
- **Password:** "your password"

Modify the Elasticsearch connection details in `streamlit_app.py` as necessary to match your setup.

## Preparing the Data

The application requires a pre-indexed Elasticsearch database. Follow these steps to prepare your data:

1. Index your data into Elasticsearch. Refer to the `embed_and_store.py` script for guidance on embedding textual data and storing it in Elasticsearch.
2. Ensure the indexed data is compatible with the search queries performed by the application.

## Acknowledgements

- Sentence Transformers for the embedding model.
- Elasticsearch for the vector search engine.
- Streamlit for the web interface.
