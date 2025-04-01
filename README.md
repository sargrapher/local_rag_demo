# Qwen Document Embeddings

This project uses the GTE-Qwen2-7B-instruct model to generate embeddings for documents and store them in ChromaDB for semantic search. It supports various document types and provides flexible text chunking options.

## What is this for?

This is a local Retrieval-Augmented Generation (RAG) system that allows you to:
- Process and understand your documents locally without sending data to external services
- Create semantic search capabilities across your document collection
- Ask questions about your documents and get accurate, contextual answers
- Analyze relationships and patterns across multiple documents
- Work with various document formats (PDF, Word, Text, etc.) in a unified way

Key Features:
- 🔒 **Fully Local**: All processing happens on your machine, ensuring data privacy
- 📚 **Multiple Document Types**: Support for text, PDF, Word, PowerPoint, and more
- 🔍 **Smart Search**: Uses advanced embeddings for semantic understanding
- 🧩 **Flexible Chunking**: Multiple methods to split documents optimally
- 💬 **Interactive Chat**: Natural conversation interface with your documents
- 🚀 **Easy Setup**: Simple installation with clear instructions

Perfect for:
- Researchers analyzing large collections of papers or documents
- Students studying complex texts or course materials
- Professionals managing technical documentation
- Anyone wanting to build a personal knowledge base

## System Requirements

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install build-essential libpoppler-cpp-dev pkg-config python-dev-is-python3
```

### Windows
- Install Microsoft Visual C++ Build Tools
- Install Magic Binary from https://github.com/pidydx/libmagicwin64

## Complete Setup Guide

1. Create and activate conda environment:
```bash
conda create -n local_rag_demo python=3.12
conda activate local_rag_demo
```

2. Install system dependencies (if on Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install build-essential libpoppler-cpp-dev pkg-config python-dev-is-python3
```

3. Install Python dependencies:
```bash
# Option 1: Install from requirements.txt
pip install -r requirements.txt

# Option 2: If Option 1 fails, try installing packages individually:
pip install torch transformers chromadb python-magic langchain langchain-community langchain-core langchain-ollama langchain-huggingface tiktoken

# Option 3: If you're having permission issues, use:
python3 -m pip install --user -r requirements.txt
```

Note: If you encounter issues with pip, you might need to:
- Upgrade pip: `python -m pip install --upgrade pip`
- Install packages for your user: `python -m pip install --user -r requirements.txt`
- Or use a virtual environment: `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`

4. Download the required model:
```bash
python download_model.py
```

5. Create the necessary directories:
```bash
mkdir -p documents qwen_db
```

6. Place your documents in the `documents` directory
   Example: Add a text version of the US Constitution:
   ```bash
   # Create or download your document
   curl -o documents/constitution.txt https://raw.githubusercontent.com/username/repo/main/documents/constitution.txt
   ```

7. Create the vector store:
```bash
python make_chroma_vectorstore.py
```

8. Start chatting with your documents:
```bash
python chat_with_docs.py
```

## Document Processing

### Text Chunking

The project uses the nomic-embed-text model for generating document embeddings. This model is optimized for semantic search and provides high-quality embeddings for text documents.

The project supports flexible text chunking with different methods and parameters. You can use the `show_chunks.py` script to preview how your documents will be chunked:

```bash
python show_chunks.py --chunk-size 100 --chunk-overlap 20 --method token documents/constitution.txt
```

Available chunking methods:
- `token`: Token-based chunking using tiktoken
- `character`: Character-based chunking
- `word`: Word-based chunking

Parameters:
- `--chunk-size`: Size of each chunk (default: 100)
- `--chunk-overlap`: Number of tokens/characters/words to overlap between chunks (default: 20)
- `--method`: Chunking method to use (default: token)

### Supported Document Types

The project supports various document types:
- Text files (.txt)
- PDF documents (.pdf)
- Word documents (.docx)
- PowerPoint presentations (.pptx)
- Excel spreadsheets (.xlsx)
- Markdown files (.md)
- RTF documents (.rtf)
- EPUB ebooks (.epub)

## Ollama Setup

1. Install Ollama:
```bash
curl https://ollama.ai/install.sh | sh
```

2. Start the Ollama service (if not already running as a system service):
```bash
ollama serve
```
Note: If you see "address already in use" error, this means Ollama is already running as a system service and you can skip this step.

3. In a new terminal, pull the required models:
```bash
ollama pull mistral:7b-4bit
ollama pull llama2
ollama pull neural-chat
ollama pull deepseek-r1
ollama pull nomic-embed-text  # Required for converting documents into searchable vectors
```

Note: The nomic-embed-text model is essential for the document processing pipeline. It converts your text into numerical vectors that capture semantic meaning, enabling intelligent search and retrieval. Unlike the other models which are used for chat/interaction, nomic-embed-text specifically handles the document understanding and indexing phase.

4. Verify Ollama is running:
```bash
curl http://localhost:11434/api/version
```

