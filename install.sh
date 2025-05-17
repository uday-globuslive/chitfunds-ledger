#!/bin/bash
# Installation script that handles dependency conflicts

echo "Installing ChitFunds Ledger dependencies..."

# Install Django and other dependencies first
pip install django==4.2.10 \
    django-crispy-forms==2.0 \
    crispy-bootstrap5==0.7 \
    djangotoolbox==1.8.0 \
    pymongo==4.6.1 \
    dnspython==2.4.2 \
    pillow==10.1.0 \
    python-dotenv==1.0.0 \
    django-storages==1.14.2 \
    django-allauth==0.57.0 \
    requests==2.31.0 \
    gunicorn==21.2.0 \
    whitenoise==6.5.0 \
    pytz==2023.3 \
    sqlparse==0.4.4

# Try to install Djongo without dependencies
echo "Installing Djongo without dependencies..."
pip install --no-deps git+https://github.com/doableware/djongo.git

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    # Set USE_DJONGO to False by default to use SQLite fallback
    echo "USE_DJONGO=False" >> .env
fi

echo "Installation complete. By default, we've configured the app to use SQLite."
echo "To use MongoDB, edit your .env file and set USE_DJONGO=True after setting up your MongoDB connection."
echo "Run 'python test_mongodb.py' to test your MongoDB connection."