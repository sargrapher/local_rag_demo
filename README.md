# Local RAG Demo with Docker

This project demonstrates a Retrieval-Augmented Generation (RAG) application using Docker, Ollama, and ChromaDB. The application processes documents, creates embeddings, and stores them in a vector database for efficient retrieval.

## Quick Start

1. **Docker Setup**
   - Follow the detailed instructions in [DOCKER_SETUP.md](DOCKER_SETUP.md)
   - Or use these basic commands:
     ```bash
     # Build and start
     docker-compose up --build
     
     # Start chat interface (in new terminal)
     docker-compose exec app python3 chat_with_docs.py
     ```

2. **Manual Setup**
   - Install dependencies from `requirements.txt`
   - Run `make_chroma_vectorstore.py` to process documents
   - Start `chat_with_docs.py` to interact with documents

## Prerequisites

- Docker and Docker Compose installed
- Ollama installed and running on the host machine
- At least 8GB of RAM recommended
- Sufficient disk space for document storage and vector database

## Documentation

- [DOCKER_SETUP.md](DOCKER_SETUP.md) - Detailed Docker setup and usage guide
- [SETUP.md](SETUP.md) - Manual setup instructions
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contributing guidelines

## Features

- Local document processing
- Multiple LLM support through Ollama
- Interactive chat interface
- No cloud dependencies
- Support for various document formats

## Project Structure

```
local_rag_demo/
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
├── documents/             # Directory for input documents
├── chromadb/             # Directory for vector database
└── *.py                  # Python scripts for processing
```

## Configuration

The application can be configured through environment variables in `docker-compose.yml`:

- `OLLAMA_HOST`: URL of the Ollama service (default: http://localhost:11434)

## Troubleshooting

1. **Port Conflicts**
   - If port 11434 is already in use:
     ```bash
     # Check if Ollama is already running
     ps aux | grep ollama
     
     # If Ollama is running, you can use it directly
     # If not, stop any process using the port
     sudo lsof -i :11434
     sudo kill <PID>
     ```

2. **Permission Issues**
   - If you encounter permission errors:
     ```bash
     sudo usermod -aG docker $USER
     newgrp docker
     ```

3. **Container Issues**
   - To clean up and start fresh:
     ```bash
     docker-compose down -v
     docker system prune -f
     ```

4. **Ollama Connection Issues**
   - Ensure Ollama is running before starting the container
   - Check Ollama status:
     ```bash
     ollama list
     ```
   - If needed, pull the required model:
     ```bash
     ollama pull llama2
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

## Success Indicators

When the application runs successfully, you should see:
1. Documents being processed: `Processed: documents/<filename>`
2. Embeddings being added: `Add of existing embedding ID: doc_X`
3. Final confirmation: `Successfully added X embeddings to ChromaDB`
4. Exit code 0 indicating successful completion

## Notes

- The application uses the host network mode to communicate with Ollama
- Documents are processed and stored in the `chromadb` directory
- The vector database persists between runs
- Make sure Ollama is running before starting the application

## Security Considerations

- The application runs with host network mode for simplicity
- In production, consider using a more restricted network configuration
- Ensure proper access controls for the documents directory
- Keep Ollama updated for security patches

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License