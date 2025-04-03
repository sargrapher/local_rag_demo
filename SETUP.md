# Setup Guide for Local RAG Demo

## System Requirements

### Prerequisites
- Python 3.10 or higher
- Git
- At least 8GB RAM (16GB recommended)
- At least 10GB free disk space

### Optional but Recommended
- Conda for dependency management
- 7-Zip for better file extraction support

## Platform-Specific Dependencies

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y build-essential python3-dev
```

### Windows
1. Install Microsoft Visual C++ Build Tools:
   - Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Run the installer
   - Select "Desktop development with C++"
   - Install

2. Install Magic Binary:
   - The setup script will handle this automatically
   - If manual installation is needed, download from: https://github.com/pidydx/libmagicwin64/releases/download/5.39/magic.zip
   - Extract and copy files to the appropriate locations

3. Install Ollama:
   - Download from: https://ollama.com/download/OllamaSetup.exe
   - Run the installer
   - After installation, close and reopen PowerShell
   - Open a new PowerShell window as Administrator
   - Run `ollama serve`
   - In another terminal, run `ollama pull mistral:7b-4bit`
   - Note: You may need to restart your computer after installation
   - **Important:** The Ollama installation and model download may take quite a while, especially on slower connections. The initial model download (mistral:7b-4bit) is approximately 4GB and may take 10-30 minutes depending on your internet speed.

## Complete Setup Guide

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/local_rag_demo.git
cd local_rag_demo
```

### 2. Set Up Python Environment

#### Option A: Using Conda (Recommended)
```bash
# Create and activate Conda environment
conda create -n local_rag_demo python=3.10 -y
conda activate local_rag_demo

# Install dependencies
pip install -r requirements.txt
```

#### Option B: Using venv
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Install System Dependencies

#### Windows
Run the setup script:
```powershell
.\setup_windows.ps1
```

#### Linux
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y build-essential python3-dev
```

### 4. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 5. Download Required Models
```bash
# Pull the Mistral model
ollama pull mistral:7b-4bit
```

### 6. Create Required Directories
```bash
# Linux/macOS
mkdir -p documents chromadb

# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path "documents"
New-Item -ItemType Directory -Force -Path "chromadb"
```

### 7. Set Up Ollama
1. Start Ollama service:
   ```bash
   # Windows (PowerShell as Administrator)
   ollama serve

   # Linux/macOS
   sudo systemctl start ollama
   ```

2. Verify Ollama is running:
   ```bash
   curl http://localhost:11434/api/version
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

## Troubleshooting

### Common Issues

1. Permission Issues with pip:
   ```bash
   # Try using --user flag
   pip install --user -r requirements.txt
   
   # Or use sudo (Linux/macOS)
   sudo pip install -r requirements.txt
   ```

2. Ollama Address Already in Use:
   ```bash
   # Find the process using port 11434
   netstat -ano | findstr :11434  # Windows
   lsof -i :11434  # Linux/macOS
   
   # Kill the process
   taskkill /PID <PID> /F  # Windows
   kill -9 <PID>  # Linux/macOS
   ```

3. Magic Binary Issues:
   - Ensure magic.dll is in the correct location
   - Check file permissions
   - Try reinstalling the magic binary

### Windows-Specific Issues

1. Visual C++ Build Tools:
   - Ensure "Desktop development with C++" is installed
   - Try repairing the installation if issues persist

2. Magic Binary:
   - The setup script should handle this automatically
   - If manual installation is needed, follow the instructions in the Windows section

3. Ollama Installation:
   - Run PowerShell as Administrator
   - Ensure Windows Defender or antivirus isn't blocking the installation
   - Try running `ollama serve` in a new PowerShell window as Administrator

4. Python Environment:
   - If using venv, ensure the activation script is run
   - Check PATH environment variable includes Python and pip

## Support

For issues or questions:
1. Check the troubleshooting guide
2. Review the code documentation
3. Open an issue on GitHub 