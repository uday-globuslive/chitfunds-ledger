# ChitFunds Ledger - Project Summary

## Overview

ChitFunds Ledger is a web application designed to help users track and manage their chit fund investments. It provides a centralized platform for recording payments, uploading receipt images, and monitoring payment progress across multiple chit funds.

## Project Structure

```
chitfunds_ledger/
├── alternative_mongodb_connection.py  # Direct PyMongo connection alternative
├── chitfunds_ledger/                  # Main Django project directory
│   ├── chit_app/                      # Main application
│   │   ├── adapters.py                # Custom adapters for user approval
│   │   ├── admin.py                   # Admin site configuration
│   │   ├── forms.py                   # Form definitions
│   │   ├── models.py                  # Data models
│   │   ├── static/                    # Static assets
│   │   ├── templates/                 # HTML templates
│   │   ├── urls.py                    # URL routing
│   │   └── views.py                   # View functions and classes
│   ├── chitfunds_ledger/              # Project settings
│   │   ├── settings.py                # Main settings file with DB configuration
│   │   ├── urls.py                    # Main URL routing
│   │   └── wsgi.py                    # WSGI configuration
│   ├── manage.py                      # Django management script
│   ├── media/                         # User uploaded files (receipts)
│   ├── static/                        # Project-wide static files
│   └── templates/                     # Project-wide templates
├── commands.sh                        # Quick-start commands
├── DEPLOYMENT.md                      # Deployment instructions
├── force_sqlite.py                    # Script to configure SQLite
├── install.sh                         # Installation script
├── install-pythonanywhere.sh          # PythonAnywhere installation script
├── MONGODB_TROUBLESHOOTING.md         # MongoDB troubleshooting guide
├── quick-setup.sh                     # All-in-one setup script
├── README.md                          # Project documentation
├── requirements.txt                   # Dependencies
├── requirements-pymongo.txt           # Dependencies for PyMongo approach
├── setup-pythonanywhere.md            # PythonAnywhere setup guide
└── test_mongodb.py                    # MongoDB connection test script
```

## Key Features

### 1. User Authentication & Authorization

- **Secure Registration & Login**: Robust user authentication system using Django Allauth
- **Email Verification**: Email-based account verification to confirm user identities 
- **Admin Approval**: Administrator approval option for new user accounts
- **Profile Management**: Users can update their profile information and account settings

### 2. Chit Fund Management

- **Multiple Chit Funds**: Users can add and manage multiple chit fund schemes
- **Detailed Information**: Track total amount, monthly contributions, duration, start and end dates
- **Progress Tracking**: Visual charts to monitor payment progress
- **Calculation Tools**: Automatic calculation of remaining amounts and next payment dates

### 3. Payment Tracking

- **Payment Records**: Record all payments made toward chit funds
- **Receipt Upload**: Upload and store images of payment receipts
- **Payment History**: Comprehensive history of all payments with filtering options
- **Reference Numbers**: Store payment reference numbers for verification purposes

### 4. Dashboard & Visualization

- **User Dashboard**: Summary view of all chit funds and recent payments
- **Visual Charts**: Progress charts using Chart.js to visualize payment completion
- **Financial Summary**: Overview of total investment, amount paid, and remaining balance
- **Recent Activity**: Quick access to recent payments and notifications

### 5. Notifications

- **System Notifications**: Internal notification system for important updates
- **Email Notifications**: Email alerts for account approval and other key events
- **Reminder System**: Payment due date reminders to help users stay on track

### 6. Admin Features

- **User Management**: Administrators can approve, view, and manage user accounts
- **Content Management**: Access to all system data through Django admin interface
- **Customizable Settings**: Configure system behavior through environment variables

## Technical Implementation

### Architecture

- **Backend Framework**: Django 4.2.10
- **Database Options**:
  - **SQLite**: Default and easiest to set up
  - **MongoDB**: Using Djongo ORM or direct PyMongo connection
  - **PostgreSQL**: Recommended for production environments
