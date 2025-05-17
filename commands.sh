#!/bin/bash
# Quick-start commands for ChitFunds Ledger

# Activate virtual environment (if not already activated)
# source venv/bin/activate

# Run migrations
python chitfunds_ledger/manage.py migrate

# Create superuser
python chitfunds_ledger/manage.py createsuperuser

# Collect static files
python chitfunds_ledger/manage.py collectstatic --noinput

# Run development server on all network interfaces (0.0.0.0) with port 8000
# This allows connections from other machines on the network
python chitfunds_ledger/manage.py runserver 0.0.0.0:8000
