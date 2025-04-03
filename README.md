# Local RAG Demo

A local RAG (Retrieval Augmented Generation) system using Ollama and ChromaDB. This project allows you to chat with your documents locally, without any cloud dependencies.

## Features

- Local document processing
- Multiple LLM support through Ollama
- Interactive chat interface
- No cloud dependencies
- Support for various document formats

## Quick Start

1. Place your documents in the `documents` directory
2. Run the vector store creation script:
   ```bash
   python make_chroma_vectorstore.py
   ```
3. Start the chat interface:
   ```bash
   python chat_with_docs.py
   ```

## Project Structure

```
local_rag_demo/
├── documents/          # Place your documents here
├── chromadb/          # Vector store database
├── setup_windows.ps1  # Windows setup script
├── make_chroma_vectorstore.py  # Creates the vector store
├── chat_with_docs.py  # Main chat interface
├── show_chunks.py     # Demonstrates text chunking
├── show_tokens.py     # Shows tokenization
└── read_embeddings.py # Inspects stored embeddings
```

## Supported Models

The following Ollama models are supported:
- `mistral:7b-4bit` (recommended)
- `llama2`
- `neural-chat`
- `deepseek-r1`
- `nomic-embed-text`

## Setup

For detailed setup instructions, see [SETUP.md](SETUP.md). Alternatively, you can use the automated setup script:

### Windows
```powershell
.\setup_windows.ps1
```

This script will handle the installation of dependencies and setup of the environment automatically.

> **Note:** The Ollama installation and model download may take quite a while, especially on slower connections. The initial model download (mistral:7b-4bit) is approximately 4GB and may take 10-30 minutes depending on your internet speed.

### After Setup

If you used Conda for the setup:
```bash
# Activate the Conda environment
conda activate local_rag_demo
```

If you used venv:
```bash
# On Windows
.\venv\Scripts\activate

# On Linux/macOS
source venv/bin/activate
```

## Scripts Overview

### 1. make_chroma_vectorstore.py
**Description:** Creates a vector store database using ChromaDB for RAG systems. It handles document loading, text chunking, embedding generation, and storage.

**Process Flow:**
1. Document Loading: Recursively finds all supported files in the specified directory
2. Text Processing: Splits documents into manageable chunks with overlap
3. Embedding Generation: Converts text chunks to vector embeddings using Ollama's nomic-embed-text model
4. Vector Storage: Stores embeddings in ChromaDB with metadata

**Usage:**
```bash
# Basic usage
python make_chroma_vectorstore.py

# With custom chunk size and overlap
python make_chroma_vectorstore.py --chunk_size 1000 --chunk_overlap 200
```

### 2. chat_with_docs.py
**Description:** Implements a Retrieval-Augmented Generation (RAG) chatbot that answers questions about your documents by combining document retrieval with LLM-powered response generation.

**Architecture:**
1. Document Retrieval: Uses ChromaDB for semantic search
2. Response Generation: Uses Ollama's LLM models for context-aware responses

**Usage:**
```bash
# Default model (mistral:7b-4bit)
python chat_with_docs.py

# With specific model
python chat_with_docs.py --model llama2

# Adjust number of documents to retrieve
python chat_with_docs.py --num_docs 5
```

**Interactive Commands:**
- 'quit' or 'exit': End the chat session
- Empty input: Skipped
- Any other input: Processed as a question

### 3. show_chunks.py
**Description:** Demonstrates different text chunking strategies used in RAG systems, showing how text is broken down into smaller, manageable pieces while preserving context.

**Chunking Strategies:**
1. Recursive Character Splitting: Most sophisticated, splits on natural boundaries
2. Character-Based Splitting: Simple approach that splits on character count
3. Token-Based Splitting: Splits based on token count for LLM context windows

**Usage:**
```bash
# Basic usage
python show_chunks.py input.txt

# With specific chunking method
python show_chunks.py --method recursive input.txt
python show_chunks.py --method character --chunk_size 500 input.txt
python show_chunks.py --method token --chunk_size 1000 --chunk_overlap 200 input.txt
```

### 4. show_tokens.py
**Description:** Demonstrates how text is broken into tokens using OpenAI's tiktoken library, supporting different encodings used by various GPT models.

**Available Encodings:**
- cl100k_base: Used by GPT-4, GPT-3.5-turbo
- p50k_base: Used by GPT-3 models like davinci
- r50k_base: Used by older GPT-3 models

**Usage:**
```bash
# Default encoding (cl100k_base)
python show_tokens.py "Your text here"

# Specific encoding
python show_tokens.py --encoding p50k_base "Your text here"
```

### 5. read_embeddings.py
**Description:** Reads and displays document embeddings stored in a ChromaDB collection, helping to inspect the embedded documents in your vector store.

**Key Features:**
- Connects to a persistent ChromaDB instance
- Retrieves all documents and their associated metadata
- Displays document content previews and metadata
- Shows total document count in the collection

**Usage:**
```bash
# Simply run the script
python read_embeddings.py
```

## Recommended Workflow

1. **Setup Environment:**
   - Run `setup_windows.ps1` to set up the environment and dependencies
   - Activate the environment (Conda or venv)

2. **Prepare Documents:**
   - Place documents in the `documents` directory

3. **Create Vector Store:**
   - Run `make_chroma_vectorstore.py` to process documents and create embeddings

4. **Analyze Documents (Optional):**
   - Use `show_chunks.py` to see how documents are chunked
   - Use `show_tokens.py` to understand tokenization
   - Use `read_embeddings.py` to inspect the stored embeddings

5. **Start Chat Interface:**
   - Run `chat_with_docs.py` to interact with your documents
   - Ask questions about the content of your documents

## License

MIT License 