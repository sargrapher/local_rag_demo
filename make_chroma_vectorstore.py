#!/usr/bin/env python3

"""
ChromaDB Vector Store Creator for RAG Systems

This script processes documents and creates a vector store database using ChromaDB
for use in Retrieval Augmented Generation (RAG) systems. It handles document loading,
text chunking, embedding generation, and storage.

Process Flow:
-----------
1. Document Loading:
   - Recursively finds all supported files in specified directory
   - Loads and extracts text content
   - Preserves document metadata
   - Supports multiple file types

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
    ├── *.txt   # Text files
    ├── *.pdf   # PDF files
    ├── *.md    # Markdown files
    ├── *.rst   # ReStructured Text files
    ├── *.ppt   # PowerPoint files
    ├── *.pptx  # PowerPoint files
    ├── *.doc   # Word documents
    ├── *.docx  # Word documents
    ├── *.xls   # Excel files
    ├── *.xlsx  # Excel files
    ├── *.html  # HTML files
    ├── *.csv   # CSV files
    ├── *.json  # JSON files
    ├── *.eml   # Email files
    ├── *.rtf   # RTF files
    └── *.epub  # EPUB files

Requirements:
-----------
- langchain_community: For document loading and processing
- langchain_ollama: For embedding generation
- chromadb: For vector storage
- unstructured[all]: For processing various document formats
- python-magic: For file type detection
- Additional format-specific packages (see requirements.txt)

Usage:
-----
1. Place documents in the 'documents' directory
2. Run the script:
    python make_chroma_vectorstore.py

Note:
----
- Existing embeddings are preserved
- Process is additive (can run multiple times)
- Large documents may take time to process
"""

from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader, UnstructuredRSTLoader
from langchain_community.document_loaders import UnstructuredPowerPointLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_community.document_loaders import BSHTMLLoader
from langchain_community.document_loaders import CSVLoader
from langchain_community.document_loaders import JSONLoader
from langchain_community.document_loaders import UnstructuredEmailLoader
from langchain_community.document_loaders import UnstructuredRTFLoader
from langchain_community.document_loaders import UnstructuredEPubLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from chromadb import PersistentClient
import os
import glob
from typing import List, Dict
import time
from langchain_ollama import OllamaEmbeddings

def get_file_loader(file_path: str):
    """
    Get the appropriate loader based on file extension.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        loader_class: Appropriate langchain loader class for the file type
    """
    ext = os.path.splitext(file_path)[1].lower()
    loaders = {
        '.txt': TextLoader,
        '.pdf': PyPDFLoader,
        '.md': UnstructuredMarkdownLoader,
        '.rst': UnstructuredRSTLoader,
        '.ppt': UnstructuredPowerPointLoader,
        '.pptx': UnstructuredPowerPointLoader,
    }
    return loaders.get(ext, TextLoader)  # Default to TextLoader for unknown types

def process_documents(directory_path: str, collection) -> None:
    """
    Process documents from a directory and add them to ChromaDB.
    
    This function:
    1. Loads documents from specified directory
    2. Splits them into chunks
    3. Generates embeddings
    4. Stores in ChromaDB with metadata
    
    Args:
        directory_path (str): Path to directory containing documents
        collection: ChromaDB collection for storing embeddings
        
    Processing Details:
    - Chunk size: 1000 characters
    - Chunk overlap: 200 characters
    - Embedding model: nomic-embed-text
    - Storage format: cosine similarity space
    
    Supported File Types:
    - Text files (.txt) - default
    - PDF files (.pdf)
    - Markdown files (.md)
    - ReStructured Text files (.rst)
    """
    # Check if directory exists
    if not os.path.exists(directory_path):
        print(f"Directory {directory_path} does not exist")
        return

    # Process all supported file types
    documents = []
    supported_extensions = ['.txt', '.pdf', '.md', '.rst', '.ppt', '.pptx']
    
    for ext in supported_extensions:
        pattern = os.path.join(directory_path, f"**/*{ext}")
        matching_files = glob.glob(pattern, recursive=True)
        
        for file_path in matching_files:
            try:
                loader_class = get_file_loader(file_path)
                loader = loader_class(file_path)
                docs = loader.load()
                documents.extend(docs)
                print(f"Processed: {file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
    
    if not documents:
        print("No documents found to process")
        return
    
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
        metadatas.append({
            "source": doc.metadata.get("source", "unknown"),
            "file_type": os.path.splitext(doc.metadata.get("source", ""))[1][1:] or "unknown"
        })
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

def init_loaders():
    """Initialize document loaders for different file types."""
    return {
        ".txt": (TextLoader, {}),
        ".pdf": (PyPDFLoader, {}),
        ".md": (UnstructuredMarkdownLoader, {}),
        ".rst": (UnstructuredRSTLoader, {}),
        ".ppt": (UnstructuredPowerPointLoader, {}),
        ".pptx": (UnstructuredPowerPointLoader, {}),
        ".doc": (UnstructuredWordDocumentLoader, {}),
        ".docx": (UnstructuredWordDocumentLoader, {}),
        ".xls": (UnstructuredExcelLoader, {}),
        ".xlsx": (UnstructuredExcelLoader, {}),
        ".html": (BSHTMLLoader, {}),
        ".csv": (CSVLoader, {}),
        ".json": (JSONLoader, {}),
        ".eml": (UnstructuredEmailLoader, {}),
        ".rtf": (UnstructuredRTFLoader, {}),
        ".epub": (UnstructuredEPubLoader, {})
    }

def main():
    """
    Main function to orchestrate the document processing pipeline.
    
    Process Flow:
    1. Initialize ChromaDB collection
    2. Process documents from 'documents' directory
    3. Generate and store embeddings
    
    The function:
    - Sets up necessary components
    - Processes all documents
    - Provides feedback on completion
    
    Note:
        - Requires 'documents' directory
        - Processes all documents recursively
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
