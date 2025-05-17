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
- MongoDB (using Djongo ORM)
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

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example` and set your environment variables

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

### MongoDB Setup

1. Sign up for a MongoDB Atlas account at https://www.mongodb.com/cloud/atlas
2. Create a new cluster
3. In the "Security" tab, create a database user with read and write privileges
4. In the "Network Access" tab, add your IP address or allow access from anywhere
5. In the "Databases" tab, click "Connect" and choose "Connect your application"
6. Copy the connection string and update it in your `.env` file

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
   pip install -r requirements-pythonanywhere.txt
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

   # Add your project directory to the sys.path
   path = '/home/yourusername/chitfunds_ledger'
   if path not in sys.path:
       sys.path.insert(0, path)

   # Set environment variables
   os.environ['DJANGO_SETTINGS_MODULE'] = 'chitfunds_ledger.settings'

   # Activate virtual environment
   activate_this = os.path.join('/home/yourusername/chitfunds_ledger/venv/bin/activate_this.py')
   with open(activate_this) as file_:
       exec(file_.read(), dict(__file__=activate_this))

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

## License

This project is licensed under the MIT License - see the LICENSE file for details.
