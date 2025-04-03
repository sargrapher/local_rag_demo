#!/usr/bin/env python3

"""
ChromaDB Embeddings Reader

This script provides functionality to read and display document embeddings stored in a ChromaDB
collection. It's designed to work with RAG (Retrieval Augmented Generation) systems and
helps inspect the embedded documents in your vector store.

Key Features:
------------
- Connects to a persistent ChromaDB instance
- Retrieves all documents and their associated metadata
- Displays document content previews and metadata
- Shows total document count in the collection

Technical Details:
----------------
- Uses ChromaDB's Client for stable storage
- Assumes documents are stored in 'document_embeddings' collection
- Preserves and displays original document IDs
- Shows metadata associated with each embedding

Usage:
-----
Simply run the script:
    python read_embeddings.py

The script will:
1. Connect to the local ChromaDB instance
2. Retrieve all stored documents
3. Display summary information
4. Show details for each document

Requirements:
-----------
- chromadb: For accessing the vector store
- Existing ChromaDB database in ./chromadb directory

Note:
----
This script is read-only and won't modify your embeddings database.
It's safe to use for inspection and debugging purposes.
"""

from chromadb import Client, PersistentClient
from typing import Dict, List, Any

def read_embeddings() -> None:
    """
    Read and display all document embeddings from the ChromaDB collection.
    
    This function:
    1. Connects to the local ChromaDB instance
    2. Retrieves the 'document_embeddings' collection
    3. Fetches all documents and their metadata
    4. Displays formatted information about each document
    
    The output includes:
    - Total number of documents in the collection
    - For each document:
        - Document ID
        - Preview of the text content (first 200 characters)
        - Associated metadata
    
    Raises:
        Exception: If ChromaDB connection fails or collection doesn't exist
    
    Example output:
        Total documents in collection: 3
        
        Document 1 (ID: doc_001):
        Text snippet: This is the beginning of the document...
        Metadata: {'source': 'file1.txt', 'date': '2024-03-05'}
    """
    # Initialize ChromaDB client with the same path as the storage program
    chroma_client = PersistentClient(path="./chromadb")
    
    # Get the existing collection
    collection = chroma_client.get_collection(name="document_embeddings")
    
    # Get all documents and their metadata
    results = collection.get()
    
    # Print the results
    print(f"Total documents in collection: {len(results['ids'])}")
    print("\nDocuments and their metadata:")
    for i, (doc_id, document, metadata) in enumerate(zip(results['ids'], results['documents'], results['metadatas'])):
        print(f"\nDocument {i+1} (ID: {doc_id}):")
        print(f"Text snippet: {document[:200]}...")  # Print first 200 characters
        print(f"Metadata: {metadata}")

def main() -> None:
    """
    Main function to handle script execution and error handling.
    
    Wraps the read_embeddings function with error handling to provide
    clear feedback if something goes wrong.
    """
    try:
        read_embeddings()
    except Exception as e:
        print(f"Error reading embeddings: {e}")
        print("\nPlease ensure:")
        print("1. ChromaDB is properly installed")
        print("2. The ./chromadb directory exists and contains your database")
        print("3. The 'document_embeddings' collection exists")
        return 1
    return 0

if __name__ == "__main__":
    exit(main()) 