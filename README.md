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
└── chat_with_docs.py  # Main chat interface
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

## License

MIT License 