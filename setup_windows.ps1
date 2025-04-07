# Setup script for Local RAG Demo
# This script automates the setup process for Windows users

# Scripts Overview:
# 1. make_chroma_vectorstore.py
#    - Creates a vector store database using ChromaDB for RAG systems
#    - Handles document loading, text chunking, embedding generation, and storage
#    - Usage: python make_chroma_vectorstore.py [--chunk_size 1000] [--chunk_overlap 200]
#
# 2. chat_with_docs.py
#    - Implements a RAG chatbot that answers questions about your documents
#    - Uses ChromaDB for document retrieval and Ollama's LLM models for responses
#    - Usage: python chat_with_docs.py [--model mistral:7b-4bit] [--num_docs 3]
#
# 3. show_chunks.py
#    - Demonstrates different text chunking strategies
#    - Shows how text is broken down into manageable pieces
#    - Usage: python show_chunks.py input.txt [--method recursive|character|token]
#
# 4. show_tokens.py
#    - Shows how text is broken into tokens using tiktoken
#    - Supports different encodings (cl100k_base, p50k_base, r50k_base)
#    - Usage: python show_tokens.py "text" [--encoding cl100k_base]
#
# 5. read_embeddings.py
#    - Reads and displays document embeddings from ChromaDB
#    - Shows document content previews and metadata
#    - Usage: python read_embeddings.py
#
# Recommended Workflow:
# 1. Run this setup script
# 2. Activate the environment (conda activate local_rag_demo)
# 3. Place documents in the 'documents' directory
# 4. Run make_chroma_vectorstore.py to create embeddings
# 5. (Optional) Use show_chunks.py, show_tokens.py, or read_embeddings.py to analyze
# 6. Run chat_with_docs.py to interact with your documents

# Function to check if a command exists
function Test-Command($Command) {
    return [bool](Get-Command -Name $Command -ErrorAction SilentlyContinue)
}

# Function to check if Python is installed
function Test-PythonInstalled {
    try {
        $pythonVersion = python --version
        if ($pythonVersion -match "Python 3\.(1[0-2]|[0-9])") {
            Write-Host "Python 3.10 or higher is installed: $pythonVersion"
            return $true
        } else {
            Write-Host "Python 3.10 or higher is required. Found: $pythonVersion"
            return $false
        }
    } catch {
        Write-Host "Python is not installed or not in PATH"
        return $false
    }
}

# Function to check if Conda is installed
function Test-CondaInstalled {
    try {
        $condaVersion = conda --version 2>&1
        if ($condaVersion) {
            return $true
        }
        return $false
    }
    catch {
        return $false
    }
}

# Function to check if Ollama is installed
function Test-OllamaInstalled {
    try {
        $ollamaVersion = ollama --version 2>&1
        if ($ollamaVersion) {
            return $true
        }
        return $false
    }
    catch {
        return $false
    }
}

# Function to check if 7-Zip is installed
function Test-7ZipInstalled {
    try {
        $7zipVersion = 7z --version 2>&1
        if ($7zipVersion) {
            return $true
        }
        return $false
    }
    catch {
        return $false
    }
}

