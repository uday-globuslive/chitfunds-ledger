# SQLite Setup for ChitFunds Ledger

SQLite is now the recommended database backend for the ChitFunds Ledger application. This document explains how to set up, optimize, and manage SQLite for this application.

## Why SQLite?

While MongoDB was originally planned for this application, we've made SQLite the default for several reasons:

1. **Simplicity**: SQLite requires no separate server setup
2. **Reliability**: SQLite is a mature, stable database solution
3. **Performance**: Excellent performance for small to medium-sized applications
4. **Compatibility**: Perfect compatibility with Django's ORM
5. **Portability**: The database is contained in a single file
6. **Zero Configuration**: Works out of the box with minimal setup

## Quick Setup with SQLite

The easiest way to ensure SQLite is being used is to run the `force_sqlite.py` script:

```bash
chmod +x force_sqlite.py
./force_sqlite.py
```

This script:
1. Creates a `.env` file with SQLite configuration
2. Sets up necessary directories for the application
3. Creates a `commands.sh` script with common commands

## Manual Setup with SQLite

If you prefer to manually configure SQLite:

1. Ensure your `.env` file contains:
   ```
   USE_DJONGO=False
   USE_POSTGRES=False
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

5. Collect static files:
   ```bash
   python chitfunds_ledger/manage.py collectstatic
   ```

6. Run the development server:
   ```bash
   python chitfunds_ledger/manage.py runserver
   ```

7. Visit http://127.0.0.1:8000/ in your browser

## Optimizing SQLite Performance

For optimal performance with SQLite:

### 1. Enable WAL Mode

WAL (Write-Ahead Logging) mode can significantly improve concurrent access performance. You can enable it by adding the following to your `settings.py`:

```python
from django.db import connection

def activate_wal_mode():
    """Activate WAL mode for SQLite for better concurrency."""
    cursor = connection.cursor()
    cursor.execute('PRAGMA journal_mode=WAL;')
    cursor.execute('PRAGMA synchronous=NORMAL;')
    cursor.execute('PRAGMA temp_store=MEMORY;')
    cursor.execute('PRAGMA mmap_size=30000000000;')
    cursor.close()

# Connect signal to activate WAL mode after connection is established
from django.db.backends.signals import connection_created
connection_created.connect(lambda **kwargs: activate_wal_mode())
```

### 2. Regular Vacuuming

SQLite databases benefit from periodic vacuuming to reclaim space and optimize performance:

```python
# Add to a management command or scheduled task
def vacuum_database():
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('VACUUM;')
    cursor.close()
```

### 3. Index Your Database

Ensure important query fields are indexed for faster lookup:

```python
# Example in models.py
class Payment(models.Model):
    # Fields...
    payment_date = models.DateField(default=timezone.now, db_index=True)
    # More fields...
    
    class Meta:
        indexes = [
            models.Index(fields=['payment_method']),
            models.Index(fields=['reference_number']),
        ]
```

## Backup and Maintenance

### Backing Up SQLite Database

To back up your SQLite database:

```bash
# Simple file copy (when app is not running)
cp chitfunds_ledger/db.sqlite3 db.sqlite3.backup

# Using SQLite's dump command (safer)
sqlite3 chitfunds_ledger/db.sqlite3 .dump > db_backup.sql
```

### Restoring from Backup

To restore from a backup:

```bash
# From file copy
cp db.sqlite3.backup chitfunds_ledger/db.sqlite3

# From SQL dump
sqlite3 chitfunds_ledger/db.sqlite3 < db_backup.sql
```

## Alternative Database Options

### PostgreSQL Alternative

For production use, PostgreSQL is recommended over SQLite:

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

4. The application already includes PostgreSQL adapter in requirements.txt

### MongoDB Direct Access

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

## Long-term Considerations

### When to Consider Switching from SQLite

While SQLite is excellent for most use cases, consider switching to PostgreSQL when:

1. Your application has many concurrent users (more than 10-20 simultaneous writers)
2. Your database grows beyond several GB
3. You need advanced database features like full-text search or complex joins
4. You're deploying in a distributed environment with multiple web servers

### Transitioning to PostgreSQL

To transition from SQLite to PostgreSQL:

1. Update your `.env` file with PostgreSQL settings
2. Create a PostgreSQL database
3. Use Django's `dumpdata` and `loaddata` commands to migrate data:
   ```bash
   # Export data from SQLite
   python chitfunds_ledger/manage.py dumpdata > data.json
   
   # Update settings to use PostgreSQL and run migrations
   python chitfunds_ledger/manage.py migrate
   
   # Import data into PostgreSQL
   python chitfunds_ledger/manage.py loaddata data.json
   ```

## Conclusion

SQLite provides a reliable and easy-to-use database solution for the ChitFunds Ledger application. It eliminates the compatibility issues encountered with MongoDB/Djongo while maintaining excellent performance for typical usage scenarios.

For most users, running the `force_sqlite.py` script followed by the standard application setup commands will provide the optimal configuration for this application.