## Troubleshooting

### Common Issues

1. If you encounter permission issues with pip:
   ```bash
   python -m pip install --user -r requirements.txt
   ```

2. If you see "address already in use" for Ollama:
   - This means Ollama is already running as a system service
   - You can skip starting the Ollama service

3. If you encounter issues with document processing:
   - Make sure all system dependencies are installed
   - Check that the document is in a supported format
   - Verify the document is not corrupted

4. If you see CUDA-related errors:
   - Make sure you have the correct CUDA version installed
   - Try running with CPU only by setting `CUDA_VISIBLE_DEVICES=""`

### Getting Help

If you encounter any issues:
1. Check the error messages carefully
2. Make sure all dependencies are installed correctly
3. Verify your system meets the requirements
4. Check the project's issue tracker for similar problems

## Installation

1. Clone the repository
2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Creating the Vector Store

Basic usage with default directories:
```bash
python make_chroma_vectorstore.py
```

Specify custom directories:
```bash
python make_chroma_vectorstore.py --docs-dir /path/to/documents --db-path /path/to/database
```

### Chatting with Documents

The chat interface allows you to interact with your documents using natural language queries. It uses semantic search to find relevant information and provides context-aware responses.

Basic usage with default model (Mistral):
```bash
python chat_with_docs.py
```

Use a different model:
```bash
python chat_with_docs.py llama2
python chat_with_docs.py neural-chat
```

Features:
- Natural language queries about your documents
- Context-aware responses with relevant document excerpts
- Support for multiple LLM models
- Interactive chat interface
- Semantic search across all processed documents

Example queries:
- "What does the Constitution say about freedom of speech?"
- "What are the requirements to be President?"
- "What powers does Congress have?"
- "What is the process for amending the Constitution?"

Tips for best results:
1. Ask specific questions about the content
2. Reference specific articles or sections when possible
3. The system will provide relevant excerpts from the documents
4. You can ask follow-up questions to get more details
5. Type 'quit' to exit the chat interface

Note: The quality of responses depends on:
- The relevance of the documents to your question
- The chunking strategy used during document processing
- The LLM model being used
- The context window size of the model

All available options:
```bash
python chat_with_docs.py --help
```

Command line options:
- `--docs-dir`: Directory containing documents to process (default: ./documents)
- `--db-path`: Directory for ChromaDB storage (default: ./qwen_db)
- `--model-path`: Path to the local model files (default: ./models/gte-Qwen2-7B-instruct)

Examples:
```bash
# Process documents from a specific directory
python make_chroma_vectorstore.py --docs-dir /home/user/my_documents

# Store ChromaDB in a custom location
python make_chroma_vectorstore.py --db-path /data/embeddings_db

# Specify both directories
python make_chroma_vectorstore.py --docs-dir /home/user/my_documents --db-path /data/embeddings_db

# Use a different model path
python make_chroma_vectorstore.py --model-path /path/to/custom/model
```

Now you can:
1. Use default locations by running `python make_chroma_vectorstore.py`
2. Specify custom locations using command line arguments
3. See all options with `python make_chroma_vectorstore.py --help`

The script will create any directories that don't exist and provide appropriate feedback. All paths can be either relative or absolute.

The script will:
- Process all documents in the `documents` directory
- Generate embeddings using Qwen2-7B-instruct
- Store the embeddings and document content in `qwen_db`

Supported document types:
- PDF files (*.pdf)
- Word documents (*.doc, *.docx)
- Text files (*.txt)
- Markdown files (*.md)
- ReStructured Text files (*.rst)
- PowerPoint files (*.ppt, *.pptx)
- Excel files (*.xls, *.xlsx)
- HTML files (*.html)
- CSV files (*.csv)
- JSON files (*.json)
- Email files (*.eml)
- RTF files (*.rtf)
- EPUB files (*.epub)

## Directory Structure
```
.
├── README.md
├── make_chroma_vectorstore.py
├── requirements.txt
├── documents/     # Place your documents here
└── qwen_db/       # ChromaDB storage (created automatically)
```

## Technical Details

### Document Processing
- Chunk size: 1000 characters
- Chunk overlap: 200 characters
- Embedding model: nomic-embed-text
  - A specialized model for converting text into high-dimensional vectors
  - Optimized for semantic similarity and information retrieval
  - Creates numerical representations that capture the meaning of text
  - Used to enable semantic search across your documents
  - Allows finding related content even when exact words don't match
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
- Mistral (default) or other LLM model for querying (e.g., llama2, neural-chat)

## Notes
- This is an educational project to understand RAG systems
- Each utility can be used independently to explore different aspects
- Great starting point for building more complex document Q&A systems
- All processing is done locally for privacy and learning purposes

## Initial Setup

1. First, download the model (this is a one-time operation):
```bash
python download_model.py
```
This will download the model files (several GB) to the `./models` directory.

2. After downloading, the script will run completely locally without requiring internet access 