# Function to download and extract magic files
function Setup-MagicFiles {
    Write-Host "Setting up magic files..."
    
    # Create magic directory if it doesn't exist
    $magicDir = Join-Path $env:USERPROFILE "local_rag_demo_venv\Scripts\Lib\site-packages\magic"
    if (-not (Test-Path $magicDir)) {
        New-Item -ItemType Directory -Force -Path $magicDir | Out-Null
    }
    
    # Create DLLs directory if it doesn't exist
    $dllsDir = Join-Path $env:USERPROFILE "local_rag_demo_venv\Scripts\DLLs"
    if (-not (Test-Path $dllsDir)) {
        New-Item -ItemType Directory -Force -Path $dllsDir | Out-Null
    }
    
    Write-Host "Downloading magic files..."
    
    # Create temporary directory
    $tempDir = Join-Path $env:TEMP "magic_setup"
    if (Test-Path $tempDir) {
        Remove-Item -Path $tempDir -Recurse -Force
    }
    New-Item -ItemType Directory -Force -Path $tempDir | Out-Null
    
    # Download URL for magic files
    $downloadUrl = "https://github.com/pidydx/libmagicwin64/releases/download/5.39/magic.zip"
    
    Write-Host "Attempting download with curl..."
    try {
        # Try using curl first
        curl.exe -L -k $downloadUrl -o "$tempDir\magic.zip"
        if ($LASTEXITCODE -ne 0) {
            throw "curl download failed"
        }
    }
    catch {
        Write-Host "curl download failed, trying PowerShell..."
        try {
            # Fallback to PowerShell download
            [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
            Invoke-WebRequest -Uri $downloadUrl -OutFile "$tempDir\magic.zip"
        }
        catch {
            Write-Host "Download failed. Please download manually from:"
            Write-Host "https://github.com/pidydx/libmagicwin64/releases/download/5.39/magic.zip"
            Write-Host "`nAfter downloading:"
            Write-Host "1. Extract the zip file"
            Write-Host "2. Copy magic.dll to: $dllsDir"
            Write-Host "3. Copy magic.mgc to: $magicDir"
            return
        }
    }
    
    Write-Host "Download completed successfully."
    Write-Host "Extracting magic files..."
    
    try {
        if (Test-7ZipInstalled) {
            # Use 7-Zip if available
            Write-Host "Using 7-Zip to extract files..."
            Set-Location $tempDir
            & 7z x magic.zip -y
        }
        else {
            # Use PowerShell's Expand-Archive
            Write-Host "Using PowerShell to extract files..."
            Expand-Archive -Path "$tempDir\magic.zip" -DestinationPath $tempDir -Force
        }
        
        # Verify files exist
        if (-not (Test-Path "$tempDir\magic.dll") -or -not (Test-Path "$tempDir\magic.mgc")) {
            throw "Required files not found in extracted archive"
        }
        
        # Copy files to their destinations
        Copy-Item "$tempDir\magic.dll" $dllsDir -Force
        Copy-Item "$tempDir\magic.mgc" $magicDir -Force
        
        Write-Host "Magic files setup completed successfully."
    }
    catch {
        Write-Host "Failed to extract files. Please download and extract manually."
        Write-Host "Error details: $_"
        Write-Host "`nManual steps:"
        Write-Host "1. Download from: https://github.com/pidydx/libmagicwin64/releases/download/5.39/magic.zip"
        Write-Host "2. Extract the zip file"
        Write-Host "3. Copy magic.dll to: $dllsDir"
        Write-Host "4. Copy magic.mgc to: $magicDir"
    }
    finally {
        # Clean up temporary directory
        if (Test-Path $tempDir) {
            Remove-Item -Path $tempDir -Recurse -Force
        }
    }
}

# Function to install Ollama
function Install-Ollama {
    Write-Host "`nInstalling Ollama..."
    
    # Download Ollama installer
    $installerUrl = "https://ollama.com/download/OllamaSetup.exe"
    $installerPath = "OllamaSetup.exe"
    
    Write-Host "Downloading Ollama installer..."
    try {
        Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath
    } catch {
        Write-Host "Failed to download Ollama installer. Please download manually from: $installerUrl"
        Write-Host "After downloading, run the installer and restart your computer."
        return $false
    }
    
    # Run the installer
    Write-Host "Running Ollama installer..."
    try {
        Start-Process -FilePath $installerPath -Wait
    } catch {
        Write-Host "Failed to run Ollama installer. Please run it manually."
        return $false
    }
    
    # Clean up
    Remove-Item $installerPath -Force
    
    Write-Host "`nOllama has been installed. Please follow these steps:"
    Write-Host "1. Close and reopen PowerShell"
    Write-Host "2. Open a new PowerShell window as Administrator"
    Write-Host "3. Run 'ollama serve'"
    Write-Host "4. In another terminal, run 'ollama pull mistral:7b-4bit'"
    Write-Host "`nNote: You may need to restart your computer after installation."
    Write-Host "Important: The Ollama installation and model download may take quite a while,"
    Write-Host "especially on slower connections. The initial model download (mistral:7b-4bit)"
    Write-Host "is approximately 4GB and may take 10-30 minutes depending on your internet speed."
    
    return $true
}

# Function to install Conda
function Install-Conda {
    Write-Host "`nInstalling Miniconda..."
    
    # Download Miniconda installer
    $installerUrl = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe"
    $installerPath = "Miniconda3-latest-Windows-x86_64.exe"
    
    Write-Host "Downloading Miniconda installer..."
    try {
        Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath
    } catch {
        Write-Host "Failed to download Miniconda installer. Please download manually from: $installerUrl"
        Write-Host "After downloading, run the installer and restart your computer."
        return $false
    }
    
    # Run the installer silently
    Write-Host "Running Miniconda installer..."
    try {
        Start-Process -FilePath $installerPath -ArgumentList "/S /D=$env:USERPROFILE\miniconda3" -Wait
    } catch {
        Write-Host "Failed to run Miniconda installer. Please run it manually."
        return $false
    }
    
    # Clean up
    Remove-Item $installerPath -Force
    
    # Add Conda to PATH for current session
    $env:Path = "$env:USERPROFILE\miniconda3;$env:USERPROFILE\miniconda3\Scripts;$env:USERPROFILE\miniconda3\Library\bin;$env:Path"
    
    Write-Host "`nMiniconda has been installed. Please follow these steps:"
    Write-Host "1. Close and reopen PowerShell"
    Write-Host "2. Run the setup script again"
    
    return $true
}

# Main setup process
Write-Host "Starting Local RAG Demo setup..."

# Check Python installation
if (-not (Test-PythonInstalled)) {
    Write-Host "Please install Python 3.10 or higher and try again."
    exit 1
}

# Check Conda installation
if (-not (Test-CondaInstalled)) {
    Write-Host "Conda not found. Attempting to install..."
    if (Install-Conda) {
        Write-Host "Conda installation successful. Please close and reopen PowerShell, then run this script again."
        exit 0
    } else {
        Write-Host "Conda installation failed. Please install manually and try again."
        exit 1
    }
}

# Create Conda environment
Write-Host "`nCreating Conda environment..."
conda create -n local_rag_demo python=3.10 -y

# Activate environment and install dependencies
Write-Host "`nActivating environment and installing dependencies..."
conda activate local_rag_demo
pip install -r requirements.txt

# Check Ollama installation
if (-not (Test-OllamaInstalled)) {
    Install-Ollama
}

# Create required directories
Write-Host "`nCreating required directories..."
New-Item -ItemType Directory -Force -Path "documents"
New-Item -ItemType Directory -Force -Path "chromadb"

# Setup magic files
Setup-MagicFiles

Write-Host "`nSetup complete! Next steps:"
Write-Host "1. Activate the environment: conda activate local_rag_demo"
Write-Host "2. Place your documents in the 'documents' directory"
Write-Host "3. Create the vector store: python make_chroma_vectorstore.py"
Write-Host "4. Start the chat interface: python chat_with_docs.py"
Write-Host "`nFor more information about the scripts and their usage, see the comments at the top of this file."