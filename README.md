# Local Document Chat with Ollama

This project is a simple example of creating a local chat interface for your documents using a local Ollama LLM. It contains utilities that allow the exploration of each step in the process of generating local embeddings, storing them, and using them for document retrieval and question answering.

## Overview

The project demonstrates the key components of a RAG (Retrieval-Augmented Generation) system:
1. Document processing and embedding generation
2. Vector storage and retrieval
3. LLM-powered question answering

## Utility Programs

### Document Processing and Exploration

#### `show_chunks.py`
Demonstrates how documents are split into chunks:
- Shows different chunking strategies (recursive, character, token-based)
- Displays chunk boundaries and overlap
- Helps understand how documents are prepared for embedding
```bash
python show_chunks.py your_document.pdf
```

#### `show_tokens.py`
Explores how text is tokenized:
- Shows how different models tokenize text
- Displays token IDs and their text
- Helps understand token-based text processing
```bash
python show_tokens.py "Your text here"
```

### Core RAG Components

#### `make_chroma_vectorstore.py`
Processes documents and creates the vector database:
- Loads PDF documents from a directory
- Splits them into semantic chunks
- Generates embeddings using Ollama's nomic-embed-text
- Stores everything in a ChromaDB database
```bash
python make_chroma_vectorstore.py
```

#### `chat_with_docs.py`
Interactive chat interface for document Q&A:
- Retrieves relevant document chunks
- Uses Ollama LLM for response generation
- Provides conversational interface
```bash
python chat_with_docs.py mistral
```

#### `read_embeddings.py`
Utility to inspect the vector database:
- Shows stored documents and their metadata
- Displays embedding statistics
- Helps verify document processing
```bash
python read_embeddings.py
```

## Setup

1. **Install Dependencies**
```bash
pip install langchain-community langchain-ollama chromadb
```

2. **Install Ollama**
- Install from [Ollama's website](https://ollama.ai)
- Pull required models:
```bash
ollama pull nomic-embed-text  # for embeddings
ollama pull mistral           # or any other model for chat
```

3. **Prepare Documents**
```bash
mkdir documents
# Add your PDF files to the 'documents' directory
```

## Learning Path

1. Start by exploring document chunking:
   ```bash
   python show_chunks.py sample.pdf
   ```

2. Understand tokenization:
   ```bash
   python show_tokens.py "Sample text to tokenize"
   ```

3. Process your documents:
   ```bash
   python make_chroma_vectorstore.py
   ```

4. Inspect the results:
   ```bash
   python read_embeddings.py
   ```

5. Start chatting with your documents:
   ```bash
   python chat_with_docs.py mistral
   ```

## Project Structure
```
.
├── README.md
├── show_chunks.py            # Document chunking demonstration
├── show_tokens.py           # Tokenization exploration
├── make_chroma_vectorstore.py # Vector database creation
├── chat_with_docs.py        # Interactive chat interface
├── read_embeddings.py       # Database inspection tool
├── documents/               # Your PDF files
└── chromadb/               # Vector database storage
```

## Technical Details

### Document Processing
- Chunk size: 1000 characters
- Chunk overlap: 200 characters
- Embedding model: nomic-embed-text
- Vector similarity: Cosine similarity

### Requirements

#### Python Packages
- Python 3.x
- langchain-community
- langchain-ollama
- chromadb

#### Local Installation
- Ollama (running locally)

#### Required Models
- nomic-embed-text (for generating embeddings)
- At least one LLM model for querying (e.g., mistral, llama2, or neural-chat)

## Notes
- This is an educational project to understand RAG systems
- Each utility can be used independently to explore different aspects
- Great starting point for building more complex document Q&A systems
- All processing is done locally for privacy and learning purposes 