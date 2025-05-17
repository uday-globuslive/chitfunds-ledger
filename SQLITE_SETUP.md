# SQLite Setup for ChitFunds Ledger

Due to compatibility issues between Django 4.2.10 and Djongo, we're setting up the application with SQLite initially to get it running. This document explains how to proceed.

## Initial Setup with SQLite

We've configured the app to use SQLite by default by setting `USE_DJONGO=False` in the `.env` file. This will allow you to run migrations and get the application up and running quickly.

## Steps to Run with SQLite

1. Ensure you have the `.env` file with `USE_DJONGO=False`:
   ```
   USE_DJONGO=False
   ```

2. Install dependencies using the installation script:
   ```bash
   ./install.sh
   ```

3. Run migrations:
   ```bash
   python chitfunds_ledger/manage.py migrate
   ```

4. Create a superuser:
   ```bash
   python chitfunds_ledger/manage.py createsuperuser
   ```

5. Run the development server:
   ```bash
   python chitfunds_ledger/manage.py runserver
   ```

6. Visit http://127.0.0.1:8000/ in your browser

## PostgreSQL Alternative

Another option is to use PostgreSQL instead of MongoDB. PostgreSQL is a robust relational database that works well with Django.

### Setting up PostgreSQL:

1. Install PostgreSQL:
   ```bash
   # Ubuntu/Debian
   sudo apt install postgresql postgresql-contrib
   
   # macOS (using Homebrew)
   brew install postgresql
   ```

2. Create a PostgreSQL database:
   ```bash
   sudo -u postgres psql
   CREATE DATABASE chitfunds_db;
   CREATE USER chitfunds_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE chitfunds_db TO chitfunds_user;
   \q
   ```

3. Update the `.env` file:
   ```
   USE_DJONGO=False
   USE_POSTGRES=True
   DB_NAME=chitfunds_db
   DB_USER=chitfunds_user
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

4. Install PostgreSQL adapter for Python:
   ```bash
   pip install psycopg2-binary
   ```

5. Update `settings.py` to use PostgreSQL when `USE_POSTGRES=True`:
   ```python
   # In the database configuration section, add this code
   if os.environ.get('USE_POSTGRES', 'False').lower() == 'true':
       DATABASES = {
           'default': {
               'ENGINE': 'django.db.backends.postgresql',
               'NAME': os.environ.get('DB_NAME', 'chitfunds_db'),
               'USER': os.environ.get('DB_USER', 'chitfunds_user'),
               'PASSWORD': os.environ.get('DB_PASSWORD', 'your_password'),
               'HOST': os.environ.get('DB_HOST', 'localhost'),
               'PORT': os.environ.get('DB_PORT', '5432'),
           }
       }
       print("Using PostgreSQL backend.")
   ```

## MongoDB Direct Access

Even when using SQLite or PostgreSQL for Django's ORM, you can still use direct PyMongo calls to store and retrieve specific data in MongoDB. The `alternative_mongodb_connection.py` file provides a framework for this.

Example usage:

```python
from alternative_mongodb_connection import direct_mongodb_connection

# Get a MongoDB collection
collection = direct_mongodb_connection('payments')

# Insert a document
result = collection.insert_one({
    'user_id': 123,
    'amount': 500,
    'date': datetime.datetime.now(),
    'receipt_image_path': '/path/to/image.jpg'
})

# Find documents
payments = collection.find({'user_id': 123})
for payment in payments:
    print(payment)
```

## Long-term Solution

If you'd like to use MongoDB as your primary database in the future, consider:

1. Using an older version of Django (3.2 LTS) which has better compatibility with Djongo
2. Using MongoEngine instead of Djongo (a more mature ODM for MongoDB)
3. Upgrading to a newer version of Djongo when it becomes compatible with Django 4.2+

For now, SQLite provides the fastest path to a working application, with PostgreSQL as a robust alternative for production use.