#!/usr/bin/env python3

"""
Tokenize text using OpenAI's tiktoken library.

This script demonstrates how text is broken into tokens using the same tokenizers
that OpenAI's models use. It supports different encodings used by various GPT models.

Available encodings:
- cl100k_base: Used by GPT-4, GPT-3.5-turbo, text-embedding-ada-002
- p50k_base:   Used by GPT-3 models like davinci
- r50k_base:   Used by older GPT-3 models

Usage examples:
    # Default (cl100k_base encoding)
    ./show_tokens_tiktoken.py "Your text here"
    
    # Specific encoding
    ./show_tokens_tiktoken.py --encoding p50k_base "Your text here"
    
    # Multiple words
    ./show_tokens_tiktoken.py "This is a longer piece of text"

Key advantages:
- Runs completely locally (no API calls)
- Very fast tokenization
- Matches OpenAI's tokenization exactly
- Useful for counting tokens before sending to OpenAI APIs
- No model downloads needed

Installation:
    pip install tiktoken

Note: Token counts from this script will match exactly what OpenAI's API would count,
      helping you stay within token limits and estimate API costs.
"""

import argparse
import tiktoken

def setup_argparse():
    """Set up command-line argument parsing."""
    parser = argparse.ArgumentParser(
        description='Show tokens using tiktoken',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Hello, world!"
  %(prog)s --encoding p50k_base "Testing different encodings"
  %(prog)s "Multiple words get tokenized differently"
        """
    )
    parser.add_argument('text', help='Text to tokenize', nargs='+')
    parser.add_argument(
        '--encoding', 
        default='cl100k_base',
        choices=['cl100k_base', 'p50k_base', 'r50k_base'],
        help='Tiktoken encoding to use (default: cl100k_base)'
    )
    return parser.parse_args()

def main():
    args = setup_argparse()
    text = ' '.join(args.text)
    
    try:
        # Initialize tokenizer
        encoding = tiktoken.get_encoding(args.encoding)
        
        # Get tokens
        token_ids = encoding.encode(text)
        tokens = [encoding.decode([id]) for id in token_ids]
        
        # Print results
        print(f"\nInput text: {text}")
        print(f"Encoding: {args.encoding}")
        print("\nTokens:")
        for i, (token, token_id) in enumerate(zip(tokens, token_ids), 1):
            print(f"{i:3d}: {repr(token)} (ID: {token_id})")
        print(f"\nTotal tokens: {len(tokens)}")
        
        # Print model association
        model_info = {
            'cl100k_base': 'GPT-4, GPT-3.5-turbo, text-embedding-ada-002',
            'p50k_base': 'GPT-3 models like davinci',
            'r50k_base': 'Older GPT-3 models'
        }
        print(f"\nThis encoding is used by: {model_info.get(args.encoding, 'Unknown models')}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main() 