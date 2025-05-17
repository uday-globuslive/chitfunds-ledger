# ChitFunds Ledger

A Django-based web application for tracking and managing chit fund investments. Users can keep track of multiple chit funds, record payments with receipt images, and monitor their payment progress.

## Features

- User registration and authentication with email verification
- Admin approval system for user accounts
- Dashboard with summary of all chit funds and payments
- Add and manage multiple chit fund schemes
- Record payments with receipt image uploads
- Track payment progress with visual charts
- Filter and search payment history
- Notification system for important updates
- Responsive design for mobile and desktop

## Technology Stack

- Django 4.2.10
- MongoDB (using Djongo ORM or direct PyMongo)
- Bootstrap 5
- Chart.js for data visualization
- Django Allauth for authentication
- Crispy Forms for form styling

## Setup Instructions

### Local Development Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd chitfunds_ledger
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies using the install script (handles dependency conflicts):
   ```
   chmod +x install.sh
   ./install.sh
   ```

   If you encounter issues with Djongo, you can try the direct PyMongo approach:
   ```
   pip install -r requirements-pymongo.txt
   ```

4. Create a `.env` file based on `.env.example` and set your environment variables:
   ```
   # Create a .env file
   cp .env.example .env
   # Edit the .env file with your specific settings
   ```

5. Migrate the database:
   ```
   python chitfunds_ledger/manage.py migrate
   ```

6. Create a superuser (admin):
   ```
   python chitfunds_ledger/manage.py createsuperuser
   ```

7. Run the development server:
   ```
   python chitfunds_ledger/manage.py runserver
   ```

8. Visit http://127.0.0.1:8000/ in your browser

### MongoDB Connection

You can test your MongoDB connection before running the application:

```bash
python test_mongodb.py
```

If you encounter issues connecting to MongoDB, refer to the `MONGODB_TROUBLESHOOTING.md` file for detailed solutions.

### Switching Between MongoDB Connection Methods

The application supports two ways of connecting to MongoDB:

1. **Djongo ORM** (default): Set `USE_DJONGO=True` in your `.env` file
2. **Direct PyMongo**: Set `USE_DJONGO=False` in your `.env` file

### Email Configuration

For email functionality (account verification, approvals), configure the email settings in your `.env` file. For Gmail, you might need to create an App Password if you have 2FA enabled.

## Deployment to PythonAnywhere

1. Sign up for a PythonAnywhere account at https://www.pythonanywhere.com/

2. Open a bash console and clone your repository:
   ```
   git clone <repository-url>
   cd chitfunds_ledger
   ```

3. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate
   chmod +x install-pythonanywhere.sh
   ./install-pythonanywhere.sh
   ```

4. Create a `.env` file with your production settings

5. Create a web app through the PythonAnywhere dashboard:
   - Choose "Manual configuration" and your Python version
   - Set the virtual environment path to `/home/yourusername/chitfunds_ledger/venv`
   - Set the source code directory to `/home/yourusername/chitfunds_ledger`

6. Configure the WSGI file (edit the provided file at `/var/www/yourusername_pythonanywhere_com_wsgi.py`):
   ```python
   import os
   import sys
   from dotenv import load_dotenv

   # Load environment variables
   project_folder = os.path.expanduser('~/chitfunds_ledger')
   load_dotenv(os.path.join(project_folder, '.env'))

   # Add your project directory to the sys.path
   path = '/home/yourusername/chitfunds_ledger'
   if path not in sys.path:
       sys.path.insert(0, path)

   # Set environment variables
   os.environ['DJANGO_SETTINGS_MODULE'] = 'chitfunds_ledger.settings'

   # Import Django WSGI handler
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

7. Configure static files in the PythonAnywhere web app dashboard:
   - URL: `/static/`
   - Directory: `/home/yourusername/chitfunds_ledger/chitfunds_ledger/staticfiles`

8. Collect static files:
   ```
   python chitfunds_ledger/manage.py collectstatic
   ```

9. Reload the web app from the PythonAnywhere dashboard

For more detailed deployment instructions, refer to `setup-pythonanywhere.md`.

## Troubleshooting

If you encounter issues:

1. Check the `MONGODB_TROUBLESHOOTING.md` file for MongoDB-specific issues
2. Review the application logs in `chitfunds_ledger/debug.log`
3. Ensure your MongoDB connection is working by running `python test_mongodb.py`
4. If Djongo causes issues, try setting `USE_DJONGO=False` in your `.env` file

## License

This project is licensed under the MIT License - see the LICENSE file for details.