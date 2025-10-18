#!/usr/bin/env python3
"""
Script to set up Git LFS for large model files and database files.
This helps with deploying large files to Render.
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a shell command and return success status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            return True
        else:
            print(f"❌ {description} - Failed")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False

def main():
    print("🔧 Setting up Git LFS for Large Files")
    print("=" * 50)
    
    # Check if git is available
    if not run_command("git --version", "Checking Git availability"):
        print("❌ Git is not available. Please install Git first.")
        return False
    
    # Check if git-lfs is available
    if not run_command("git lfs version", "Checking Git LFS availability"):
        print("❌ Git LFS is not available. Please install Git LFS first.")
        print("Download from: https://git-lfs.github.io/")
        return False
    
    # Initialize Git LFS
    if not run_command("git lfs install", "Initializing Git LFS"):
        return False
    
    # Track large files
    large_file_patterns = [
        "*.joblib",
        "*.pkl",
        "*.pickle",
        "chroma_db/**",
        "*.parquet",
        "*.csv"
    ]
    
    print("\n📁 Setting up LFS tracking for large files:")
    for pattern in large_file_patterns:
        if not run_command(f"git lfs track \"{pattern}\"", f"Tracking {pattern}"):
            return False
    
    # Create .gitattributes file
    print("\n📝 Creating .gitattributes file...")
    try:
        with open(".gitattributes", "w") as f:
            for pattern in large_file_patterns:
                f.write(f"{pattern} filter=lfs diff=lfs merge=lfs -text\n")
        print("✅ .gitattributes file created")
    except Exception as e:
        print(f"❌ Failed to create .gitattributes: {e}")
        return False
    
    print("\n🎉 Git LFS setup complete!")
    print("\nNext steps:")
    print("1. Add the .gitattributes file: git add .gitattributes")
    print("2. Add your large files: git add artifacts/ chroma_db/")
    print("3. Commit: git commit -m 'Add large files with LFS'")
    print("4. Push: git push")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
