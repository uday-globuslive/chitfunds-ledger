# MongoDB Connection Troubleshooting Guide

This guide provides solutions for common issues when connecting Django to MongoDB using Djongo.

## Common Issues and Solutions

### 1. Installation Errors with Djongo and Django

**Issue**: Dependency conflict between Djongo and Django versions.

**Solution A - Use the GitHub version**:
```bash
pip uninstall djongo sqlparse -y
pip install "git+https://github.com/doableware/djongo.git@djongo-2.0.0"
```

**Solution B - Use PyMongo directly**:
If Djongo continues to cause issues, you can use the alternative approach provided in `alternative_mongodb_connection.py`, which uses PyMongo directly.

### 2. Connection Issues with MongoDB Atlas

**Error**: `ServerSelectionTimeoutError: connection attempt failed`

**Solutions**:
1. Check if the MongoDB Atlas IP whitelist includes your server's IP
2. Verify username and password in the connection string
3. Ensure the cluster is running and accessible
4. Test connection with a simple PyMongo script:

```python
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.environ.get('MONGODB_URI')
client = MongoClient(uri)
db = client.admin
# Check connection
print(db.command('ping'))
```

### 3. Djongo Compatibility Issues

**Issue**: Schema validation errors or field type incompatibility.

**Solutions**:
1. Set `ENFORCE_SCHEMA: False` in your database settings
2. Add the latest version of `djangotoolbox`
3. Modify models to use MongoDB-compatible field types

### 4. Alternative Connection Approach

If you continue to have issues with Djongo, you can switch to using PyMongo directly with Django:

1. Copy the `alternative_mongodb_connection.py` file to your project
2. Update your models to use the `MongoDBModel` mixin
3. Update your settings.py to include:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'mongodb': {
        'ENGINE': 'django.db.backends.dummy',
        'NAME': 'chitfunds_db',
    }
}

DATABASE_ROUTERS = ['your_app.alternative_mongodb_connection.MongoDBRouter']
```

4. Modify your models to include MongoDB collection information:

```python
from django.db import models
from your_app.alternative_mongodb_connection import MongoDBModel

class YourModel(models.Model, MongoDBModel):
    name = models.CharField(max_length=100)
    
    class Meta:
        mongodb_collection = 'your_collection'
```

5. Use MongoDB-specific methods for CRUD operations:

```python
# Create
instance = YourModel(name="Test")
instance.mongo_save()

# Read
results = YourModel.mongo_find({"name": "Test"})

# Update
instance.name = "Updated"
instance.mongo_save()

# Delete
instance.mongo_delete()
```

### 5. Debugging Connection Issues

Add these settings to your Django settings.py for more verbose logging:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'djongo': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'pymongo': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

### 6. Verify MongoDB Atlas Configuration

1. Check if your MongoDB Atlas cluster is running
2. Verify database user permissions (should have readWrite role)
3. Make sure you've whitelisted the appropriate IP addresses
4. Test connection with MongoDB Compass client
5. Ensure you're using the correct connection string format:
   ```
   mongodb+srv://<username>:<password>@<cluster-url>/<dbname>?retryWrites=true&w=majority
   ```

## If All Else Fails

If you continue to experience issues with Djongo, consider these alternatives:

1. Use `pymongo` directly (see the `alternative_mongodb_connection.py` file)
2. Use `mongoengine` as a more mature MongoDB ODM for Python
3. Use Django with a relational database (MySQL, PostgreSQL) and consider using MongoDB only for specific features via PyMongo