- **Frontend**: Bootstrap 5, Chart.js
- **Authentication**: Django Allauth
- **Form Processing**: Django Crispy Forms with Bootstrap 5 integration
- **File Storage**: Local file system (configurable for cloud storage)

### Models

The application is built around four main data models:

#### Profile Model
```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
```

#### ChitFund Model
```python
class ChitFund(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    duration_months = models.PositiveIntegerField()
    monthly_amount = models.DecimalField(max_digits=12, decimal_places=2)
    organizer = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chit_funds')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Methods for calculating payments, progress, etc.
```

#### Payment Model
```python
class Payment(models.Model):
    chit_fund = models.ForeignKey(ChitFund, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField(default=timezone.now)
    payment_method = models.CharField(max_length=50)
    reference_number = models.CharField(max_length=100, blank=True)
    receipt_image = models.ImageField(upload_to=receipt_upload_path, blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### Notification Model
```python
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Design Patterns

- **Model-View-Template (MVT)**: Django's adaptation of the MVC pattern
- **Class-Based Views**: Utilizes Django's class-based views for code organization
- **Form Validation**: Custom form validation for data integrity
- **Permission Mixins**: LoginRequiredMixin and UserPassesTestMixin for access control

### Database Flexibility

The application is designed to work with multiple database backends, controlled through environment variables in the `.env` file:

```python
# settings.py
if os.environ.get('USE_POSTGRES', 'False').lower() == 'true':
    # PostgreSQL configuration
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'chitfunds_db'),
            # Other PostgreSQL settings...
        }
    }
elif os.environ.get('USE_DJONGO', 'False').lower() == 'true':
    # MongoDB configuration with Djongo
    DATABASES = {
        'default': {
            'ENGINE': 'djongo',
            'NAME': os.environ.get('MONGODB_NAME', 'chitfunds_db'),
            # Other MongoDB settings...
        }
    }
else:
    # SQLite configuration (default)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

### Security Features

- **Environment Variables**: Sensitive information stored in environment variables
- **Password Hashing**: Secure password storage using Django's authentication system
- **CSRF Protection**: Cross-Site Request Forgery protection in forms
- **Secure File Uploads**: Validation and secure handling of uploaded files
- **Content Security**: User data isolation through permission checks

## Deployment Options

- **Local Development**: Full setup guide for local development environment
- **PythonAnywhere**: Detailed instructions for deploying to PythonAnywhere
- **MongoDB Atlas**: Integration with MongoDB Atlas for cloud database hosting
- **PostgreSQL**: Support for PostgreSQL in production environments

## Quick Setup

The application includes a quick setup script that automates the installation process:

```bash
./quick-setup.sh
```

This script:
1. Creates a virtual environment
2. Configures SQLite database (using force_sqlite.py)
3. Installs all dependencies
4. Prepares the application for immediate use

## Troubleshooting

The application includes troubleshooting resources:

- **MongoDB Troubleshooting**: Detailed guide for resolving MongoDB connection issues
- **Database Fallback**: Automatic fallback to SQLite if MongoDB connection fails
- **Alternative MongoDB Connection**: Direct PyMongo connection as an alternative to Djongo
- **Debug Logging**: Comprehensive logging configuration for troubleshooting

## Future Enhancements

Potential areas for future development:

1. **Mobile App**: Develop a mobile application for on-the-go access
2. **Payment Reminders**: Automated email/SMS reminders for upcoming payments
3. **Data Export**: Export functionality for reports and tax purposes
4. **Advanced Analytics**: Additional financial metrics and reporting
5. **Multi-language Support**: Internationalization for global users
6. **API Integration**: Payment gateway integration for direct payments
7. **Document Storage**: Store additional related documents beyond receipts

## Target Users

- **Individual Investors**: People participating in multiple chit fund schemes
- **Family Managers**: Individuals managing family investments
- **Small Groups**: Informal chit fund groups needing a management tool
- **Financial Planners**: Professionals helping clients manage investments