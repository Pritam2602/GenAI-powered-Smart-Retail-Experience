#!/usr/bin/env python3
"""
Migration script to help transition from the old structure to the new modular structure.
This script will help you migrate your existing GenAI Smart Retail project.
"""

import os
import shutil
import sys
from pathlib import Path

def create_directory_structure():
    """Create the new modular directory structure."""
    print("Creating modular directory structure...")
    
    # Create main directories
    directories = [
        "smart_retail",
        "smart_retail/models",
        "smart_retail/routes", 
        "smart_retail/utils",
        "smart_retail/static",
        "smart_retail/tests"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")

def backup_existing_files():
    """Backup existing important files."""
    print("Backing up existing files...")
    
    backup_dir = Path("backup_original")
    backup_dir.mkdir(exist_ok=True)
    
    files_to_backup = [
        "server/app.py",
        "streamlit_app.py", 
        "requirements.txt",
        "README.md"
    ]
    
    for file_path in files_to_backup:
        if Path(file_path).exists():
            backup_path = backup_dir / Path(file_path).name
            shutil.copy2(file_path, backup_path)
            print(f"Backed up: {file_path} -> {backup_path}")

def copy_artifacts():
    """Copy model artifacts to the new structure."""
    print("Copying model artifacts...")
    
    artifacts_dir = Path("artifacts")
    if artifacts_dir.exists():
        # Copy artifacts to new location
        new_artifacts = Path("smart_retail/artifacts")
        if not new_artifacts.exists():
            shutil.copytree(artifacts_dir, new_artifacts)
            print("Copied artifacts directory")
        else:
            print("Artifacts directory already exists in new structure")
    else:
        print("No artifacts directory found")

def copy_chroma_db():
    """Copy ChromaDB to the new structure."""
    print("Copying ChromaDB...")
    
    chroma_dir = Path("chroma_db")
    if chroma_dir.exists():
        new_chroma = Path("smart_retail/chroma_db")
        if not new_chroma.exists():
            shutil.copytree(chroma_dir, new_chroma)
            print("Copied ChromaDB directory")
        else:
            print("ChromaDB directory already exists in new structure")
    else:
        print("No ChromaDB directory found")

def create_startup_script():
    """Create a startup script for the new modular structure."""
    print("Creating startup script...")
    
    startup_script = """#!/usr/bin/env python3
\"\"\"
Startup script for the modular GenAI Smart Retail system.
\"\"\"

import sys
import os
from pathlib import Path

# Add the smart_retail directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    import uvicorn
    from smart_retail.main import app
    
    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8001))
    
    print(f"Starting GenAI Smart Retail API on {host}:{port}")
    print(f"API Documentation: http://{host}:{port}/docs")
    print(f"ReDoc Documentation: http://{host}:{port}/redoc")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
"""
    
    with open("start_smart_retail.py", "w") as f:
        f.write(startup_script)
    
    # Make it executable
    os.chmod("start_smart_retail.py", 0o755)
    print("Created startup script: start_smart_retail.py")

def create_dockerfile():
    """Create a Dockerfile for the new structure."""
    print("Creating Dockerfile...")
    
    dockerfile_content = """FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY smart_retail/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY smart_retail/ ./smart_retail/
COPY artifacts/ ./artifacts/
COPY chroma_db/ ./chroma_db/

# Expose port
EXPOSE 8001

# Set environment variables
ENV PYTHONPATH=/app
ENV HOST=0.0.0.0
ENV PORT=8001

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8001/health/z || exit 1

# Run the application
CMD ["python", "-m", "smart_retail.main"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    print("Created Dockerfile")

def create_docker_compose():
    """Create docker-compose.yml for easy deployment."""
    print("Creating docker-compose.yml...")
    
    compose_content = """version: '3.8'

services:
  smart-retail-api:
    build: .
    ports:
      - "8001:8001"
    environment:
      - HOST=0.0.0.0
      - PORT=8001
    volumes:
      - ./artifacts:/app/artifacts
      - ./chroma_db:/app/chroma_db
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health/z"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
"""
    
    with open("docker-compose.yml", "w") as f:
        f.write(compose_content)
    
    print("Created docker-compose.yml")

def create_migration_instructions():
    """Create migration instructions."""
    print("Creating migration instructions...")
    
    instructions = """# Migration Instructions

## Congratulations! Your GenAI Smart Retail project has been upgraded to a modular structure!

### What was created:

1. **Modular Structure**: 
   - `smart_retail/` - Main application directory
   - `smart_retail/models/` - ML models and data models
   - `smart_retail/routes/` - API endpoints
   - `smart_retail/utils/` - Utility functions
   - `smart_retail/config.py` - Configuration management

2. **Backup Files**: 
   - `backup_original/` - Your original files are backed up here

3. **New Files**:
   - `start_smart_retail.py` - Easy startup script
   - `Dockerfile` - For containerized deployment
   - `docker-compose.yml` - For easy deployment

### How to run the new modular system:

#### Option 1: Direct Python
```bash
python start_smart_retail.py
```

#### Option 2: Using the module
```bash
python -m smart_retail.main
```

#### Option 3: Using Docker
```bash
docker-compose up --build
```

### API Documentation:
- Interactive docs: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

### What's different:

1. **Better Organization**: Code is now split into logical modules
2. **Professional Structure**: Industry-standard FastAPI project layout
3. **Enhanced Documentation**: Auto-generated API docs
4. **Better Error Handling**: Comprehensive error handling and validation
5. **Configuration Management**: Centralized settings
6. **Input Validation**: Robust data validation
7. **Trend Analysis**: Fashion trend insights
8. **Modular ML Models**: Better model management

### Next Steps (Level 2):

1. **Upgrade AI Models**: 
   - Implement Sentence Transformers for better recommendations
   - Add SHAP for model explainability
   - Integrate Google Trends API

2. **Frontend Upgrade**:
   - Create React + TailwindCSS frontend
   - Add real-time analytics dashboard
   - Implement AI chatbot

3. **Deployment**:
   - Deploy to Render/Railway
   - Set up CI/CD pipeline
   - Add monitoring and logging

### Need Help?

- Check the `smart_retail/README.md` for detailed documentation
- Review the API docs at `/docs` endpoint
- All your original files are in `backup_original/`

Happy coding!
"""
    
    with open("MIGRATION_INSTRUCTIONS.md", "w") as f:
        f.write(instructions)
    
    print("Created migration instructions: MIGRATION_INSTRUCTIONS.md")

def main():
    """Main migration function."""
    print("Starting migration to modular GenAI Smart Retail structure...")
    print("=" * 60)
    
    try:
        # Step 1: Create directory structure
        create_directory_structure()
        
        # Step 2: Backup existing files
        backup_existing_files()
        
        # Step 3: Copy artifacts
        copy_artifacts()
        
        # Step 4: Copy ChromaDB
        copy_chroma_db()
        
        # Step 5: Create startup script
        create_startup_script()
        
        # Step 6: Create Docker files
        create_dockerfile()
        create_docker_compose()
        
        # Step 7: Create instructions
        create_migration_instructions()
        
        print("=" * 60)
        print("Migration completed successfully!")
        print("\nNext steps:")
        print("1. Review the new structure in smart_retail/")
        print("2. Check MIGRATION_INSTRUCTIONS.md for details")
        print("3. Run: python start_smart_retail.py")
        print("4. Visit: http://localhost:8001/docs")
        print("\nYour original files are backed up in backup_original/")
        
    except Exception as e:
        print(f"Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
