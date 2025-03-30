# Qwen Document Embeddings

This project uses the GTE-Qwen2-7B-instruct model to generate embeddings for documents and store them in ChromaDB for semantic search.

## System Requirements

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install build-essential libpoppler-cpp-dev pkg-config python-dev-is-python3
```

### Windows
- Install Microsoft Visual C++ Build Tools
- Install Magic Binary from https://github.com/pidydx/libmagicwin64

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

Basic usage with default model (Mistral):
```bash
python chat_with_docs.py
```

Use a different model:
```bash
python chat_with_docs.py llama2
python chat_with_docs.py neural-chat
```

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