# PythonAnywhere Setup Guide for ChitFunds Ledger

This guide will walk you through the steps to deploy the ChitFunds Ledger application on PythonAnywhere.

## 1. Sign Up for PythonAnywhere

1. Go to [PythonAnywhere](https://www.pythonanywhere.com/) and sign up for an account
2. Choose a plan that suits your needs (even the free tier works for starting out)

## 2. Set Up the Project

### 2.1. Open a Bash Console

1. From your PythonAnywhere dashboard, click on "Bash" under the "Consoles" section

### 2.2. Clone the Repository

```bash
git clone https://github.com/yourusername/chitfunds_ledger.git
cd chitfunds_ledger
```

### 2.3. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 2.4. Install Dependencies

```bash
pip install -r requirements-pythonanywhere.txt
```

### 2.5. Create Environment Variables

Create a `.env` file with all the necessary environment variables:

```bash
nano .env
```

Add your environment variables as per the `.env.example` file, especially your MongoDB connection details:

```
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com

MONGODB_NAME=chitfunds_db
MONGODB_URI=mongodb+srv://your-mongodb-connection-string
MONGODB_USERNAME=your-mongodb-username
MONGODB_PASSWORD=your-mongodb-password
MONGODB_AUTH_SOURCE=admin

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@chitfunds.com
```

### 2.6. Migrate and Create Superuser

```bash
python chitfunds_ledger/manage.py migrate
python chitfunds_ledger/manage.py createsuperuser
```

### 2.7. Collect Static Files

```bash
python chitfunds_ledger/manage.py collectstatic
```

## 3. Configure Web App

### 3.1. Create a New Web App

1. Go to the "Web" tab in your PythonAnywhere dashboard
2. Click on "Add a new web app"
3. Choose your domain name (e.g., yourusername.pythonanywhere.com)
4. Select "Manual configuration"
5. Choose Python version (3.8 or newer)

### 3.2. Configure Virtual Environment

In the web app configuration:

1. Set the path to your virtual environment:
   ```
   /home/yourusername/chitfunds_ledger/venv
   ```

### 3.3. Configure WSGI File

Click on the WSGI configuration file link and replace its contents with:

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

# Set the environment variable for Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'chitfunds_ledger.settings'

# Import Django WSGI handler
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Replace `yourusername` with your actual PythonAnywhere username.

### 3.4. Configure Static Files

In the web app configuration, add a static files mapping:

1. URL: `/static/`
2. Directory: `/home/yourusername/chitfunds_ledger/chitfunds_ledger/staticfiles`

Add another mapping for media files:

1. URL: `/media/`
2. Directory: `/home/yourusername/chitfunds_ledger/chitfunds_ledger/media`

### 3.5. Create the Media Directory

```bash
mkdir -p /home/yourusername/chitfunds_ledger/chitfunds_ledger/media
chmod 755 /home/yourusername/chitfunds_ledger/chitfunds_ledger/media
```

## 4. Configure MongoDB Atlas

### 4.1. Set Up MongoDB Atlas

1. Sign up for MongoDB Atlas at [https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster (the free tier is sufficient for starting)
3. Under "Security" > "Database Access", create a database user with read and write privileges
4. Under "Security" > "Network Access", add an IP address entry with `0.0.0.0/0` to allow access from anywhere (including PythonAnywhere)
5. Under "Databases" > "Connect", choose "Connect your application" and copy the connection string
6. Update your `.env` file with the MongoDB connection details

## 5. Final Steps

### 5.1. Reload the Web App

Go back to the "Web" tab in your PythonAnywhere dashboard and click the "Reload" button for your web app.

### 5.2. Visit Your Site

Click on the link to your website (e.g., `yourusername.pythonanywhere.com`) to verify it's working correctly.

### 5.3. Visit the Admin Panel

Go to `yourusername.pythonanywhere.com/admin` and log in with the superuser credentials you created earlier.

## 6. Troubleshooting

### 6.1. Check the Error Logs

If you encounter issues, check the error logs in the "Web" tab of your PythonAnywhere dashboard.

### 6.2. Django Settings

Ensure that your `settings.py` is properly configured to use environment variables and has the correct settings for production.

### 6.3. Common Issues

- **Static files not loading**: Make sure you've run `collectstatic` and configured the static files mapping correctly.
- **MongoDB connection issues**: Ensure your MongoDB Atlas cluster allows connections from anywhere and your connection string is correct.
- **Email sending problems**: Check your email configuration, especially if using Gmail (you might need an App Password).

## 7. Maintenance

### 7.1. Updating the Application

To update your application with the latest changes:

```bash
cd ~/chitfunds_ledger
git pull
source venv/bin/activate
pip install -r requirements-pythonanywhere.txt
python chitfunds_ledger/manage.py migrate
python chitfunds_ledger/manage.py collectstatic --noinput
```

Then reload your web app from the PythonAnywhere dashboard.
