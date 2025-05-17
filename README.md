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
- Database options:
  - SQLite (default and recommended)
  - MongoDB (using Djongo ORM or direct PyMongo)
  - PostgreSQL (for production)
- Bootstrap 5
- Chart.js for data visualization
- Django Allauth for authentication
- Crispy Forms for form styling

## Quick Start Setup (SQLite)

The easiest way to get started is using SQLite:

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

3. Run the SQLite setup script:
   ```
   chmod +x force_sqlite.py
   ./force_sqlite.py
   ```

4. Install dependencies:
   ```
   chmod +x install.sh
   ./install.sh
   ```

5. Run the commands script for database setup and server start:
   ```
   chmod +x commands.sh
   ./commands.sh
   ```

6. Visit http://127.0.0.1:8000/ in your browser

## Detailed Setup Instructions

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

7. Collect static files:
   ```
   python chitfunds_ledger/manage.py collectstatic
   ```

8. Run the development server:
   ```
   python chitfunds_ledger/manage.py runserver
   ```

9. Visit http://127.0.0.1:8000/ in your browser

## Database Options

### SQLite (Default and Recommended)

The application is configured to use SQLite by default. This is suitable for development and small deployments.

To ensure SQLite is used:
```
./force_sqlite.py
```

### MongoDB (via Djongo)

To use MongoDB:

1. Set up a MongoDB instance (locally or using MongoDB Atlas)
2. Edit the `.env` file and set `USE_DJONGO=True`
3. Configure the MongoDB connection parameters in the `.env` file

You can test your MongoDB connection before running the application:
```bash
python test_mongodb.py
```

If you encounter issues connecting to MongoDB, refer to the `MONGODB_TROUBLESHOOTING.md` file for detailed solutions.

#### Alternative MongoDB Connection

If you encounter issues with Djongo compatibility, you can use the alternative direct MongoDB connection provided in `alternative_mongodb_connection.py`.

### PostgreSQL (Recommended for Production)

For production use, PostgreSQL is recommended:

1. Set up a PostgreSQL database
2. Edit the `.env` file and set `USE_POSTGRES=True`
3. Configure the PostgreSQL connection parameters in the `.env` file

## Email Configuration

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

For more detailed deployment instructions, refer to `setup-pythonanywhere.md` and `DEPLOYMENT.md`.

## Troubleshooting

If you encounter issues:

1. Check the `MONGODB_TROUBLESHOOTING.md` file for MongoDB-specific issues
2. Review the application logs in `chitfunds_ledger/debug.log`
3. Ensure your MongoDB connection is working by running `python test_mongodb.py`
4. If Djongo causes issues, try setting `USE_DJONGO=False` in your `.env` file
5. Run `./force_sqlite.py` to reset to SQLite configuration
6. Check if all required directories exist (static, media, staticfiles)

## License

This project is licensed under the MIT License - see the LICENSE file for details.