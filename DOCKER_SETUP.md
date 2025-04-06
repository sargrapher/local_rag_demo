# Docker Setup Guide for Local RAG Demo

This guide provides detailed instructions for setting up and running the Local RAG Demo using Docker.

## Prerequisites

- Docker installed
- Docker Compose installed
- Ollama installed and running
- At least 8GB of RAM
- Sufficient disk space (at least 10GB recommended)

## Initial Setup

1. **Install Docker and Docker Compose**
   ```bash
   # For Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install docker.io docker-compose
   
   # Add your user to the docker group
   sudo usermod -aG docker $USER
   newgrp docker
   ```

2. **Verify Docker Installation**
   ```bash
   # Check Docker version
   docker --version
   
   # Check Docker Compose version
   docker-compose --version
   
   # Verify Docker is running
   docker ps
   ```

3. **Install and Configure Ollama**
   ```bash
   # Install Ollama (if not already installed)
   curl https://ollama.ai/install.sh | sh
   
   # Start Ollama service
   ollama serve
   
   # Pull the required model
   ollama pull llama2
   
   # Verify Ollama is running
   ollama list
   ```

## Project Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd local_rag_demo
   ```

2. **Prepare Documents**
   ```bash
   # Create documents directory
   mkdir -p documents
   
   # Copy your documents
   cp /path/to/your/documents/* documents/
   ```

## Running the Application

1. **Ensure Ollama is Running**
   ```bash
   # Check if Ollama is running
   ps aux | grep ollama
   
   # If not running, start it
   ollama serve
   ```

2. **Build and Start the Container**
   ```bash
   # Build and start the container
   docker-compose up --build
   ```

   This will:
   - Build the Docker image
   - Process documents in the `documents` directory
   - Create embeddings
   - Store them in ChromaDB

3. **Verify the Setup**
   ```bash
   # Check if the container is running
   docker ps
   
   # Check container logs
   docker-compose logs -f
   ```

   Successful output should show:
   - Document processing messages
   - Embedding creation messages
   - "Successfully added X embeddings to ChromaDB"
   - Exit code 0

## Using the Application

1. **Start the Chat Interface**
   ```bash
   # In a new terminal
   docker-compose exec app python3 chat_with_docs.py
   ```

2. **Interact with Documents**
   - Type your questions
   - The system will search documents and generate responses
   - Type 'quit' or 'exit' to end the session

3. **View Document Chunks**
   ```bash
   docker-compose exec app python3 show_chunks.py documents/your_document.txt
   ```

4. **Inspect Embeddings**
   ```bash
   docker-compose exec app python3 read_embeddings.py
   ```

## Troubleshooting

1. **Container Issues**
   ```bash
   # Clean up containers and volumes
   docker-compose down -v
   
   # Remove unused images
   docker system prune -f
   
   # Rebuild and start
   docker-compose up --build
   ```

2. **Ollama Connection Issues**
   - Ensure Ollama is running before starting the container
   - Check Ollama status: `ollama list`
   - Verify model is pulled: `ollama pull llama2`
   - Check Ollama logs: `journalctl -u ollama`

3. **Permission Issues**
   ```bash
   # Add user to docker group
   sudo usermod -aG docker $USER
   newgrp docker
   
   # Fix volume permissions
   sudo chown -R $USER:$USER .
   ```

4. **Port Conflicts**
   ```bash
   # Check if port 11434 is in use
   sudo lsof -i :11434
   
   # Stop conflicting process
   sudo kill <PID>
   ```

## Common Commands

```bash
# Start the application
docker-compose up --build

# Stop the application
docker-compose down

# View logs
docker-compose logs -f

# Clean up resources
docker-compose down -v
docker system prune -f

# Check Ollama status
ollama list

# Pull required model
ollama pull llama2
```

## Configuration Files

1. **docker-compose.yml**
   ```yaml
   version: '3.8'
   services:
     app:
       build: .
       volumes:
         - ./documents:/app/documents
         - ./chromadb:/app/chromadb
       environment:
         - OLLAMA_HOST=http://localhost:11434
   ```

2. **Dockerfile**
   ```dockerfile
   FROM python:3.12-slim
   RUN apt-get update && apt-get install -y \
       build-essential \
       python3-dev \
       libmagic1
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   RUN mkdir -p /app/documents /app/chromadb
   COPY . .
   ENV PYTHONUNBUFFERED=1
   CMD ["python3", "make_chroma_vectorstore.py"]
   ```

## Managing the Application

1. **Stop the Application**
   ```bash
   sudo docker-compose down
   ```

2. **Clean Up Resources**
   ```bash
   # Remove containers and volumes
   sudo docker-compose down -v
   
   # Clean up unused resources
   sudo docker system prune -f
   ```

3. **Update Documents**
   - Add new files to the `documents` directory
   - Run `sudo docker-compose up --build` to process them

## Best Practices

1. **Resource Management**
   - Monitor system resources
   - Clean up unused containers
   - Keep documents organized

2. **Document Organization**
   - Use meaningful filenames
   - Avoid extremely large files
   - Keep related documents together

3. **Security**
   - Keep Docker updated
   - Use secure document permissions
   - Monitor container logs

## Common Commands Reference

```bash
# Start application
sudo docker-compose up --build

# Stop application
sudo docker-compose down

# View logs
sudo docker-compose logs -f

# Clean up
sudo docker-compose down -v
sudo docker system prune -f

# Execute commands in container
sudo docker-compose exec app <command>

# Check container status
sudo docker ps

# View container logs
sudo docker logs <container_id>
```

## Notes

- The application uses host network mode for simplicity
- Documents are processed and stored in the `chromadb` directory
- The vector database persists between runs
- Make sure to clean up resources when not in use 