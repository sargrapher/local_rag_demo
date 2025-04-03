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

## Next Steps

1. Place your documents in the `documents` directory
2. Create the vector store:
   ```bash
   python make_chroma_vectorstore.py
   ```
3. Start the chat interface:
   ```bash
   python chat_with_docs.py
   ```

## Support

For issues or questions:
1. Check the troubleshooting guide
2. Review the code documentation
3. Open an issue on GitHub 