#!/usr/bin/env python3

"""
Text Chunking Demonstration Tool

This script demonstrates different text chunking strategies commonly used in RAG
(Retrieval Augmented Generation) systems and other NLP applications. Chunking is
the process of breaking down large texts into smaller, manageable pieces while
preserving context and meaning.

Chunking Strategies:
------------------
1. Recursive Character Splitting (--method recursive):
   - Most sophisticated approach
   - Attempts to split on natural boundaries in this order:
     a) Paragraph breaks ("\n\n")
     b) Line breaks ("\n")
     c) Sentences (". ")
     d) Words (" ")
     e) Characters ("")
   - Best for maintaining semantic coherence
   - Ideal for structured text with clear paragraph breaks

2. Character-Based Splitting (--method character):
   - Simple approach that splits purely on character count
   - Uses newline as a separator
   - Less sophisticated but more predictable
   - Useful when you need exact chunk sizes
   - May break sentences or words at boundaries

3. Token-Based Splitting (--method token):
   - Splits text based on token count rather than characters
   - Important for LLM context windows which are token-based
   - Helps prevent token overflow issues
   - More accurate for LLM token limit constraints
   - Uses tiktoken for token counting

Chunk Overlap:
------------
The script supports chunk overlap to maintain context between chunks:
- Helps preserve context across chunk boundaries
- Useful for capturing sentences or concepts that span chunks
- Trade-off: More overlap means more duplicate content
- Typical overlap: 10-20% of chunk size

Usage:
-----
Basic usage:
    python show_chunks.py input.txt

With specific method:
    python show_chunks.py input.txt --method recursive
    python show_chunks.py input.txt --method character
    python show_chunks.py input.txt --method token

Customize chunk size and overlap:
    python show_chunks.py input.txt --chunk-size 500 --chunk-overlap 100

Dependencies:
-----------
- langchain: For text splitting implementations
- tiktoken: Required for token-based splitting
"""

import argparse
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TokenTextSplitter
)

def read_file(file_path):
    """
    Read and return the content of a text file.
    
    Args:
        file_path (str): Path to the file to read
        
    Returns:
        str: Content of the file
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        UnicodeDecodeError: If the file encoding is not UTF-8
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def chunk_text(text, method='recursive', chunk_size=1000, chunk_overlap=200):
    """
    Split text into chunks using different methods.
    
    Args:
        text (str): The input text to chunk
        method (str): Chunking method to use:
            - 'recursive': Smart splitting on natural boundaries
            - 'character': Simple character-based splitting
            - 'token': Token-aware splitting for LLM context windows
        chunk_size (int): Target size of each chunk:
            - For 'recursive' and 'character': in characters
            - For 'token': in tokens
        chunk_overlap (int): Amount of overlap between chunks:
            - For maintaining context across chunk boundaries
            - Should be smaller than chunk_size
            - Typically 10-20% of chunk_size
    
    Returns:
        list: List of text chunks
        
    Examples:
        # Recursive splitting (default)
        chunks = chunk_text(long_text)
        
        # Character-based splitting with custom size
        chunks = chunk_text(long_text, method='character', chunk_size=500)
        
        # Token-based splitting for LLM context
        chunks = chunk_text(long_text, method='token', chunk_size=1000)
    """
    if method == 'recursive':
        # RecursiveCharacterTextSplitter is more sophisticated,
        # it tries to split on punctuation and whitespace first
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]  # Ordered by priority
        )
    elif method == 'character':
        # Simple character-based splitting
        splitter = CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separator="\n"
        )
    elif method == 'token':
        # Token-based splitting (useful for LLM context windows)
        splitter = TokenTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    else:
        raise ValueError(f"Unknown chunking method: {method}")
    
    return splitter.split_text(text)

def display_chunks(chunks):
    """
    Display chunks with clear separation and statistics.
    
    Args:
        chunks (list): List of text chunks to display
        
    Output format:
        - Total number of chunks
        - For each chunk:
            - Chunk number and length
            - Chunk content with clear separators
    """
    print(f"\nTotal number of chunks: {len(chunks)}")
    print("-" * 80)
    
    for i, chunk in enumerate(chunks, 1):
        print(f"\nChunk {i} (length: {len(chunk)} characters):")
        print("=" * 40)
        print(chunk.strip())
        print("=" * 40)

def main():
    """
    Main function to run the text chunking demonstration.
    
    Process:
        1. Parse command line arguments
        2. Read input file
        3. Apply selected chunking method
        4. Display resulting chunks
        
    Returns:
        int: 0 for success, 1 for errors
    """
    parser = argparse.ArgumentParser(
        description='Demonstrate text chunking methods',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  Basic usage:
    %(prog)s input.txt
  
  Use specific chunking method:
    %(prog)s input.txt --method token
  
  Custom chunk size and overlap:
    %(prog)s input.txt --chunk-size 500 --chunk-overlap 100
        '''
    )
    parser.add_argument('file', help='Path to the text file to chunk')
    parser.add_argument('--method', choices=['recursive', 'character', 'token'],
                      default='recursive', help='Chunking method to use')
    parser.add_argument('--chunk-size', type=int, default=1000,
                      help='Target size of each chunk')
    parser.add_argument('--chunk-overlap', type=int, default=200,
                      help='Number of characters/tokens to overlap between chunks')
    
    args = parser.parse_args()
    
    try:
        # Read the input file
        text = read_file(args.file)
        print(f"\nRead {len(text)} characters from {args.file}")
        
        # Chunk the text
        chunks = chunk_text(
            text,
            method=args.method,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap
        )
        
        # Display the chunks
        display_chunks(chunks)
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 