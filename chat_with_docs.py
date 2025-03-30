#!/usr/bin/env python3

"""
Document-based Chat Interface using RAG

This script implements a Retrieval-Augmented Generation (RAG) chatbot that can answer
questions about your documents. It combines document retrieval from a vector store
with LLM-powered response generation.

Architecture:
------------
1. Document Retrieval:
   - Uses ChromaDB as vector store
   - Employs Ollama embeddings for semantic search
   - Retrieves relevant context for each query

2. Response Generation:
   - Uses Ollama's LLM models for generation
   - Grounds responses in retrieved context
   - Maintains conversation flow

Key Features:
------------
- Interactive chat interface
- Semantic search in documents
- Context-aware responses
- Multiple LLM model support
- Persistent document storage
- Configurable chunk retrieval

Usage:
-----
Run with specific model:
    python chat_with_docs.py llama2
    python chat_with_docs.py mistral
    python chat_with_docs.py [model_name]

Interactive Commands:
    'quit' or 'exit': End the chat session
    Empty input: Skipped
    Any other input: Processed as a question

Requirements:
-----------
- chromadb: Vector store for document embeddings
- langchain_ollama: For LLM and embeddings
- Ollama: Running locally with desired models

Note:
----
Ensure documents are pre-embedded in ChromaDB before running this script.
The quality of responses depends on:
- Document content in the database
- Chosen LLM model
- Quality of retrieved context
"""

import sys
import argparse
from chromadb import PersistentClient
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage

def setup_argparse():
    """
    Set up command-line argument parsing for model selection.
    
    Returns:
        argparse.Namespace: Parsed command-line arguments containing:
            - model: Name of the Ollama model to use (defaults to 'mistral')
            
    Example:
        args = setup_argparse()
        model_name = args.model  # e.g., 'mistral', 'llama2', 'neural-chat'
    """
    parser = argparse.ArgumentParser(
        description='Chat with your documents using an Ollama model',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
    %(prog)s              # Uses default model (mistral)
    %(prog)s llama2       # Use llama2 model
    %(prog)s neural-chat  # Use neural-chat model
        '''
    )
    parser.add_argument('model', nargs='?', default='mistral',
                       help='Name of the Ollama model to use (default: mistral)')
    return parser.parse_args()

def get_relevant_context(query, collection, embeddings_model):
    """
    Retrieve relevant context from the document collection based on the query.
    
    Uses semantic search to find the most relevant document chunks for the given query.
    The search process:
    1. Converts query to embedding vector
    2. Finds similar vectors in ChromaDB
    3. Returns concatenated relevant chunks
    
    Args:
        query (str): The user's question
        collection: ChromaDB collection containing document embeddings
        embeddings_model: Model used to convert query to embeddings
    
    Returns:
        str: Concatenated relevant document snippets
        
    Example:
        context = get_relevant_context(
            "What is the capital of France?",
            collection,
            embeddings_model
        )
    """
    # Convert the query into an embedding vector
    query_embedding = embeddings_model.embed_query(query)
    
    # Search the collection for similar documents
    # n_results determines how many relevant documents to retrieve
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )
    
    # Combine the retrieved documents into a single context string
    context = "\n".join(results['documents'][0])
    return context

def generate_response(llm, context, query):
    """
    Generate a response using the LLM based on the context and query.
    
    The function:
    1. Creates a system message to control response behavior
    2. Combines context and query into a human message
    3. Gets LLM response based on both messages
    
    Args:
        llm: The language model (Ollama)
        context (str): Retrieved relevant document snippets
        query (str): The user's question
    
    Returns:
        str: The LLM's response
        
    Note:
        The system message ensures responses are grounded in the provided context
        and prevents hallucination or making up information.
    """
    # Define the system message that controls the LLM's behavior
    system_message = """You are a helpful assistant that only answers questions based on the provided context. 
    If you cannot find the answer in the context, say "I cannot answer this question based on the available documents."
    Do not make up or infer information that is not directly supported by the context."""
    
    # Combine context and query into a human message
    human_message = f"""Context: {context}

    Question: {query}"""
    
    # Create the message list in the format expected by the chat model
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=human_message)
    ]
    
    # Get response from LLM using invoke
    response = llm.invoke(messages)
    return response.content

def main():
    """
    Main function to run the interactive chat loop.
    
    The function:
    1. Sets up the RAG system components:
       - ChromaDB client and collection
       - Embedding model for semantic search
       - LLM model for response generation
    2. Runs an interactive chat loop
    3. Handles user input and generates responses
    
    Flow:
    1. User inputs question
    2. System retrieves relevant context
    3. LLM generates response using context
    4. Response is displayed to user
    
    The loop continues until user types 'quit' or 'exit'
    
    Note:
        - ChromaDB collection must exist and be populated
        - Ollama must be running with requested model
    """
    # Parse command line arguments
    args = setup_argparse()
    
    # Initialize ChromaDB client with persistent storage
    chroma_client = PersistentClient(path="./chromadb")
    
    # Get or create the collection of document embeddings
    # This collection must be populated with documents before running this script
    collection = chroma_client.get_collection(name="document_embeddings")
    
    # Initialize the embedding model and chat model
    embeddings_model = OllamaEmbeddings(model="nomic-embed-text")  # For converting queries to vectors
    llm = ChatOllama(model=args.model)  # For generating responses
    
    print(f"Chat initialized with {args.model}. Type 'quit' to exit.")
    print("Ask a question about your documents:")
    
    # Main chat loop
    while True:
        query = input("\nYou: ").strip()
        
        # Check for exit commands
        if query.lower() in ['quit', 'exit']:
            break
            
        if not query:
            continue
            
        try:
            # Step 1: Get relevant context from ChromaDB
            context = get_relevant_context(query, collection, embeddings_model)
            
            # Note: For improved accuracy, a reranking step could be added here using
            # models like sentence-transformers' cross-encoder (e.g., 'cross-encoder/ms-marco-MiniLM-L-6-v2')
            # to better order the retrieved chunks based on relevance to the query
            
            # Step 2: Generate response using the LLM
            response = generate_response(llm, context, query)
            
            print("\nAssistant:", response.strip())
            
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()