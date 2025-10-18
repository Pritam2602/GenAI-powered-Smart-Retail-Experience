#!/usr/bin/env python3
"""
Script to prepare the project for deployment to Render and Streamlit Community Cloud.
This script checks for required files and provides deployment instructions.
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and print status."""
    if os.path.exists(file_path):
        print(f"[OK] {description}: {file_path}")
        return True
    else:
        print(f"[MISSING] {description}: {file_path}")
        return False

def check_directory_exists(dir_path, description):
    """Check if a directory exists and print status."""
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        file_count = len(list(Path(dir_path).rglob('*')))
        print(f"[OK] {description}: {dir_path} ({file_count} files)")
        return True
    else:
        print(f"[MISSING] {description}: {dir_path}")
        return False

def main():
    print("GenAI Fashion Hub - Deployment Preparation Check")
    print("=" * 60)
    
    # Check required files
    required_files = [
        ("server/app.py", "FastAPI Application"),
        ("streamlit_app.py", "Streamlit Frontend"),
        ("requirements.txt", "Python Dependencies"),
        ("render.yaml", "Render Configuration"),
        ("Procfile", "Process Configuration"),
        ("DEPLOYMENT_GUIDE.md", "Deployment Guide")
    ]
    
    print("\nChecking Required Files:")
    all_files_exist = True
    for file_path, description in required_files:
        if not check_file_exists(file_path, description):
            all_files_exist = False
    
    # Check required directories
    required_dirs = [
        ("artifacts", "Model Artifacts"),
        ("chroma_db", "ChromaDB Vector Database")
    ]
    
    print("\nChecking Required Directories:")
    all_dirs_exist = True
    for dir_path, description in required_dirs:
        if not check_directory_exists(dir_path, description):
            all_dirs_exist = False
    
    # Check model files specifically
    print("\nChecking Model Files:")
    model_files = [
        "artifacts/fast_price_models_api.joblib",
        "artifacts/price_model_improved.joblib"
    ]
    
    models_exist = True
    for model_file in model_files:
        if not check_file_exists(model_file, "Model File"):
            models_exist = False
    
    # Summary
    print("\n" + "=" * 60)
    print("DEPLOYMENT READINESS SUMMARY:")
    print("=" * 60)
    
    if all_files_exist and all_dirs_exist and models_exist:
        print("READY FOR DEPLOYMENT!")
        print("\nNext Steps:")
        print("1. Push your code to GitHub")
        print("2. Deploy backend to Render (see DEPLOYMENT_GUIDE.md)")
        print("3. Deploy frontend to Streamlit Community Cloud")
        print("4. Set API_BASE_URL environment variable in Streamlit")
    else:
        print("NOT READY - Missing required files/directories")
        print("\nPlease ensure all required files and directories exist before deploying.")
        
        if not all_files_exist:
            print("\nMissing files detected. Please check the file paths above.")
        if not all_dirs_exist:
            print("\nMissing directories detected. Please ensure artifacts/ and chroma_db/ exist.")
        if not models_exist:
            print("\nMissing model files. Please run the training scripts to generate models.")
    
    print("\nFor detailed deployment instructions, see DEPLOYMENT_GUIDE.md")
    
    return all_files_exist and all_dirs_exist and models_exist

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
