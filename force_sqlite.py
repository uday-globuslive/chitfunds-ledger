#!/usr/bin/env python3
"""
This script ensures that the project uses SQLite by creating/updating the .env file
with the correct settings. This helps bypass Djongo compatibility issues.
"""

import os
from pathlib import Path

def main():
    # Get the root directory of the project
    script_dir = Path(__file__).resolve().parent
    env_file = script_dir / '.env'
    
    print("Setting up project to use SQLite database...")
    
    # Create or update .env file
    env_content = """# Database Configuration
USE_DJONGO=False
USE_POSTGRES=False

# Security settings
SECRET_KEY=django-insecure-secret-key-for-development-only
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# MongoDB settings (not used with SQLite)
MONGODB_NAME=chitfunds_db
MONGODB_URI=mongodb://localhost:27017
MONGODB_USERNAME=
MONGODB_PASSWORD=
MONGODB_AUTH_SOURCE=admin

# Email settings
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@chitfunds.com
"""
    
    # Write to .env file
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print("Created .env file with SQLite configuration.")
    print("You can now run migrations with: python chitfunds_ledger/manage.py migrate")
    
    # Create necessary directories
    os.makedirs(script_dir / 'chitfunds_ledger' / 'static', exist_ok=True)
    os.makedirs(script_dir / 'chitfunds_ledger' / 'staticfiles', exist_ok=True)
    os.makedirs(script_dir / 'chitfunds_ledger' / 'media', exist_ok=True)
    print("Created required directories.")
    
    # Create quick-start commands file
    with open(script_dir / 'commands.sh', 'w') as f:
        f.write("""#!/bin/bash
# Quick-start commands for ChitFunds Ledger

# Activate virtual environment (if not already activated)
# source venv/bin/activate

# Run migrations
python chitfunds_ledger/manage.py migrate

# Create superuser
python chitfunds_ledger/manage.py createsuperuser

# Collect static files
python chitfunds_ledger/manage.py collectstatic --noinput

# Run development server
python chitfunds_ledger/manage.py runserver
""")
    os.chmod(script_dir / 'commands.sh', 0o755)
    print("Created commands.sh with quick-start commands.")
    
    print("\nSetup complete! Run the following commands to start the application:")
    print("  chmod +x commands.sh")
    print("  ./commands.sh")

if __name__ == "__main__":
    main()