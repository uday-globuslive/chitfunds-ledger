#!/bin/bash
# Installation script for PythonAnywhere that handles dependency conflicts

echo "Installing ChitFunds Ledger dependencies for PythonAnywhere..."

# Install Django and other dependencies first
pip install django==4.2.10 \
    django-crispy-forms==2.0 \
    crispy-bootstrap5==0.7 \
    djangotoolbox==1.8.0 \
    pymongo[srv]==4.6.1 \
    dnspython==2.4.2 \
    pillow==10.1.0 \
    python-dotenv==1.0.0 \
    django-storages==1.14.2 \
    django-allauth==0.57.0 \
    requests==2.31.0 \
    whitenoise==6.5.0 \
    sqlparse==0.4.4

# Install Djongo without dependencies to avoid conflicts
echo "Installing Djongo without dependencies..."
pip install --no-deps git+https://github.com/doableware/djongo.git

echo "Installation complete. If you encounter issues with Djongo, try the alternative PyMongo approach."
echo "Run 'python test_mongodb.py' to test your MongoDB connection."