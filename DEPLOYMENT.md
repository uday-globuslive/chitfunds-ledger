# ChitFunds Ledger Deployment Guide

This document provides a comprehensive guide for deploying the ChitFunds Ledger application in both development and production environments.

## Project Setup Overview

The ChitFunds Ledger is a Django-based web application with the following structure:

```
chitfunds_ledger/
├── chitfunds_ledger/         # Django project folder
│   ├── chitfunds_ledger/     # Project settings
│   ├── chit_app/            # Main application
│   ├── static/              # Static files (CSS, JS, images)
│   ├── media/               # User-uploaded files (receipts)
│   ├── templates/           # Global templates
│   └── manage.py            # Django management script
├── requirements.txt         # Python dependencies for local development
├── requirements-pythonanywhere.txt  # Dependencies for PythonAnywhere
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore file
├── README.md                # Project documentation
└── setup-pythonanywhere.md  # PythonAnywhere-specific setup guide
```

## Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/chitfunds_ledger.git
   cd chitfunds_ledger
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Update the variables with your MongoDB and email settings

5. **Run migrations**:
   ```bash
   python chitfunds_ledger/manage.py migrate
   ```

6. **Create a superuser**:
   ```bash
   python chitfunds_ledger/manage.py createsuperuser
   ```

7. **Run the development server**:
   ```bash
   python chitfunds_ledger/manage.py runserver
   ```

8. **Access the application**:
   - Website: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## MongoDB Cloud Setup

For both local development and production, you'll need a MongoDB Atlas database:

1. **Sign up for MongoDB Atlas**:
   - Go to [https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
   - Create a free account and set up a new project

2. **Create a cluster**:
   - Choose the free tier
   - Select your preferred cloud provider and region

3. **Configure database access**:
   - Under "Security" > "Database Access", create a database user with read and write privileges
   - Remember the username and password

4. **Configure network access**:
   - Under "Security" > "Network Access", add your IP address
   - For production, add `0.0.0.0/0` to allow access from anywhere

5. **Get connection string**:
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string and replace `<username>` and `<password>` with your database user credentials
   - Update your `.env` file with this connection string

## PythonAnywhere Deployment

For a detailed guide on deploying to PythonAnywhere, refer to `setup-pythonanywhere.md`. Here's a summary:

1. **Create a PythonAnywhere account**:
   - Sign up at [https://www.pythonanywhere.com/](https://www.pythonanywhere.com/)

2. **Clone and set up the repository**:
   - Open a Bash console in PythonAnywhere
   - Clone your repository
   - Create a virtual environment and install dependencies
   - Set up environment variables

3. **Configure the web app**:
   - Create a new web app with manual configuration
   - Set up the virtual environment path
   - Configure the WSGI file
   - Set up static and media file mappings

4. **Initialize the database**:
   - Run migrations
   - Create a superuser

5. **Reload the web app**:
   - Go to the "Web" tab and click "Reload"

## Environment Variables

Here's a detailed explanation of all environment variables used in the application:

| Variable | Description | Example |
|----------|-------------|---------|
| SECRET_KEY | Django secret key for security | `django-insecure-secret-key` |
| DEBUG | Enable debug mode (set to False in production) | `True` or `False` |
| ALLOWED_HOSTS | Comma-separated list of allowed hosts | `localhost,127.0.0.1,yourdomain.com` |
| MONGODB_NAME | MongoDB database name | `chitfunds_db` |
| MONGODB_URI | MongoDB connection URI | `mongodb+srv://...` |
| MONGODB_USERNAME | MongoDB username | `dbuser` |
| MONGODB_PASSWORD | MongoDB password | `dbpassword` |
| MONGODB_AUTH_SOURCE | MongoDB authentication source | `admin` |
| EMAIL_BACKEND | Django email backend | `django.core.mail.backends.smtp.EmailBackend` |
| EMAIL_HOST | SMTP server host | `smtp.gmail.com` |
| EMAIL_PORT | SMTP server port | `587` |
| EMAIL_USE_TLS | Use TLS for email | `True` |
| EMAIL_HOST_USER | Email username | `your-email@gmail.com` |
| EMAIL_HOST_PASSWORD | Email password or app password | `your-password` |
| DEFAULT_FROM_EMAIL | Default sender email | `noreply@chitfunds.com` |

## Common Issues and Troubleshooting

### Database Connection Issues

- **MongoDB Atlas connection failures**:
  - Check if your IP is whitelisted in the Network Access settings
  - Verify username and password in the connection string
  - Ensure the cluster is running

### Static and Media Files

- **Files not loading**:
  - Check if `collectstatic` has been run
  - Verify static and media URL and ROOT settings in settings.py
  - Ensure file permissions are correct

### Email Issues

- **Email sending failures**:
  - If using Gmail, enable "Less secure apps" or create an App Password if using 2FA
  - Verify EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
  - Check the email backend configuration

## Maintenance

### Updating the Application

To update the application with the latest changes:

```bash
git pull
pip install -r requirements.txt
python chitfunds_ledger/manage.py migrate
python chitfunds_ledger/manage.py collectstatic --noinput
```

Then restart the development server or reload the PythonAnywhere web app.

### Backing Up Data

To backup your MongoDB Atlas database:

1. Go to your MongoDB Atlas dashboard
2. Select your cluster
3. Click "Backup" and follow the instructions to create a backup

## Security Considerations

- Always use HTTPS in production
- Keep your SECRET_KEY secure and different in each environment
- Never commit the `.env` file to version control
- Keep MongoDB credentials secure
- Regularly update dependencies to address security vulnerabilities