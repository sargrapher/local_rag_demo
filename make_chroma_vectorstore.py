#!/usr/bin/env python3

"""
ChromaDB Vector Store Creator for RAG Systems

This script processes PDF documents and creates a vector store database using ChromaDB
for use in Retrieval Augmented Generation (RAG) systems. It handles document loading,
text chunking, embedding generation, and storage.

Process Flow:
-----------
1. Document Loading:
   - Recursively finds all PDFs in specified directory
   - Loads and extracts text content
   - Preserves document metadata

2. Text Processing:
   - Splits documents into manageable chunks
   - Uses recursive character splitting for better semantic boundaries
   - Maintains chunk overlap for context preservation

3. Embedding Generation:
   - Converts text chunks to vector embeddings
   - Uses Ollama's nomic-embed-text model
   - Processes documents in sequence

4. Vector Storage:
   - Stores embeddings in ChromaDB
   - Maintains document-embedding relationships
   - Preserves source metadata
   - Uses cosine similarity for retrieval

Directory Structure:
-----------------
documents/
    └── *.pdf  # Place your PDF files here

Requirements:
-----------
- langchain_community: For document loading and processing
- langchain_ollama: For embedding generation
- chromadb: For vector storage
- Ollama: Running locally with nomic-embed-text model

Usage:
-----
1. Place PDF documents in the 'documents' directory
2. Run the script:
    python make_chroma_vectorstore.py

Note:
----
- Existing embeddings are preserved
- Process is additive (can run multiple times)
- Large documents may take time to process
"""

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from chromadb import PersistentClient
import os
import time
from langchain_ollama import OllamaEmbeddings

def process_documents(directory_path, collection):
    """
    Process PDF documents from a directory and add them to ChromaDB.
    
    This function:
    1. Loads PDF documents from specified directory
    2. Splits them into chunks
    3. Generates embeddings
    4. Stores in ChromaDB with metadata
    
    Args:
        directory_path (str): Path to directory containing PDF files
        collection: ChromaDB collection for storing embeddings
        
    Processing Details:
    - Chunk size: 1000 characters
    - Chunk overlap: 200 characters
    - Embedding model: nomic-embed-text
    - Storage format: cosine similarity space
    
    Document Processing Flow:
    1. Directory scanning
    2. PDF loading and text extraction
    3. Text chunking
    4. Embedding generation
    5. Vector storage
    
    Note:
        - Requires PDFs in the specified directory
        - May take significant time for large documents
        - Preserves document source in metadata
    """
    # Check if directory exists
    if not os.path.exists(directory_path):
        print(f"Directory {directory_path} does not exist")
        return

    # Load PDF documents from the specified directory
    loader = DirectoryLoader(directory_path, glob="**/*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    
    # Initialize Ollama embeddings
    embedding_model = OllamaEmbeddings(model="nomic-embed-text")
    
    # Generate embeddings
    embeddings = []
    metadatas = []
    ids = []
    
    for i, doc in enumerate(texts):
        embedding = embedding_model.embed_query(doc.page_content)
        embeddings.append(embedding)
        metadatas.append({"source": doc.metadata.get("source", "unknown")})
        ids.append(f"doc_{i}")
    
    # Add documents and embeddings to ChromaDB
    collection.add(
        embeddings=embeddings,
        documents=[doc.page_content for doc in texts],
        metadatas=metadatas,
        ids=ids
    )

    print(f"Successfully added {len(embeddings)} embeddings to ChromaDB.")

def init_embeddings():
    """
    Initialize or connect to a persistent ChromaDB instance.
    
    This function:
    1. Creates/connects to local ChromaDB
    2. Initializes/retrieves document collection
    3. Sets up vector similarity space
    
    Returns:
        ChromaDB collection: Initialized collection for document embeddings
        
    Technical Details:
    - Storage: Local persistent storage
    - Collection name: 'document_embeddings'
    - Similarity metric: cosine
    - Storage location: ./chromadb
    
    Note:
        Creates storage directory if it doesn't exist
    """
    # Initialize ChromaDB client with local persistence
    chroma_client = PersistentClient(path="./chromadb")
    
    # Create or get collection
    collection = chroma_client.get_or_create_collection(
        name="document_embeddings",
        metadata={"hnsw:space": "cosine"}
    )
    
    return collection

def main():
    """
    Main function to orchestrate the document processing pipeline.
    
    Process Flow:
    1. Initialize ChromaDB collection
    2. Process documents from 'documents' directory
    3. Generate and store embeddings
    
    The function:
    - Sets up necessary components
    - Processes all PDF documents
    - Provides feedback on completion
    
    Note:
        - Requires 'documents' directory
        - Processes all PDFs recursively
        - Maintains persistent storage
    """
    directory_path = "documents"
    collection = init_embeddings()  # Initialize persistent ChromaDB
    process_documents(directory_path, collection)
    print("Embeddings created and stored in ChromaDB successfully.")

if __name__ == "__main__":
    directory_path = "documents"
    collection = init_embeddings()  # Initialize persistent ChromaDB
    process_documents(directory_path, collection)
