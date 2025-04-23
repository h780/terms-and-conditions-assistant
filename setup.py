#!/usr/bin/env python
import os
import shutil
import sys

def setup_environment():
    """Set up the environment for the Terms & Conditions Assistant."""
    print("Setting up Terms & Conditions Assistant environment...")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("⚠️  .env file already exists. Do you want to overwrite it? (y/n)")
        response = input().lower()
        if response != 'y':
            print("Setup aborted. Keeping existing .env file.")
            return
    
    # Copy .env.example to .env
    if os.path.exists('.env.example'):
        shutil.copy('.env.example', '.env')
        print("✅ Created .env file from .env.example")
        print("⚠️  Please edit the .env file to add your API keys")
    else:
        print("❌ .env.example file not found. Please create it manually.")
    
    # Check if Ollama is installed
    try:
        import subprocess
        subprocess.run(['ollama', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ Ollama is installed")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("❌ Ollama is not installed or not in PATH")
        print("Please install Ollama from https://ollama.ai/")
    
    # Check if llama2 model is pulled
    try:
        subprocess.run(['ollama', 'list'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ Ollama is running")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("❌ Ollama is not running")
        print("Please start Ollama with: ollama serve")
    
    print("\nSetup complete! You can now run the application with: python app.py")

if __name__ == "__main__":
    setup_environment() 