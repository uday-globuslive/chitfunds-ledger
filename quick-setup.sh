#!/bin/bash
# Quick setup script for ChitFunds Ledger
# This script sets up the environment, installs dependencies, and prepares the application

echo "===== ChitFunds Ledger Quick Setup ====="
echo "This script will set up the application with SQLite database."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Run force_sqlite.py to ensure SQLite configuration
echo "Configuring SQLite database..."
chmod +x force_sqlite.py
./force_sqlite.py

# Install dependencies
echo "Installing dependencies..."
chmod +x install.sh
./install.sh

# Make commands.sh executable
chmod +x commands.sh

echo "===== Setup Complete! ====="
echo "To start the application, run:"
echo "  source venv/bin/activate"
echo "  ./commands.sh"
echo ""
echo "The application will be available at http://127.0.0.1:8000/"
echo "To access from other machines on your network, use your machine's IP address:"
echo "  http://YOUR_IP_ADDRESS:8000/"
echo "Admin login: username='admin', password='admin123'"